# ESIA Workspace - Comprehensive Developer Documentation

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Architecture Overview](#2-architecture-overview)
3. [Detailed Module Documentation](#3-detailed-module-documentation)
4. [Development Guide](#4-development-guide)
5. [Deployment & Operations](#5-deployment--operations)
6. [API Reference](#6-api-reference)
7. [Contributing Guidelines](#7-contributing-guidelines)

---

# 1. Executive Summary

## What is ESIA Workspace?

**ESIA Workspace** is a comprehensive, AI-powered monorepo for processing and analyzing Environmental and Social Impact Assessment (ESIA) documents. It provides an end-to-end solution for extracting, analyzing, and ensuring compliance of ESIA reports with international standards (IFC EHS Guidelines, ADB, World Bank requirements).

**Location**: `M:\GitHub\esia-workspace`

## Purpose and Value

### Primary Purpose
Transform unstructured ESIA documents (PDFs/DOCX) into structured, validated, and compliance-checked data through an intelligent pipeline that:

1. **Extracts** domain-specific facts from documents using LLM-based extraction
2. **Analyzes** extracted facts for consistency, compliance, and completeness
3. **Validates** against international standards and best practices
4. **Presents** findings through interactive dashboards and detailed reports

### Value Proposition

- **Time Savings**: Automates manual review processes that typically take days or weeks
- **Compliance Assurance**: Validates against IFC EHS Guidelines, ADB, World Bank standards
- **Quality Control**: Detects inconsistencies, gaps, and threshold violations automatically
- **Transparency**: Provides traceable, auditable analysis with page references
- **Accessibility**: Web-based interface accessible from any modern browser
- **Scalability**: Processes documents of any size with progress tracking

### Target Users

- **Environmental Consultants**: Review and validate ESIA documents
- **Regulatory Bodies**: Assess compliance with international standards
- **Financial Institutions**: Evaluate loan applications with ESIA requirements
- **Project Developers**: Self-assess document quality before submission

## Key Capabilities

### 1. Document Processing Pipeline
- PDF/DOCX ingestion with automatic format detection
- Semantic chunking with page tracking (via Docling)
- Multi-page document support with progress monitoring
- Resilient processing with checkpoint/resume capability

### 2. Intelligent Fact Extraction
- LLM-based extraction using DSPy framework
- 80+ unit conversions with automatic normalization
- Archetype-based pattern matching for domain-specific facts
- Categorization into 8 categories and 32 subcategories
- Caching mechanism (37-80% hit rate) to reduce LLM API costs

### 3. Comprehensive Analysis
- Context-aware consistency checking (like-for-like comparisons)
- Unit standardization detection
- Threshold compliance validation against IFC EHS limits
- Gap analysis for missing expected content
- Conflict detection with 2% tolerance (detects ×10 errors)

### 4. Professional Reporting
- Interactive HTML dashboard with dark theme
- Detailed Excel workbook exports
- CSV outputs for integration with other tools
- Page-referenced findings for traceability
- Severity indicators (Critical, High, Medium, Low)

### 5. Developer-Friendly Architecture
- Monorepo structure with clear package boundaries
- Shared utilities and type definitions
- TypeScript for type safety
- Python for AI/ML processing
- Hot reload for rapid development
- Comprehensive documentation

## Technology Stack Summary

### Frontend
- **React 19.2.0** - Modern UI framework with concurrent features
- **TypeScript 5.8.2** - Type-safe development
- **Vite 6.2.0** - Lightning-fast build tool and dev server
- **Tailwind CSS 3.4.0** - Utility-first styling

### Backend
- **Node.js with Express 4.18.2** - Web server and API
- **Multer 1.4.5** - File upload handling
- **ES Modules** - Modern JavaScript module system

### AI/ML Processing
- **Python 3.9+** - Core processing language
- **DSPy** - Language model programming framework
- **Docling** - PDF-to-markdown conversion with semantic chunking
- **OpenRouter API** - LLM integration (supports any model)
- **Pandas** - Data manipulation and analysis

### Development Tools
- **pnpm** - Fast, disk-efficient package manager
- **Git** - Version control with monorepo support
- **PowerShell** - Windows command-line development

### Infrastructure
- **File System** - Document and output storage
- **In-Memory State** - Pipeline execution tracking
- **JSON/JSONL** - Data interchange format

---

# 2. Architecture Overview

## System Components

The ESIA Workspace is organized as a monorepo with five main packages:

```
esia-workspace/
├── packages/
│   ├── app/              # Web application (React + Express)
│   ├── pipeline/         # Python orchestration pipeline
│   ├── fact-extractor/   # Fact extraction engine
│   ├── fact-analyzer/    # Analysis and consistency engine
│   └── shared/           # Shared TypeScript utilities
├── package.json          # Workspace root configuration
├── pnpm-workspace.yaml   # Package manager workspace config
└── tsconfig.base.json    # Shared TypeScript configuration
```

### Component Responsibilities

#### 1. App Package (`@esia/app`)
- **Type**: Node.js (React + Express)
- **Port**: Frontend (3000), Backend (5000)
- **Responsibilities**:
  - User interface for document upload
  - File handling and validation
  - Pipeline orchestration and status tracking
  - Real-time progress updates
  - Result presentation


#### 2. Pipeline Package (`@esia/pipeline`)
- **Type**: Python
- **Responsibilities**:
  - Orchestrates the 3-step processing workflow
  - Coordinates fact-extractor and fact-analyzer
  - Manages unified input/output directories
  - Provides CLI interface for automation
  - Handles filename sanitization

#### 3. Fact Extractor Package (`@esia/fact-extractor`)
- **Type**: Python
- **Responsibilities**:
  - Converts PDF/DOCX to semantic chunks
  - Extracts domain-specific facts using DSPy
  - Normalizes units and values
  - Categorizes facts into taxonomy
  - Generates CSV outputs

#### 4. Fact Analyzer Package (`@esia/fact-analyzer`)
- **Type**: Python
- **Responsibilities**:
  - Analyzes extracted facts for consistency
  - Validates against IFC/ADB/World Bank standards
  - Detects gaps in expected content
  - Generates HTML dashboard and Excel reports
  - Provides detailed issue tracking

#### 5. Shared Package (`@esia/shared`)
- **Type**: TypeScript
- **Responsibilities**:
  - Common type definitions
  - Utility functions (sanitization, formatting)
  - Shared constants
  - Reusable business logic

## Data Flow Diagrams

### High-Level System Flow

```
┌─────────────────┐
│  User Browser   │
│  (Port 3000)    │
└────────┬────────┘
         │ HTTP/WebSocket
         ▼
┌─────────────────────────┐
│   React Frontend        │
│   - File upload UI      │
│   - Progress tracking   │
│   - Results display     │
└────────┬────────────────┘
         │ REST API (/api/*)
         ▼
┌─────────────────────────┐
│   Express Backend       │
│   (Port 5000)           │
│   - File handling       │
│   - Pipeline execution  │
│   - Status polling      │
└────────┬────────────────┘
         │ Subprocess spawn
         ▼
┌─────────────────────────────────────────────────┐
│          Python Pipeline                        │
│  (run-esia-pipeline.py)                         │
│                                                  │
│  Step 1: ┌──────────────────────┐              │
│          │  Docling Chunking    │              │
│          │  - PDF → Markdown    │              │
│          │  - Semantic chunks   │              │
│          │  - Page tracking     │              │
│          └──────────┬───────────┘              │
│                     │                           │
│  Step 2: ┌──────────▼───────────┐              │
│          │  Fact Extraction     │              │
│          │  - DSPy LLM calls    │              │
│          │  - Unit normalization│              │
│          │  - Categorization    │              │
│          └──────────┬───────────┘              │
│                     │                           │
│  Step 3: ┌──────────▼───────────┐              │
│          │  Fact Analysis       │              │
│          │  - Consistency check │              │
│          │  - Threshold validate│              │
│          │  - Gap analysis      │              │
│          │  - Report generation │              │
│          └──────────────────────┘              │
│                                                  │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │  Output Storage     │
         │  - data/outputs/    │
         │  - CSV files        │
         │  - HTML dashboard   │
         │  - Excel workbook   │
         └─────────────────────┘
```

### Detailed Pipeline Flow

```
┌──────────────────────────────────────────────────────────────┐
│                     PDF Upload Process                       │
└──────────────────────────────────────────────────────────────┘

User uploads PDF
      │
      ▼
Frontend validation (PDF only, max 50MB)
      │
      ▼
POST /api/upload with FormData
      │
      ▼
Backend (Multer middleware)
      │
      ├─ Save to: data/pdf/{timestamp}-{filename}.pdf
      │
      ├─ Generate execution ID: exec-{timestamp}-{random}
      │
      ├─ Sanitize filename: "My Report.pdf" → "my_report"
      │
      └─ Trigger executePipeline() (non-blocking)
            │
            ▼
      ┌─────────────────────────────────────────────────┐
      │  Background Pipeline Execution                  │
      │                                                  │
      │  1. Spawn Python subprocess                     │
      │     - python run-esia-pipeline.py {pdf_path}    │
      │     - Working dir: M:/GitHub/esia-pipeline      │
      │     - Environment: PYTHONIOENCODING=utf-8       │
      │                                                  │
      │  2. Monitor stdout/stderr                       │
      │     - Regex pattern matching for progress       │
      │     - Extract: "Page 42 of 411"                 │
      │     - Update execution status in memory         │
      │                                                  │
      │  3. Handle completion                           │
      │     - Exit code 0: status = 'completed'         │
      │     - Exit code non-0: status = 'failed'        │
      │     - Timeout: kill process                     │
      │                                                  │
      └─────────────────────────────────────────────────┘
            │
            ▼
Return response immediately (don't wait for pipeline)
      │
      ▼
Frontend polls GET /api/pipeline/{executionId} every 1-2 seconds
      │
      ▼
Backend returns current execution status
      │
      └─ { id, status, steps: [{ stepId, status, progress }] }
            │
            ▼
      Display progress in UI
```

---

# 3. Detailed Module Documentation

## packages/app: Frontend & Backend

### Purpose and Responsibilities

The app package is the primary user-facing component that provides:

1. **Web Interface** - React-based UI for document upload and result viewing
2. **File Management** - Backend handling of PDF uploads with validation
3. **Pipeline Orchestration** - Spawning and monitoring Python pipeline execution
4. **Real-Time Updates** - Progress tracking with polling-based status updates
5. **Result Presentation** - Display of processing results and analysis reports

### Key Files

**Frontend:**
- `app/page.tsx` - Root page
- `components/FileUpload.tsx` - Upload UI (573 lines)
- `services/apiService.ts` - API client
- `types.ts` - Type definitions

**Backend:**
- `server.js` - Express server
- `pipelineExecutor.js` - Pipeline orchestration
- `pipeline.config.js` - Configuration

### How to Run

```bash
cd packages/app
npm install
npm run dev              # Frontend + Backend
npm run dev:frontend    # Frontend only (port 3000)
npm run dev:server      # Backend only (port 5000)
```

---

## packages/pipeline: Orchestration

### Purpose and Responsibilities

Orchestrates the 3-step ESIA processing pipeline:
1. Document chunking (Docling)
2. Fact extraction (DSPy + LLM)
3. Analysis and reporting

### Key Files

- `run-esia-pipeline.py` - Main orchestrator
- `config.py` - Configuration management
- Subdirectories for extractor and analyzer

### How to Run

```bash
python run-esia-pipeline.py data/pdfs/report.pdf
python run-esia-pipeline.py data/pdfs/report.pdf --verbose
python run-esia-pipeline.py data/pdfs/report.pdf --steps 1,3
```

---

## packages/fact-extractor: Extraction Engine

### Purpose and Responsibilities

1. Chunks PDFs using Docling with semantic understanding
2. Extracts domain-specific facts using DSPy + LLM
3. Normalizes 80+ unit types
4. Categorizes facts into taxonomy
5. Generates CSV outputs

### Key Files

- `esia_extractor.py` (1,300+ lines) - Main extraction engine
- `step1_pdf_to_markdown.py` - PDF conversion
- `step2_extract_facts.py` - Fact extraction wrapper

### How to Run

```bash
cd packages/fact-extractor
pip install -r requirements.txt
python esia_extractor.py input.md ./output
```

---

## packages/fact-analyzer: Analysis Engine

### Purpose and Responsibilities

1. Context-aware consistency checking
2. Threshold validation (IFC/ADB/World Bank)
3. Gap analysis for missing content
4. Unit standardization detection
5. HTML dashboard and Excel report generation

### Key Files

- `analyze_esia_v2.py` - Main entry point
- `esia_analyzer/reviewer.py` - Core analysis logic
- `esia_analyzer/consistency.py` - Consistency checking
- `esia_analyzer/exporters/` - Report generation

### How to Run

```bash
python analyze_esia_v2.py data/outputs/esia_mentions.csv
```

---

## packages/shared: Shared Utilities

### Purpose

Provides TypeScript types and utilities used across packages:
- Type definitions
- Utility functions (sanitization, ID generation)
- Constants

### Key Functions

```typescript
import {
  sanitizeFilename,
  generateExecutionId,
  formatFileSize
} from '@esia/shared';
```

---

# 4. Development Guide

## Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.9+
- pnpm 8+
- Git

### Initial Setup

```bash
# Clone and navigate
git clone <repo-url> esia-workspace
cd esia-workspace

# Install Node dependencies
pnpm install

# Install Python dependencies
cd packages/fact-extractor
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
cd ../..

# Configure environment
cd packages/app
cat > .env.local << EOF
GEMINI_API_KEY=your_key_here
EOF

cd ../pipeline
cat > .env << EOF
OPENROUTER_API_KEY=your_key_here
EOF
```

## Development Workflow

### Starting Services

```bash
# All services
pnpm dev

# Specific service
pnpm dev:app
```

### Accessing Services
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- Health: http://localhost:5000/health

### Git Workflow

```bash
# Feature branch
git checkout -b feature/description

# Commit with conventional messages
git commit -m "feat(scope): description"

# Push and create PR
git push -u origin feature/description
```

### Common Tasks

**Add API Endpoint:**
1. Edit `packages/app/server.js`
2. Define types in `packages/shared/src/types.ts`
3. Create client function in `packages/app/services/apiService.ts`

**Add Python Step:**
1. Create step script
2. Update `packages/app/pipeline.config.js`
3. Add progress monitoring

**Modify Shared Utility:**
1. Edit file in `packages/shared/src/`
2. Build: `cd packages/shared && npm run build`
3. Use in other packages

## Debugging

### Frontend
```javascript
// Browser DevTools (F12)
// Check Console and Network tabs
console.log('Debug:', value);

// Vite logs
// Check server terminal
```

### Backend
```javascript
// Add logging
import { logger } from './logger.js';
logger.info('Message', data);

// Enable inspector
node --inspect server.js
// chrome://inspect
```

### Python
```python
# Add print statements
print(f"DEBUG: {variable}")

# Use pdb
import pdb; pdb.set_trace()

# Run with verbose flag
python run-esia-pipeline.py file.pdf --verbose
```

---

# 5. Deployment & Operations

## Environment Configuration

### App Package (.env.local)
```env
GEMINI_API_KEY=your_key
PORT=5000
NODE_ENV=production
```

### Pipeline Package (.env)
```env
GOOGLE_API_KEY=your_key
OPENROUTER_API_KEY=your_key
OUTPUT_DIR=./data/outputs
```

## Deployment Options

### Development
```bash
pnpm install
pnpm dev
```

### Production (Traditional)
```bash
# Build
npm run build

# Configure environment
export NODE_ENV=production
export PORT=5000

# Start with PM2
pm2 start packages/app/server.js
```

### Docker
```bash
docker-compose up -d
```

## Monitoring

### Health Check
```bash
curl http://localhost:5000/health
```

### Logs
```bash
# Backend
tail -f packages/app/logs/error.log

# Python
tail -f packages/pipeline/pipeline_output.log
```

### Common Issues

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <pid> /F

# Linux/Mac
lsof -i :5000
kill -9 <pid>
```

**Pipeline timeout:**
- Increase timeout in `pipeline.config.js`
- Check Python dependencies
- Verify API keys in `.env`

**Frontend not updating:**
- Check polling interval
- Verify execution ID
- Check CORS configuration

---

# 6. API Reference

## REST Endpoints

### Upload File
```
POST /api/upload
Content-Type: multipart/form-data

Request: file (PDF, max 50MB)

Response (200):
{
  "message": "File uploaded successfully",
  "filename": "1704067200000-report.pdf",
  "pipeline": {
    "executionId": "exec-1704067200000-abc123",
    "status": "running"
  }
}
```

### Get Status
```
GET /api/pipeline/:executionId

Response (200):
{
  "id": "exec-1704067200000-abc123",
  "status": "running",
  "steps": [{
    "stepId": "full_pipeline",
    "status": "running",
    "progress": {
      "currentPage": 42,
      "totalPages": 411
    }
  }]
}
```

### Get All Executions
```
GET /api/pipeline

Response (200):
{
  "executions": [/* ... */]
}
```

### Health Check
```
GET /health

Response (200):
{
  "status": "ok"
}
```

## Type Definitions

```typescript
interface PipelineExecution {
  id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  startTime: string;
  endTime?: string;
  steps: PipelineStep[];
}

interface PipelineStep {
  stepId: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  name: string;
  progress?: Record<string, any>;
}
```

---

# 7. Contributing Guidelines

## Code Style

### TypeScript/JavaScript
- Use ES modules (import/export)
- Prefer `const` over `let`
- camelCase for variables/functions
- PascalCase for classes/interfaces
- UPPER_SNAKE_CASE for constants

### Python
- Follow PEP 8
- 4 spaces indentation
- snake_case for functions/variables
- PascalCase for classes
- Type hints for functions

## Testing

**Frontend (Vitest + Testing Library):**
```typescript
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

describe('Component', () => {
  it('should render', () => {
    render(<Component />);
    expect(screen.getByText('text')).toBeInTheDocument();
  });
});
```

**Backend (Supertest):**
```typescript
import request from 'supertest';

describe('API', () => {
  it('uploads file', async () => {
    const response = await request(app)
      .post('/api/upload')
      .attach('file', 'test.pdf')
      .expect(200);
  });
});
```

**Python (pytest):**
```python
def test_sanitize():
    assert sanitize_pdf_stem("Test.pdf") == "Test"
```

## PR Process

### Branch Naming
- Feature: `feature/description`
- Bug fix: `fix/description`
- Docs: `docs/description`

### Commit Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

### PR Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/pass
- [ ] Documentation updated
- [ ] No debug code
- [ ] Type errors resolved

## Documentation

**Always include:**
- Function/parameter descriptions
- Request/response examples
- Error cases
- Usage examples

**Update when:**
- Adding features
- Changing APIs
- Modifying configuration
- Updating dependencies

---

## Key Documentation Files

- `README.md` - Project overview
- `QUICK_START.md` - Getting started
- `packages/app/claude.md` - App architecture
- `packages/fact-extractor/CLAUDE.md` - Extraction details
- `packages/fact-analyzer/claude.md` - Analysis architecture

---

**Last Updated**: 2025-11-30
**Status**: Production-Ready
**Maintainers**: ESIA Team
