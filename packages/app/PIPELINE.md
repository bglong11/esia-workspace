# ESIA Pipeline Integration

This document explains how the ESIA application integrates with the ESIA data processing pipeline.

## Architecture

```
User Upload (PDF)
    ↓
Frontend (http://localhost:3004)
    ↓
Backend Server (http://localhost:5000)
    ├─→ Saves PDF to ./data/pdfs/{timestamp}-{original_name}
    └─→ Triggers Pipeline Execution
         ├─→ Extract Text
         ├─→ Validate ESIA
         ├─→ Sanitize & Normalize
         └─→ Index & Store
```

## How It Works

### 1. File Upload
- User uploads a PDF through the web interface
- Frontend validates file type (PDF only) and size (max 50MB)
- File is sent to backend via POST `/api/upload`

### 2. Pipeline Initialization
- Backend saves the file to `./data/pdfs/{timestamp}-{filename}`
- Pipeline executor is triggered with the saved filename
- **Root Name Generation**: The filename is sanitized to create a clean root name
  - Removes timestamp prefix
  - Converts to lowercase
  - Replaces spaces and special characters with underscores
  - Example: `1704067200000-My ESIA Report.pdf` → `my_esia_report`

### 3. Pipeline Execution
The pipeline processes through these steps (configurable in `pipeline.config.js`):

1. **Extract**: Extract text content from PDF
2. **Validate**: Validate ESIA content structure
3. **Sanitize**: Sanitize and normalize ESIA data
4. **Index**: Index and store processed data

Each step receives:
- `PDF_FILE`: The uploaded PDF filename
- `SANITIZED_NAME`: The clean root name for output

### 4. Frontend Monitoring
After upload completes:
- Backend returns pipeline execution ID and sanitized root name
- Frontend polls `/api/pipeline/{executionId}` every 1-2 seconds
- User sees real-time pipeline progress
- Final message shows: `"✓ Pipeline completed! Output: {sanitized_name}"`

## API Endpoints

### POST /api/upload
Upload a PDF and start pipeline processing

**Request:**
```
Content-Type: multipart/form-data
Body: file (PDF file)
```

**Response:**
```json
{
  "message": "File uploaded successfully",
  "filename": "1704067200000-my_report.pdf",
  "size": 1024000,
  "path": "/data/pdfs/1704067200000-my_report.pdf",
  "pipeline": {
    "executionId": "exec-1704067200000-abc123xyz",
    "status": "running",
    "sanitizedName": "my_report"
  }
}
```

### GET /api/pipeline/:executionId
Get the status of a pipeline execution

**Response:**
```json
{
  "id": "exec-1704067200000-abc123xyz",
  "pdfFilename": "1704067200000-my_report.pdf",
  "sanitizedName": "my_report",
  "status": "completed|running|failed",
  "startTime": "2025-11-30T12:00:00.000Z",
  "endTime": "2025-11-30T12:00:05.000Z",
  "steps": [
    {
      "stepId": "extract",
      "status": "completed"
    },
    {
      "stepId": "validate",
      "status": "completed"
    },
    {
      "stepId": "sanitize",
      "status": "completed"
    },
    {
      "stepId": "index",
      "status": "completed"
    }
  ]
}
```

### GET /api/pipeline
Get all pipeline executions (history)

**Response:**
```json
{
  "executions": [
    { /* execution objects */ }
  ]
}
```

## Configuration

### Pipeline Steps (pipeline.config.js)
Modify the `steps` array to add/remove/change pipeline stages:

```javascript
steps: [
  {
    id: 'extract',
    name: 'Extract Text',
    description: 'Extract text content from PDF',
    command: 'python',
    args: ['scripts/extract_text.py'],
    timeout: 300000,
  },
  // ... more steps
]
```

### Upload Limits
- Maximum file size: 50MB (configurable in `server.js` and `FileUpload.tsx`)
- Allowed types: PDF only

## Example Pipeline Integration

To integrate with your actual ESIA pipeline:

1. **Update pipeline.config.js** with your actual script commands
2. **Implement pipeline scripts** in `scripts/` directory that accept:
   - `{PDF_FILE}`: The uploaded PDF path
   - `{SANITIZED_NAME}`: The clean root name
   - `{ROOT_NAME}`: Alias for sanitized name

Example script usage:
```bash
python scripts/extract_text.py data/pdfs/1704067200000-report.pdf my_report
```

## Directory Structure

```
esv/
├── server.js                 # Backend server with upload & pipeline endpoints
├── pipelineExecutor.js       # Pipeline execution logic
├── pipeline.config.js        # Pipeline configuration
├── data/
│   └── pdfs/                 # Uploaded PDF files
│       └── {timestamp}-{filename}.pdf
├── scripts/                  # Your pipeline scripts
│   ├── extract_text.py
│   ├── validate_esia.py
│   ├── sanitize_esia.py
│   └── index_esia.py
└── components/
    └── FileUpload.tsx        # Frontend upload component
```

## Development

### Start Backend
```bash
npm run dev:server
# Server runs on http://localhost:5000
```

### Start Frontend
```bash
npm run dev:frontend
# Frontend runs on http://localhost:3004
```

### Start Both
```bash
npm run dev
# Requires both to be started (backend + frontend)
```

## Testing

Upload a PDF through http://localhost:3004 and watch:
1. File is saved to `./data/pdfs/`
2. Pipeline begins execution (current implementation simulates steps)
3. Frontend shows progress in real-time
4. Success message shows sanitized root name for next pipeline stages

The sanitized filename becomes the key identifier for downstream processing in your pipeline.
