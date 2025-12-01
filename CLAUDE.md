# CLAUDE.md - ESIA Workspace Developer Guide

This file provides guidance to Claude Code when working with the ESIA Workspace. It explains the project structure, architecture, and key implementation details for all components.

## Workspace Overview

**Name:** ESIA Workspace (Environmental and Social Impact Assessment)
**Type:** Full-stack document intelligence application
**Location:** `M:\GitHub\esia-workspace`
**Purpose:** End-to-end ESIA document extraction, analysis, and reporting system

### Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│           ESIA WORKSPACE ARCHITECTURE                    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ FRONTEND (React + Tailwind CSS)                    │ │
│  │ packages/app                                       │ │
│  │ • File upload with progress                        │ │
│  │ • Real-time pipeline monitoring                    │ │
│  │ • Results visualization                            │ │
│  └────────────────────────────────────────────────────┘ │
│                      ↓ (Express API)                    │
│  ┌────────────────────────────────────────────────────┐ │
│  │ BACKEND (Express.js + Node.js)                     │ │
│  │ packages/app/server.js                             │ │
│  │ • File upload handling (Multer)                    │ │
│  │ • Pipeline orchestration                           │ │
│  │ • Execution status tracking                        │ │
│  └────────────────────────────────────────────────────┘ │
│                   ↓ (Python subprocess)                 │
│  ┌────────────────────────────────────────────────────┐ │
│  │ PIPELINE (Python)                                  │ │
│  │ packages/pipeline                                  │ │
│  │                                                    │ │
│  │ Step 1: Document Chunking                          │ │
│  │   esia-fact-extractor-pipeline/                    │ │
│  │   step1_docling_hybrid_chunking.py                 │ │
│  │   PDF/DOCX → chunks.jsonl + meta.json              │ │
│  │                                                    │ │
│  │ Step 2: Fact Extraction                            │ │
│  │   esia-fact-extractor-pipeline/src/                │ │
│  │   esia_extractor.py                                │ │
│  │   chunks.jsonl → facts.json (using DSPy + LLM)     │ │
│  │                                                    │ │
│  │ Step 3: Quality Analysis                           │ │
│  │   esia-fact-analyzer/                              │ │
│  │   analyze_esia_v2.py                               │ │
│  │   facts.json → HTML dashboard + Excel report       │ │
│  └────────────────────────────────────────────────────┘ │
│                      ↓                                   │
│  ┌────────────────────────────────────────────────────┐ │
│  │ OUTPUTS (File Storage)                             │ │
│  │ packages/pipeline/data/outputs/                    │ │
│  │ • Chunks (chunks.jsonl)                            │ │
│  │ • Facts (facts.json)                               │ │
│  │ • HTML Dashboard (review.html)                     │ │
│  │ • Excel Report (review.xlsx)                       │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Quick Start for Claude Code

When working on this workspace:
1. **Frontend issues?** See `packages/app/` - React/Tailwind components
2. **Backend issues?** See `packages/app/server.js` - Express API server
3. **Pipeline issues?** See `packages/pipeline/claude.md` - Python pipeline guide
4. **Installation?** See `packages/pipeline/REQUIREMENTS_GUIDE.md`
5. **Architecture?** See `packages/pipeline/DIRECTORY_STRUCTURE.md`

### ⚠️ CRITICAL: Python Environment Configuration ⚠️

**MANDATORY REQUIREMENT - READ THIS EVERY TIME:**

**Python 3.12 from venv312 MUST BE ACTIVATED/CHECKED EVERY TIME PYTHON IS RUN**

**BEFORE running ANY Python command:**
1. ✅ **ALWAYS verify** you're using `packages/pipeline/venv312/Scripts/python.exe`
2. ✅ **ALWAYS check** the pipeline.config.js uses the correct path
3. ✅ **NEVER use** system Python or any other Python installation
4. ✅ **ALWAYS test** the Python version before running pipeline commands

**Required Configuration:**
- **Location:** `packages/pipeline/venv312/`
- **Python Version:** Python 3.12 (ONLY)
- **Python Executable:** `packages/pipeline/venv312/Scripts/python.exe`
- **Configuration File:** `packages/app/pipeline.config.js`

**The pipeline.config.js MUST ALWAYS specify:**

```javascript
pythonExecutable: path.resolve('../pipeline/venv312/Scripts/python.exe')
```

**Verification Command (run this BEFORE executing pipeline):**

```bash
cd packages/pipeline
venv312/Scripts/python.exe --version  # Should output: Python 3.12.x
```

**Why This Matters:**
- The venv312 environment contains ALL required dependencies
- PyTorch with CUDA support (for GPU acceleration)
- torchvision (v0.20.1+cu121)
- Docling and all pipeline-specific packages
- System Python is missing these dependencies and WILL FAIL

---

## Workspace Structure

```
esia-workspace/
├── CLAUDE.md                           # This file (workspace guide)
├── CONSOLIDATION_SUMMARY.md            # Requirements consolidation summary
├── pipeline_flow.md                    # Pipeline execution guide
├── pnpm-workspace.yaml                 # Monorepo workspace config
├── package.json                        # Root workspace dependencies
│
├── packages/
│   ├── app/                            # FRONTEND & BACKEND
│   │   ├── index.html                  # Vite entry HTML
│   │   ├── index.tsx                   # React root entry
│   │   ├── server.js                   # Express backend server
│   │   ├── pipelineExecutor.js         # Pipeline subprocess orchestrator
│   │   ├── pipeline.config.js          # Pipeline configuration
│   │   │
│   │   ├── app/                        # Next.js-style App Router
│   │   │   ├── layout.tsx              # Root layout
│   │   │   ├── page.tsx                # Home page
│   │   │   └── globals.css             # Global Tailwind styles
│   │   │
│   │   ├── components/
│   │   │   └── FileUpload.tsx          # Main upload component
│   │   │
│   │   ├── services/
│   │   │   └── apiService.ts           # API client
│   │   │
│   │   ├── data/
│   │   │   ├── pdf/                    # Uploaded PDFs
│   │   │   └── output/                 # Processing results
│   │   │
│   │   └── [config files]
│   │       ├── vite.config.ts
│   │       ├── tsconfig.json
│   │       ├── tailwind.config.js
│   │       └── package.json
│   │
│   ├── pipeline/                       # PYTHON PIPELINE
│   │   ├── requirements.txt             # Consolidated dependencies
│   │   ├── REQUIREMENTS_GUIDE.md        # Installation guide
│   │   ├── DIRECTORY_STRUCTURE.md       # Architecture analysis
│   │   ├── claude.md                    # Pipeline-specific guide
│   │   ├── pipeline_flow.md             # Step-by-step execution
│   │   ├── run-esia-pipeline.py         # Main orchestrator
│   │   ├── config.py                    # Root configuration
│   │   │
│   │   ├── data/
│   │   │   ├── pdfs/                    # Input documents
│   │   │   └── outputs/                 # Pipeline outputs
│   │   │
│   │   ├── esia-fact-extractor-pipeline/    # Steps 1 & 2
│   │   │   ├── step1_docling_hybrid_chunking.py
│   │   │   ├── step3_extraction_with_archetypes.py
│   │   │   ├── src/                     # Core modules
│   │   │   └── data/archetypes/         # Domain reference data
│   │   │
│   │   └── esia-fact-analyzer/          # Step 3
│   │       ├── analyze_esia_v2.py
│   │       └── esia_analyzer/
│   │           ├── reviewer.py
│   │           ├── exporters/
│   │           └── factsheet/
│   │
│   └── shared/                          # SHARED UTILITIES
│       └── src/
│           ├── types.ts                 # Shared TypeScript types
│           ├── utils.ts                 # Shared utility functions
│           └── index.ts                 # Exports
│
└── .gitignore, .env.example, etc.
```

---

## Key Technologies by Component

### Frontend (packages/app)
- **React 19** - Latest React with concurrent features
- **TypeScript 5** - Type safety
- **Vite 6** - Ultra-fast dev server and build tool
- **Tailwind CSS 3** - Utility-first styling
- **Next.js routing structure** - File-based routing conventions

### Backend (packages/app)
- **Express 4** - Lightweight web server
- **Multer 1** - File upload middleware
- **Node.js** - JavaScript runtime

### Pipeline (packages/pipeline)
**See `packages/pipeline/claude.md` for complete details**

#### Extraction (Python)
- **Docling** - PDF/DOCX parsing
- **DSPy** - LLM programming framework
- **Google Gemini API** - LLM provider
- **Tiktoken** - Token counting

#### Analysis (Python)
- **Pure Python** - Rule-based logic
- **openpyxl** - Excel generation
- **Jinja2** - HTML templating

---

## Frontend Development

### File Upload Component
**File:** `packages/app/components/FileUpload.tsx` (580 lines)

**Features:**
- Drag-and-drop PDF upload
- File validation (PDF only, max 50MB)
- Upload progress bar
- Real-time pipeline status polling
- Step-by-step progress display
- Cancellable uploads

### Backend API
**File:** `packages/app/server.js`

**Endpoints:**
- `POST /api/upload` - Upload PDF and trigger pipeline
- `GET /api/pipeline/:executionId` - Get execution status
- `GET /api/pipeline` - Get execution history
- `GET /health` - Health check

### API Service
**File:** `packages/app/services/apiService.ts`

**Functions:**
- `uploadFile(file, onProgress)` - Upload with progress
- `getPipelineStatus(executionId)` - Poll pipeline status

---

## Backend Development

### Express Server Setup
**File:** `packages/app/server.js`

Key features:
- Multer file upload handling
- UTF-8 encoding support
- 50MB file size limit
- Async pipeline execution (non-blocking)

### Pipeline Executor
**File:** `packages/app/pipelineExecutor.js`

Responsibilities:
- Spawns Python subprocess
- Manages execution state
- Monitors stdout/stderr
- Tracks progress with page numbers
- Cleans up old executions

### Pipeline Configuration
**File:** `packages/app/pipeline.config.js`

Defines:
- Python executable path
- Pipeline script location
- Default step selections
- Output directories

---

## Python Pipeline Development

### For Complete Pipeline Details
**See:** `packages/pipeline/claude.md`

Quick overview:
- **Step 1:** Document chunking (Docling, GPU-accelerated)
- **Step 2:** Fact extraction (DSPy + Gemini API)
- **Step 3:** Quality analysis (Rule-based, pure Python)

### Key Files
- **Orchestrator:** `packages/pipeline/run-esia-pipeline.py`
- **Extractor:** `packages/pipeline/esia-fact-extractor-pipeline/src/esia_extractor.py`
- **Analyzer:** `packages/pipeline/esia-fact-analyzer/esia_analyzer/reviewer.py`
- **Dependencies:** `packages/pipeline/requirements.txt` (single source of truth)

---

## Development Workflow

### 1. Frontend Development

```bash
cd packages/app

# Install dependencies
pnpm install

# Start Vite dev server (port 3000)
pnpm dev

# Build for production
pnpm build
```

**Important:**
- Dev server proxies `/api/*` to `http://127.0.0.1:5000`
- Backend server must be running on port 5000
- Tailwind CSS is compiled automatically

### 2. Backend Development

```bash
cd packages/app

# Backend runs alongside frontend
# Express server listens on port 5000
# Serves file upload endpoints
```

**Important:**
- Backend must be running before frontend can upload files
- Check `server.js` for port configuration
- API endpoints in `server.js`

### 3. Pipeline Development

```bash
cd packages/pipeline

# Install dependencies
pip install -r requirements.txt

# Set API key
$env:GOOGLE_API_KEY = "your_key"

# Run complete pipeline
python run-esia-pipeline.py data/pdfs/document.pdf --steps 1,2,3 --verbose

# Run specific steps
python run-esia-pipeline.py document.pdf --steps 1  # Chunking only
python run-esia-pipeline.py document.pdf --steps 2  # Extraction only
python run-esia-pipeline.py document.pdf --steps 3  # Analysis only
```

**For detailed pipeline development, see:**
- `packages/pipeline/claude.md` - Pipeline-specific guide
- `packages/pipeline/REQUIREMENTS_GUIDE.md` - Installation guide
- `packages/pipeline/DIRECTORY_STRUCTURE.md` - Architecture guide

---

## Common Development Tasks

### Task: Fix Frontend Bug
1. Check `packages/app/components/` for UI issues
2. Check `packages/app/services/apiService.ts` for API calls
3. Check browser console for errors
4. Verify backend server is running on port 5000

### Task: Fix Backend Bug
1. Check `packages/app/server.js` for endpoint issues
2. Check `packages/app/pipelineExecutor.js` for subprocess handling
3. Check `packages/app/pipeline.config.js` for configuration
4. Test with: `curl http://localhost:5000/health`

### Task: Fix Pipeline Bug
1. **See `packages/pipeline/claude.md`** for complete guide
2. Run with `--verbose` flag to see detailed logs
3. Test individual steps separately
4. Check `data/outputs/` for intermediate results

### Task: Add New Pipeline Feature
1. Decide if it's extraction (Steps 1-2) or analysis (Step 3)
2. **See `packages/pipeline/claude.md`** for implementation patterns
3. Update `packages/pipeline/requirements.txt` if adding dependencies
4. Test complete pipeline end-to-end

### Task: Add New Frontend Feature
1. Create component in `packages/app/components/`
2. Update `packages/app/app/page.tsx` to use it
3. Add styling with Tailwind CSS classes
4. Test with dev server running

---

## Running the Complete Application

### Full Stack Setup

```bash
# From workspace root
cd esia-workspace

# 1. Install all dependencies
pnpm install

# 2. Install Python pipeline dependencies
cd packages/pipeline
pip install -r requirements.txt

# 3. Set API key
$env:GOOGLE_API_KEY = "your_key"

# 4. From workspace root, start frontend
pnpm dev

# 5. In another terminal, start backend
cd packages/app
node server.js
```

Then open browser at `http://localhost:3000`

### Testing the Pipeline

```powershell
# Option 1: Upload via UI
# Go to http://localhost:3000, upload PDF, watch progress

# Option 2: Test directly
cd packages/pipeline
python run-esia-pipeline.py data/pdfs/test.pdf --steps 1,2,3 --verbose
```

---

## Environment Variables

### Frontend/Backend
```bash
# packages/app/.env (if needed)
VITE_API_URL=http://127.0.0.1:5000
```

### Pipeline
```bash
# packages/pipeline/.env (REQUIRED)
GOOGLE_API_KEY=your_google_api_key
OPENROUTER_API_KEY=your_openrouter_api_key  # Optional
```

**Important:**
- Never commit `.env` files
- Use `.gitignore` to prevent accidental commits
- Set environment variables before running

---

## File Organization Best Practices

### Frontend/Backend
- **Components:** Keep in `packages/app/components/`
- **Services:** Keep API logic in `packages/app/services/`
- **Styles:** Use Tailwind CSS classes (avoid custom CSS when possible)
- **Configs:** Centralize in root config files (vite.config.ts, etc.)

### Pipeline
- **Python modules:** Keep in `src/` subdirectories
- **Scripts:** Step files at package root (step1_*, step3_*)
- **Data:** Reference data in `data/archetypes/`, inputs in `data/pdfs/`, outputs in `data/outputs/`
- **Docs:** Keep documentation separate from code

---

## Testing

### Frontend Testing
```bash
cd packages/app

# Unit tests (if configured)
pnpm test

# Manual testing
pnpm dev  # Start dev server, test in browser
```

### Backend Testing
```bash
# Test health endpoint
curl http://localhost:5000/health

# Test API
curl -X POST http://localhost:5000/api/upload \
  -F "file=@document.pdf"
```

### Pipeline Testing
```bash
cd packages/pipeline

# Run complete pipeline
python run-esia-pipeline.py test.pdf --steps 1,2,3 --verbose

# Test individual steps
python run-esia-pipeline.py test.pdf --steps 1
python run-esia-pipeline.py test.pdf --steps 2
python run-esia-pipeline.py test.pdf --steps 3
```

---

## Troubleshooting

### Frontend Issues

**"Cannot GET /"**
- Frontend server not running
- Solution: `pnpm dev` from `packages/app/`

**"API connection failed"**
- Backend server not running
- Solution: `node server.js` from `packages/app/`

**"File upload stuck"**
- Backend not responding
- Solution: Check `server.js` is running, check port 5000

### Backend Issues

**"PORT already in use"**
- Another process using port 5000
- Solution: Kill process or change port in `server.js`

**"File not found"**
- Wrong path to pipeline script
- Solution: Check `pipeline.config.js` paths are correct

### Pipeline Issues

**See `packages/pipeline/REQUIREMENTS_GUIDE.md`** for complete troubleshooting

---

## Red Flags (Don't Do This)

❌ **Don't commit `.env` files** - Use `.gitignore`
❌ **Don't hardcode API keys** - Always use environment variables
❌ **Don't merge pipeline directories** - They serve different purposes
❌ **Don't remove consolidated requirements.txt** - It's the single source of truth
❌ **Don't create new top-level packages** - Keep in `packages/` subdirectories
❌ **Don't change port numbers** - Document any changes clearly
❌ **Don't skip `--verbose` when debugging** - It's essential information

---

## Documentation Hierarchy

1. **This file (CLAUDE.md)** - Workspace overview and integration
2. **packages/pipeline/claude.md** - Pipeline-specific developer guide
3. **packages/pipeline/pipeline_flow.md** - Step-by-step execution guide
4. **packages/pipeline/REQUIREMENTS_GUIDE.md** - Installation and dependencies
5. **packages/pipeline/DIRECTORY_STRUCTURE.md** - Architecture analysis

---

## Getting Help

1. **Frontend/Backend issues?** Check `packages/app/` files
2. **Pipeline issues?** See `packages/pipeline/claude.md`
3. **Installation issues?** See `packages/pipeline/REQUIREMENTS_GUIDE.md`
4. **Architecture questions?** See `packages/pipeline/DIRECTORY_STRUCTURE.md`
5. **Running the app?** See this file's "Running the Complete Application" section
6. **Not sure where to start?** Read this file, then `packages/pipeline/claude.md`

---

## Quick Reference Commands

```powershell
# Frontend development
cd packages/app
pnpm dev              # Start dev server

# Backend
cd packages/app
node server.js        # Start backend

# Pipeline
cd packages/pipeline
pip install -r requirements.txt        # Install deps
$env:GOOGLE_API_KEY = "key"            # Set API key
python run-esia-pipeline.py doc.pdf    # Run pipeline

# View results
Get-ChildItem packages/pipeline/data/outputs/
Invoke-Item packages/pipeline/data/outputs/doc_review.html
```

---

## For Claude Code Users

When working on this workspace:

1. **Read this file first** - Understand overall architecture
2. **Identify which component** - Frontend, backend, or pipeline?
3. **Check component-specific guide:**
   - Frontend/Backend: See `packages/app/` code structure
   - Pipeline: See `packages/pipeline/claude.md`
4. **Follow best practices** from the relevant guide
5. **Test thoroughly** before committing

---

**Last Updated:** December 1, 2025
**Version:** 1.0
**Status:** Active Development
**Architecture:** React + Express + Python
**Primary OS:** Windows (PowerShell)
**Target Audience:** Full-stack developers and Claude Code

