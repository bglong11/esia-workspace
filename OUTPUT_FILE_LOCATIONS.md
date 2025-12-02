# ESIA Pipeline Output Files - Location Guide

This document describes all files output from the ESIA pipeline and their locations.

## Overview

The ESIA pipeline processes ESIA documents through multiple steps:
- **Step 1:** Document chunking (creates chunks, metadata)
- **Step 2:** Fact extraction (creates facts)
- **Step 3:** Quality analysis (creates review files)
- **Step 4:** Factsheet generation (creates comprehensive reports)

All output files are stored in a single directory and named with a consistent pattern.

---

## Output Directory

**Location:** `packages/pipeline/data/outputs/`

**Full Path:** `m:\GitHub\esia-workspace\packages\pipeline\data\outputs\`

All pipeline outputs go to this directory, regardless of which steps are executed.

---

## File Naming Convention

All output files follow this naming pattern:

```
{TIMESTAMP}-{SANITIZED_FILENAME}_{EXTENSION}
```

**Example:**
- Input file: `DUMMY Lake Toba ESIA.pdf`
- Timestamp: `1764674954477`
- Output files:
  - `1764674954477-DUMMY Lake Toba ESIA_chunks.jsonl`
  - `1764674954477-DUMMY Lake Toba ESIA_meta.json`
  - `1764674954477-DUMMY Lake Toba ESIA_facts.json`
  - `1764674954477-DUMMY Lake Toba ESIA_review.xlsx`
  - `1764674954477-DUMMY Lake Toba ESIA_review.html`

---

## Output Files by Step

### Step 1: Document Chunking (Docling)

**Files Generated:**

#### 1.1 `{name}_chunks.jsonl`
- **Purpose:** Chunked document text
- **Format:** JSON Lines (one JSON object per line)
- **Content:**
  - Document sections/chunks
  - Page numbers for each chunk
  - Chunk metadata (size, position)
- **Size:** Varies by document size (typically 1-50 MB)
- **Example:**
  ```
  {"chunk_id": 0, "text": "1.1 Project Overview...", "page_start": 1, "page_end": 1}
  {"chunk_id": 1, "text": "The project is...", "page_start": 1, "page_end": 2}
  ```

#### 1.2 `{name}_meta.json`
- **Purpose:** Document metadata and extracted tables
- **Format:** JSON
- **Content:**
  - Document information (filename, pages, chunks)
  - Table extraction results
  - Document structure analysis
- **Size:** Typically 10-500 KB
- **Example:**
  ```json
  {
    "document": {
      "original_filename": "DUMMY Lake Toba ESIA.pdf",
      "total_pages": 101,
      "total_chunks": 52
    },
    "tables": [...],
    "statistics": {...}
  }
  ```

---

### Step 2: Fact Extraction (DSPy + Gemini API)

**Files Generated:**

#### 2.1 `{name}_facts.json`
- **Purpose:** All extracted facts from the document
- **Format:** JSON
- **Content:**
  - Structured facts organized by section and domain
  - Page references for each fact
  - Extraction metadata (confidence, archetype matches)
- **Size:** Typically 50 KB - 2 MB
- **Structure:**
  ```json
  {
    "document": "1764674954477-DUMMY Lake Toba ESIA.pdf",
    "extraction_date": "2025-12-02T08:00:01.697743",
    "sections": {
      "1.1 Project Overview": {
        "section": "1.1 Project Overview",
        "page_start": 1,
        "page_end": 1,
        "extracted_facts": {
          "executive_summary": {
            "project_overview_Project_Name": "Sumatera PSHP [Page 1]",
            "project_overview_Project_Location": "North Sumatra [Page 1]"
          }
        }
      }
    }
  }
  ```

---

### Step 3: Quality Analysis (esia-fact-analyzer)

**Files Generated:**

#### 3.1 `{name}_review.xlsx`
- **Purpose:** Excel analysis report
- **Format:** Excel Workbook (.xlsx)
- **Sheets:**
  - Summary (document info)
  - Project Summary (key findings)
  - Fact Categories (breakdown by category)
  - Consistency Issues (data conflicts)
  - Unit Standardization (unit recommendations)
  - Threshold Compliance (threshold checks)
  - Gap Analysis (missing content)
- **Size:** Typically 100 KB - 2 MB
- **Source:** `esia-fact-analyzer/analyze_esia_v2.py`

#### 3.2 `{name}_review.html`
- **Purpose:** Interactive HTML analysis dashboard
- **Format:** HTML with inline CSS
- **Content:**
  - All analysis from Excel in formatted HTML
  - Styled tables and sections
  - Browser-viewable analysis report
- **Size:** Typically 100 KB - 1 MB
- **Source:** `esia-fact-analyzer/exporters/html_exporter.py`

---

### Step 4: Factsheet Generation (generate_esia_factsheet.py)

**Files Generated:**

#### 4.1 `{name}_review.xlsx` (Comprehensive Version)
- **Purpose:** Comprehensive ESIA review factsheet in Excel
- **Format:** Excel Workbook (.xlsx)
- **Sheets:** (8 sheets total)
  1. **Summary** - Document statistics and metadata
  2. **Project Summary** - 5-section project overview
  3. **Fact Categories** - Categorized facts with counts
  4. **Consistency Issues** - Data inconsistencies with severity levels
  5. **Unit Standardization** - Unit conversion recommendations
  6. **Threshold Compliance** - Environmental threshold checks
  7. **Gap Analysis** - Missing or incomplete sections
  8. **Facts** - ⭐ NEW - All extracted facts in tabular format
- **Size:** Typically 200 KB - 3 MB
- **Facts Sheet Columns:**
  - Section (e.g., "1.1 Project Overview")
  - Domain (e.g., "executive_summary")
  - Field (e.g., "Project Name")
  - Value (e.g., "Sumatera PSHP")
  - Page (e.g., "1")

#### 4.2 `{name}_review.html` (Comprehensive Version)
- **Purpose:** Interactive HTML factsheet dashboard
- **Format:** HTML with inline CSS styling
- **Sections:**
  - Header with document info
  - Project summary
  - Fact categories table
  - Consistency issues (if any)
  - Unit standardization (if any)
  - Threshold compliance results
  - Gap analysis
- **Size:** Typically 200 KB - 2 MB
- **Styling:** Professional dark blue headers, color-coded severity levels

---

## Download Package Contents

When a user clicks **Download** from the web UI, they receive a ZIP file containing:

```
{timestamp}-{name}_results.zip
├── {name}_chunks.jsonl          (Step 1)
├── {name}_meta.json             (Step 1)
├── {name}_facts.json            (Step 2)
├── {name}_review.xlsx           (Step 3 & 4 combined)
└── {name}_review.html           (Step 3 & 4 combined)
```

**Total Files in Download:** 5

**Download Logic:** (`packages/app/server.js`)
- Uses `execution.sanitizedName` to locate files
- Includes all available files from Steps 1-4
- If a file doesn't exist, it's skipped with a warning log

---

## File Location by Step

### After Step 1 Completes
```
outputs/
├── {name}_chunks.jsonl
└── {name}_meta.json
```

### After Step 2 Completes
```
outputs/
├── {name}_chunks.jsonl
├── {name}_meta.json
└── {name}_facts.json
```

### After Step 3 Completes
```
outputs/
├── {name}_chunks.jsonl
├── {name}_meta.json
├── {name}_facts.json
├── {name}_review.xlsx        (from analyzer)
└── {name}_review.html        (from analyzer)
```

### After Step 4 Completes
```
outputs/
├── {name}_chunks.jsonl
├── {name}_meta.json
├── {name}_facts.json
├── {name}_review.xlsx        (updated with 8 sheets)
└── {name}_review.html        (updated with full dashboard)
```

---

## File Access Methods

### 1. Web UI Download
- Upload PDF → Pipeline processes → Click "Download"
- Gets ZIP with 5 files
- Location: `packages/app/server.js` line 138-205

### 2. Direct File System Access
```powershell
# View all outputs
ls m:\GitHub\esia-workspace\packages\pipeline\data\outputs\

# Find files for specific document
ls m:\GitHub\esia-workspace\packages\pipeline\data\outputs\*1764674954477*

# Open Excel report
start "m:\GitHub\esia-workspace\packages\pipeline\data\outputs\1764674954477-DUMMY Lake Toba ESIA_review.xlsx"

# Open HTML report
start "m:\GitHub\esia-workspace\packages\pipeline\data\outputs\1764674954477-DUMMY Lake Toba ESIA_review.html"
```

### 3. Python Script Access
```python
from pathlib import Path

output_dir = Path("packages/pipeline/data/outputs")
name = "1764674954477-DUMMY Lake Toba ESIA"

# Load specific files
chunks = load_jsonl(output_dir / f"{name}_chunks.jsonl")
facts = json.load(open(output_dir / f"{name}_facts.json"))
meta = json.load(open(output_dir / f"{name}_meta.json"))
```

---

## File Size Reference

For a typical ESIA document (100 pages):

| File | Size | Compression |
|------|------|-------------|
| `_chunks.jsonl` | 5-20 MB | 80-90% |
| `_meta.json` | 100-500 KB | 70-85% |
| `_facts.json` | 200-800 KB | 75-85% |
| `_review.xlsx` | 300-1000 KB | 80-90% |
| `_review.html` | 200-500 KB | 75-85% |
| **ZIP Total** | 800-3000 KB | (combined) |

---

## Cleanup & Archival

### Removing Old Files
```powershell
# Remove files older than 30 days
$cutoff = (Get-Date).AddDays(-30)
Get-ChildItem "m:\GitHub\esia-workspace\packages\pipeline\data\outputs\" |
  Where-Object { $_.LastWriteTime -lt $cutoff } |
  Remove-Item -Force
```

### Archiving to Cloud
- Archive completed outputs to cloud storage (S3, Azure, Google Cloud)
- Keep local copies for last 30 days
- Use timestamp-based naming for easy retrieval

---

## Configuration

The output directory is configured in:
- **Pipeline:** `packages/pipeline/config.py` (UNIFIED_OUTPUT_DIR)
- **Backend:** `packages/app/pipeline.config.js` (outputDir)
- **Executor:** `packages/app/pipelineExecutor.js` (pipelineConfig.outputDir)

All reference the same location: `packages/pipeline/data/outputs/`

---

## Key Notes

1. **Single Directory:** All outputs go to one directory regardless of project
2. **Timestamp Isolation:** Timestamp in filename prevents collisions
3. **Step Independence:** Each step can run independently, outputs accumulate
4. **Download Package:** Contains only final outputs (5 files), not intermediate files
5. **Web UI Friendly:** Filenames sanitized to be URL-safe and filesystem-safe
6. **Fact Sheet:** Step 4 generates comprehensive Excel/HTML with all analysis

---

## Related Files

- **Pipeline Orchestrator:** `packages/pipeline/run-esia-pipeline.py`
- **Factsheet Generator:** `packages/pipeline/generate_esia_factsheet.py`
- **Download Endpoint:** `packages/app/server.js` (GET /api/download/:executionId)
- **Configuration:** `packages/app/pipeline.config.js`

---

**Last Updated:** December 2, 2025
**Version:** 1.0
**Status:** Production
