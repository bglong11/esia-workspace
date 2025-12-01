# ESIA.ai - Project Documentation

## ⚠️ Important Development Notes

**ALWAYS USE POWERSHELL for Windows commands.** The project is developed on Windows, and PowerShell provides better compatibility and reliability for file operations, encoding handling, and command execution.

---

## Project Overview

**ESIA.ai** is an AI-powered Environmental and Social Impact Assessment (ESIA) document processing application. It provides a web-based interface for users to upload PDF documents and process them through a sophisticated pipeline that:

- Extracts and chunks PDF content into semantic units with page tracking
- Extracts domain-specific facts using archetype-based extraction
- Analyzes extracted data for consistency and compliance

**Location**: `M:\GitHub\esia-ai`

---

## Tech Stack

### Frontend
- **React 19.2.0** - UI framework
- **TypeScript 5.8.2** - Type safety
- **Vite 6.2.0** - Build tool and dev server
- **Tailwind CSS 3.4.0** - Utility-first styling
- **Next.js 16.0.5** - Full-stack framework (minimal usage)

### Backend
- **Node.js** with **Express 4.18.2** - Web server (port 5000)
- **Multer 1.4.5** - File upload middleware
- **ES Modules** - Modern JavaScript

### External Integration
- **Python Pipeline** - Located at `M:\GitHub\esia-pipeline`
- Runs as subprocess for document processing

---

## Project Structure

```
M:\GitHub\esia-ai/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout with Tailwind
│   ├── page.tsx           # Home page (main container)
│   └── globals.css        # Global styles
├── components/
│   └── FileUpload.tsx     # Main upload component (573 lines)
├── services/
│   └── apiService.ts      # Frontend API client
├── data/                  # Data storage
│   ├── pdfs/             # Uploaded PDFs (timestamped)
│   ├── outputs/          # Pipeline processing output
│   └── metadata/         # Pipeline execution records
├── server.js              # Express backend
├── pipeline.config.js     # Pipeline orchestration config
├── pipelineExecutor.js    # Pipeline execution engine
├── index.html & index.tsx # React entry points
├── types.ts               # TypeScript definitions
├── vite.config.ts         # Vite configuration
├── tsconfig.json          # TypeScript config
├── tailwind.config.js     # Tailwind config
├── postcss.config.js      # PostCSS config
├── next.config.js         # Next.js config
├── package.json           # Dependencies & scripts
├── .env.local             # Environment variables
└── .gitignore             # Git ignore rules
```

---

## Key Components

### Frontend

**FileUpload Component** (`components/FileUpload.tsx` - 573 lines)
- Drag-and-drop file input
- Upload progress tracking with percentage
- Real-time pipeline status monitoring
- Step-by-step progress display (including page-level progress)
- Error handling and user feedback
- Cancellable uploads

**API Service** (`services/apiService.ts`)
- `uploadFile(file, onProgress)` - Upload with progress callback
- `getPipelineStatus(executionId)` - Fetch pipeline execution status

### Backend

**Express Server** (`server.js` - port 5000)
- POST `/api/upload` - Upload PDF and trigger pipeline
- GET `/api/pipeline/:executionId` - Get execution status
- GET `/api/pipeline` - Get all executions (history)
- File serving via Multer with timestamped filenames

**Pipeline Executor** (`pipelineExecutor.js`)
- Spawns Python subprocess for document processing
- Manages execution state and progress tracking
- Cleans up old executions (> 1 hour)
- Regex pattern matching for progress extraction

---

## Data Flow

1. User uploads PDF via FileUpload component
2. Frontend validates file (PDF only, max 50MB)
3. File sent to `POST /api/upload` with progress tracking
4. Backend saves to `data/pdfs/{timestamp}-{filename}.pdf`
5. Backend triggers `executePipeline()` asynchronously
6. Server returns execution ID immediately
7. Frontend polls `/api/pipeline/{executionId}` every 1-2 seconds
8. Backend spawns Python subprocess: `python run-esia-pipeline.py {pdf_path}`
9. Python processes through 3 steps:
   - Chunks PDF into semantic units
   - Extracts domain-specific facts
   - Analyzes for consistency/compliance
10. Frontend displays real-time progress with step status
11. Pipeline outputs saved to `data/outputs/`

---

## API Endpoints

### Upload
```
POST /api/upload
Content-Type: multipart/form-data

Response:
{
  "message": "File uploaded successfully",
  "filename": "1704067200000-report.pdf",
  "size": 102400,
  "path": "/data/pdfs/1704067200000-report.pdf",
  "pipeline": {
    "executionId": "exec-1704067200000-abc123",
    "status": "running",
    "sanitizedName": "report"
  }
}
```

### Pipeline Status
```
GET /api/pipeline/:executionId

Response:
{
  "id": "exec-1704067200000-abc123",
  "pdfFilename": "1704067200000-report.pdf",
  "sanitizedName": "report",
  "status": "running|completed|failed",
  "startTime": "2025-11-30T12:00:00.000Z",
  "endTime": "2025-11-30T12:00:05.000Z",
  "steps": [
    {
      "stepId": "full_pipeline",
      "status": "completed|running|failed|pending",
      "name": "Docling Hybrid Chunking",
      "description": "Converting PDF to semantic chunks...",
      "progress": { "currentPage": 42, "totalPages": 200 }
    }
  ]
}
```

---

## Running the Project

### Installation
```bash
npm install
```

### Development
```bash
npm run dev              # Run frontend (3000) & backend (5000) in parallel
npm run dev:frontend    # Frontend only (Vite on port 3000)
npm run dev:server      # Backend only (Express on port 5000)
```

### Build
```bash
npm run build           # Build frontend with Vite
npm run preview         # Preview production build
```

### Environment Setup
Create/update `.env.local`:
```
GEMINI_API_KEY=your_api_key_here
```

### Access
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000

---

## Architecture Patterns

### Client-Server Architecture
- React frontend communicates with Express backend via REST API
- Vite proxy handles `/api/*` routes to backend (:5000)

### Async Pipeline Execution
- Non-blocking upload response (returns immediately)
- Frontend polls for status updates (1-2 second intervals)
- Real-time progress tracking

### File Storage Pattern
- Timestamped filenames prevent collisions: `{timestamp}-{original_name}.pdf`
- Filename sanitization for downstream processing
- Example: `1704067200000-My ESIA Report.pdf` → `my_esia_report`

### State Management
- Component-level state with React hooks
- In-memory execution status map on backend
- Auto-cleanup of old executions

---

## Key Features

- **Drag-and-Drop Upload** - Intuitive file input
- **Real-Time Progress** - Upload and pipeline progress tracking
- **Live Step Monitoring** - Step-by-step execution status
- **Page-Level Progress** - Shows "Page X of Y" during processing
- **Error Handling** - Graceful fallbacks and user-friendly messages
- **Responsive Design** - Mobile-friendly with Tailwind CSS
- **Accessibility** - ARIA labels, roles, semantic HTML
- **Cancellable Uploads** - Users can abort in-progress uploads
- **Execution History** - Backend maintains all pipeline executions

---

## Configuration Files

| File | Purpose |
|------|---------|
| `vite.config.ts` | Vite dev server config (port 3000), API proxy, TypeScript aliases |
| `tsconfig.json` | TypeScript: ES2022 target, JSX support, path aliases |
| `tailwind.config.js` | Tailwind CSS theme and content paths |
| `postcss.config.js` | PostCSS plugins: Tailwind, Autoprefixer |
| `pipeline.config.js` | Pipeline settings: script paths, timeouts, output dirs |
| `.env.local` | Environment variables (GEMINI_API_KEY) |
| `next.config.js` | Next.js configuration (minimal) |
| `package.json` | Dependencies, build scripts, project metadata |

---

## Database

**No traditional database is configured.** Currently uses:
- **File System**: PDFs, outputs, and metadata stored in `./data/`
- **In-Memory**: Pipeline execution status (lost on server restart)
- **Auto-Cleanup**: Executions older than 1 hour are cleaned up

---

## Testing

**No testing framework is currently configured.** Consider adding:
- Vitest or Jest for unit testing
- React Testing Library for component tests
- Integration tests for upload pipeline

---

## Important Notes

- Python pipeline located at `M:\GitHub\esia-pipeline` (separate repository)
- API key required: Set `GEMINI_API_KEY` in `.env.local`
- Backend spawns Python subprocess for processing
- Frontend handles all UI/UX, backend manages orchestration
- Graceful fallback if Python script missing (mock execution)

---

## Quick Start for New Developers

1. Install dependencies: `npm install`
2. Set API key in `.env.local`
3. Start development: `npm run dev`
4. Navigate to http://localhost:3000
5. Upload a PDF and monitor pipeline progress

---

## External Dependencies

- **Frontend Port**: 3000 (Vite)
- **Backend Port**: 5000 (Express)
- **Python Pipeline**: `M:\GitHub\esia-pipeline`
- **Node.js**: Required runtime
- **Python**: Required for pipeline execution
