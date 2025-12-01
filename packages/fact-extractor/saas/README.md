# ESIA Fact Extractor - SaaS Application

Web-based SaaS application for extracting and managing facts from PDF documents.

## Features

- 📤 **PDF Upload**: Drag & drop or browse to upload PDF/Markdown files
- ⚡ **Async Processing**: Background processing with real-time progress tracking
- 📊 **Interactive Table**: View, edit, and manage extracted facts
- 🔍 **Search & Filter**: Find facts quickly, filter by conflicts
- ⚠️ **Conflict Detection**: Automatic detection of contradictions
- 💾 **Export**: Download results as CSV
- ✏️ **Manual Corrections**: Edit facts and add comments
- 📱 **Responsive**: Works on desktop and mobile

## Architecture

```
Frontend (HTML/CSS/JS) → FastAPI Backend → SQLite Database
                              ↓
                      Background Processing
                              ↓
                    PDF → Text → LLM Extraction
                              ↓
                        Fact Normalization
```

## Prerequisites

1. **Python 3.9+**
2. **Ollama** with Qwen2.5:7B-Instruct model
   ```bash
   ollama pull qwen2.5:7b-instruct
   ollama serve
   ```

## Installation

1. **Install dependencies**:
   ```bash
   cd saas/backend
   pip install -r requirements.txt
   ```

2. **Initialize database** (automatic on first run)

## Running the Application

### Development Mode

```bash
cd saas/backend
python main.py
```

The application will be available at: **http://localhost:8000**

### Production Mode

```bash
cd saas/backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Usage

1. **Open** http://localhost:8000 in your browser
2. **Upload** a PDF or Markdown file
3. **Wait** for processing (progress bar shows real-time status)
4. **Review** extracted facts in the interactive table
5. **Edit** facts by clicking the edit button
6. **Filter** to show only conflicts
7. **Export** results to CSV

## API Endpoints

### Upload Document
```
POST /api/upload
Content-Type: multipart/form-data
Body: file (PDF or MD)

Response:
{
  "job_id": 1,
  "session_id": "uuid",
  "message": "File uploaded successfully",
  "status": "pending"
}
```

### Get Job Status
```
GET /api/jobs/{job_id}

Response:
{
  "id": 1,
  "status": "completed",
  "progress": 100,
  "total_chunks": 25,
  ...
}
```

### Get Facts
```
GET /api/jobs/{job_id}/facts

Response: Array of fact objects
```

### Update Fact
```
PATCH /api/facts/{fact_id}
Content-Type: application/json

Body:
{
  "value_normalized": 1000.5,
  "unit_normalized": "kg",
  "user_comment": "Verified value",
  "user_edited": true
}
```

### Delete Fact
```
DELETE /api/facts/{fact_id}
```

### Export to CSV
```
GET /api/jobs/{job_id}/export/csv
```

## Database Schema

### Jobs Table
- `id`: Primary key
- `session_id`: Unique session identifier
- `filename`: Stored filename
- `original_filename`: Original upload filename
- `status`: pending | processing | completed | failed
- `progress`: 0-100
- `total_chunks`: Number of text chunks
- `processed_chunks`: Chunks processed so far
- `created_at`, `updated_at`, `completed_at`: Timestamps

### Facts Table
- `id`: Primary key
- `job_id`: Foreign key to jobs
- `signature`: Canonical fact identifier
- `name`: Fact name
- `fact_type`: quantity | categorical
- `value_raw`, `value_num`: Original values
- `unit_raw`, `unit_normalized`: Units
- `value_normalized`: Normalized numeric value
- `evidence`: Source text quote
- `page`: Page number
- `occurrence_count`: Number of times mentioned
- `has_conflict`: Boolean flag
- `conflict_description`: Conflict details
- `user_edited`: Boolean flag
- `user_comment`: User notes

## Configuration

### Environment Variables

Create a `.env` file in `saas/backend/`:

```env
# Database
DATABASE_URL=sqlite:///./esia_saas.db

# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b-instruct

# Server
HOST=0.0.0.0
PORT=8000
```

### Customization

**Change chunk size** (saas/core/extractor.py:185):
```python
chunks = chunk_markdown(text, max_chars=4000)
```

**Adjust conflict threshold** (saas/core/extractor.py:112):
```python
def detect_conflicts(cluster, tolerance=0.02):  # 2% tolerance
```

## Deployment

### Docker (Recommended)

Coming soon - Docker Compose setup with:
- FastAPI backend
- Ollama container
- PostgreSQL database
- Nginx reverse proxy

### Cloud Deployment

**For cloud deployment**, consider:
1. Replace SQLite with PostgreSQL
2. Use cloud storage for uploaded files (S3, GCS)
3. Deploy Ollama on GPU instance
4. Use Redis for production task queue
5. Add authentication (OAuth, JWT)

## Troubleshooting

### "Connection refused" to Ollama
```bash
# Start Ollama service
ollama serve
```

### "Model not found"
```bash
# Pull the required model
ollama pull qwen2.5:7b-instruct
```

### Database errors
```bash
# Delete database and restart
rm esia_saas.db
python main.py
```

### Slow processing
- Ollama needs GPU for best performance
- Reduce chunk size for faster (but less accurate) extraction
- Process smaller documents first

## Development

### Project Structure
```
saas/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database configuration
│   └── requirements.txt  # Python dependencies
├── core/
│   └── extractor.py      # PDF processing & extraction
├── frontend/
│   ├── index.html        # Main UI
│   ├── app.js           # Frontend logic
│   └── styles.css       # Styling
├── uploads/             # Temporary uploads
├── results/             # Processing results
└── README.md           # This file
```

### Adding Features

**New extraction field**:
1. Add to `Fact` dataclass in `core/extractor.py`
2. Add column to `models.Fact` in `backend/models.py`
3. Add to `schemas.FactBase` in `backend/schemas.py`
4. Update frontend table in `frontend/index.html`

**New unit type**:
1. Add to `UNIT_CONVERSIONS` in `esia_extractor.py` (root)
2. Test with sample document

## Performance

- **Upload**: < 1 second
- **Processing**: ~15-45 seconds per chunk (depends on Ollama/GPU)
- **Display**: Instant
- **Export**: < 1 second for 1000 facts

## Security Considerations

For production deployment:
- Add file size limits
- Implement rate limiting
- Add user authentication
- Sanitize file uploads
- Use HTTPS
- Set CORS origins properly
- Add input validation
- Use environment variables for secrets

## License

MIT License - See LICENSE file

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the main project README
3. Open an issue on GitHub
