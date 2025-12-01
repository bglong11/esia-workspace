"""
FastAPI backend for ESIA Fact Extractor SaaS
"""

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from pathlib import Path
import shutil
import uuid
import sys
from typing import List

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

from database import engine, Base, get_db
import models
import schemas
from core.extractor import process_document
from file_sanitizer import validate_filename

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="ESIA Fact Extractor API",
    description="API for extracting facts from PDF documents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Directories
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
RESULTS_DIR = Path(__file__).parent.parent / "results"
UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    """Serve frontend"""
    index_path = frontend_path / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "ESIA Fact Extractor API", "status": "running"}


@app.post("/api/upload", response_model=schemas.UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    """
    Upload PDF file for processing

    Returns job information including job_id for tracking
    """
    # Validate file type
    if not file.filename.lower().endswith(('.pdf', '.md')):
        raise HTTPException(status_code=400, detail="Only PDF and MD files are supported")

    # Validate filename safety
    is_valid, reason = validate_filename(file.filename)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Invalid filename: {reason}")

    # Generate unique session ID and filename (UUID-based for security)
    session_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    unique_filename = f"{session_id}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    # Save uploaded file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Create job in database
    job = models.Job(
        session_id=session_id,
        filename=unique_filename,
        original_filename=file.filename,
        status="pending"
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Start background processing
    background_tasks.add_task(process_job, job.id, str(file_path))

    return schemas.UploadResponse(
        job_id=job.id,
        session_id=session_id,
        message="File uploaded successfully. Processing started.",
        status="pending"
    )


def process_job(job_id: int, file_path: str):
    """
    Background task to process uploaded document

    Args:
        job_id: Database job ID
        file_path: Path to uploaded file
    """
    from database import SessionLocal

    db = SessionLocal()
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if not job:
        return

    try:
        # Update status
        job.status = "processing"
        db.commit()

        # Progress callback
        def update_progress(current: int, total: int, status: str):
            job.progress = current
            job.status = f"processing: {status}"
            db.commit()

        # Process document
        results = process_document(file_path, progress_callback=update_progress)

        # Store facts in database
        job.total_chunks = results['total_chunks']
        job.processed_chunks = results['total_chunks']

        # Store consolidated facts (to avoid duplicates)
        for fact in results['consolidated_facts']:
            db_fact = models.Fact(
                job_id=job.id,
                signature=fact.signature,
                name=fact.name,
                fact_type=fact.type,
                value_raw=fact.value,
                value_num=fact.value_num,
                unit_raw=fact.unit,
                value_normalized=fact.normalized_value,
                unit_normalized=fact.normalized_unit,
                evidence=fact.evidence[:1000] if fact.evidence else None,  # Limit length
                page=fact.page,
                chunk_id=fact.chunk_id,
                aliases="; ".join(fact.aliases) if fact.aliases else None,
                occurrence_count=getattr(fact, 'occurrence_count', 1),
                has_conflict=getattr(fact, 'has_conflict', False),
                conflict_description=getattr(fact, 'conflict_description', None),
                min_value=getattr(fact, 'min_value', None),
                max_value=getattr(fact, 'max_value', None),
                # Factsheet categorization
                category=getattr(fact, 'category', None),
                subcategory=getattr(fact, 'subcategory', None),
                categorization_confidence=getattr(fact, 'categorization_confidence', None),
                categorization_rationale=getattr(fact, 'categorization_rationale', None)
            )
            db.add(db_fact)

        # Update job status
        job.status = "completed"
        job.progress = 100
        job.completed_at = func.now()
        db.commit()

    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        db.commit()
    finally:
        db.close()


@app.get("/api/jobs/{job_id}", response_model=schemas.JobResponse)
async def get_job_status(job_id: int, db: Session = Depends(get_db)):
    """Get job status and progress"""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/api/jobs/{job_id}/facts", response_model=List[schemas.FactResponse])
async def get_job_facts(job_id: int, db: Session = Depends(get_db)):
    """Get all extracted facts for a job"""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    facts = db.query(models.Fact).filter(models.Fact.job_id == job_id).all()
    return facts


@app.get("/api/jobs/{job_id}/complete", response_model=schemas.JobWithFacts)
async def get_job_complete(job_id: int, db: Session = Depends(get_db)):
    """Get complete job information including all facts"""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.patch("/api/facts/{fact_id}", response_model=schemas.FactResponse)
async def update_fact(
    fact_id: int,
    fact_update: schemas.FactUpdate,
    db: Session = Depends(get_db)
):
    """Update a fact (user corrections)"""
    fact = db.query(models.Fact).filter(models.Fact.id == fact_id).first()
    if not fact:
        raise HTTPException(status_code=404, detail="Fact not found")

    # Update fields
    if fact_update.value_normalized is not None:
        fact.value_normalized = fact_update.value_normalized
    if fact_update.unit_normalized is not None:
        fact.unit_normalized = fact_update.unit_normalized
    if fact_update.user_comment is not None:
        fact.user_comment = fact_update.user_comment
    fact.user_edited = fact_update.user_edited

    db.commit()
    db.refresh(fact)
    return fact


@app.delete("/api/facts/{fact_id}")
async def delete_fact(fact_id: int, db: Session = Depends(get_db)):
    """Delete a fact"""
    fact = db.query(models.Fact).filter(models.Fact.id == fact_id).first()
    if not fact:
        raise HTTPException(status_code=404, detail="Fact not found")

    db.delete(fact)
    db.commit()
    return {"message": "Fact deleted successfully"}


@app.get("/api/jobs/{job_id}/export/csv")
async def export_to_csv(job_id: int, db: Session = Depends(get_db)):
    """Export facts to CSV"""
    import pandas as pd
    import io
    from fastapi.responses import StreamingResponse

    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    facts = db.query(models.Fact).filter(models.Fact.job_id == job_id).all()

    # Convert to DataFrame
    data = []
    for fact in facts:
        data.append({
            'Fact Name': fact.name,
            'Value': fact.value_normalized,
            'Unit': fact.unit_normalized,
            'Type': fact.fact_type,
            'Page': fact.page,
            'Occurrences': fact.occurrence_count,
            'Has Conflict': fact.has_conflict,
            'Conflict Description': fact.conflict_description or '',
            'Min Value': fact.min_value,
            'Max Value': fact.max_value,
            'Evidence': fact.evidence or '',
            'User Comment': fact.user_comment or '',
            'User Edited': fact.user_edited
        })

    df = pd.DataFrame(data)

    # Convert to CSV
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=facts_{job_id}.csv"}
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ESIA Fact Extractor API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
