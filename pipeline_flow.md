# ESIA Pipeline Flow - Windows PowerShell Guide

This document details the complete steps for running the ESIA (Environmental and Social Impact Assessment) document processing pipeline using Windows PowerShell.

## Overview

The ESIA Pipeline is a 3-step document processing system:
1. **Step 1**: Document Chunking - Convert PDF/DOCX into semantic chunks
2. **Step 2**: Fact Extraction - Extract domain-specific facts using LLM
3. **Step 3**: Quality Analysis - Analyze facts for consistency and compliance

**Total Execution Time**: 12-35 minutes (depending on document size)

---

## Prerequisites

### System Requirements
- Windows 10/11
- Python 3.10+ installed and added to PATH
- Git installed
- Sufficient disk space (5GB+ recommended)
- GPU recommended (NVIDIA with CUDA) for faster document parsing

### API Keys Required
- `GOOGLE_API_KEY` - For Gemini API (primary LLM provider)
- `OPENROUTER_API_KEY` - Optional alternative LLM provider

### Python Dependencies
All required packages are listed in:
- `packages/pipeline/esia-fact-extractor-pipeline/requirements.txt`
- `packages/pipeline/esia-fact-analyzer/requirements.txt`

---

## Setup Instructions

### 1. Navigate to Pipeline Directory

```powershell
# From workspace root
cd M:\GitHub\esia-workspace\packages\pipeline
```

### 2. Create Environment Configuration

Create a `.env` file in the pipeline directory (`packages/pipeline/.env`):

```powershell
# Using PowerShell to create .env file
@"
GOOGLE_API_KEY=your_google_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
"@ | Out-File -FilePath ".env" -Encoding UTF8
```

Or manually create the file with your favorite editor and add:
```
GOOGLE_API_KEY=your_google_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Install Python Dependencies

```powershell
# Install all pipeline dependencies
pip install -r .\esia-fact-extractor-pipeline\requirements.txt
pip install -r .\esia-fact-analyzer\requirements.txt
```

### 4. Prepare Input Documents

```powershell
# Create data directories if they don't exist
if (-not (Test-Path ".\data\pdfs")) {
    New-Item -ItemType Directory -Path ".\data\pdfs" -Force
}
if (-not (Test-Path ".\data\outputs")) {
    New-Item -ItemType Directory -Path ".\data\outputs" -Force
}

# Copy your PDF/DOCX files to data/pdfs directory
Copy-Item "C:\Path\To\Your\Document.pdf" ".\data\pdfs\"
```

---

## Running the Pipeline

### Option A: Run Complete Pipeline (All Steps)

```powershell
# Run all 3 steps on a document
python run-esia-pipeline.py .\data\pdfs\your_document.pdf
```

**Expected Output:**
- `your_document_chunks.jsonl` - Semantic document chunks
- `your_document_meta.json` - Document metadata
- `your_document_facts.json` - Extracted facts
- `your_document_review.html` - Interactive analysis dashboard
- `your_document_review.xlsx` - Detailed analysis workbook

### Option B: Run Specific Steps

```powershell
# Run only Step 1 (Chunking)
python run-esia-pipeline.py .\data\pdfs\your_document.pdf --steps 1

# Run only Step 2 (Extraction)
python run-esia-pipeline.py .\data\pdfs\your_document.pdf --steps 2

# Run only Step 3 (Analysis)
python run-esia-pipeline.py .\data\pdfs\your_document.pdf --steps 3

# Run Steps 1 and 3, skip Step 2
python run-esia-pipeline.py .\data\pdfs\your_document.pdf --steps 1,3
```

### Option C: Run with Verbose Output

```powershell
# Enable debug logging to see detailed processing steps
python run-esia-pipeline.py .\data\pdfs\your_document.pdf --verbose
```

### Option D: Run Individual Steps Manually

#### Step 1: Document Chunking

```powershell
cd .\esia-fact-extractor-pipeline

# Basic chunking
python step1_docling_hybrid_chunking.py "..\data\pdfs\your_document.pdf"

# With GPU mode specification (cpu or gpu)
python step1_docling_hybrid_chunking.py "..\data\pdfs\your_document.pdf" --gpu-mode cpu --verbose

cd ..
```

**Output Files:**
- `data/outputs/your_document_chunks.jsonl` - JSONL format (one chunk per line)
- `data/outputs/your_document_meta.json` - Document statistics

#### Step 2: Fact Extraction

```powershell
cd .\esia-fact-extractor-pipeline

python step3_extraction_with_archetypes.py `
  --chunks ..\data\outputs\your_document_chunks.jsonl `
  --output ..\data\outputs\your_document_facts.json

cd ..
```

**Output Files:**
- `data/outputs/your_document_facts.json` - Structured extracted facts

#### Step 3: Quality Analysis

```powershell
cd .\esia-fact-analyzer

python analyze_esia_v2.py `
  --input-dir ..\data\outputs `
  --output-dir ..\data\outputs `
  --chunks your_document_chunks.jsonl `
  --meta your_document_meta.json

cd ..
```

**Output Files:**
- `data/outputs/your_document_review.html` - Interactive dashboard (open in browser)
- `data/outputs/your_document_review.xlsx` - Detailed Excel workbook

---

## Processing Multiple Documents

### Batch Processing with PowerShell Script

```powershell
# Process all PDFs in the data/pdfs directory
$pdfFiles = Get-ChildItem -Path ".\data\pdfs" -Filter "*.pdf"

foreach ($file in $pdfFiles) {
    Write-Host "Processing: $($file.Name)"
    python run-esia-pipeline.py $file.FullName
    Write-Host "Completed: $($file.Name)`n"
}

Write-Host "Batch processing completed!"
```

### Process with Error Handling

```powershell
# Process with error handling and status reporting
$pdfFiles = Get-ChildItem -Path ".\data\pdfs" -Filter "*.pdf"
$processed = 0
$failed = 0

foreach ($file in $pdfFiles) {
    Write-Host "Processing: $($file.Name)" -ForegroundColor Cyan

    try {
        python run-esia-pipeline.py $file.FullName
        $processed++
        Write-Host "✓ Completed: $($file.Name)" -ForegroundColor Green
    }
    catch {
        $failed++
        Write-Host "✗ Failed: $($file.Name) - $_" -ForegroundColor Red
    }

    Write-Host ""
}

Write-Host "=== Processing Summary ===" -ForegroundColor Yellow
Write-Host "Processed: $processed"
Write-Host "Failed: $failed"
Write-Host "Total: $($processed + $failed)"
```

---

## Expected Outputs

### Step 1 Output Files
```
data/outputs/
├── your_document_chunks.jsonl       # Semantic chunks (JSONL format)
└── your_document_meta.json          # Document metadata and statistics
```

### Step 2 Output Files
```
data/outputs/
└── your_document_facts.json         # Extracted facts organized by domain
```

### Step 3 Output Files
```
data/outputs/
├── your_document_review.html        # Interactive dashboard (open in browser)
└── your_document_review.xlsx        # Detailed analysis workbook
```

### Viewing Results

**HTML Dashboard (Interactive):**
```powershell
# Open the HTML dashboard in your default browser
Start-Process ".\data\outputs\your_document_review.html"
```

**Excel Report:**
```powershell
# Open the Excel workbook
Start-Process ".\data\outputs\your_document_review.xlsx"
```

**JSON Facts (Command Line):**
```powershell
# View extracted facts in PowerShell
Get-Content ".\data\outputs\your_document_facts.json" | ConvertFrom-Json | ConvertTo-Json

# Or format nicely
$facts = Get-Content ".\data\outputs\your_document_facts.json" | ConvertFrom-Json
$facts | Format-Table -AutoSize
```

---

## Troubleshooting

### Common Issues

#### 1. API Key Not Found
```
Error: GOOGLE_API_KEY not found
```

**Solution:**
- Verify `.env` file exists in `packages/pipeline/` directory
- Check API key is correctly set: `Get-Content .\.env`
- Restart PowerShell terminal after creating `.env` file

#### 2. Python Module Not Found
```
Error: No module named 'docling'
```

**Solution:**
```powershell
# Reinstall all dependencies
pip install --upgrade pip
pip install -r .\esia-fact-extractor-pipeline\requirements.txt
pip install -r .\esia-fact-analyzer\requirements.txt
```

#### 3. Out of Memory
```
Error: CUDA out of memory
```

**Solution:**
```powershell
# Run Step 1 with CPU instead of GPU
python step1_docling_hybrid_chunking.py "document.pdf" --gpu-mode cpu
```

#### 4. PDF Processing Fails
```
Error: Failed to parse PDF
```

**Solution:**
- Verify PDF file is not corrupted: `Test-Path ".\data\pdfs\your_document.pdf"`
- Try with a different PDF file
- Check if PDF requires a password

#### 5. API Rate Limit Exceeded
```
Error: Too many requests to LLM API
```

**Solution:**
```powershell
# Use OpenRouter as alternative LLM provider
# Update OPENROUTER_API_KEY in .env file
# The system will automatically switch providers if primary fails
```

---

## Performance Optimization

### Faster Processing on CPU

```powershell
# Run Step 1 with CPU (if GPU is unavailable)
cd .\esia-fact-extractor-pipeline
python step1_docling_hybrid_chunking.py "..\data\pdfs\document.pdf" --gpu-mode cpu
cd ..
```

### Parallel Processing (Multiple Documents)

```powershell
# Use Background Jobs for true parallel processing
$pdfFiles = Get-ChildItem -Path ".\data\pdfs" -Filter "*.pdf"

foreach ($file in $pdfFiles) {
    $scriptBlock = {
        param($filePath)
        python run-esia-pipeline.py $filePath
    }

    Start-Job -ScriptBlock $scriptBlock -ArgumentList $file.FullName -Name "process_$($file.BaseName)"
}

# Monitor jobs
Get-Job | Wait-Job
Get-Job | Receive-Job
```

### Monitor Processing Progress

```powershell
# Watch output files being created
Watch-Output -Path ".\data\outputs" -Filter "*.json*" -Action {
    param($EventArgs)
    Write-Host "File updated: $($EventArgs.Name)"
}
```

---

## Getting Help

### View Available Commands

```powershell
# Show pipeline help
python run-esia-pipeline.py --help

# Show version
python run-esia-pipeline.py --version
```

### Check Pipeline Status

```powershell
# List input documents
Get-ChildItem -Path ".\data\pdfs" -Filter "*.pdf" | Format-Table Name, Length, LastWriteTime

# List output files
Get-ChildItem -Path ".\data\outputs" | Format-Table Name, Length, LastWriteTime
```

### View Logs

```powershell
# Logs are printed to console during execution
# For persistent logs, redirect to file
python run-esia-pipeline.py .\data\pdfs\document.pdf > pipeline.log 2>&1

# View log contents
Get-Content pipeline.log -Tail 50  # Last 50 lines
```

---

## Integration with Workspace

### From Workspace Root

```powershell
# Navigate to workspace root
cd M:\GitHub\esia-workspace

# Run pipeline via workspace command
pnpm dev:pipeline

# This is equivalent to running the pipeline directly
cd packages/pipeline
python run-esia-pipeline.py .\data\pdfs\your_document.pdf
```

---

## Next Steps

After running the pipeline:

1. **Review HTML Dashboard** - Open `your_document_review.html` for interactive analysis
2. **Check Excel Report** - Review detailed findings in `your_document_review.xlsx`
3. **Analyze Extracted Facts** - View `your_document_facts.json` for raw extracted data
4. **Export Results** - Use the dashboard to export specific findings
5. **Generate Reports** - Combine multiple documents for comparative analysis

---

## Additional Resources

- **QUICKSTART.md** - 60-second setup guide
- **CLI_USAGE.md** - Complete CLI reference
- **ARCHITECTURE.md** - Technical architecture details
- **README_INTEGRATION.md** - Integration documentation

---

## Contact & Support

For issues or questions:
- Check documentation in `packages/pipeline/docs/`
- Review pipeline logs with `--verbose` flag
- Verify environment configuration in `.env` file
- Check API key validity and rate limits

---

**Last Updated:** December 2024
**Pipeline Version:** 1.0
**Supported OS:** Windows 10/11 with PowerShell 5.1+
