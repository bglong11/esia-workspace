# ESIA Pipeline - Updated Usage Guide

## Quick Start (Updated)

### New Required Format

```bash
python run-esia-pipeline.py <PDF_FILE> [OPTIONS]
```

The PDF file path is now a **required positional argument**.

## Usage Examples

### Basic Usage (All Steps)
```bash
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf
```

### Specific Steps
```bash
# Extract only
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 1

# Extract and analyze (skip sync)
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 1,3

# Analyze only (reuse existing extraction)
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 3
```

### Debug Mode
```bash
# Full verbosity
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --verbose

# Short form
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf -v
```

### With Spaces and Special Characters
```bash
# Works with any filename - automatically sanitized
python run-esia-pipeline.py "Project XYZ (Draft) v2.pdf"
python run-esia-pipeline.py "My ESIA Report - Final.pdf"
python run-esia-pipeline.py "/absolute/path/to/document.pdf"
```

## Command-Line Arguments

### Positional Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `PDF_FILE` | Path | ✅ Yes | Path to PDF or DOCX file to process |

### Optional Arguments

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `--steps` | - | str | `1,2,3` | Steps to run (1=extract, 2=sync, 3=analyze) |
| `--verbose` | `-v` | flag | false | Enable debug logging |
| `--help` | `-h` | flag | - | Show help message |
| `--version` | - | flag | - | Show version and exit |

## Stem Sanitization

The PDF filename is automatically converted to a safe "stem" for use in output files.

### Sanitization Examples

| Input Filename | Sanitized Stem | Output Files |
|---|---|---|
| `ESIA Report.pdf` | `ESIA_Report` | `ESIA_Report_chunks.jsonl` |
| `Project XYZ (Draft).pdf` | `Project_XYZ_Draft` | `Project_XYZ_Draft_chunks.jsonl` |
| `ESIA-Final-v2.pdf` | `ESIA_Final_v2` | `ESIA_Final_v2_chunks.jsonl` |
| `my esia (copy) 2024.pdf` | `my_esia_copy_2024` | `my_esia_copy_2024_chunks.jsonl` |

### Sanitization Rules

1. Spaces → underscores
2. Special characters (parentheses, hyphens, etc.) → underscores
3. Multiple consecutive underscores → single underscore
4. Leading/trailing underscores → removed
5. Hyphens → underscores (for consistency)

## Complete Workflow

### Step 1: Prepare Your PDF
```bash
# Place your PDF anywhere
cp ~/Downloads/my_esia.pdf ./data/pdfs/
```

### Step 2: Run Pipeline
```bash
# Simple command - filename is extracted automatically
python run-esia-pipeline.py ./data/pdfs/my_esia.pdf
```

### Step 3: Check Results
```bash
# Find output files
ls esia-fact-extractor-pipeline/hybrid_chunks_output/
ls esia-fact-analyzer/data/html/

# Open HTML dashboard in browser
open esia-fact-analyzer/data/html/my_esia_review.html
```

## Common Workflows

### Workflow 1: Simple Processing
```bash
python run-esia-pipeline.py /path/to/document.pdf
```
Runs all 3 steps, outputs files with sanitized filename stem.

### Workflow 2: Debug Extraction
```bash
python run-esia-pipeline.py /path/to/document.pdf --steps 1 --verbose
```
Runs extraction only with detailed logging to diagnose issues.

### Workflow 3: Re-analyze Without Re-extracting
```bash
# Original run
python run-esia-pipeline.py /path/to/document.pdf

# Later, just re-analyze
python run-esia-pipeline.py /path/to/document.pdf --steps 3
```

### Workflow 4: Batch Processing
```bash
#!/bin/bash
for pdf in data/pdfs/*.pdf; do
    echo "Processing: $pdf"
    python run-esia-pipeline.py "$pdf"
done
```

### Workflow 5: Extract Multiple Documents
```bash
# Extract first document
python run-esia-pipeline.py doc1.pdf --steps 1

# Extract second document
python run-esia-pipeline.py doc2.pdf --steps 1

# Analyze both
python run-esia-pipeline.py doc1.pdf --steps 3
python run-esia-pipeline.py doc2.pdf --steps 3
```

## File Path Options

All of these work:

```bash
# Relative path
python run-esia-pipeline.py ESIA_Report.pdf

# Relative path with directory
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf

# Absolute path
python run-esia-pipeline.py /home/user/documents/ESIA_Report.pdf

# With spaces (use quotes)
python run-esia-pipeline.py "My ESIA Report.pdf"

# Windows path
python run-esia-pipeline.py "C:\Users\User\Documents\ESIA_Report.pdf"

# Current directory
python run-esia-pipeline.py ./ESIA_Report.pdf
```

## Output Files Location

All output files use the sanitized stem from your input filename:

```
Input:  "Project ABC (Draft).pdf"
Stem:   "Project_ABC_Draft"

Outputs:
├─ esia-fact-extractor-pipeline/hybrid_chunks_output/
│  ├─ Project_ABC_Draft_chunks.jsonl        (Step 1 output)
│  ├─ Project_ABC_Draft_meta.json           (Step 1 output)
│  └─ esia_facts_with_archetypes.json       (Step 1 output)
│
├─ esia-fact-analyzer/data/hybrid_chunks_output/
│  ├─ Project_ABC_Draft_chunks.jsonl        (Step 2 copies)
│  └─ Project_ABC_Draft_meta.json           (Step 2 copies)
│
└─ esia-fact-analyzer/data/
   ├─ html/
   │  └─ Project_ABC_Draft_review.html      (Step 3 output - OPEN THIS!)
   └─ Project_ABC_Draft_review.xlsx         (Step 3 output)
```

## Validation

The pipeline validates your PDF file before processing:

✅ File exists
✅ Path is a file (not directory)
✅ File extension is .pdf or .docx
✅ File is readable

```bash
# Error: File doesn't exist
$ python run-esia-pipeline.py nonexistent.pdf
ERROR - PDF file not found: nonexistent.pdf

# Error: Path is directory
$ python run-esia-pipeline.py ./data/
ERROR - Path is not a file: ./data/

# Warning: Wrong extension (but still runs)
$ python run-esia-pipeline.py document.txt
WARNING - File extension is .txt, expected .pdf or .docx
```

## Progress Output

When you run the pipeline, you'll see:

```
2025-11-29 14:30:45 - INFO - ESIA Pipeline Starting
2025-11-29 14:30:45 - INFO - Input file: data/pdfs/ESIA_Report.pdf
2025-11-29 14:30:45 - INFO - Sanitized stem: ESIA_Report
2025-11-29 14:30:45 - DEBUG - ✓ PDF file validated: /absolute/path/ESIA_Report.pdf
2025-11-29 14:30:45 - INFO - Steps to execute: [1, 2, 3]

2025-11-29 14:30:46 - INFO - ======================================================================
2025-11-29 14:30:46 - INFO - STEP 1: Running ESIA Fact Extractor
2025-11-29 14:30:46 - INFO - ======================================================================
2025-11-29 14:30:46 - INFO - Output stem: ESIA_Report
...
```

This shows you exactly what stem was derived from your filename.

## Troubleshooting

### "PDF file not found"
```bash
# Check file exists
ls -la data/pdfs/ESIA_Report.pdf

# Check absolute path
python run-esia-pipeline.py "$(pwd)/data/pdfs/ESIA_Report.pdf"
```

### "Path is not a file"
```bash
# Make sure it's a file, not directory
ls -la data/pdfs/  # Is ESIA_Report.pdf here?
```

### Output files not generated
```bash
# Run with verbose to see what's happening
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --verbose

# Check if files were created with different stem
ls esia-fact-extractor-pipeline/hybrid_chunks_output/
```

### Special characters in filename causing issues
```bash
# Use quotes to protect filename
python run-esia-pipeline.py "My ESIA (Draft) v2.pdf"
```

## Help & Version

```bash
# Show all available options
python run-esia-pipeline.py --help

# Show version
python run-esia-pipeline.py --version
```

## Comparison: Old vs New

### Old (No Longer Works)
```bash
python run-esia-pipeline.py --pdf-stem "ESIA_Report"
# Error: unrecognized arguments: --pdf-stem
```

### New (Correct)
```bash
python run-esia-pipeline.py "ESIA_Report.pdf"
# Stem is automatically extracted: ESIA_Report
```

## Key Improvements

✅ **Simpler** - Just pass the PDF file path
✅ **Automatic** - Stem is derived from filename
✅ **Flexible** - Works with any filename format
✅ **Safe** - Special characters automatically handled
✅ **Clear** - Logging shows the sanitized stem

## Summary

| Aspect | Details |
|--------|---------|
| **Required Input** | PDF/DOCX file path |
| **Auto-derivation** | Filename stem → sanitized output stem |
| **Output naming** | Uses sanitized stem for all files |
| **Steps** | Optional (default: 1,2,3) |
| **Logging** | Optional verbose mode |

---

**For detailed information**, see `PDF_STEM_UPDATE.md`

**For quick start**, see `QUICKSTART.md`

**For full reference**, see `CLI_USAGE.md`
