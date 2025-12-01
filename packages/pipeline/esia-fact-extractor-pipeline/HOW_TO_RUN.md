# How to Run the Pipeline - Step by Step Guide

## Quick Start (60 seconds)

### Option 1: Without Translation (Original Language Only)
```bash
cd /m/GitHub/esia-fact-extractor-pipeline
python step1_docling_hybrid_chunking.py "path/to/your/document.pdf"
```

### Option 2: With Translation to English
```bash
cd /m/GitHub/esia-fact-extractor-pipeline
export GOOGLE_API_KEY="your-api-key-here"
python step1_docling_hybrid_chunking.py "path/to/your/document.pdf" --translate-to-english --verbose
```

---

## Detailed Instructions

### Step 1: Open Terminal
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **PowerShell**: Press `Win + R`, type `powershell`, press Enter
- **Git Bash**: Right-click → "Git Bash Here" (if installed)

### Step 2: Navigate to Project Directory
```bash
cd /m/GitHub/esia-fact-extractor-pipeline
```

Or using Windows paths:
```bash
cd M:\GitHub\esia-fact-extractor-pipeline
```

### Step 3: Check Your Input File
Make sure your PDF is in the correct location:
```bash
# Windows
dir "path\to\your\document.pdf"

# Linux/Mac
ls "path/to/your/document.pdf"
```

### Step 4: Run the Pipeline

#### Option A: Without Translation (Fastest)
```bash
python step1_docling_hybrid_chunking.py "data/inputs/pdfs/ESIA_Report_Final_Elang AMNT.pdf"
```

#### Option B: With Translation (Requires API Key)
```bash
# Set API key (choose one)

# Windows Command Prompt:
set GOOGLE_API_KEY=your-actual-api-key

# Windows PowerShell:
$env:GOOGLE_API_KEY="your-actual-api-key"

# Linux/Mac:
export GOOGLE_API_KEY="your-actual-api-key"

# Then run pipeline:
python step1_docling_hybrid_chunking.py "data/inputs/pdfs/ESIA_Report_Final_Elang AMNT.pdf" --translate-to-english --verbose
```

### Step 5: Wait for Processing
- **Phase 1** (Docling parsing): 5-20 minutes (depends on document size)
- **Phase 2** (Translation): 2-5 minutes (if enabled)
- **Total**: 10-30 minutes for typical ESIA document

---

## Command Reference

### Basic Command
```bash
python step1_docling_hybrid_chunking.py "document.pdf"
```

### With Translation
```bash
python step1_docling_hybrid_chunking.py "document.pdf" --translate-to-english
```

### With Verbose Output (See Progress)
```bash
python step1_docling_hybrid_chunking.py "document.pdf" --verbose
```

### With Translation + Verbose
```bash
python step1_docling_hybrid_chunking.py "document.pdf" --translate-to-english --verbose
```

### Custom Output Directory
```bash
python step1_docling_hybrid_chunking.py "document.pdf" --output-dir "./my_output"
```

### Custom Chunk Size
```bash
python step1_docling_hybrid_chunking.py "document.pdf" --chunk-max-tokens 3000
```

### With Images Extraction
```bash
python step1_docling_hybrid_chunking.py "document.pdf" --enable-images
```

### All Options Combined
```bash
python step1_docling_hybrid_chunking.py "document.pdf" \
  --translate-to-english \
  --verbose \
  --output-dir "./output" \
  --chunk-max-tokens 3000 \
  --enable-images
```

---

## Common File Paths

### Test Document (Provided)
```bash
"data/inputs/pdfs/ESIA_Report_Final_Elang AMNT.pdf"
```

### Your Own Documents
```bash
# If in project directory:
"data/inputs/pdfs/your_document.pdf"

# If on Desktop:
"C:\Users\YourUsername\Desktop\document.pdf"

# If on Desktop (relative):
"~/Desktop/document.pdf"

# Absolute path:
"C:\path\to\your\document.pdf"
```

---

## Expected Output

### Files Created
After running, you'll find these files in `hybrid_chunks_output/`:

**Without Translation**:
```
hybrid_chunks_output/
├── document_chunks.jsonl           ← Original chunks
├── document_meta.json              ← Metadata
└── document.md                     ← Markdown (optional)
```

**With Translation**:
```
hybrid_chunks_output/
├── document_chunks.jsonl           ← Original chunks
├── document_chunks_english.jsonl   ← English translation ✓
├── document_meta.json              ← Metadata (with translation info)
└── document.md                     ← Markdown (optional)
```

### Sample Output
```
[1/5] Creating DocumentConverter...
[2/5] Converting PDF to Docling document...
  ✓ Document converted
  Pages: 458
[3/5] Setting up HybridChunker...
[4/5] Extracting chunks to JSONL...
  ✓ Streamed 245 chunks to document_chunks.jsonl

[POST-TRANSLATION] Translating chunks to English...
  [2.1/3] Loading original chunks...
    ✓ Loaded 245 chunks
  [2.2/3] Detecting source language...
    ✓ Detected: id
  [2.3/3] Translating 245 chunks to English...
    ✓ Successfully translated 245/245 chunks
    ✓ English JSONL: document_chunks_english.jsonl

[5/5] Extracting tables and images...
✓ Metadata exported: document_meta.json
✓ Original chunks: document_chunks.jsonl
✓ English chunks: document_chunks_english.jsonl
```

---

## API Keys Setup

### Getting a Google API Key

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** (or select existing)
3. **Enable Gemini API**: Search for "Generative Language API"
4. **Create API Key**: Go to Credentials → Create Credentials → API Key
5. **Copy your key** and use it in the pipeline

### Alternative: LibreTranslate (Free, No Key)
```bash
python step1_docling_hybrid_chunking.py "document.pdf" \
  --translate-to-english \
  --translation-provider libretranslate
```

---

## Troubleshooting

### Error: "No module named 'docling'"
```bash
# Install dependencies
pip install -r requirements.txt
```

### Error: "File not found"
- Check file path is correct
- Use absolute path or relative path from project directory
- Don't forget quotes around paths with spaces

```bash
# Correct:
python step1_docling_hybrid_chunking.py "data/inputs/pdfs/ESIA_Report_Final_Elang AMNT.pdf"

# Wrong:
python step1_docling_hybrid_chunking.py data/inputs/pdfs/ESIA_Report_Final_Elang AMNT.pdf
```

### Error: "GOOGLE_API_KEY not set"
- Set the environment variable before running
- Or use LibreTranslate instead (no key needed)

### Command Takes Too Long (Stuck?)
- **This is normal!** Large documents take 10-20 minutes
- Check CPU/GPU usage in Task Manager
- Don't close the window until done

### No Output Displayed
- Use `--verbose` flag to see progress
- This is normal - Docling doesn't output much by default

---

## Monitoring Progress

### Check if Process is Running (Windows)
```bash
tasklist | find "python"
```

### Check Output Directory
```bash
dir hybrid_chunks_output
```

### Monitor File Size Growth
```bash
# Shows files being written
dir hybrid_chunks_output /s
```

---

## Next Steps After Running

### Step 2: Fact Extraction
Once you have the JSONL files, extract facts:

```bash
python step2_fact_extraction.py --chunks hybrid_chunks_output/document_chunks.jsonl
```

It will **automatically detect and use** the English version if available!

### Verify Results
```bash
# Check page numbers match
jq '.page' hybrid_chunks_output/document_chunks.jsonl | sort -u > orig_pages.txt
jq '.page' hybrid_chunks_output/document_chunks_english.jsonl | sort -u > eng_pages.txt
diff orig_pages.txt eng_pages.txt
# Should produce no output (pages are identical)
```

---

## Common Use Cases

### Use Case 1: Indonesian ESIA to English
```bash
export GOOGLE_API_KEY="your-key"
python step1_docling_hybrid_chunking.py "indonesian_esia.pdf" --translate-to-english --verbose
```

### Use Case 2: English ESIA (No Translation)
```bash
python step1_docling_hybrid_chunking.py "english_esia.pdf" --verbose
```

### Use Case 3: Spanish ESIA with LibreTranslate
```bash
python step1_docling_hybrid_chunking.py "spanish_esia.pdf" \
  --translate-to-english \
  --translation-provider libretranslate \
  --verbose
```

### Use Case 4: Large Document (Optimize)
```bash
python step1_docling_hybrid_chunking.py "large_esia_500pages.pdf" \
  --gpu-mode cuda \
  --chunk-max-tokens 3000 \
  --verbose
```

---

## Performance Tips

### Faster Processing
- Use `--gpu-mode cuda` if you have NVIDIA GPU
- Increase `--chunk-max-tokens` to 3000 (fewer chunks = faster)
- Use LibreTranslate (faster than Google)

### Better Quality
- Use smaller chunks: `--chunk-max-tokens 2000`
- Use Google translation (higher quality)
- Enable images: `--enable-images`

### Save Resources
- Run without `--verbose` (slightly faster)
- Use default GPU mode (auto-detect)

---

## Getting Help

### Check Help Text
```bash
python step1_docling_hybrid_chunking.py --help
```

### Look at Documentation
- **Quick Start**: 00_START_HERE.md
- **Quick Reference**: POST_JSONL_QUICK_REFERENCE.md
- **Full Guide**: PLAN_JSONL_POST_TRANSLATION.md
- **Troubleshooting**: DEPLOYMENT_READY.md

---

## Summary

**Simplest Command** (No Translation):
```bash
python step1_docling_hybrid_chunking.py "path/to/document.pdf"
```

**Recommended Command** (With Translation + Progress):
```bash
export GOOGLE_API_KEY="your-key"
python step1_docling_hybrid_chunking.py "path/to/document.pdf" --translate-to-english --verbose
```

**With All Options**:
```bash
python step1_docling_hybrid_chunking.py "document.pdf" \
  --translate-to-english \
  --verbose \
  --enable-images \
  --output-dir ./output
```

---

## What Happens Next?

1. ✅ **Phase 1**: Docling parses PDF and creates original JSONL
2. ✅ **Phase 2**: Translation creates English JSONL (same pages)
3. ✅ **Output**: Check `hybrid_chunks_output/` folder
4. ✅ **Step 2**: Use the JSONL files for fact extraction

**Page numbers are guaranteed to be identical in both files!** 🚀

