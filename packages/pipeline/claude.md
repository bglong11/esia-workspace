# CLAUDE.md - Pipeline Developer Guide

This file provides guidance to Claude Code when working with the ESIA Pipeline repository. It explains the project structure, architecture, and key implementation details.

## Project Overview

**Name:** ESIA Pipeline (Environmental and Social Impact Assessment)
**Type:** Multi-step document intelligence system
**Location:** `M:\GitHub\esia-workspace\packages\pipeline`
**Purpose:** Automated extraction and analysis of ESIA documents (PDF/DOCX)

### What It Does

1. **Step 1: Document Chunking** - Convert PDF/DOCX to semantic chunks with page tracking
2. **Step 2: Fact Extraction** - Extract domain-specific facts using DSPy and LLM
3. **Step 3: Quality Analysis** - Analyze facts for consistency, gaps, and compliance

**Pipeline Duration:** 12-35 minutes per document

---

## Architecture Overview

### Two Main Components

```
┌─────────────────────────────────────────────────┐
│  ESIA PIPELINE (packages/pipeline)              │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ STEPS 1 & 2: esia-fact-extractor-pipeline│  │
│  ├──────────────────────────────────────────┤  │
│  │ • Step 1: PDF/DOCX → chunks.jsonl        │  │
│  │ • Step 2: chunks → facts.json            │  │
│  │ Tech: Docling, DSPy, Gemini API         │  │
│  └──────────────────────────────────────────┘  │
│               ↓ (chunks.jsonl, facts.json)     │
│  ┌──────────────────────────────────────────┐  │
│  │ STEP 3: esia-fact-analyzer               │  │
│  ├──────────────────────────────────────────┤  │
│  │ • Consistency checking                   │  │
│  │ • Gap analysis                           │  │
│  │ • IFC threshold validation               │  │
│  │ • HTML + Excel report generation         │  │
│  │ Tech: Pure Python, rule-based            │  │
│  └──────────────────────────────────────────┘  │
│               ↓ (review.html, review.xlsx)     │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Orchestration

**File:** `run-esia-pipeline.py`

Coordinates both components in sequence. Can run all steps or specific steps.

```python
# Run all steps (1, 2, 3)
python run-esia-pipeline.py document.pdf

# Run specific steps
python run-esia-pipeline.py document.pdf --steps 1,2  # Extraction only
python run-esia-pipeline.py document.pdf --steps 3    # Analysis only
```

---

## Directory Structure

```
packages/pipeline/
├── requirements.txt                    # Single consolidated requirements
├── REQUIREMENTS_GUIDE.md               # Installation guide
├── pipeline_flow.md                    # Windows PowerShell execution guide
├── DIRECTORY_STRUCTURE.md              # Directory analysis (no duplication)
├── claude.md                           # This file
├── run-esia-pipeline.py                # Main orchestrator script
├── config.py                           # Root configuration
│
├── data/
│   ├── pdfs/                           # Input directory for PDF/DOCX files
│   └── outputs/                        # Output directory for all results
│
├── esia-fact-extractor-pipeline/       # STEPS 1 & 2 (Extraction)
│   ├── step1_docling_hybrid_chunking.py
│   ├── step2_fact_extraction.py
│   ├── step3_extraction_with_archetypes.py
│   ├── src/                            # Core modules
│   │   ├── esia_extractor.py           # DSPy-based extractor
│   │   ├── generated_signatures.py     # 40+ domain signatures
│   │   ├── llm_manager.py              # Gemini/OpenRouter abstraction
│   │   ├── archetype_mapper.py         # Domain mapping
│   │   ├── project_type_classifier.py  # Classify project type
│   │   └── [7 more modules...]
│   ├── data/archetypes/                # Domain patterns and reference data
│   └── docs/                           # Extraction documentation
│
└── esia-fact-analyzer/                 # STEP 3 (Analysis)
    ├── analyze_esia_v2.py              # Main analysis script
    ├── esia_analyzer/                  # Analysis package
    │   ├── reviewer.py                 # ESIAReviewer class
    │   ├── consistency.py              # Consistency checks
    │   ├── gaps.py                     # Gap analysis
    │   ├── thresholds.py               # IFC compliance
    │   ├── exporters/
    │   │   ├── html.py                 # HTML dashboard
    │   │   └── excel.py                # Excel workbook
    │   └── factsheet/                  # Executive summary generation
    └── docs/                           # Analysis documentation
```

### Data Flow

```
INPUT: data/pdfs/{filename}.pdf or .docx

STEP 1 (Chunking):
  ↓
OUTPUT: data/outputs/{filename}_chunks.jsonl
OUTPUT: data/outputs/{filename}_meta.json

STEP 2 (Extraction):
  ↓
OUTPUT: data/outputs/{filename}_facts.json

STEP 3 (Analysis):
  ↓
OUTPUT: data/outputs/{filename}_review.html
OUTPUT: data/outputs/{filename}_review.xlsx
```

---

## Key Files & Modules

### Extraction Pipeline (esia-fact-extractor-pipeline)

| File | Lines | Purpose |
|------|-------|---------|
| `step1_docling_hybrid_chunking.py` | 660 | Document parsing → semantic chunks |
| `step3_extraction_with_archetypes.py` | 280 | Chunks → facts via archetypes |
| `src/esia_extractor.py` | 350 | DSPy-based fact extraction |
| `src/generated_signatures.py` | 5,000+ | 40+ domain-specific signatures |
| `src/llm_manager.py` | 200+ | Gemini API abstraction |
| `src/archetype_mapper.py` | 900+ | Domain mapping logic |

### Analysis Pipeline (esia-fact-analyzer)

| File | Lines | Purpose |
|------|-------|---------|
| `analyze_esia_v2.py` | 200+ | Main analysis orchestrator |
| `esia_analyzer/reviewer.py` | 427 | ESIAReviewer class |
| `esia_analyzer/consistency.py` | 180 | Contradiction detection |
| `esia_analyzer/gaps.py` | 170 | Missing content analysis |
| `esia_analyzer/thresholds.py` | 130 | IFC compliance checking |
| `esia_analyzer/exporters/html.py` | 1,500+ | Interactive dashboard |
| `esia_analyzer/exporters/excel.py` | 250 | Excel report generation |

---

## Key Technologies

### Extraction Phase (Steps 1 & 2)

- **Docling** - PDF/DOCX parsing with layout analysis
- **HybridChunker** - Token-aware semantic chunking
- **DSPy** - Language model programming framework
- **Google Gemini API** - LLM for fact extraction
- **Tiktoken** - OpenAI's token counter
- **PyTorch** - GPU detection and acceleration

### Analysis Phase (Step 3)

- **Pure Python** - No external ML/LLM
- **Regex & Rules** - Pattern-based analysis
- **openpyxl** - Excel file generation
- **Jinja2** - HTML template rendering

---

## Common Development Tasks

### Running the Pipeline

```powershell
# From pipeline root directory
cd packages/pipeline

# Run complete pipeline
python run-esia-pipeline.py data/pdfs/document.pdf

# Run specific steps
python run-esia-pipeline.py document.pdf --steps 1      # Chunking only
python run-esia-pipeline.py document.pdf --steps 2      # Extraction only
python run-esia-pipeline.py document.pdf --steps 3      # Analysis only

# Run with verbose output
python run-esia-pipeline.py document.pdf --verbose

# Help
python run-esia-pipeline.py --help
```

### Installation

```powershell
# Navigate to pipeline directory
cd packages/pipeline

# Install all dependencies
pip install -r requirements.txt

# With optional features
pip install -r requirements.txt langdetect requests python-dotenv

# With all features
pip install -r requirements.txt langdetect requests python-dotenv openrouter
```

### Environment Setup

```powershell
# Set API keys in PowerShell (Windows)
$env:GOOGLE_API_KEY = "your_google_api_key"
$env:OPENROUTER_API_KEY = "your_openrouter_api_key"  # Optional

# Or create .env file in pipeline root
GOOGLE_API_KEY=your_google_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

### Testing Individual Steps

```powershell
# Test Step 1 (Document Chunking)
cd esia-fact-extractor-pipeline
python step1_docling_hybrid_chunking.py "..\data\pdfs\test.pdf" --verbose

# Test Step 2 (Fact Extraction)
python step3_extraction_with_archetypes.py `
  --chunks ..\data\outputs\test_chunks.jsonl `
  --output ..\data\outputs\test_facts.json

# Test Step 3 (Analysis)
cd ..\esia-fact-analyzer
python analyze_esia_v2.py `
  --input-dir ..\data\outputs `
  --chunks test_chunks.jsonl
```

### Debugging

```powershell
# Check if dependencies are installed
python -c "import docling, dspy, openpyxl; print('✓ OK')"

# Test API connection
python -c "from packages.pipeline.esia-fact-extractor-pipeline.src.llm_manager import LLMManager; print(LLMManager().test())"

# View environment variables
$env:GOOGLE_API_KEY
$env:OPENROUTER_API_KEY

# Run with verbose logging
python run-esia-pipeline.py document.pdf --verbose 2>&1 | Tee-Object pipeline.log
```

---

## Important Concepts

### Step 1: Document Chunking

**Input:** PDF or DOCX file

**Process:**
1. Convert DOCX → PDF (for consistent page tracking)
2. Parse PDF using Docling (GPU-accelerated)
3. Extract text, tables, images
4. Tokenize chunks using tiktoken
5. Split respecting semantic boundaries
6. Track exact page numbers from Docling

**Output:**
- `chunks.jsonl` - One JSON object per line (JSONL format)
- `meta.json` - Document statistics, tables, metadata

**Key Feature:** Streaming output (memory-efficient for large documents)

**Default Settings:**
- Max tokens per chunk: 2,500
- Tokenizer model: gpt-4o
- Peer merging: enabled (merge small fragments)

### Step 2: Fact Extraction

**Input:** chunks.jsonl

**Process:**
1. Load chunks line-by-line
2. Classify document project type (Solar, Hydro, Coal, etc.)
3. Match chunks to 40+ domain archetypes
4. Apply DSPy signatures to extract structured facts
5. Call Gemini API for each signature
6. Merge archetype-specific insights
7. Return structured facts.json

**Output:** facts.json with domain-organized facts

**Key Feature:** Archetype-based extraction (domain patterns pre-defined)

**Available Archetypes:**
- core_esia - Main ESIA sections
- core_cross_cutting - Cross-cutting concerns
- core_ifc_performance_standards - IFC standards
- project_specific_esia - Project-type-specific

### Step 3: Analysis

**Input:** facts.json (and optionally chunks.jsonl, meta.json)

**Process:**
1. **Consistency Checking** - Find contradictions in facts
2. **Gap Analysis** - Identify missing required content
3. **Unit Validation** - Check units are consistent
4. **Threshold Validation** - Check against IFC World Bank standards
5. **Report Generation** - Create HTML dashboard and Excel workbook

**Output:**
- `review.html` - Interactive dashboard (open in browser)
- `review.xlsx` - Detailed Excel workbook with sheets

**Key Feature:** Pure Python, rule-based (no LLM required)

---

## Data Formats

### Chunks JSONL Format

```json
{
  "chunk_id": 0,
  "page": 1,
  "section": "Project Description",
  "text": "Project: Laleia Solar IPP... [content]",
  "token_count": 2450,
  "metadata": {
    "headings": ["ESIA", "Project Description"],
    "captions": [],
    "doc_items_count": 4,
    "origin": {"filename": "ESIA_2025.pdf"}
  }
}
```

### Metadata JSON Format

```json
{
  "document": {
    "original_filename": "ESIA_2025.pdf",
    "total_pages": 77,
    "processed_at": "2025-11-26T21:01:18.450711"
  },
  "files": {
    "chunks": "ESIA_2025_chunks.jsonl",
    "format": "jsonl"
  },
  "tables": [
    {
      "table_id": 0,
      "page": 5,
      "position": "table_0_page_5",
      "content": "| Col1 | Col2 |..."
    }
  ],
  "statistics": {
    "total_chunks": 117,
    "avg_tokens_per_chunk": 176.6,
    "total_tokens": 20664,
    "pages_with_chunks": 77
  }
}
```

### Facts JSON Format

```json
{
  "project_description": {
    "project_name": "Laleia Solar IPP",
    "location": "Kenya",
    "capacity_mw": 100.5,
    "technology": "Solar PV"
  },
  "environmental_impacts": {
    "air_quality": "Minimal impact during operation",
    "water_resources": "No water requirement"
  },
  "mitigation_measures": [
    {
      "impact": "Land use",
      "measure": "Environmental management plan"
    }
  ]
}
```

---

## Configuration & Secrets

### Required Environment Variables

```
GOOGLE_API_KEY          Required - Google Gemini API key
OPENROUTER_API_KEY      Optional - OpenRouter fallback LLM
```

### Configuration Files

- `packages/pipeline/.env` - Environment variables (git-ignored)
- `packages/pipeline/config.py` - Root configuration
- `packages/pipeline/esia-fact-extractor-pipeline/src/config.py` - Extractor config

**Never commit API keys!** Always use `.env` files and `.gitignore`.

---

## Error Handling & Common Issues

### Installation Errors

**"No module named 'docling'"**
```powershell
pip install --upgrade docling docling-core
```

**"CUDA out of memory"**
```powershell
python step1_docling_hybrid_chunking.py document.pdf --gpu-mode cpu
```

**"Cannot import google.genai"**
```powershell
pip uninstall google-genai -y
pip install google-genai
```

### Runtime Errors

**"API key not found"**
- Check `.env` file exists in pipeline root
- Set `$env:GOOGLE_API_KEY` in PowerShell before running

**"Failed to parse PDF"**
- Verify PDF is not corrupted: `Get-Content document.pdf | Measure-Object -Character`
- Try with different PDF file
- Check if PDF is password-protected

**"Rate limit exceeded"**
- Wait or use OpenRouter as alternative LLM
- Reduce number of concurrent extractions

---

## Performance Characteristics

### Step 1 (Chunking)
| Document Size | Time | Memory |
|---------------|------|--------|
| 1-10 pages | < 1 sec | < 500 MB |
| 10-100 pages | 1-10 sec | < 1 GB |
| 100+ pages | 10-60 sec | Streaming (constant) |

**GPU Speedup:** 3-5x faster with CUDA

### Step 2 (Extraction)
| Chunks | LLM Calls | Time |
|--------|-----------|------|
| 50 | ~20 | 10-20 min |
| 100 | ~40 | 20-40 min |
| 200 | ~80 | 40-80 min |

**Bottleneck:** LLM API latency (5-10 sec per call)

### Step 3 (Analysis)
| Chunks | Time | Memory |
|--------|------|--------|
| Any | 2-5 min | < 100 MB |

**No LLM calls** - Pure Python rule-based analysis

---

## Testing & Quality

### Unit Tests

Located in individual component directories:
- `esia-fact-extractor-pipeline/tests/`
- `esia-fact-analyzer/tests/`

Run tests:
```powershell
pytest esia-fact-extractor-pipeline/tests/
pytest esia-fact-analyzer/tests/
```

### Integration Tests

Test complete pipeline:
```powershell
python run-esia-pipeline.py data/pdfs/test_esia.pdf --steps 1,2,3 --verbose
```

### Quality Checklist

Before committing:
- [ ] All dependencies in `requirements.txt`
- [ ] Code follows Python style guide (PEP 8)
- [ ] Type hints on function signatures
- [ ] Docstrings on public methods
- [ ] No hardcoded API keys
- [ ] Works in Windows PowerShell
- [ ] Works with CPU mode (`--gpu-mode cpu`)
- [ ] Error messages are user-friendly

---

## Documentation Hierarchy

1. **pipeline_flow.md** - Windows PowerShell execution guide (START HERE for users)
2. **REQUIREMENTS_GUIDE.md** - Installation and dependency details
3. **DIRECTORY_STRUCTURE.md** - Explanation of directories and structure
4. **claude.md** - This file (developer reference)
5. **Individual component docs:**
   - `esia-fact-extractor-pipeline/docs/` - Extraction details
   - `esia-fact-analyzer/README.md` - Analysis details

---

## Frontend UI Integration

The pipeline will eventually be called from the frontend React app:

```typescript
// Frontend (React)
POST /api/upload → {file, executionId}
     ↓
// Backend (Express) calls:
python run-esia-pipeline.py data/pdfs/{filename} --steps 1,2,3
     ↓
// Pipeline orchestrator coordinates:
esia-fact-extractor-pipeline (Steps 1-2)
esia-fact-analyzer (Step 3)
     ↓
// Backend returns results:
{
  status: "completed",
  chunks: {...},
  facts: {...},
  html_report: "...",
  excel_report: "..."
}
     ↓
// Frontend displays results
```

---

## Development Workflow

### 1. **Understanding the Code**
   - Read: `DIRECTORY_STRUCTURE.md` (understand components)
   - Read: `claude.md` (this file - understand architecture)
   - Read: `pipeline_flow.md` (understand execution)

### 2. **Setting Up Environment**
   ```powershell
   pip install -r requirements.txt
   $env:GOOGLE_API_KEY = "your_key"
   ```

### 3. **Running Pipeline**
   ```powershell
   python run-esia-pipeline.py data/pdfs/test.pdf --steps 1,2,3 --verbose
   ```

### 4. **Debugging Issues**
   ```powershell
   # Check logs from --verbose output
   # Test individual steps
   # Check API keys are set
   ```

### 5. **Making Changes**
   - Keep extraction and analysis separate
   - Update requirements.txt if adding dependencies
   - Update docs if changing behavior
   - Test with `--verbose` flag
   - Update CLAUDE.md if architecture changes

### 6. **Committing Changes**
   - Never commit `.env` files
   - Include docstrings and type hints
   - Run all tests before committing
   - Write clear commit messages

---

## Key Implementation Patterns

### Pattern 1: Generator for Streaming

**Used in Step 1 for memory efficiency:**
```python
def stream_chunks(file_path):
    for chunk_dict in chunks:
        yield json.dumps(chunk_dict)  # One per line
```

**Benefit:** Process 100MB documents without loading into memory

### Pattern 2: DSPy Signatures

**Used in Step 2 for declarative extraction:**
```python
class ProjectDescriptionSignature(dspy.Signature):
    context = dspy.InputField(desc="Document chunk")
    project_name = dspy.OutputField(desc="Name of project")
    location = dspy.OutputField(desc="Project location")
```

**Benefit:** Declarative, LLM-agnostic fact extraction

### Pattern 3: Rule-Based Analysis

**Used in Step 3 for reliability:**
```python
def check_consistency(facts):
    for fact in facts:
        if contradicts(fact, other_fact):
            report_issue(fact)
```

**Benefit:** Deterministic, no LLM hallucinations

### Pattern 4: Configuration Management

```python
# Load from .env or environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not set")
```

**Benefit:** Works in development and production

---

## Naming Conventions

### Files
- **Python files:** `snake_case.py` (e.g., `esia_extractor.py`)
- **Scripts:** `step1_name.py`, `step2_name.py`, `step3_name.py`
- **Config:** `config.py`, `.env`

### Classes
- **PascalCase:** `ESIAExtractor`, `ESIAReviewer`, `HybridChunker`
- **Signatures:** `[Domain]Signature` (e.g., `ProjectDescriptionSignature`)

### Functions
- **snake_case:** `extract_facts()`, `check_consistency()`, `load_chunks()`

### Constants
- **UPPER_CASE:** `MAX_TOKENS = 2500`, `CHUNK_SIZE = 2048`

---

## Future Enhancement Opportunities

1. **Parallel Processing** - Process multiple documents concurrently
2. **Caching** - Cache chunked documents for re-extraction
3. **Vector Database** - Embed chunks for semantic search
4. **Custom Extraction** - Allow users to define custom signatures
5. **Streaming API** - HTTP endpoint for pipeline
6. **Web UI** - Already planned (React frontend)
7. **Monitoring Dashboard** - Track pipeline performance
8. **Cost Analytics** - Monitor API usage and costs

---

## Quick Reference Commands

```powershell
# Navigate
cd M:\GitHub\esia-workspace\packages\pipeline

# Setup
pip install -r requirements.txt
$env:GOOGLE_API_KEY = "key"

# Run pipeline
python run-esia-pipeline.py data/pdfs/doc.pdf --verbose

# Test components
python esia-fact-extractor-pipeline/step1_docling_hybrid_chunking.py doc.pdf
python esia-fact-analyzer/analyze_esia_v2.py --input-dir data/outputs

# Check status
Get-ChildItem data/outputs
Get-Content data/outputs/doc_facts.json

# View results
Invoke-Item data/outputs/doc_review.html  # Open in browser
Invoke-Item data/outputs/doc_review.xlsx  # Open in Excel
```

---

## Getting Help

1. **Check documentation:** `pipeline_flow.md`, `REQUIREMENTS_GUIDE.md`
2. **Run with verbose:** `--verbose` flag shows detailed logs
3. **Check errors:** Review error messages and stack traces
4. **Test individual steps:** Run each component separately
5. **Verify setup:** Check requirements installed, API keys set
6. **Check logs:** Output files in `data/outputs/`

---

**Last Updated:** December 1, 2025
**Version:** 1.0
**Status:** Active Development
**Python:** 3.8+ required
**OS:** Windows (PowerShell), Linux/Mac (Bash)
