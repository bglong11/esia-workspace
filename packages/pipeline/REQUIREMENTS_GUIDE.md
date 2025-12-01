# ESIA Pipeline Requirements - Complete Guide

## Overview

The ESIA Pipeline dependencies have been **consolidated into a single `requirements.txt`** file located in the pipeline root directory:

```
M:\GitHub\esia-workspace\packages\pipeline\requirements.txt
```

This single file contains all dependencies needed for the complete 3-step pipeline:
1. **Step 1**: Document Chunking (PDF/DOCX → semantic chunks)
2. **Step 2**: Fact Extraction (chunks → structured facts)
3. **Step 3**: Quality Analysis (facts → HTML dashboard + Excel report)

---

## Installation

### Standard Installation (Recommended)

From the pipeline root directory:

```powershell
# Windows PowerShell
cd M:\GitHub\esia-workspace\packages\pipeline
pip install -r requirements.txt
```

Or from any directory:

```powershell
pip install -r "M:\GitHub\esia-workspace\packages\pipeline\requirements.txt"
```

### With Optional Features

**Translation Support (non-English documents):**
```powershell
pip install -r requirements.txt langdetect requests
```

**Alternative LLM Provider (OpenRouter):**
```powershell
pip install -r requirements.txt openrouter
```

**Environment Management (.env file loading):**
```powershell
pip install -r requirements.txt python-dotenv
```

**All Features:**
```powershell
pip install -r requirements.txt langdetect requests python-dotenv openrouter
```

---

## Dependencies Breakdown

### Core Dependencies (8 packages)

These are **essential** and always installed:

| Package | Version | Purpose |
|---------|---------|---------|
| `docling` | ≥1.0.0 | PDF/DOCX parsing |
| `docling-core[chunking-openai]` | ≥1.0.0 | Token-aware semantic chunking |
| `tiktoken` | ≥0.5.0 | Exact token counting |
| `torch` | ≥2.0.0 | GPU acceleration |
| `tqdm` | ≥4.65.0 | Progress bars |
| `dspy-ai` | Latest | DSPy framework for extraction |
| `google-genai` | Latest | Google Gemini API |
| `openpyxl` | Latest | Excel export |

### Optional Dependencies (5 packages)

Install only if needed for specific features:

| Package | Purpose | Use Case |
|---------|---------|----------|
| `langdetect` | Language detection | Processing non-English ESIA documents |
| `google-cloud-translate` | Google Cloud Translation | High-quality translation |
| `requests` | HTTP library | LibreTranslate API (free) |
| `openrouter` | Alternative LLM provider | Fallback to OpenRouter if Gemini unavailable |
| `python-dotenv` | Environment loading | Auto-load from .env files |

---

## File Structure

### Old Structure (Before Consolidation)
```
packages/pipeline/
├── esia-fact-extractor-pipeline/
│   └── requirements.txt  ← Old location (still exists for backward compatibility)
├── esia-fact-analyzer/
│   └── (no requirements.txt - uses only core deps)
```

### New Structure (After Consolidation)
```
packages/pipeline/
├── requirements.txt  ← NEW: Single source of truth
├── esia-fact-extractor-pipeline/
│   └── requirements.txt  ← DEPRECATED: Points to parent
├── esia-fact-analyzer/
├── REQUIREMENTS_GUIDE.md  ← This file
└── pipeline_flow.md       ← Step-by-step execution guide
```

---

## Backward Compatibility

The old `esia-fact-extractor-pipeline/requirements.txt` still exists but is **deprecated**. It now includes the parent requirements.txt:

```
# esia-fact-extractor-pipeline/requirements.txt
-r ../requirements.txt
```

This allows existing scripts and documentation to continue working without changes.

---

## Python Requirements

- **Python 3.8+** required (type hints, dataclasses, f-strings)
- **Recommended: Python 3.10+** for best compatibility

Check your Python version:

```powershell
python --version
```

---

## Environment Variables

### Required for Pipeline Operation

Create a `.env` file in the pipeline root directory:

```
GOOGLE_API_KEY=your_google_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Or set in PowerShell before running:

```powershell
$env:GOOGLE_API_KEY = "your_google_api_key_here"
python run-esia-pipeline.py document.pdf
```

### Getting API Keys

**Google Gemini API:**
1. Go to https://ai.google.dev/
2. Create new API key
3. Set in `.env` or environment

**OpenRouter API (Optional):**
1. Go to https://openrouter.ai/
2. Create account and get API key
3. Set in `.env` for fallback provider

---

## Installation Verification

After installation, verify all dependencies are installed:

```powershell
# Check all core packages
python -c "
import docling, docling_core, tiktoken, torch, tqdm, dspy, google, openpyxl
print('✓ All core dependencies installed successfully!')
"
```

Check individual components:

```powershell
# Check Docling
python -c "from docling.document_converter import DocumentConverter; print('✓ Docling OK')"

# Check DSPy
python -c "import dspy; print('✓ DSPy OK')"

# Check Gemini
python -c "from google import genai; print('✓ Google Gemini OK')"

# Check PyTorch
python -c "import torch; print(f'✓ PyTorch OK (CUDA available: {torch.cuda.is_available()})')"

# Check openpyxl
python -c "import openpyxl; print('✓ openpyxl OK')"
```

---

## Troubleshooting

### Common Installation Issues

**Issue: `No module named 'docling'`**
```powershell
# Solution: Reinstall specific package
pip install --upgrade docling docling-core
```

**Issue: `CUDA out of memory`**
```powershell
# Solution: Run Step 1 with CPU
python step1_docling_hybrid_chunking.py document.pdf --gpu-mode cpu
```

**Issue: `ImportError: cannot import name 'genai' from 'google'`**
```powershell
# Solution: Reinstall google-genai
pip uninstall google-genai -y
pip install google-genai
```

**Issue: `API key not found`**
```powershell
# Verify .env file exists
Get-Content .\.env

# Or set in PowerShell
$env:GOOGLE_API_KEY = "your-key"
```

**Issue: `pip install fails on torch`**
```powershell
# torch may require specific system packages
# On Windows, this usually works, but ensure:
# 1. Visual C++ Build Tools installed
# 2. Latest pip: pip install --upgrade pip

# Alternative: Install CPU-only version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

---

## GPU Support (Optional)

PyTorch can use GPU for faster document processing. Check GPU availability:

```powershell
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}')"
```

If you have an NVIDIA GPU:

```powershell
# Install CUDA-enabled torch (requires NVIDIA CUDA Toolkit)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

If you only have CPU:

```powershell
# Use CPU (slower but works)
python step1_docling_hybrid_chunking.py document.pdf --gpu-mode cpu
```

---

## Usage After Installation

### Run Complete Pipeline

```powershell
cd M:\GitHub\esia-workspace\packages\pipeline
python run-esia-pipeline.py data/pdfs/document.pdf
```

### Run Specific Steps

```powershell
# Step 1 only (chunking)
python run-esia-pipeline.py document.pdf --steps 1

# Step 2 only (extraction)
python run-esia-pipeline.py document.pdf --steps 2

# Step 3 only (analysis)
python run-esia-pipeline.py document.pdf --steps 3

# Steps 1 and 3 (skip extraction)
python run-esia-pipeline.py document.pdf --steps 1,3
```

### Run with Verbose Output

```powershell
python run-esia-pipeline.py document.pdf --verbose
```

---

## Dependency Cleanup

To remove all installed dependencies:

```powershell
# Create a list of installed packages
pip freeze > installed_packages.txt

# Uninstall everything
pip uninstall -r installed_packages.txt -y

# Clean up
Remove-Item installed_packages.txt
```

To update all dependencies:

```powershell
pip install -r requirements.txt --upgrade
```

---

## Integration with IDE

### PyCharm

1. **Open project** in PyCharm
2. **Settings** → **Project: esia-workspace** → **Python Interpreter**
3. Click gear icon → **Add**
4. Select **Existing Environment** → Navigate to Python executable
5. PyCharm will automatically detect `requirements.txt`
6. Install dependencies via UI or:
   ```
   pip install -r requirements.txt
   ```

### Visual Studio Code

1. **Open** `packages/pipeline` in VS Code
2. **Create virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Select interpreter:** Ctrl+Shift+P → "Python: Select Interpreter" → Choose venv

---

## Version Pinning (Advanced)

If you need to pin specific versions (for reproducibility):

```powershell
# Generate locked versions
pip freeze > requirements-lock.txt

# Then install from locked versions
pip install -r requirements-lock.txt
```

---

## Next Steps

After installation:

1. ✅ **Set up environment variables** (GOOGLE_API_KEY)
2. ✅ **Prepare PDF/DOCX documents** in `data/pdfs/`
3. ✅ **Run the pipeline:**
   ```powershell
   python run-esia-pipeline.py data/pdfs/your_document.pdf
   ```
4. ✅ **Check results** in `data/outputs/`
5. ✅ **View HTML dashboard** - open `your_document_review.html` in browser

For step-by-step instructions, see:
- **`pipeline_flow.md`** - Complete execution guide
- **`CLAUDE.md`** - Technical architecture details
- **`CLI_USAGE.md`** - CLI reference

---

## Support & Issues

If you encounter issues:

1. **Check logs** with `--verbose` flag
2. **Verify API keys** are set correctly
3. **Reinstall dependencies:** `pip install -r requirements.txt --upgrade`
4. **Check Python version:** `python --version` (should be 3.8+)
5. **Review documentation** in `docs/` directory

---

**Last Updated:** December 2024
**Requirements Version:** 1.0
**Python Compatibility:** 3.8+
