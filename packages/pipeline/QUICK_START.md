# Quick Start - ESIA Pipeline with Python 3.12

## Easy Ways to Run the Pipeline

Choose one of these methods:

### Method 1: PowerShell Script (Recommended)

```powershell
cd M:\GitHub\esia-workspace\packages\pipeline

# Run with automatic venv312 activation
.\run-pipeline.ps1 data/pdfs/document.pdf

# With options
.\run-pipeline.ps1 data/pdfs/document.pdf --steps 1,2,3
.\run-pipeline.ps1 data/pdfs/document.pdf --verbose
.\run-pipeline.ps1 data/pdfs/document.pdf --steps 1,2,3 --verbose
```

**Advantages:**
- ✅ Automatically activates venv312
- ✅ Shows Python version being used
- ✅ Nice colored output
- ✅ Shows command being executed

### Method 2: Batch File (Windows Command Prompt)

```batch
cd M:\GitHub\esia-workspace\packages\pipeline

REM Run with automatic venv312 activation
run-pipeline.bat data/pdfs/document.pdf

REM With options
run-pipeline.bat data/pdfs/document.pdf --steps 1,2,3
run-pipeline.bat data/pdfs/document.pdf --verbose
```

**Advantages:**
- ✅ Works from Command Prompt (cmd.exe)
- ✅ Can double-click to run
- ✅ No PowerShell execution policy issues
- ✅ Same venv312 auto-activation

### Method 3: Manual Activation (If You Prefer)

```powershell
cd M:\GitHub\esia-workspace\packages\pipeline

# Activate venv312 manually
.\venv312\Scripts\Activate.ps1

# Run pipeline
python run-esia-pipeline.py data/pdfs/document.pdf --steps 1,2,3 --verbose

# Deactivate when done
deactivate
```

**Advantages:**
- ✅ Full control over environment
- ✅ Can run multiple commands
- ✅ Useful for debugging

---

## Examples

### Example 1: Basic Pipeline Run
```powershell
.\run-pipeline.ps1 data/pdfs/myfile.pdf
```
Runs all 3 steps (1, 2, 3) with default settings.

### Example 2: Run Only Chunking
```powershell
.\run-pipeline.ps1 data/pdfs/myfile.pdf --steps 1
```
Only runs Step 1 (document chunking).

### Example 3: Run Extraction and Analysis
```powershell
.\run-pipeline.ps1 data/pdfs/myfile.pdf --steps 2,3
```
Skips chunking, runs extraction and analysis.

### Example 4: Verbose Mode
```powershell
.\run-pipeline.ps1 data/pdfs/myfile.pdf --verbose
```
Shows detailed logs during execution.

### Example 5: Complete with All Options
```powershell
.\run-pipeline.ps1 data/pdfs/myfile.pdf --steps 1,2,3 --verbose
```
Runs all steps with detailed output.

---

## Setting API Key

### Before Running Pipeline (Required)

```powershell
# Set Google Gemini API key
$env:GOOGLE_API_KEY = "your_api_key_here"

# Optional: Set alternative LLM provider
$env:OPENROUTER_API_KEY = "your_api_key_here"

# Now run pipeline
.\run-pipeline.ps1 data/pdfs/document.pdf
```

Or create a `.env` file in the pipeline directory:
```
GOOGLE_API_KEY=your_api_key_here
OPENROUTER_API_KEY=your_api_key_here
```

---

## File Structure

```
packages/pipeline/
├── run-pipeline.ps1          ← PowerShell runner (NEW)
├── run-pipeline.bat          ← Batch file runner (NEW)
├── QUICK_START.md            ← This file (NEW)
├── run-esia-pipeline.py      ← Main pipeline script
├── venv312/                  ← Python 3.12 environment
│   └── Scripts/
│       ├── python.exe        ← Python 3.12 executable
│       └── Activate.ps1      ← Activation script
└── data/
    ├── pdfs/                 ← Your input PDFs
    └── outputs/              ← Pipeline outputs
```

---

## Troubleshooting

### "run-pipeline.ps1 is not recognized"

**Solution:** Make sure you're in the correct directory:
```powershell
cd M:\GitHub\esia-workspace\packages\pipeline
.\run-pipeline.ps1 data/pdfs/document.pdf
```

The `.\` is required to run scripts in the current directory.

### "PowerShell execution policy" error

**Solution:** Run this once:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

Or use the batch file instead:
```batch
run-pipeline.bat data/pdfs/document.pdf
```

### "venv312 not found"

**Solution:** Create it:
```powershell
"M:\Python\Python3_12\python.exe" -m venv venv312
pip install -r requirements.txt
```

### "API key not found"

**Solution:** Set before running:
```powershell
$env:GOOGLE_API_KEY = "your_key"
.\run-pipeline.ps1 data/pdfs/document.pdf
```

### "ModuleNotFoundError"

**Solution:** Reinstall dependencies in venv312:
```powershell
.\venv312\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Verifying Setup

Check that Python 3.12 is ready:

```powershell
# Show which Python will be used
.\venv312\Scripts\python.exe --version

# Should output: Python 3.12.7

# List installed packages
.\venv312\Scripts\pip.exe list
```

---

## Next Steps

1. **Copy PDF to `data/pdfs/`**
   ```powershell
   Copy-Item "C:\path\to\your\document.pdf" "data\pdfs\"
   ```

2. **Set API key**
   ```powershell
   $env:GOOGLE_API_KEY = "your_key"
   ```

3. **Run pipeline**
   ```powershell
   .\run-pipeline.ps1 data/pdfs/document.pdf --verbose
   ```

4. **Check results**
   ```powershell
   # View outputs
   Get-ChildItem data/outputs/

   # Open HTML dashboard
   Invoke-Item data/outputs/document_review.html
   ```

---

## Performance Tips

- **First run takes longer** - Models are downloaded/cached
- **GPU mode is faster** - Set `--gpu-mode cuda` if available
- **CPU mode works too** - Use `--gpu-mode cpu` if needed
- **Batch processing** - Process multiple PDFs in a loop

---

**Status:** ✅ Ready to use
**Python:** 3.12.7
**Created:** December 1, 2025
