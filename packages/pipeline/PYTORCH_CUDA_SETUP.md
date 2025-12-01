# PyTorch CUDA Installation Guide

**Status:** ✅ PyTorch 2.5.1 with CUDA 12.1 installed

## Installation Summary

PyTorch with CUDA 12.1 support has been successfully installed in venv312:
- **PyTorch:** 2.5.1+cu121
- **torchvision:** 0.20.1+cu121
- **torchaudio:** 2.5.1+cu121
- **Environment:** Python 3.12.7 (venv312)

## Verify Installation

Open PowerShell in the pipeline directory:

```powershell
cd M:\GitHub\esia-workspace\packages\pipeline

# Activate venv312
.\venv312\Scripts\Activate.ps1

# Check PyTorch version and CUDA support
python -c "import torch; print('PyTorch installed'); print(f'CUDA: {torch.cuda.is_available()}')"
```

## Check GPU Availability

If you have an NVIDIA GPU:

```powershell
# Activate venv312 first
.\venv312\Scripts\Activate.ps1

# Check GPU
python -c "import torch; print(f'GPU Available: {torch.cuda.is_available()}'); print(f'GPU Count: {torch.cuda.device_count()}'); print(f'GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
```

## Installed Packages

The following packages were installed:
- torch-2.5.1+cu121
- torchvision-0.20.1+cu121
- torchaudio-2.5.1+cu121
- numpy-2.3.3
- pillow-11.3.0
- sympy-1.13.1
- And all required dependencies

## Next Steps

### Test Step 1 with GPU Support

```powershell
# Activate venv312
.\venv312\Scripts\Activate.ps1

# Test Step 1 with auto GPU detection
python run-esia-pipeline.py data/pdfs/document.pdf --steps 1 --verbose

# Or explicitly use GPU mode
python step1_docling_hybrid_chunking.py document.pdf --gpu-mode auto
```

### If GPU is Available

The pipeline will automatically use GPU for:
- Docling PDF/DOCX parsing (faster processing)
- Model inference if needed

### If GPU is NOT Available

The pipeline will automatically fall back to CPU:
- Still works perfectly
- Just slower than GPU
- No configuration needed

## Troubleshooting

### "CUDA is not available" Error

This means your system doesn't have an NVIDIA GPU. That's OK:
- The pipeline works fine in CPU mode
- Install NVIDIA CUDA Toolkit if you want GPU support
- Currently using CPU-only mode is acceptable

### "Module not found" Error

Reactivate venv312:
```powershell
.\venv312\Scripts\Activate.ps1
pip list  # Should show torch, torchvision, torchaudio
```

### Permission Denied on Activation

Run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

## Using the Pipeline with PyTorch CUDA

### Option 1: Automatic GPU Detection (Recommended)

```powershell
.\run-pipeline.ps1 data/pdfs/document.pdf --steps 1,2,3 --verbose
```
- Automatically detects and uses GPU if available
- Falls back to CPU if not available
- No configuration needed

### Option 2: Explicit GPU Mode

```powershell
# Force GPU (if available)
python step1_docling_hybrid_chunking.py document.pdf --gpu-mode cuda

# Force CPU
python step1_docling_hybrid_chunking.py document.pdf --gpu-mode cpu

# Auto-detect (recommended)
python step1_docling_hybrid_chunking.py document.pdf --gpu-mode auto
```

## Performance Notes

With CUDA 12.1 installed (if GPU available):
- **Step 1 (GPU):** 1-5 minutes per document
- **Step 1 (CPU):** 5-15 minutes per document
- **Step 2:** Depends on LLM API (not GPU-accelerated in current setup)
- **Step 3:** Fast on both (rule-based)

## Environment Info

```
Python: 3.12.7
venv: M:\GitHub\esia-workspace\packages\pipeline\venv312
PyTorch: 2.5.1+cu121
CUDA: 12.1 support enabled
Docling: Compatible
Status: Ready to use
```

## Next Steps

1. **Test GPU availability:**
   ```powershell
   .\venv312\Scripts\Activate.ps1
   python -c "import torch; print(torch.cuda.is_available())"
   ```

2. **If GPU not detected, install NVIDIA CUDA:**
   - Download from: https://developer.nvidia.com/cuda-downloads
   - Install CUDA 12.1 Toolkit
   - Restart computer
   - Re-test

3. **Run pipeline:**
   ```powershell
   .\run-pipeline.ps1 data/pdfs/document.pdf --steps 1 --verbose
   ```

## Important Notes

- ✅ PyTorch with CUDA support is installed
- ✅ venv312 is set up and ready
- ✅ Auto GPU detection is enabled
- ⚠️ Requires NVIDIA GPU to see performance benefits
- ℹ️ CPU mode works fine without GPU

---

**Status:** ✅ PyTorch CUDA Installation Complete
**Date:** December 1, 2025
**Ready to Use:** Yes
