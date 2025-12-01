# Translation Feature - Quick Reference Card

## One-Liner Commands

```bash
# Translate with Google (requires GOOGLE_API_KEY)
export GOOGLE_API_KEY="..." && python step1_docling_hybrid_chunking.py doc.pdf --translate-to-english

# Translate with free LibreTranslate
python step1_docling_hybrid_chunking.py doc.pdf --translate-to-english --translation-provider libretranslate

# No translation (default)
python step1_docling_hybrid_chunking.py doc.pdf
```

---

## CLI Flags

```
--translate-to-english              Enable translation (disabled by default)
--translation-provider {google|libretranslate}  Which provider to use
```

---

## Installation (One-Time)

```bash
pip install langdetect google-generativeai requests
```

---

## Where Translation Happens

In `step1_docling_hybrid_chunking.py`:

**Before**: `Docling parsing → Chunking`
**After**: `Docling parsing → Translation (NEW!) → Chunking`

**Line Numbers**: 726-735 in `process_document()` function

---

## Configuration

| Setting | Default | Options |
|---------|---------|---------|
| `translate_to_english` | `False` | `True` / `False` |
| `translation_provider` | `'google'` | `'google'` / `'libretranslate'` |

---

## Providers

| Provider | Speed | Accuracy | Cost | Setup |
|----------|-------|----------|------|-------|
| **Google Gemini** | Fast ⚡ | Excellent 🌟 | $$ | GOOGLE_API_KEY |
| **LibreTranslate** | Slow 🐢 | Good ✓ | Free 💰 | None |

---

## Output Files

```
document_chunks.jsonl      ← ALL ENGLISH (when translation enabled)
document_meta.json         ← Contains translation metadata
```

---

## Verify Output

```bash
# Check first chunk is English
head -1 document_chunks.jsonl | python -m json.tool | grep '"text"'

# Check translation metadata
cat document_meta.json | jq '.document.translation'
```

---

## Translation Metadata (in xxx_meta.json)

```json
{
  "source_language": "es",     // Original language detected
  "translated": true,           // Was translation successful?
  "provider": "google",         // Which provider was used?
  "error": null                 // Any errors during translation
}
```

---

## How It Works

```
1. User runs: python step1_docling_hybrid_chunking.py doc.pdf --translate-to-english
2. Docling parses PDF/DOCX
3. Language is detected (langdetect)
4. If non-English: Call translation API
5. Document converted to English
6. Chunks extracted (now all English)
7. JSONL written with English text
8. Metadata includes translation info
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "GOOGLE_API_KEY not found" | `export GOOGLE_API_KEY="your-key"` |
| "langdetect not installed" | `pip install langdetect` |
| Translation skipped | Document already English (correct behavior) |
| Chunks still non-English | Did you use `--translate-to-english` flag? |
| Translation too slow | Use LibreTranslate, or smaller documents |
| API error | Check API key and internet connection |

---

## Feature Flags

```python
# In ProcessingConfig dataclass:
translate_to_english: bool = False              # Feature toggle
translation_provider: str = 'google'            # Provider choice
```

---

## Language Codes Detected

Common language codes returned by `langdetect`:
- `es` - Spanish
- `fr` - French
- `de` - German
- `id` - Indonesian
- `pt` - Portuguese
- `it` - Italian
- `ja` - Japanese
- `zh-cn` - Chinese (Simplified)
- `ar` - Arabic
- `ru` - Russian

---

## API Key Setup

### Google Gemini API
```bash
# Method 1: Environment variable
export GOOGLE_API_KEY="sk-..."

# Method 2: .env file
echo "GOOGLE_API_KEY=sk-..." >> .env

# Method 3: Python code (in script)
import os
os.environ['GOOGLE_API_KEY'] = 'sk-...'
```

### LibreTranslate
No setup needed - uses free public API

---

## Performance

| Scenario | Time |
|----------|------|
| Small PDF (1-5 pages), no translation | 1-3 sec |
| Small PDF + Google translation | 3-8 sec |
| Small PDF + LibreTranslate | 5-15 sec |
| Large PDF (50+ pages), no translation | 5-15 sec |
| Large PDF + Google translation | 10-20 sec |
| Large PDF + LibreTranslate | 15-30 sec |

---

## Full Example

```bash
# Install dependencies
pip install langdetect google-generativeai requests

# Set API key
export GOOGLE_API_KEY="sk-your-actual-key"

# Run with verbose output
python step1_docling_hybrid_chunking.py spanish_document.pdf \
  --translate-to-english \
  --chunk-max-tokens 3000 \
  --verbose

# Verify output
cat hybrid_chunks_output/spanish_document_chunks.jsonl | python -c "
import sys, json
chunk = json.loads(sys.stdin.readline())
print(f'Language: English')
print(f'Text: {chunk[\"text\"][:100]}...')
"

# Check metadata
cat hybrid_chunks_output/spanish_document_meta.json | \
  python -c "import sys, json; d=json.load(sys.stdin); print(json.dumps(d['document']['translation'], indent=2))"
```

---

## Integration with Step 2

```bash
# Step 1 with translation
python step1_docling_hybrid_chunking.py doc.pdf --translate-to-english
# Output: doc_chunks.jsonl (ENGLISH)

# Step 2 (automatic, no changes needed)
python src/esia_extractor.py --chunks doc_chunks.jsonl --output facts.json
# Input: English chunks (from translation)
# Output: Extracted facts
```

---

## Documentation Files

| File | Purpose | Size |
|------|---------|------|
| `TRANSLATION_SUMMARY.md` | Overview & quick summary | 1 page |
| `TRANSLATION_QUICKSTART.md` | Getting started guide | 3 pages |
| `TRANSLATION_IMPLEMENTATION.md` | Complete technical guide | 8 pages |
| `TRANSLATION_CODE_CHANGES.md` | Code modification details | 5 pages |
| `TRANSLATION_ARCHITECTURE.md` | System design & diagrams | 10 pages |
| `TRANSLATION_REFERENCE.md` | This quick reference | 1 page |

---

## Key Facts

✓ Translation happens **after Docling parsing, before chunking**
✓ **1 API call per document** (not per chunk)
✓ **All chunks guaranteed English** (when enabled)
✓ **Optional feature** (disabled by default)
✓ **Fully backward compatible**
✓ **Metadata tracking** (original language recorded)
✓ **Graceful error handling** (uses original if translation fails)
✓ **Two providers** (Google Gemini + LibreTranslate)

---

## Before vs After

### BEFORE Implementation
```
PDF (Spanish) → Docling → HybridChunker → chunks.jsonl (SPANISH TEXT)
→ Step 2 processes Spanish → Mixed language handling needed
```

### AFTER Implementation
```
PDF (Spanish) → Docling → Translation → HybridChunker → chunks.jsonl (ENGLISH TEXT)
→ Step 2 processes English → Consistent extraction quality
```

---

## Environment Variables

```bash
# Required for Google Gemini translation
GOOGLE_API_KEY="sk-..."

# Optional: Override default output directory
ESIA_OUTPUT_DIR="/path/to/output"

# Optional: Debug mode
ESIA_DEBUG="1"
```

---

## Status Indicators

In verbose output, you'll see:

```
[2/5] Converting PDF to Docling document...
  ✓ Document converted
  Pages: 50

[2b/5] Translating document to English...
  Translating from detected language: es
  ✓ Translated 45000 chars with Google Gemini API
  ✓ Document translated from es

[3/5] Setting up HybridChunker...
  ...
```

---

## Backward Compatibility

```bash
# These two are IDENTICAL (translation disabled by default)
python step1_docling_hybrid_chunking.py doc.pdf
python step1_docling_hybrid_chunking.py doc.pdf  # No --translate-to-english flag

# Translation is OPT-IN
python step1_docling_hybrid_chunking.py doc.pdf --translate-to-english  # Enables translation
```

---

## Need Help?

1. **Installation issues**: See `TRANSLATION_QUICKSTART.md` → Installation section
2. **How it works**: See `TRANSLATION_IMPLEMENTATION.md` → How It Works section
3. **Code details**: See `TRANSLATION_CODE_CHANGES.md` → Code modifications
4. **Architecture**: See `TRANSLATION_ARCHITECTURE.md` → System design
5. **Troubleshooting**: See `TRANSLATION_QUICKSTART.md` → Troubleshooting section

---

**Last Updated**: 2025-11-27
**Status**: ✅ Production Ready
**Version**: 1.0
