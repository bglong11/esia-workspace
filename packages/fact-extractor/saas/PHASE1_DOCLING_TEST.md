# Phase 1: Docling Installation & Testing

Complete guide for testing Docling before integration.

---

## 🎯 What Phase 1 Does

1. ✅ Installs Docling with CPU support
2. ✅ Tests PDF extraction
3. ✅ Tests DOCX extraction
4. ✅ Verifies markdown output quality
5. ✅ Confirms Docling is ready for integration

---

## 📋 Prerequisites

- Python 3.9 or higher
- pip package manager
- Sample PDF or DOCX file for testing

---

## 🚀 Installation Steps

### Step 1: Navigate to Backend Directory

**Linux/Mac:**
```bash
cd /path/to/esia-fact-extractor/saas/backend
```

**Windows:**
```powershell
cd M:\GitHub\esia-fact-extractor\saas\backend
```

### Step 2: Install Docling

```bash
# Install from requirements file
pip install -r requirements.txt

# Or install Docling directly
pip install docling
```

**Expected output:**
```
Collecting docling>=1.0.0
  Downloading docling-1.x.x-py3-none-any.whl
Installing collected packages: ...
Successfully installed docling-1.x.x
```

### Step 3: Verify Installation

```bash
python -c "from docling.document_converter import DocumentConverter; print('✓ Docling installed')"
```

**Expected output:**
```
✓ Docling installed
```

---

## 🧪 Running Tests

### Quick Test (No Files)

```bash
python test_docling.py
```

**Expected output:**
```
================================================================================
Phase 1: Testing Docling Installation
================================================================================

✓ Docling imported successfully
...
✓ All tests passed! Docling is ready to use.
```

---

### Test with PDF File

```bash
python test_docling.py --pdf /path/to/test.pdf
```

**Example:**
```bash
# Using the sample ESIA file (if you have it as PDF)
python test_docling.py --pdf ../../sample_esia.pdf

# Or any other PDF
python test_docling.py --pdf "C:\Users\YourName\Documents\test.pdf"
```

**Expected output:**
```
================================================================================
Phase 1: Testing Docling Installation
================================================================================

✓ Docling imported successfully

--------------------------------------------------------------------------------
Test 1: PDF Extraction
--------------------------------------------------------------------------------
Testing with: test.pdf
  Converter created...
  Converting document...
  Exporting to markdown...

✓ PDF extraction successful!
  Time: 12.45 seconds
  Characters extracted: 45,123
  Lines: 890

Preview (first 500 characters):
----------------------------------------
# Document Title

This is the extracted content from the PDF...

## Section 1
Content here...
----------------------------------------

✓ Markdown quality check passed!

================================================================================
Test Summary
================================================================================
  ✓ PASS: Docling Installation
  ✓ PASS: PDF Extraction

✓ All tests passed! Docling is ready to use.
```

---

### Test with DOCX File

```bash
python test_docling.py --docx /path/to/test.docx
```

**Example:**
```bash
python test_docling.py --docx "C:\Users\YourName\Documents\esia_report.docx"
```

---

### Test Both PDF and DOCX

```bash
python test_docling.py --pdf test.pdf --docx test.docx
```

---

### Save Extracted Text

```bash
python test_docling.py --pdf test.pdf --output extracted.md
```

This will:
1. Extract text from `test.pdf`
2. Save to `extracted.md`
3. Display results

---

## 📊 What to Look For

### Successful Test
✅ No import errors
✅ Extraction completes in <30 seconds (typical PDF)
✅ Output has >1000 characters
✅ Markdown formatting preserved (headers, paragraphs)
✅ Quality checks pass

### Potential Issues

#### Issue 1: Import Error
```
✗ Failed to import Docling: No module named 'docling'
```

**Fix:**
```bash
pip install docling
```

#### Issue 2: Slow Extraction
```
✓ PDF extraction successful!
  Time: 120.50 seconds  # Too slow!
```

**Possible causes:**
- Large PDF file (>50 pages)
- Scanned PDF requiring OCR
- Old CPU

**Fix:** This is normal for CPU mode with large files. GPU will help later.

#### Issue 3: Poor Quality Output
```
✗ Contains markdown headers: False
```

**Possible causes:**
- Scanned PDF (image-based)
- Encrypted/protected PDF
- Corrupted file

**Fix:** Try a different test file or enable OCR.

---

## 🔍 Comparing Outputs

### Test with Current System (pdfplumber)

Create a comparison script to see the difference:

```bash
# Extract with pdfplumber (current)
python -c "
import pdfplumber
with pdfplumber.open('test.pdf') as pdf:
    text = '\n\n'.join([page.extract_text() for page in pdf.pages])
    with open('pdfplumber_output.txt', 'w') as f:
        f.write(text)
print('pdfplumber output saved')
"

# Extract with Docling (new)
python test_docling.py --pdf test.pdf --output docling_output.md

# Compare
echo "=== pdfplumber ===" && head -50 pdfplumber_output.txt
echo "=== Docling ===" && head -50 docling_output.md
```

**Expected differences:**
- Docling preserves more structure (headers, tables)
- Docling outputs proper markdown
- Docling handles complex layouts better
- Docling may be slower but more accurate

---

## 📈 Performance Benchmarks

Run with different file types:

```bash
# Small PDF (10 pages)
time python test_docling.py --pdf small.pdf

# Medium PDF (50 pages)
time python test_docling.py --pdf medium.pdf

# Large PDF (100+ pages)
time python test_docling.py --pdf large.pdf
```

**Expected times (CPU mode):**
- Small (10 pages): 5-15 seconds
- Medium (50 pages): 30-60 seconds
- Large (100+ pages): 60-180 seconds

---

## ✅ Phase 1 Completion Checklist

- [ ] Docling installed successfully
- [ ] Test script runs without errors
- [ ] PDF extraction works
- [ ] DOCX extraction works (if you have DOCX file)
- [ ] Output quality is good
- [ ] Performance is acceptable for your use case

**If all checked:**
✅ Phase 1 Complete! Ready for Phase 2.

**If any issues:**
Review the troubleshooting section above.

---

## 🎯 Next Steps

Once Phase 1 tests pass:

```bash
# Say to Claude:
"implement phase 2"
```

This will:
- Update `core/extractor.py` to use Docling
- Replace `PDFProcessor` with `DocumentProcessor`
- Add DOCX support
- Keep markdown fallback

---

## 🐛 Troubleshooting

### Docling Installation Issues

**Problem:** `pip install docling` fails

**Solutions:**

1. **Update pip:**
   ```bash
   python -m pip install --upgrade pip
   pip install docling
   ```

2. **Check Python version:**
   ```bash
   python --version  # Must be 3.9+
   ```

3. **Install with verbose:**
   ```bash
   pip install docling --verbose
   ```

4. **Try specific version:**
   ```bash
   pip install docling==1.0.0
   ```

### Extraction Issues

**Problem:** PDF extraction fails

**Check:**
1. Is the PDF readable? (Try opening in PDF viewer)
2. Is it encrypted? (Password-protected)
3. Is it a scanned image? (No selectable text)

**Solutions:**
- For scanned PDFs: OCR will be needed (later feature)
- For encrypted: Remove password first
- For corrupted: Try a different file

### Performance Issues

**Problem:** Extraction takes >5 minutes

**Solutions:**
1. Accept it for development (GPU will help later)
2. Test with smaller files first
3. Check CPU usage (should be 100% during extraction)

---

## 📞 Getting Help

If you encounter issues:

1. **Check the error message** in the test output
2. **Review Docling logs** (if any)
3. **Try with a different test file**
4. **Check Docling documentation:** https://github.com/DS4SD/docling

---

## 📚 Additional Resources

- [Docling GitHub](https://github.com/DS4SD/docling)
- [Docling Documentation](https://ds4sd.github.io/docling/)
- [Python multiprocessing](https://docs.python.org/3/library/multiprocessing.html)

---

**Ready to test!** Run `python test_docling.py --pdf your_file.pdf` 🚀
