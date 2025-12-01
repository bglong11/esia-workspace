"""
Celery tasks for document processing with Docling
"""

import subprocess
import sys
from pathlib import Path
from celery_app import celery_app
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database import SessionLocal
import models

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from core.extractor import FactExtractor, configure_llm, chunk_markdown, cluster_facts, detect_conflicts


@celery_app.task(bind=True)
def process_document_with_docling(self, job_id: int, file_path: str, docling_script_path: str):
    """
    Process document using docling for extraction, then LLM for fact extraction

    Args:
        self: Celery task instance (for progress updates)
        job_id: Database job ID
        file_path: Path to uploaded PDF
        docling_script_path: Path to your standalone docling program

    Returns:
        Dictionary with extraction results
    """
    db = SessionLocal()
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if not job:
        return {'error': 'Job not found'}

    try:
        # Update status
        job.status = "processing: Extracting text with Docling..."
        job.progress = 5
        db.commit()
        self.update_state(state='PROGRESS', meta={'progress': 5, 'status': 'Extracting text with Docling'})

        # ========================================
        # Step 1: Call Docling for PDF extraction
        # ========================================

        # Option A: If your docling script outputs to stdout
        result = subprocess.run(
            ['python', docling_script_path, file_path],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        if result.returncode != 0:
            raise Exception(f"Docling extraction failed: {result.stderr}")

        # Get extracted text
        extracted_text = result.stdout

        # Option B: If your docling script saves to a file
        # output_file = file_path.replace('.pdf', '_docling.md')
        # result = subprocess.run(['python', docling_script_path, file_path, output_file], check=True)
        # with open(output_file, 'r', encoding='utf-8') as f:
        #     extracted_text = f.read()

        job.status = "processing: Text extracted, configuring LLM..."
        job.progress = 15
        db.commit()
        self.update_state(state='PROGRESS', meta={'progress': 15, 'status': 'Configuring LLM'})

        # ========================================
        # Step 2: Configure LLM
        # ========================================
        configure_llm()

        # ========================================
        # Step 3: Chunk text
        # ========================================
        job.status = "processing: Chunking text..."
        job.progress = 20
        db.commit()
        self.update_state(state='PROGRESS', meta={'progress': 20, 'status': 'Chunking text'})

        chunks = chunk_markdown(extracted_text, max_chars=4000)
        total_chunks = len(chunks)
        job.total_chunks = total_chunks
        db.commit()

        # ========================================
        # Step 4: Extract facts from chunks
        # ========================================
        extractor = FactExtractor()
        all_facts = []

        for i, chunk in enumerate(chunks):
            try:
                # Update progress (20% to 85% during extraction)
                progress = 20 + int((i + 1) / total_chunks * 65)
                job.status = f"processing: Extracting facts ({i+1}/{total_chunks})..."
                job.progress = progress
                job.processed_chunks = i + 1
                db.commit()

                self.update_state(
                    state='PROGRESS',
                    meta={
                        'progress': progress,
                        'status': f'Processing chunk {i+1}/{total_chunks}',
                        'current_chunk': i + 1,
                        'total_chunks': total_chunks
                    }
                )

                facts = extractor.extract_from_chunk(chunk, page=i+1, chunk_id=i)
                all_facts.extend(facts)

            except Exception as e:
                print(f"Error processing chunk {i}: {e}")
                continue

        # ========================================
        # Step 5: Cluster and detect conflicts
        # ========================================
        job.status = "processing: Clustering and detecting conflicts..."
        job.progress = 90
        db.commit()
        self.update_state(state='PROGRESS', meta={'progress': 90, 'status': 'Detecting conflicts'})

        clusters = cluster_facts(all_facts)

        # Store facts in database
        for signature, cluster in clusters.items():
            has_conflict, conflict_desc = detect_conflicts(cluster)
            normalized_values = [f.normalized_value for f in cluster if f.normalized_value > 0]

            # Use first fact as representative
            fact = cluster[0]

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
                evidence=fact.evidence[:1000] if fact.evidence else None,
                page=fact.page,
                chunk_id=fact.chunk_id,
                aliases="; ".join(fact.aliases) if fact.aliases else None,
                occurrence_count=len(cluster),
                has_conflict=has_conflict,
                conflict_description=conflict_desc,
                min_value=min(normalized_values) if normalized_values else None,
                max_value=max(normalized_values) if normalized_values else None
            )
            db.add(db_fact)

        # ========================================
        # Step 6: Mark as complete
        # ========================================
        job.status = "completed"
        job.progress = 100
        job.completed_at = func.now()
        db.commit()

        return {
            'status': 'completed',
            'total_facts': len(all_facts),
            'unique_facts': len(clusters),
            'conflicts': sum(1 for _, cluster in clusters.items() if detect_conflicts(cluster)[0])
        }

    except subprocess.TimeoutExpired:
        job.status = "failed"
        job.error_message = "Docling extraction timed out (>10 minutes)"
        db.commit()
        return {'error': 'Timeout'}

    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        db.commit()
        raise

    finally:
        db.close()


@celery_app.task
def cleanup_old_files(days=7):
    """Clean up uploaded files older than X days"""
    import time
    from pathlib import Path

    upload_dir = Path(__file__).parent.parent / "uploads"
    cutoff_time = time.time() - (days * 86400)

    deleted_count = 0
    for file_path in upload_dir.glob("*"):
        if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
            file_path.unlink()
            deleted_count += 1

    return f"Deleted {deleted_count} old files"
