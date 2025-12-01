# GPU Setup Guide for Step 1 Optimization

## Your Hardware

- **GPU**: NVIDIA GeForce RTX 2060 (6 GB VRAM)
- **CUDA Version**: 13.0
- **Driver Version**: 581.57 ✅ (Already installed)

## Current Status

```
PyTorch:     2.7.1+cpu  ❌ CPU variant (should be CUDA variant)
CUDA Support: Not available
Expected: 3-5x speedup when properly configured
```

## Quick Fix (5 minutes)

### Step 1: Remove Current PyTorch
```bash
pip uninstall torch torchvision torchaudio -y
```

### Step 2: Install CUDA-Enabled PyTorch
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Why cu121 (CUDA 12.1)?**
- Your GPU has CUDA 13.0 driver
- PyTorch CUDA 12.1 is fully compatible with CUDA 13.0
- It's the latest stable PyTorch CUDA variant available
- Docling supports CUDA 12.x

### Step 3: Verify Installation
```bash
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
```

**Expected Output**:
```
CUDA Available: True
Device: NVIDIA GeForce RTX 2060
```

## Running Step 1 with GPU

Once CUDA is configured:

### Option 1: Auto-Detect (Recommended)
```bash
python step1_docling_hybrid_chunking.py ./data/inputs/pdfs/TL_IPP_Supp_ESIA_2025-09-15.pdf \
  -o ./data/outputs \
  --gpu-mode auto
```

The script automatically uses GPU if available, falls back to CPU.

### Option 2: Force GPU
```bash
python step1_docling_hybrid_chunking.py ./data/inputs/pdfs/TL_IPP_Supp_ESIA_2025-09-15.pdf \
  -o ./data/outputs \
  --gpu-mode cuda
```

Use if you want to ensure GPU is used (will error if unavailable).

### Option 3: CPU-Only (for comparison)
```bash
python step1_docling_hybrid_chunking.py ./data/inputs/pdfs/TL_IPP_Supp_ESIA_2025-09-15.pdf \
  -o ./data/outputs \
  --gpu-mode cpu
```

## Performance Comparison

| Mode | Expected Time | GPU Memory | Notes |
|------|---|---|---|
| CPU (current) | 35-40 sec | N/A | Baseline |
| GPU (expected) | 7-14 sec | ~2-3 GB | 3-5x faster |

Your RTX 2060 has 6GB VRAM (plenty for this workload).

## Troubleshooting

### Still showing CPU mode after installation?
```bash
# Clear pip cache and reinstall
pip cache purge
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --force-reinstall
```

### Want to check detailed CUDA info?
```bash
python -c "
import torch
print(f'PyTorch Version: {torch.__version__}')
print(f'CUDA Available: {torch.cuda.is_available()}')
print(f'CUDA Version: {torch.version.cuda}')
print(f'GPU Count: {torch.cuda.device_count()}')
if torch.cuda.is_available():
    print(f'GPU Name: {torch.cuda.get_device_name(0)}')
    print(f'GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')
"
```

### Getting "CUDA out of memory" errors?
1. Reduce chunk size:
   ```bash
   python step1_docling_hybrid_chunking.py input.pdf --chunk-max-tokens 2000
   ```

2. Or switch to CPU temporarily:
   ```bash
   python step1_docling_hybrid_chunking.py input.pdf --gpu-mode cpu
   ```

3. Or process smaller documents first

## Installation Reference

### CUDA Toolkit Versions Compatibility

| PyTorch CUDA | Compatible GPU CUDA Drivers |
|---|---|
| CUDA 12.1 | 13.0+ ✅ Your driver works |
| CUDA 11.8 | 12.0+ |
| CUDA 11.7 | 11.8+ |

**Your setup**: CUDA 13.0 driver → Install CUDA 12.1 PyTorch ✅

## After Installation

Once GPU is set up:

1. **Test with this document** (baseline):
   ```bash
   python step1_docling_hybrid_chunking.py ./data/inputs/pdfs/TL_IPP_Supp_ESIA_2025-09-15.pdf \
     -o ./data/outputs \
     --gpu-mode auto \
     --verbose
   ```

2. **Compare times**: Should be 3-5x faster than CPU run

3. **Ready for Step 2**: Output files are identical, just faster to generate

## Next: Step 2 Setup

After Step 1 completes, you'll need API keys for Step 2 (fact extraction):

```bash
# Create .env file in project root
echo "GOOGLE_API_KEY=your_key_here" > .env
```

Then run Step 2:
```bash
python src/esia_extractor.py \
  --chunks ./data/outputs/TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl \
  --output ./data/outputs/facts.json
```

---

**Time to GPU optimization**: ~5 minutes setup + 1 test run
**Expected benefit**: 3-5x speedup on document processing
