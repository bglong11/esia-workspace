# Quick Start Guide - ESIA Fact Extractor SaaS

Get up and running in 5 minutes!

## Step 1: Prerequisites

Make sure you have:

✅ **Python 3.9+** installed
```bash
python --version
```

✅ **Ollama** installed and running
```bash
# Install Ollama first if needed
# Download from: https://ollama.ai

# Pull the required model
ollama pull qwen2.5:7b-instruct

# Start Ollama service
ollama serve
```

## Step 2: Install Dependencies

```bash
cd saas/backend
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- SQLAlchemy (database)
- pdfplumber (PDF processing)
- dspy-ai (LLM orchestration)
- pandas, uvicorn, and other utilities

## Step 3: Start the Application

### Option A: Using startup script (Recommended)

**Linux/Mac:**
```bash
cd saas
./start.sh
```

**Windows:**
```powershell
cd saas
.\start.ps1
```

### Option B: Manual start

```bash
cd saas/backend
python main.py
```

## Step 4: Open in Browser

Navigate to: **http://localhost:8000**

You should see the upload interface!

## Step 5: Upload a PDF

1. **Drag & drop** a PDF file, or click "Choose File"
2. **Wait** for processing (watch the progress bar)
3. **View** extracted facts in the interactive table

## Your First Extraction

Try with the included sample document:

```bash
# Copy sample ESIA to saas directory
cp sample_esia.md saas/sample_test.md
```

Then upload `sample_test.md` through the web interface.

## What You'll See

After processing completes, you'll see a table with:

| Column | Description |
|--------|-------------|
| **Fact Name** | The extracted fact (e.g., "Coal production annual") |
| **Value** | Normalized numeric value |
| **Unit** | Canonical unit (kg, ha, MW, etc.) |
| **Page** | Source page number |
| **Occurrences** | How many times mentioned |
| **Conflict** | ⚠️ if contradictory values found |
| **Comment/Evidence** | Source quote and your notes |
| **Actions** | Edit or delete buttons |

## Key Features to Try

### 🔍 Search Facts
Type in the search box to filter facts by name or evidence.

### ⚠️ View Conflicts Only
Check the "Show conflicts only" checkbox to see facts with contradictory values.

### ✏️ Edit a Fact
1. Click the **✏️ Edit** button
2. Modify value, unit, or add a comment
3. Click **Save Changes**

### 📥 Export to CSV
Click the **📥 Export CSV** button to download all facts as a spreadsheet.

### 🗑️ Delete Facts
Click the **🗑️** button to remove incorrect extractions.

## Common Issues

### "Connection refused" error

**Problem**: Ollama is not running

**Solution**:
```bash
ollama serve
```

### "Model not found" error

**Problem**: Qwen model not downloaded

**Solution**:
```bash
ollama pull qwen2.5:7b-instruct
```

### No facts extracted

**Problem**: PDF has no extractable text or is image-based

**Solution**:
- Ensure PDF has selectable text (not scanned image)
- Try a different PDF
- Check console for errors

### Slow processing

**Problem**: CPU-only processing is slow

**Solution**:
- Use a machine with GPU
- Reduce document size
- Be patient (15-45 seconds per chunk is normal)

## Tips for Best Results

1. **Use text-based PDFs** - Scanned PDFs need OCR first
2. **Smaller documents process faster** - Start with < 50 pages
3. **Check conflicts** - Always review facts with conflict warnings
4. **Add comments** - Document your manual corrections
5. **Export regularly** - Save your work as CSV

## Next Steps

- Read the full [README](README.md) for advanced features
- Explore the [API documentation](#api-endpoints) for integration
- Customize extraction parameters in `core/extractor.py`
- Deploy to production (see deployment guide)

## Example Workflow

```
1. Upload PDF → 2. Wait for processing → 3. Review facts
                                              ↓
4. Edit conflicts ← 5. Add comments ← 6. Filter/search
                                              ↓
7. Export CSV → 8. Use in your analysis
```

## Getting Help

- Check the [troubleshooting section](README.md#troubleshooting)
- Review backend logs in terminal
- Open browser console (F12) for frontend errors

---

**Ready to extract facts from your ESIAs!** 🚀

Navigate to http://localhost:8000 and upload your first document.
