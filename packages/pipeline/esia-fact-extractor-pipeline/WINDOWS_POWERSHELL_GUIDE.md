# Windows PowerShell - How to Set API Key and Run Pipeline

## 🔑 Setting API Key in PowerShell

### Correct Command for PowerShell:
```powershell
$env:GOOGLE_API_KEY="AIzaSyB0UFeNLhNSgkDoxl3J2iMD6Yvdm70G-VY"
```

**NOT** `export` (that's for Linux/Mac)

---

## Complete Setup in PowerShell

### Step 1: Set API Key
```powershell
$env:GOOGLE_API_KEY="AIzaSyB0UFeNLhNSgkDoxl3J2iMD6Yvdm70G-VY"
```

### Step 2: Navigate to Project
```powershell
cd M:\GitHub\esia-fact-extractor-pipeline
```

### Step 3: Run Pipeline WITH Translation
```powershell
python step1_docling_hybrid_chunking.py "data/inputs/pdfs/ESIA_Report_Final_Elang AMNT.pdf" --translate-to-english --verbose
```

---

## Common Commands

### Check If API Key is Set
```powershell
$env:GOOGLE_API_KEY
```
Should show: `AIzaSyB0UFeNLhNSgkDoxl3J2iMD6Yvdm70G-VY`

### Clear API Key (if needed)
```powershell
$env:GOOGLE_API_KEY = ""
```

### Run Pipeline (Simple, No Translation)
```powershell
python step1_docling_hybrid_chunking.py "data/inputs/pdfs/ESIA_Report_Final_Elang AMNT.pdf" --verbose
```

### Run Pipeline (With Translation + Verbose)
```powershell
$env:GOOGLE_API_KEY="AIzaSyB0UFeNLhNSgkDoxl3J2iMD6Yvdm70G-VY"
python step1_docling_hybrid_chunking.py "data/inputs/pdfs/ESIA_Report_Final_Elang AMNT.pdf" --translate-to-english --verbose
```

---

## Summary: PowerShell Cheat Sheet

| Task | Windows CMD | Windows PowerShell |
|------|-------------|-------------------|
| Set API Key | `set GOOGLE_API_KEY=value` | `$env:GOOGLE_API_KEY="value"` |
| Check API Key | `echo %GOOGLE_API_KEY%` | `$env:GOOGLE_API_KEY` |
| Run Pipeline | `python script.py args` | `python script.py args` |

---

## Your Next Command (Copy & Paste Ready)

```powershell
$env:GOOGLE_API_KEY="AIzaSyB0UFeNLhNSgkDoxl3J2iMD6Yvdm70G-VY"; python step1_docling_hybrid_chunking.py "data/inputs/pdfs/ESIA_Report_Final_Elang AMNT.pdf" --translate-to-english --verbose
```

This command:
1. Sets the API key
2. Runs the pipeline with translation
3. Shows verbose progress

---

## Expected Output

```
[1/5] Creating DocumentConverter...
[2/5] Converting PDF to Docling document...
  ✓ Document converted
  Pages: 458
[3/5] Setting up HybridChunker...
[4/5] Extracting chunks to JSONL...
  ✓ Streamed 245 chunks to ESIA_Report_Final_Elang AMNT_chunks.jsonl

[POST-TRANSLATION] Translating chunks to English...
  [2.1/3] Loading original chunks...
    ✓ Loaded 245 chunks
  [2.2/3] Detecting source language...
    ✓ Detected: id
  [2.3/3] Translating 245 chunks to English...
    ✓ Successfully translated 245/245 chunks
    ✓ English JSONL: ESIA_Report_Final_Elang AMNT_chunks_english.jsonl

[5/5] Extracting tables and images...
✓ Metadata exported: ESIA_Report_Final_Elang AMNT_meta.json
✓ Original chunks: ESIA_Report_Final_Elang AMNT_chunks.jsonl
✓ English chunks: ESIA_Report_Final_Elang AMNT_chunks_english.jsonl
```

---

## Troubleshooting

### Error: "export : The term 'export' is not recognized"
**Solution**: You're in PowerShell. Use `$env:GOOGLE_API_KEY="value"` instead of `export`

### Error: "python : The term 'python' is not recognized"
**Solution**: Python not in PATH. Either:
1. Use full path: `C:\Python313\python.exe step1_docling_hybrid_chunking.py ...`
2. Or add Python to PATH in Windows settings

### Error: "File not found"
**Solution**: Check the file path is correct
```powershell
# List files to verify
dir "data/inputs/pdfs/"
```

---

## Tips

- **To run multiple commands**: Use `;` to separate them on one line
- **To go to Project Folder**: `cd M:\GitHub\esia-fact-extractor-pipeline`
- **To see help**: `python step1_docling_hybrid_chunking.py --help`
- **To check progress**: Open File Explorer and watch `hybrid_chunks_output/` folder grow

---

**Ready to run!** Copy this command and paste it into PowerShell:

```powershell
$env:GOOGLE_API_KEY="AIzaSyB0UFeNLhNSgkDoxl3J2iMD6Yvdm70G-VY"; python step1_docling_hybrid_chunking.py "data/inputs/pdfs/ESIA_Report_Final_Elang AMNT.pdf" --translate-to-english --verbose
```

Press Enter and wait for results! 🚀

