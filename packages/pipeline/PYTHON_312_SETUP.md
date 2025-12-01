# Python 3.12 Virtual Environment Setup

## Quick Start (Python 3.12)

A Python 3.12 virtual environment has been created at:
```
M:\GitHub\esia-workspace\packages\pipeline\venv312
```

### Activate in PowerShell

```powershell
cd M:\GitHub\esia-workspace\packages\pipeline
.\venv312\Scripts\Activate.ps1

# Verify you're using Python 3.12
python --version  # Should show: Python 3.12.7
```

### After Activation

Once activated, all Python commands use Python 3.12:
```powershell
# Run pipeline
python run-esia-pipeline.py data/pdfs/document.pdf --steps 1,2,3 --verbose

# Install dependencies
pip install -r requirements.txt

# Check Python version
python --version
```

## Switching Between Python Versions

### Use Python 3.12 (Recommended for Pipeline)
```powershell
cd M:\GitHub\esia-workspace\packages\pipeline
.\venv312\Scripts\Activate.ps1
```

### Use Python 3.13 (System Default)
```powershell
deactivate  # Exit the venv312
# Now using system Python 3.13
```

## Creating New Virtual Environments

If you need to create another venv with 3.12:
```powershell
"M:\Python\Python3_12\python.exe" -m venv venv_name
```

## Troubleshooting

### "Cannot activate venv312"
Make sure you're in the pipeline directory:
```powershell
cd M:\GitHub\esia-workspace\packages\pipeline
.\venv312\Scripts\Activate.ps1
```

### "ModuleNotFoundError after activation"
The virtual environment may be missing packages. Reinstall:
```powershell
pip install -r requirements.txt
```

### Check Which Python is Active
```powershell
# Shows full path and version
python -c "import sys; print(sys.executable); print(f'Python {sys.version}')"
```

## Virtual Environment Information

**Location:** `M:\GitHub\esia-workspace\packages\pipeline\venv312`
**Python Version:** 3.12.7
**Pip Version:** 24.2
**Python Executable:** `M:\GitHub\esia-workspace\packages\pipeline\venv312\Scripts\python.exe`

## Next Steps

1. **Activate the environment:**
   ```powershell
   .\venv312\Scripts\Activate.ps1
   ```

2. **Set API key:**
   ```powershell
   $env:GOOGLE_API_KEY = "your_key"
   ```

3. **Run pipeline:**
   ```powershell
   python run-esia-pipeline.py data/pdfs/document.pdf
   ```

---

**Status:** ✅ Python 3.12 environment ready
**Created:** December 1, 2025
