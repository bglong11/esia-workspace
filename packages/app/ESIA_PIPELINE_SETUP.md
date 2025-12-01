# ESIA Pipeline Integration Setup

This document explains how the ESIA.ai upload interface integrates with your existing ESIA pipeline at `M:\GitHub\esia-pipeline`.

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│ ESIA.ai Upload Interface (http://localhost:3004)            │
│  ├─ User uploads PDF                                        │
│  └─ Backend saves to ./data/pdfs/                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ ESIA Pipeline Executor (pipelineExecutor.js)                │
│  ├─ Sanitizes filename to root name                         │
│  └─ Calls M:/GitHub/esia-pipeline/run-esia-pipeline.py     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ ESIA Pipeline (M:\GitHub\esia-pipeline)                     │
│                                                              │
│ 1️⃣  Chunk PDF                                               │
│    - Split into semantic chunks with page tracking          │
│    - Output: chunked_data/{sanitized_name}/                 │
│                                                              │
│ 2️⃣  Extract Facts                                           │
│    - Extract domain-specific facts using archetypes         │
│    - Output: extracted_facts/{sanitized_name}/              │
│                                                              │
│ 3️⃣  Analyze & Compliance                                    │
│    - Check consistency and compliance                       │
│    - Output: analysis_results/{sanitized_name}/             │
│                                                              │
│ All outputs → M:/GitHub/esia-pipeline/data/outputs/         │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

The pipeline is configured in `pipeline.config.js`:

```javascript
export const pipelineConfig = {
  name: 'ESIA Processing Pipeline',

  // Work from the ESIA pipeline directory
  workingDir: 'M:/GitHub/esia-pipeline',

  // Single pipeline step that runs the full ESIA pipeline
  steps: [
    {
      id: 'full_pipeline',
      name: 'ESIA Full Pipeline',
      script: 'M:/GitHub/esia-pipeline/run-esia-pipeline.py',
      args: ['{PDF_FILE}'],  // Path to uploaded PDF
      timeout: 1800000,  // 30 minutes
    }
  ],

  // Output directory
  outputDir: 'M:/GitHub/esia-pipeline/data/outputs',
};
```

## How It Works

### 1. Upload Flow

1. User uploads PDF via http://localhost:3004
2. Backend saves file to `./data/pdfs/{timestamp}-{original_name}.pdf`
3. Server returns upload response with `pipeline.executionId`
4. Frontend polls pipeline status every 1-2 seconds

### 2. Filename Sanitization

The uploaded filename is sanitized once and used throughout:

```
Input:     "My ESIA Report (Draft).pdf"
Saved as:  "1704067200000-My ESIA Report (Draft).pdf"
Sanitized: "my_esia_report_draft"  ← Used for all processing
```

### 3. Pipeline Execution

When pipeline starts:

```bash
cd M:/GitHub/esia-pipeline
python run-esia-pipeline.py X:\downloads\esv\data\pdfs\1704067200000-My ESIA Report (Draft).pdf
```

The ESIA pipeline script:
- Receives the full PDF path as argument
- Sanitizes filename internally (matching our sanitization)
- Runs 3-step pipeline (chunking → extraction → analysis)
- Outputs results to `M:/GitHub/esia-pipeline/data/outputs/`

### 4. Pipeline Outputs

Results are organized by sanitized name:

```
M:/GitHub/esia-pipeline/data/outputs/
├── my_esia_report_draft/
│   ├── chunks/                    # Chunked PDF segments
│   ├── extracted_facts/           # Extracted domain facts
│   ├── analysis_results/          # Compliance & consistency analysis
│   └── metadata.json              # Processing metadata
```

### 5. Frontend Status

Frontend shows pipeline status with messages:
- `"Pipeline processing started. Sanitized name: my_esia_report_draft"`
- After completion: `"✓ Pipeline completed! Output: my_esia_report_draft"`

## API Integration

### Upload Endpoint
```
POST /api/upload
Body: multipart/form-data with file

Response:
{
  "message": "File uploaded successfully",
  "filename": "1704067200000-My ESIA Report (Draft).pdf",
  "pipeline": {
    "executionId": "exec-1704067200000-abc123",
    "status": "running",
    "sanitizedName": "my_esia_report_draft"
  }
}
```

### Pipeline Status Endpoint
```
GET /api/pipeline/{executionId}

Response:
{
  "id": "exec-1704067200000-abc123",
  "sanitizedName": "my_esia_report_draft",
  "status": "running|completed|failed",
  "steps": [
    {
      "stepId": "full_pipeline",
      "status": "completed",
      "output": "..."
    }
  ]
}
```

## Requirements

Your ESIA pipeline requires:

1. **Python** installed and in PATH
   ```bash
   python --version  # Should show 3.x
   ```

2. **Dependencies installed** in the ESIA pipeline folder
   ```bash
   cd M:\GitHub\esia-pipeline
   pip install -r requirements.txt
   ```

3. **Folder structure** (should already exist):
   ```
   M:/GitHub/esia-pipeline/
   ├── run-esia-pipeline.py      # Main entry point
   ├── esia-fact-extractor-pipeline/
   ├── esia-fact-analyzer/
   ├── data/
   │   ├── pdfs/               # Input PDFs (optional - script handles)
   │   └── outputs/            # Pipeline outputs
   └── config.py
   ```

## Running the Application

### Terminal 1: Start Backend Server
```bash
cd X:\downloads\esv
node server.js
# Server runs on http://localhost:5000
```

### Terminal 2: Start Frontend Server
```bash
cd X:\downloads\esv
npm run dev:frontend
# Frontend runs on http://localhost:3004
```

### Test the Flow

1. Open http://localhost:3004 in browser
2. Upload a PDF file
3. Watch the progress in real-time
4. Check results in `M:/GitHub/esia-pipeline/data/outputs/{sanitized_name}/`

## Troubleshooting

### "Script not found" Error

Check:
1. Python path: `python --version`
2. Script exists: `ls "M:\GitHub\esia-pipeline\run-esia-pipeline.py"`
3. Permissions: Script should be executable

### Pipeline Times Out

The default timeout is 30 minutes. If processing takes longer:

Edit `pipeline.config.js`:
```javascript
timeout: 3600000,  // 60 minutes
```

### No Output Files

Check:
1. ESIA pipeline ran without errors in server logs
2. Output directory exists: `M:\GitHub\esia-pipeline\data\outputs\`
3. Python dependencies installed: `pip install -r requirements.txt`

### Connection Refused

Make sure both servers are running:
- Backend on http://localhost:5000
- Frontend on http://localhost:3004

Check with:
```bash
curl http://localhost:5000/health
curl http://localhost:3004
```

## Next Steps

1. **Copy PDFs for processing**
   ```bash
   # Upload through web interface (recommended)
   # OR copy to data/pdfs/ directly for local testing
   cp my_report.pdf X:\downloads\esv\data\pdfs\
   ```

2. **Monitor processing**
   - Watch frontend for status updates
   - Check server logs for detailed output
   - View results in `M:/GitHub/esia-pipeline/data/outputs/`

3. **Customize pipeline (optional)**
   - Modify `M:/GitHub/esia-pipeline/config.py` for parameters
   - Edit `pipeline.config.js` if you need different timeout/steps

## Key Files

| File | Purpose |
|------|---------|
| `pipeline.config.js` | Pipeline configuration & script paths |
| `pipelineExecutor.js` | Runs pipeline scripts via Node.js |
| `server.js` | Backend server & API endpoints |
| `components/FileUpload.tsx` | Frontend upload UI |
| `services/apiService.ts` | Frontend API client |

## Support

For ESIA pipeline issues, check:
- `M:/GitHub/esia-pipeline/README.md`
- `M:/GitHub/esia-pipeline/QUICKSTART.md`
- `M:/GitHub/esia-pipeline/ARCHITECTURE.md`

For ESIA.ai upload interface issues, check:
- `PIPELINE.md`
- `EXTERNAL_SCRIPTS.md`
