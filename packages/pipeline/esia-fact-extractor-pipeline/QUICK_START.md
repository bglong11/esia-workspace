# Quick Start Guide

## Step 1: Document Chunking (Already Tested ✅)

Your test is complete! Output files are ready in `./data/outputs/`

### Run Again (with different settings):

```bash
# GPU mode (after enabling CUDA - see GPU_SETUP_GUIDE.md)
python step1_docling_hybrid_chunking.py ./data/inputs/pdfs/TL_IPP_Supp_ESIA_2025-09-15.pdf \
  -o ./data/outputs --gpu-mode auto

# CPU mode
python step1_docling_hybrid_chunking.py ./data/inputs/pdfs/TL_IPP_Supp_ESIA_2025-09-15.pdf \
  -o ./data/outputs --gpu-mode cpu

# With custom options
python step1_docling_hybrid_chunking.py <input.pdf> \
  -o ./data/outputs \
  --chunk-max-tokens 3000 \
  --enable-images \
  --output-markdown \
  --verbose
```

**Output**:
- `<filename>_chunks.jsonl` - 117 semantic chunks
- `<filename>_meta.json` - Metadata & statistics

---

## Step 2: Fact Extraction (Next Phase)

### Setup (First Time Only)

1. **Install dependencies** (if not done):
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file** in project root:
   ```bash
   echo "GOOGLE_API_KEY=your_key_here" > .env
   ```

   Or with OpenRouter:
   ```bash
   echo "OPENROUTER_API_KEY=your_key_here" > .env
   ```

### Run Extraction

```bash
# Basic extraction
python src/esia_extractor.py \
  --chunks ./data/outputs/TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl \
  --output ./data/outputs/facts.json

# With custom model
python src/esia_extractor.py \
  --chunks ./data/outputs/TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl \
  --output ./data/outputs/facts.json \
  --model gpt-4o \
  --provider openrouter
```

**Output**: `facts.json` - Extracted facts with page references

---

## Step 3: Validation

```bash
# Validate extracted facts
python src/validator.py ./data/outputs/facts.json

# Classify project type
python src/project_type_classifier.py ./data/outputs/TL_IPP_Supp_ESIA_2025-09-15_meta.json
```

---

## Command Reference Card

### Step 1 Options

| Option | Example | Purpose |
|--------|---------|---------|
| `-o, --output-dir` | `-o ./my_output` | Output directory |
| `--gpu-mode` | `--gpu-mode cuda` | auto/cuda/cpu |
| `--chunk-max-tokens` | `--chunk-max-tokens 2000` | Chunk size |
| `--tokenizer-model` | `--tokenizer-model gpt-4o` | Token model |
| `--enable-images` | Flag | Extract images |
| `--disable-tables` | Flag | Skip tables |
| `--output-markdown` | Flag | Generate .md |
| `--no-json` | Flag | Skip metadata |
| `-v, --verbose` | Flag | Verbose output |

### Step 1 Examples

```bash
# Quick (CPU, default settings)
python step1_docling_hybrid_chunking.py input.pdf -o ./output

# GPU accelerated
python step1_docling_hybrid_chunking.py input.pdf -o ./output --gpu-mode auto

# Large documents (smaller chunks)
python step1_docling_hybrid_chunking.py large.pdf -o ./output --chunk-max-tokens 2000

# Full featured
python step1_docling_hybrid_chunking.py input.pdf \
  -o ./output \
  --gpu-mode auto \
  --enable-images \
  --output-markdown \
  --verbose

# DOCX (auto-converts to PDF)
python step1_docling_hybrid_chunking.py document.docx -o ./output --gpu-mode auto
```

---

## Data Flow

```
Input PDF/DOCX
    ↓
Step 1: Chunking (35-40 sec on CPU, 7-14 sec on GPU)
    ↓
Output: chunks.jsonl + meta.json
    ↓
Step 2: Fact Extraction (1-5 min depending on LLM)
    ↓
Output: facts.json
    ↓
Step 3: Validation & Analysis
    ↓
Final Results
```

---

## Common Tasks

### Test GPU Setup
```bash
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

### Check Dependencies
```bash
pip list | grep -E "torch|docling|dspy|tiktoken"
```

### Count Chunks
```bash
wc -l ./data/outputs/*_chunks.jsonl
```

### View Sample Chunk
```bash
python -c "
import json
with open('./data/outputs/TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl') as f:
    chunk = json.loads(f.readline())
    print(json.dumps(chunk, indent=2))
"
```

### Batch Process Multiple PDFs
```bash
for pdf in ./data/inputs/pdfs/*.pdf; do
    python step1_docling_hybrid_chunking.py "$pdf" -o ./data/outputs
done
```

---

## Performance Expectations

| Scenario | Time | Notes |
|----------|------|-------|
| Small (1-10 pages) CPU | <1 sec | Fast |
| Small (1-10 pages) GPU | <1 sec | Very fast |
| Medium (10-100 pages) CPU | 1-10 sec | Reasonable |
| Medium (10-100 pages) GPU | 2-5 sec | 3-5x faster |
| Large (100+ pages) CPU | 10-60 sec | Slower |
| Large (100+ pages) GPU | 5-15 sec | 5-10x faster |

Your test: 77 pages on CPU = 35-40 seconds (baseline)

---

## API Keys

### Google Gemini (Default for Step 2)
```bash
# Get key from: https://aistudio.google.com/app/apikey
echo "GOOGLE_API_KEY=key_here" > .env
```

### OpenRouter (Alternative)
```bash
# Get key from: https://openrouter.ai/
echo "OPENROUTER_API_KEY=key_here" > .env
```

---

## Troubleshooting

### CUDA Not Working?
```bash
# See GPU_SETUP_GUIDE.md for detailed instructions
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Step 1 Fails?
```bash
# Run with verbose output
python step1_docling_hybrid_chunking.py input.pdf --verbose

# Try CPU mode if GPU error
python step1_docling_hybrid_chunking.py input.pdf --gpu-mode cpu
```

### Step 2 API Error?
```bash
# Verify .env file exists
cat .env  # Should show API key

# Test API connection
python -c "from src.llm_manager import LLMManager; LLMManager().test_connection()"
```

---

## File Structure

```
project/
├── step1_docling_hybrid_chunking.py    ← Document chunking
├── src/
│   ├── esia_extractor.py               ← DSPy fact extraction
│   ├── validator.py                    ← Quality checks
│   ├── config.py                       ← Configuration
│   ├── llm_manager.py                  ← LLM abstraction
│   └── ...
├── data/
│   ├── inputs/pdfs/                    ← Your PDF files
│   └── outputs/                        ← Generated chunks & facts
├── .env                                ← API keys (create this)
└── requirements.txt                    ← Dependencies
```

---

## Getting Help

1. **CLAUDE.md** - Architecture & detailed reference
2. **STEP1_TEST_RESULTS.md** - Test results & recommendations
3. **GPU_SETUP_GUIDE.md** - GPU acceleration setup
4. **README.md** - General documentation
5. **DSPY_INTEGRATION.md** - Step 2 details

---

## Success Checklist

- [x] Step 1 produces chunks.jsonl
- [x] Chunks have required fields (page, section, text, token_count)
- [x] Metadata JSON is valid
- [ ] GPU enabled (optional but recommended)
- [ ] .env file created with API key
- [ ] Step 2 produces facts.json
- [ ] Results validated

---

**Last Updated**: 2025-11-27
**Status**: ✅ Ready to use
