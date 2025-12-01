# ESIA Pipeline - Unified Architecture (v2.0)

## Overview

The ESIA Pipeline has been refactored to use a **unified, single-directory output architecture** where:

- **Single Input**: All PDFs come from `./data/pdfs/`
- **Single Output**: All outputs go to `./data/outputs/`
- **First Step**: Filename sanitization happens immediately
- **Consistent Stem**: The sanitized stem is used throughout the entire pipeline

This eliminates redundant file copying, conflicting output directories, and filename inconsistencies.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER COMMAND                             │
│  python run-esia-pipeline.py ./data/pdfs/ESIA_Report.pdf   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  VALIDATE FILE & SANITIZE STEM                              │
│  File exists? ✓                                             │
│  Extension is PDF/DOCX? ✓                                   │
│  Sanitized stem: "ESIA_Report" → "ESIA_Report"             │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  STEP 1: DOCUMENT CHUNKING                                  │
│  Input:  ./data/pdfs/ESIA_Report.pdf                        │
│  Output: ./data/outputs/ESIA_Report_chunks.jsonl            │
│          ./data/outputs/ESIA_Report_meta.json               │
│  Time:   5-30 seconds (depending on document size)          │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  STEP 2: FACT EXTRACTION                                    │
│  Input:  ./data/outputs/ESIA_Report_chunks.jsonl            │
│  Output: ./data/outputs/ESIA_Report_facts.json              │
│  Time:   30 seconds - 5 minutes (LLM dependent)             │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  STEP 3: QUALITY ANALYSIS                                   │
│  Input:  ./data/outputs/ESIA_Report_chunks.jsonl            │
│          ./data/outputs/ESIA_Report_meta.json               │
│  Output: ./data/outputs/ESIA_Report_review.html             │
│          ./data/outputs/ESIA_Report_review.xlsx             │
│  Time:   30 seconds - 2 minutes                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  ALL OUTPUTS IN ONE PLACE                   │
│                   ./data/outputs/                           │
│  ├── ESIA_Report_chunks.jsonl                               │
│  ├── ESIA_Report_meta.json                                  │
│  ├── ESIA_Report_facts.json                                 │
│  ├── ESIA_Report_review.html                                │
│  └── ESIA_Report_review.xlsx                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Principles

### 1. Single Input Directory
- **Location**: `./data/pdfs/`
- **Purpose**: All PDF/DOCX files to be processed
- **Requirement**: User uploads files here
- **Benefit**: One place to look for input documents

### 2. Single Output Directory
- **Location**: `./data/outputs/`
- **Purpose**: ALL pipeline outputs, NO EXCEPTIONS
- **Contents**: Chunks, metadata, facts, HTML, Excel - everything
- **Benefit**: Easy to find results, no fragmented outputs

### 3. Filename Sanitization First
- **When**: Immediately after validating the input PDF
- **What**: Convert filename to safe, consistent format
- **Where**: `sanitize_pdf_stem()` in `run-esia-pipeline.py`
- **Rules**:
  - Spaces → underscores
  - Special chars → underscores
  - Multiple underscores → single underscore
  - Hyphens → underscores

  **Examples**:
  - `ESIA Report.pdf` → `ESIA_Report`
  - `Project (Draft).pdf` → `Project_Draft`
  - `my-esia-v2.pdf` → `my_esia_v2`

### 4. Consistent Stem Throughout
- **Step 1**: Output: `{stem}_chunks.jsonl`, `{stem}_meta.json`
- **Step 2**: Input: `{stem}_chunks.jsonl`, Output: `{stem}_facts.json`
- **Step 3**: Input: `{stem}_chunks.jsonl`, `{stem}_meta.json`, Output: `{stem}_review.html/xlsx`

**Result**: Perfect traceability and consistency across the entire pipeline.

---

## Pipeline Workflow

### Command Format

```bash
python run-esia-pipeline.py <pdf_file> [OPTIONS]
```

### Usage Examples

#### Run All Steps (Default)
```bash
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf
```
Runs steps 1, 2, and 3 sequentially.

#### Run Specific Steps
```bash
# Extract only (step 1)
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 1

# Extract and analyze (steps 1, 2)
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 1,2

# Analyze only (step 3) - useful if you want to re-analyze
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 3
```

#### Debug Mode
```bash
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --verbose
```
Shows detailed logging at every step.

### Step Details

#### Step 1: Document Chunking
**Command**: `step1_docling_hybrid_chunking.py`

**What it does**:
- Parses PDF/DOCX using Docling
- Extracts text with page numbers
- Creates semantic chunks respecting token limits
- Counts tokens using tiktoken

**Input**: `./data/pdfs/ESIA_Report.pdf`

**Output**:
- `./data/outputs/ESIA_Report_chunks.jsonl` - Semantic chunks (JSONL format)
- `./data/outputs/ESIA_Report_meta.json` - Metadata (tables, statistics, etc.)

**Time**: 5-30 seconds (depends on document size and parsing complexity)

**Files**: Each line in chunks.jsonl is a complete JSON object:
```json
{
  "chunk_id": 0,
  "page": 1,
  "section": "Project Description",
  "text": "Project description content...",
  "token_count": 2450,
  "metadata": {
    "headings": ["ESIA", "Project Description"],
    "doc_items_count": 4
  }
}
```

#### Step 2: Fact Extraction
**Command**: `step3_extraction_with_archetypes.py`

**What it does**:
- Loads chunks from Step 1
- Maps chunks to 50+ domain archetypes
- Applies domain-specific DSPy signatures
- Extracts structured facts using LLM
- Merges domain insights

**Input**: `./data/outputs/ESIA_Report_chunks.jsonl`

**Output**: `./data/outputs/ESIA_Report_facts.json`

**Time**: 30 seconds - 5 minutes (depends on LLM API responsiveness)

**File Format**:
```json
{
  "project_description": {
    "project_name": "...",
    "location": "...",
    "timeline": "..."
  },
  "environmental_impacts": {
    "air_quality": "...",
    "water_quality": "..."
  },
  "...": "..."
}
```

#### Step 3: Quality Analysis
**Command**: `analyze_esia_v2.py`

**What it does**:
- Loads chunks and metadata from Step 1
- Performs consistency checking (finds contradictions)
- Validates unit standardization (detects mixed units)
- Checks compliance against IFC standards
- Analyzes gaps (finds missing expected content)
- Generates HTML dashboard and Excel workbook

**Inputs**:
- `./data/outputs/ESIA_Report_chunks.jsonl`
- `./data/outputs/ESIA_Report_meta.json`

**Outputs**:
- `./data/outputs/ESIA_Report_review.html` - Interactive dashboard
- `./data/outputs/ESIA_Report_review.xlsx` - Detailed Excel workbook

**Time**: 30 seconds - 2 minutes (rule-based, no LLM calls)

**Outputs**:
- **HTML Dashboard**: Open in browser, interactive analysis results
- **Excel Workbook**: Detailed findings with page references

---

## File Organization

### Root Directory Structure
```
esia-pipeline/
├── run-esia-pipeline.py              # CLI orchestrator (MAIN ENTRY POINT)
├── config.py                         # Configuration management
├── .env                              # Environment variables (create this)
│
├── data/                             # DATA DIRECTORY
│   ├── pdfs/                         # INPUT ONLY
│   │   └── ESIA_Report.pdf          (upload here)
│   │
│   └── outputs/                      # OUTPUT ONLY (single source)
│       ├── ESIA_Report_chunks.jsonl  (step 1)
│       ├── ESIA_Report_meta.json     (step 1)
│       ├── ESIA_Report_facts.json    (step 2)
│       ├── ESIA_Report_review.html   (step 3)
│       └── ESIA_Report_review.xlsx   (step 3)
│
├── esia-fact-extractor-pipeline/     # COMPONENT 1
│   ├── step1_docling_hybrid_chunking.py
│   ├── step3_extraction_with_archetypes.py
│   ├── src/                          # Extractor modules
│   └── data/                         # Configuration (archetypes, etc.)
│
├── esia-fact-analyzer/               # COMPONENT 2
│   ├── analyze_esia_v2.py
│   └── esia_analyzer/                # Analyzer modules
│
└── Documentation/
    ├── UNIFIED_ARCHITECTURE.md       # This file
    ├── CLI_USAGE.md                  # CLI reference
    └── ... (other docs)
```

### What Happens to Old Output Directories
The following directories are **NO LONGER USED**:
- ❌ `esia-fact-extractor-pipeline/hybrid_chunks_output/`
- ❌ `esia-fact-extractor-pipeline/data/outputs/`
- ❌ `esia-fact-analyzer/data/hybrid_chunks_output/`
- ❌ `esia-fact-analyzer/data/html/`

**All outputs** now go to: `./data/outputs/`

---

## Data Flow

### Input Files
```
User uploads PDF
        ↓
./data/pdfs/ESIA_Report.pdf
```

### Step 1 Outputs
```
Docling parses document
        ↓
./data/outputs/ESIA_Report_chunks.jsonl (117 chunks, one per line)
./data/outputs/ESIA_Report_meta.json    (metadata, statistics, tables)
```

### Step 2 Uses Step 1 Outputs
```
./data/outputs/ESIA_Report_chunks.jsonl (input)
        ↓
DSPy fact extraction with archetypes
        ↓
./data/outputs/ESIA_Report_facts.json   (output)
```

### Step 3 Uses Step 1 Outputs
```
./data/outputs/ESIA_Report_chunks.jsonl (input)
./data/outputs/ESIA_Report_meta.json    (input)
        ↓
Rule-based analysis (no LLM)
        ↓
./data/outputs/ESIA_Report_review.html  (output)
./data/outputs/ESIA_Report_review.xlsx  (output)
```

---

## CLI Reference

### Basic Command
```bash
python run-esia-pipeline.py <PDF_FILE> [--steps STEPS] [--verbose]
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `PDF_FILE` | Path | ✅ Yes | Path to PDF or DOCX file |
| `--steps STEPS` | str | ❌ No | Comma-separated steps (1,2,3) Default: all |
| `--verbose` | flag | ❌ No | Enable debug logging |
| `--help` | flag | ❌ No | Show help message |
| `--version` | flag | ❌ No | Show version |

### Step Numbers

| Step | Description | Input | Output |
|------|-------------|-------|--------|
| 1 | Document Chunking | PDF file | chunks.jsonl, meta.json |
| 2 | Fact Extraction | chunks.jsonl | facts.json |
| 3 | Quality Analysis | chunks.jsonl, meta.json | review.html, review.xlsx |

### Examples

```bash
# Run all steps
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf

# Run extraction only
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 1

# Run extraction and analysis
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 1,2

# Run with debug output
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --verbose

# Custom filename with special characters
python run-esia-pipeline.py "data/pdfs/Project (Draft) v2.pdf"

# Show help
python run-esia-pipeline.py --help

# Show version
python run-esia-pipeline.py --version
```

---

## Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# API Keys (required for step 2)
GOOGLE_API_KEY=your_google_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### No Configuration Needed For
- Input/output directories (hardcoded to `./data/pdfs/` and `./data/outputs/`)
- Step commands (hardcoded to correct scripts)
- Sanitization rules (built into `sanitize_pdf_stem()`)

---

## Processing Times

| Step | Duration | Depends On |
|------|----------|-----------|
| Step 1 (Chunking) | 5-30 sec | Document size, PDF complexity |
| Step 2 (Extraction) | 30 sec - 5 min | LLM API speed, document complexity |
| Step 3 (Analysis) | 30 sec - 2 min | Number of chunks, analysis complexity |
| **Total** | **1-8 minutes** | All factors combined |

---

## Filename Sanitization Examples

Input PDF → Sanitized Stem → Output Files

| Input | Stem | Output Files |
|-------|------|--------------|
| `ESIA Report.pdf` | `ESIA_Report` | `ESIA_Report_chunks.jsonl`, etc. |
| `Project XYZ (Draft).pdf` | `Project_XYZ_Draft` | `Project_XYZ_Draft_chunks.jsonl`, etc. |
| `my-esia-v2.pdf` | `my_esia_v2` | `my_esia_v2_chunks.jsonl`, etc. |
| `ESIA (Copy) 2024.pdf` | `ESIA_Copy_2024` | `ESIA_Copy_2024_chunks.jsonl`, etc. |
| `/path/to/report final.pdf` | `report_final` | `report_final_chunks.jsonl`, etc. |

---

## Benefits of Unified Architecture

### Before (Old Multi-Directory System)
```
Outputs fragmented across 4 locations:
├── esia-fact-extractor-pipeline/hybrid_chunks_output/
├── esia-fact-extractor-pipeline/data/outputs/
├── esia-fact-analyzer/data/hybrid_chunks_output/  (copy of above)
└── esia-fact-analyzer/data/html/

Problems:
- Hard to find outputs
- Redundant file copying (Step 2)
- Inconsistent naming
- Complex maintenance
```

### After (New Unified System)
```
All outputs in ONE place:
└── data/outputs/
    ├── *_chunks.jsonl
    ├── *_meta.json
    ├── *_facts.json
    ├── *_review.html
    └── *_review.xlsx

Benefits:
- Easy to find everything
- No file copying
- Consistent naming throughout
- Simple maintenance
- Single source of truth
```

---

## Migration from Old Architecture

If you have old outputs in module directories:

```bash
# The old directories are no longer used:
# ❌ esia-fact-extractor-pipeline/hybrid_chunks_output/
# ❌ esia-fact-extractor-pipeline/data/outputs/
# ❌ esia-fact-analyzer/data/html/

# New location for all outputs:
# ✓ ./data/outputs/

# Simply run the pipeline:
python run-esia-pipeline.py ./data/pdfs/your_document.pdf

# All new outputs go to ./data/outputs/
```

---

## Troubleshooting

### Error: "PDF file not found"
```bash
# Check file exists in ./data/pdfs/
ls -la data/pdfs/

# Verify path is correct
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf
```

### Error: "Chunks file not found"
```bash
# Step 1 may have failed, run with verbose:
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 1 --verbose

# Check if chunks file was created:
ls -la data/outputs/
```

### Outputs not in ./data/outputs/
```bash
# Check that old directories don't have newer outputs:
ls -la esia-fact-extractor-pipeline/hybrid_chunks_output/
ls -la esia-fact-analyzer/data/html/

# If they exist there, delete and re-run pipeline:
rm -rf esia-fact-extractor-pipeline/hybrid_chunks_output
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf
```

### Want to see where outputs went
```bash
# After running pipeline, check:
ls -la data/outputs/

# Should see files like:
# ESIA_Report_chunks.jsonl
# ESIA_Report_meta.json
# ESIA_Report_facts.json
# ESIA_Report_review.html
# ESIA_Report_review.xlsx
```

---

## Summary

### Key Points
1. ✅ **Single input**: `./data/pdfs/`
2. ✅ **Single output**: `./data/outputs/`
3. ✅ **Sanitize first**: Filename stem created immediately
4. ✅ **Consistent stem**: Used throughout all 3 steps
5. ✅ **No file copying**: Direct input from previous step
6. ✅ **Easy to find**: All results in one location
7. ✅ **Simple to maintain**: Fewer paths to manage

### Quick Start
```bash
# 1. Place PDF in ./data/pdfs/
cp ~/Downloads/ESIA_Report.pdf ./data/pdfs/

# 2. Run pipeline
python run-esia-pipeline.py ./data/pdfs/ESIA_Report.pdf

# 3. Find results
ls ./data/outputs/
# Shows: ESIA_Report_chunks.jsonl, meta.json, facts.json, review.html, review.xlsx
```

### Next: Implementation Phases

The unified architecture is defined. Implementation requires updating:
- **Phase 1**: ✅ `run-esia-pipeline.py` (DONE)
- **Phase 2**: `step1_docling_hybrid_chunking.py` (Update default output dir)
- **Phase 3**: `step3_extraction_with_archetypes.py` (Make paths configurable)
- **Phase 4**: `analyze_esia_v2.py` (Update default paths)
- **Phase 5**: Testing and cleanup

See `REFACTORING_PLAN.md` for detailed implementation steps.
