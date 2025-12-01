# ESIA Pipeline CLI Usage Guide

## Overview

The ESIA Pipeline is a comprehensive document processing and analysis system that orchestrates three main components:

1. **Fact Extraction**: Converts PDF/DOCX documents into structured facts using archetype-based extraction
2. **Output Synchronization**: Transfers extracted data to the analyzer component
3. **Quality Analysis**: Analyzes facts for consistency, compliance, and completeness

## Quick Start

### Basic Usage - Run All Steps

```bash
python run-esia-pipeline.py
```

This runs the complete pipeline (Steps 1, 2, and 3) in sequence.

### Run Specific Steps

```bash
# Run only extraction (Step 1)
python run-esia-pipeline.py --steps 1

# Run extraction and analysis (Steps 1 and 3), skip sync
python run-esia-pipeline.py --steps 1,3

# Run sync and analyze (Steps 2 and 3)
python run-esia-pipeline.py --steps 2,3

# Run analysis only (Step 3)
python run-esia-pipeline.py --steps 3
```

### Enable Verbose Logging

```bash
# Show detailed debug information
python run-esia-pipeline.py --verbose

# Verbose mode with specific steps
python run-esia-pipeline.py --steps 1,3 --verbose
```

## CLI Arguments

### `--steps STEPS`

Comma-separated list of pipeline steps to execute.

**Valid values**: `1`, `2`, `3`

- `1` = Extract facts from PDF
- `2` = Sync outputs to analyzer
- `3` = Analyze extracted facts

**Default**: `1,2,3` (all steps)

**Examples**:
```bash
--steps 1           # Extract only
--steps 1,2,3       # All steps (default)
--steps 3           # Analyze only
```

### `--pdf-stem STEM`

The filename stem for your ESIA document.

**Default**: `ESIA_Report_Final_Elang AMNT`

**Examples**:
```bash
--pdf-stem "My_ESIA_Document"
--pdf-stem "Project_XYZ_ESIA"
```

The pipeline looks for files named `{STEM}_chunks.jsonl` and `{STEM}_meta.json`.

### `-v, --verbose`

Enable debug-level logging output.

Shows detailed information about:
- Directory validation
- File operations
- Step execution details
- Process flow

**Examples**:
```bash
python run-esia-pipeline.py --verbose
python run-esia-pipeline.py --steps 1 --verbose
```

### `--version`

Display pipeline version and exit.

```bash
python run-esia-pipeline.py --version
```

### `-h, --help`

Display help message with all available options.

```bash
python run-esia-pipeline.py --help
```

## Configuration

### Environment Variables

Create a `.env` file in the project root directory to configure the pipeline:

```env
# API Keys for LLM Providers
GOOGLE_API_KEY=your_google_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Pipeline Settings
PDF_STEM=ESIA_Report_Final_Elang AMNT
VERBOSE=false
```

The pipeline automatically loads `.env` at startup if it exists.

### Creating a Sample Configuration

Generate a sample `.env` file from Python:

```python
from pathlib import Path
from config import Config

Config.create_sample_env(Path(".env"))
```

## Pipeline Execution Flow

### Step 1: Extract Facts

**What it does**:
- Processes PDF/DOCX documents using Docling
- Performs semantic chunking with HybridChunker
- Applies archetype-based fact extraction using DSPy
- Maps document sections to 50+ domain archetypes
- Uses domain-specific signatures for extraction

**Input**:
- PDF/DOCX file in the extractor's data directory
- Archetype definitions (included)

**Output**:
- `{STEM}_chunks.jsonl` - Chunked document content
- `{STEM}_meta.json` - Metadata about chunks and tables
- `facts_with_archetypes.json` - Extracted facts organized by domain

**Time**: Depends on document size (typically 5-15 minutes)

### Step 2: Sync Outputs

**What it does**:
- Creates analyzer input directory if needed
- Copies extraction outputs to analyzer's expected location
- Validates that all required files exist

**Input**:
- `{STEM}_chunks.jsonl` from extractor
- `{STEM}_meta.json` from extractor

**Output**:
- Files copied to `esia-fact-analyzer/data/hybrid_chunks_output/`

**Time**: < 1 second

### Step 3: Analyze Facts

**What it does**:
- Loads extracted chunks and metadata
- Performs consistency checking (finds contradictions)
- Checks unit standardization (detects mixed units)
- Validates against IFC/World Bank thresholds
- Analyzes gaps (finds missing expected content)
- Generates interactive HTML dashboard
- Exports detailed analysis to Excel

**Input**:
- `{STEM}_chunks.jsonl` from analyzer input directory
- `{STEM}_meta.json` from analyzer input directory

**Output**:
- `{STEM}_review.html` - Interactive dashboard
- `{STEM}_review.xlsx` - Detailed analysis workbook

**Time**: Depends on document size (typically 2-5 minutes)

## Common Workflows

### Workflow 1: Full Pipeline Execution

Run the complete pipeline from start to finish:

```bash
python run-esia-pipeline.py
```

### Workflow 2: Extract and Analyze (Skip Manual Sync)

```bash
python run-esia-pipeline.py --steps 1,2,3
```

### Workflow 3: Re-analyze Without Re-extracting

After extraction, if you want to modify analysis settings without re-running extraction:

```bash
python run-esia-pipeline.py --steps 3
```

### Workflow 4: Debug Extraction Issues

```bash
python run-esia-pipeline.py --steps 1 --verbose
```

### Workflow 5: Process Multiple Documents

Create a shell script to process multiple documents:

```bash
#!/bin/bash

for pdf_stem in "Project_A" "Project_B" "Project_C"; do
    echo "Processing $pdf_stem..."
    python run-esia-pipeline.py --pdf-stem "$pdf_stem" --verbose
done
```

## File Structure

```
esia-pipeline/
├── run-esia-pipeline.py              # Main CLI script
├── config.py                         # Configuration management
├── esia-fact-extractor-pipeline/
│   ├── step3_extraction_with_archetypes.py
│   ├── hybrid_chunks_output/         # Extraction outputs
│   └── data/
│       └── archetypes/               # 50+ domain definitions
│
├── esia-fact-analyzer/
│   ├── analyze_esia_v2.py
│   ├── data/
│   │   ├── hybrid_chunks_output/     # Sync destination
│   │   └── html/                     # Analysis outputs
│   └── esia_analyzer/                # Analysis modules
│
└── data/
    ├── pdfs/                         # Input documents
    └── extracted/                    # Archived extractions
```

## Troubleshooting

### Error: "Extractor directory not found"

**Cause**: Component directories are missing

**Solution**:
```bash
# Verify both component directories exist
ls -la esia-fact-extractor-pipeline/
ls -la esia-fact-analyzer/
```

### Error: "Expected extractor output not found"

**Cause**: Step 1 didn't complete successfully or output files missing

**Solution**:
```bash
# Run extraction only with verbose output
python run-esia-pipeline.py --steps 1 --verbose

# Check if files exist
ls esia-fact-extractor-pipeline/hybrid_chunks_output/
```

### Error: "Analyzer failed with exit code 1"

**Cause**: Analysis step encountered issues

**Solution**:
```bash
# Run analyzer separately with verbose output
cd esia-fact-analyzer
python analyze_esia_v2.py --verbose
```

### No HTML output generated

**Cause**: Analysis completed but exports failed

**Solution**:
```bash
# Check analyzer output directory
ls -la esia-fact-analyzer/data/html/

# Run analysis with verbose logging
python run-esia-pipeline.py --steps 3 --verbose
```

## Configuration Reference

### Default Configuration

| Setting | Default Value |
|---------|---------------|
| Steps | `1,2,3` (all) |
| PDF Stem | `ESIA_Report_Final_Elang AMNT` |
| Verbose | `false` |
| Log Level | `INFO` |

### Pipeline Timeouts

The pipeline does not have hard timeouts. Processing time depends on:
- Document size (pages, text volume)
- LLM API response times
- System resources (CPU, memory, network)

## Output Files

### Extraction Outputs (`esia-fact-extractor-pipeline/hybrid_chunks_output/`)

- `{STEM}_chunks.jsonl` - Document chunks with metadata (one JSON per line)
- `{STEM}_meta.json` - Document-level metadata and page information

### Analysis Outputs (`esia-fact-analyzer/data/html/` and `.xlsx`)

- `{STEM}_review.html` - Interactive dashboard with:
  - Consistency analysis results
  - Unit standardization checks
  - Threshold compliance status
  - Gap analysis findings
  - Page references for all findings

- `{STEM}_review.xlsx` - Detailed Excel workbook with:
  - Multiple worksheets for different analysis types
  - Formulas and formatting
  - Data export ready for further processing

## Performance Notes

### Typical Execution Times

| Step | Duration | Notes |
|------|----------|-------|
| Step 1 (Extract) | 5-15 min | Depends on doc size and LLM API |
| Step 2 (Sync) | < 1 sec | Simple file copy |
| Step 3 (Analyze) | 2-5 min | Rule-based, no LLM |
| **Total** | **8-20 min** | Full pipeline |

### Resource Requirements

- **Memory**: 2-4 GB recommended
- **Disk Space**: 500 MB - 2 GB (for documents and outputs)
- **Network**: Required for LLM API calls (Step 1)
- **Python**: 3.8+ recommended

## Advanced Usage

### Monitoring Pipeline Execution

Use verbose mode with logging:

```bash
python run-esia-pipeline.py --verbose 2>&1 | tee pipeline.log
```

### Running in Background

```bash
# Run in background and save output to log
nohup python run-esia-pipeline.py > pipeline.log 2>&1 &
```

### Integration with Scripts

```python
import subprocess
import sys

# Run pipeline programmatically
result = subprocess.run(
    [sys.executable, "run-esia-pipeline.py", "--steps", "1,2,3"],
    capture_output=True,
    text=True
)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
```

## Support and Debugging

### Enable Maximum Verbosity

```bash
python run-esia-pipeline.py --verbose --steps 1 --pdf-stem "Your_Document"
```

### Check Component Status

```bash
# Verify extractor is functional
cd esia-fact-extractor-pipeline
python step3_extraction_with_archetypes.py --help

# Verify analyzer is functional
cd ../esia-fact-analyzer
python analyze_esia_v2.py --help
```

### Report Issues

Include the following when reporting issues:

1. Full command used
2. Output with `--verbose` flag
3. Python version: `python --version`
4. Component versions: Check `requirements.txt` files
5. Document name and size
6. Error messages (full traceback if available)

## Version Information

**ESIA Pipeline**: v1.0
**Python Requirements**: 3.8+
**Components**:
- Extractor: Docling 1.0+, DSPy-based
- Analyzer: Rule-based (no ML runtime needed)

---

For more information, run: `python run-esia-pipeline.py --help`
