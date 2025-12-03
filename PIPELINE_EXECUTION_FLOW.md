# Complete ESIA Pipeline Execution Flow

## Overview

**Yes, the entire 4-step pipeline WILL run with `./run-app.ps1`**

When users upload a PDF through the web interface after running `./run-app.ps1`, the complete 4-step pipeline executes automatically:

```
./run-app.ps1
    ↓
Express Backend (port 5000) + React Frontend (port 3000)
    ↓
User uploads PDF via web UI
    ↓
Backend triggers pipelineExecutor.js
    ↓
Executes all 4 steps of run-esia-pipeline.py sequentially
    ↓
Generates HTML + Excel outputs
    ↓
Frontend displays progress and results
```

---

## Execution Path

### 1. Start the Application
```bash
cd m:\GitHub\esia-workspace
.\run-app.ps1
```

**What `run-app.ps1` does:**
- ✅ Starts Express backend on port 5000
- ✅ Starts React/Vite frontend on port 3000
- ✅ Both servers run in separate PowerShell windows
- ✅ Opens http://localhost:3000 in browser

**Files involved:**
- `packages/app/server.js` - Express API server
- `packages/app/pipelineExecutor.js` - Pipeline subprocess orchestrator
- `packages/app/pipeline.config.js` - **NOW INCLUDES Step 4** ✅

### 2. User Uploads PDF

**Frontend:** User clicks "Upload" and selects PDF
- Upload component (FileUpload.tsx) sends file to backend

**Backend:** `server.js` receives upload
- POST `/api/upload` endpoint
- Saves PDF to `data/pdf/` directory
- Calls `executePipeline()` asynchronously
- Returns execution ID to frontend

### 3. Pipeline Orchestration

**File:** `packages/app/pipelineExecutor.js`

**Process:**
```javascript
executePipeline()
    ↓
For each step in pipelineConfig.steps (now 4 steps):
    ↓
    executeStep(step)
        ↓
        Spawn Python subprocess:
        `python run-esia-pipeline.py {PDF_FILE} --steps {STEP_NUMBER} --use-cuda`
        ↓
        Monitor stdout/stderr
        ↓
        Update execution status
        ↓
        Wait for completion
    ↓
Next step (sequential)
```

### 4. Python Pipeline Execution

**File:** `packages/pipeline/run-esia-pipeline.py`

**Command executed by backend:**
```bash
# Step 1
python run-esia-pipeline.py "path/to/document.pdf" --steps 1 --use-cuda

# Step 2
python run-esia-pipeline.py "path/to/document.pdf" --steps 2

# Step 3
python run-esia-pipeline.py "path/to/document.pdf" --steps 3

# Step 4 (NEW)
python run-esia-pipeline.py "path/to/document.pdf" --steps 4
```

**Step Details:**

#### Step 1: Document Chunking (Docling)
- **Input:** PDF file
- **Output:** `{stem}_chunks.jsonl`, `{stem}_meta.json`
- **Duration:** ~5-10 minutes (with GPU)
- **Script:** `esia-fact-extractor-pipeline/step1_docling_hybrid_chunking.py`

#### Step 2: Fact Extraction (DSPy + LLM)
- **Input:** `{stem}_chunks.jsonl`
- **Output:** `{stem}_facts.json`
- **Duration:** 30-120 minutes (depending on document size and LLM)
- **Script:** `esia-fact-extractor-pipeline/step3_extraction_with_archetypes.py`
- **Features:** Parallel processing, batched domain extraction

#### Step 3: Quality Analysis & Factsheet Generation
- **Input:** `{stem}_facts.json`
- **Outputs:**
  - `{stem}_analysis.html` (interactive dashboard)
  - `{stem}_analysis.xlsx` (spreadsheet)
  - `{stem}_factsheet.html` (formatted report)
  - `{stem}_factsheet.xlsx` (structured workbook)
- **Duration:** ~5-10 minutes
- **Script:** `esia-fact-analyzer/analyze_esia_v2.py`

#### Step 4: Interactive Fact Browser Generation (NEW) ✅
- **Input:** `{stem}_meta.json` (from Step 1)
- **Outputs:**
  - `{stem}_fact_browser.html` (~1.5 MB, interactive viewer with collapsible tables)
  - `{stem}_fact_browser.xlsx` (~227 KB, organized by ESIA category)
- **Duration:** ~2-3 seconds
- **Script:** `build_fact_browser.py`
- **Features:**
  - Collapsible table row headers (grouped by 5 rows)
  - Global search with highlighting
  - 9 ESIA categories with auto-classification
  - Page provenance tracking
  - Professional styling

### 5. Output Files

**All outputs saved to:** `m:\GitHub\esia-workspace\data\outputs\`

```
data/outputs/
├── {stem}_chunks.jsonl                 (Step 1)
├── {stem}_meta.json                    (Step 1)
├── {stem}_facts.json                   (Step 2)
├── {stem}_analysis.html                (Step 3)
├── {stem}_analysis.xlsx                (Step 3)
├── {stem}_factsheet.html               (Step 3)
├── {stem}_factsheet.xlsx               (Step 3)
├── {stem}_fact_browser.html            (Step 4) ✨ NEW
└── {stem}_fact_browser.xlsx            (Step 4) ✨ NEW
```

### 6. Frontend Progress Display

**File:** `packages/app/components/FileUpload.tsx`

**Real-time updates:**
- Polls `/api/pipeline/:executionId` every 500ms
- Displays step progress (Step 1 of 4 → Step 2 of 4 → etc.)
- Shows page-level progress for Step 1
- Updates status on completion or error
- Provides download links for outputs

---

## Configuration

### Pipeline Steps Configuration

**File:** `packages/app/pipeline.config.js` (UPDATED ✅)

```javascript
steps: [
  {
    id: 'step1_chunking',
    name: 'Step 1: Document Chunking',
    script: '../run-esia-pipeline.py',
    args: ['{PDF_FILE}', '--steps', '1', '--use-cuda'],
    timeout: 600000,  // 10 minutes
  },
  {
    id: 'step2_extraction',
    name: 'Step 2: Fact Extraction',
    script: '../run-esia-pipeline.py',
    args: ['{PDF_FILE}', '--steps', '2'],
    timeout: 14400000,  // 4 hours
  },
  {
    id: 'step3_analysis',
    name: 'Step 3: Fact Analysis & Factsheet Generation',
    script: '../run-esia-pipeline.py',
    args: ['{PDF_FILE}', '--steps', '3'],
    timeout: 600000,  // 10 minutes
  },
  {
    id: 'step4_fact_browser',
    name: 'Step 4: Interactive Fact Browser',
    script: '../run-esia-pipeline.py',
    args: ['{PDF_FILE}', '--steps', '4'],
    timeout: 60000,  // 1 minute
  },
]
```

### Python Version

**Required:** Python 3.12 from `packages/pipeline/venv312/`
- Configured in `pipeline.config.js:76`
- Used by `pipelineExecutor.js` when spawning subprocess

---

## Testing the Complete Flow

### Option 1: Via Web UI (Recommended)

```bash
# 1. Start application
.\run-app.ps1

# 2. Open http://localhost:3000 in browser
# 3. Click "Upload PDF"
# 4. Select a PDF file (< 50 MB)
# 5. Watch the 4-step pipeline progress
# 6. Download results when complete
```

### Option 2: Direct Python CLI (For Debugging)

```bash
cd packages/pipeline

# Run all 4 steps
python run-esia-pipeline.py "path/to/document.pdf" --steps 1,2,3,4

# Or run Step 4 only (if previous steps completed)
python run-esia-pipeline.py "path/to/document.pdf" --steps 4

# With verbose output
python run-esia-pipeline.py "path/to/document.pdf" --steps 1,2,3,4 --verbose
```

---

## Troubleshooting

### Issue: Backend not starting

**Solution:**
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill the process if needed
taskkill /PID <PID> /F

# Try again
.\run-app.ps1
```

### Issue: Frontend not loading

**Solution:**
- Backend must be running on port 5000
- Check backend window for errors
- Verify `server.js` is running

### Issue: Pipeline step hangs

**Solution:**
- Check `packages/pipeline/.env.local` has API key configured
- Verify Python path: `packages/pipeline/venv312/Scripts/python.exe`
- Try running step directly:
  ```bash
  cd packages/pipeline
  venv312/Scripts/python.exe run-esia-pipeline.py test.pdf --steps 4 --verbose
  ```

### Issue: Step 4 doesn't generate output

**Solution:**
- Verify Step 1 completed (creates `*_meta.json`)
- Check `data/outputs/` for input file
- Run Step 4 manually:
  ```bash
  python run-esia-pipeline.py "path/to/document.pdf" --steps 4
  ```

---

## Files Modified for Step 4 Integration

| File | Change | Impact |
|------|--------|--------|
| `packages/pipeline/build_fact_browser.py` | Created (~950 lines) | New Step 4 implementation |
| `packages/pipeline/run-esia-pipeline.py` | Added `run_fact_browser()` function | Step 4 execution support |
| `packages/app/pipeline.config.js` | Added Step 4 configuration | ✅ Frontend now includes Step 4 |
| `PIPELINE_INTEGRATION.md` | Created | Documentation for integration |

---

## Performance Summary

### Typical Execution Times (200-page document)

| Step | Time | Notes |
|------|------|-------|
| Step 1: Chunking | 5-10 min | GPU accelerated |
| Step 2: Extraction | 30-120 min | LLM-dependent |
| Step 3: Analysis | 5-10 min | Pure Python |
| Step 4: Fact Browser | 2-3 sec | Very fast ✨ |
| **Total** | **40-150 min** | Parallel workers in Step 2 |

---

## Summary

✅ **Yes, the entire 4-step pipeline runs with `./run-app.ps1`**

**Complete Execution Flow:**
1. User runs `.\run-app.ps1` → Starts backend + frontend
2. User uploads PDF via web UI → Backend triggers pipeline
3. Backend executes Steps 1, 2, 3, 4 sequentially → Each calls `run-esia-pipeline.py`
4. Frontend displays real-time progress → User sees all 4 steps complete
5. Results available for download → HTML, Excel, and analysis dashboards

**Key Update:** `pipeline.config.js` now includes Step 4 (Fact Browser) configuration, enabling the complete 4-step pipeline through the web interface.

---

**Last Updated:** December 3, 2025
**Version:** 1.0 - Complete 4-Step Pipeline Integration
**Status:** Production Ready ✅
