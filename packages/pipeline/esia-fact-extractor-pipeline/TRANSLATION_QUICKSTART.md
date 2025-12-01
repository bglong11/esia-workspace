# Translation Feature - Quick Start Guide

## TL;DR

The ESIA pipeline now automatically **translates non-English documents to English** before chunking. This ensures your `xxx_chunks.jsonl` output is always in English.

---

## Installation

```bash
# Install translation dependencies
pip install langdetect google-generativeai requests
```

---

## Quick Usage

### Option 1: Use Google Gemini (Recommended)

```bash
# Set your API key first
export GOOGLE_API_KEY="sk-..."

# Run with translation
python step1_docling_hybrid_chunking.py document.pdf --translate-to-english
```

### Option 2: Use LibreTranslate (Free)

```bash
# No API key needed!
python step1_docling_hybrid_chunking.py document.pdf \
  --translate-to-english \
  --translation-provider libretranslate
```

### Option 3: No Translation (Default)

```bash
# Translation disabled by default (backward compatible)
python step1_docling_hybrid_chunking.py document.pdf
```

---

## What Gets Translated?

✓ **Chunk text** - All text in JSONL chunks
✓ **Section headings** - Converted to English
✓ **Metadata** - Preserved

**Note**: Tables and images keep original language, but page numbers are preserved.

---

## Check Translation Status

After processing, check the metadata file:

```bash
# View translation metadata
cat document_meta.json | jq '.document.translation'
```

Output:
```json
{
  "source_language": "es",
  "translated": true,
  "provider": "google",
  "error": null
}
```

---

## Full Command Examples

```bash
# Spanish document → English with Google
python step1_docling_hybrid_chunking.py esia_spanish.pdf \
  --translate-to-english \
  --verbose

# Indonesian document → English with LibreTranslate
python step1_docling_hybrid_chunking.py esia_indonesian.pdf \
  --translate-to-english \
  --translation-provider libretranslate \
  --verbose

# English document (skip translation automatically)
python step1_docling_hybrid_chunking.py esia_english.pdf \
  --translate-to-english \
  --verbose
  # Translation will be skipped (already English)
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "GOOGLE_API_KEY not found" | Set `export GOOGLE_API_KEY="your-key"` |
| "langdetect not installed" | `pip install langdetect` |
| "Translation returned same text" | Document is already English |
| Translation is very slow | Document is large; try smaller chunks |
| Getting non-English output | Translation failed; check API key and error in metadata |

---

## Where Translation Happens

In `step1_docling_hybrid_chunking.py`:

1. **[2/5]** - Docling parses document
2. **[2b/5]** - Translation occurs here ← NEW
3. **[3-5/5]** - Chunking and extraction (now in English)

---

## Output Guarantee

When you run with `--translate-to-english`:

```
✓ xxx_chunks.jsonl - 100% English chunks
✓ xxx_meta.json - Includes translation metadata
✓ Your downstream pipeline - Receives only English
```

---

## Backward Compatibility

The translation feature is **disabled by default**. Your existing scripts will work unchanged:

```bash
# These two are equivalent
python step1_docling_hybrid_chunking.py document.pdf
python step1_docling_hybrid_chunking.py document.pdf  # No translation by default
```

---

## Next: Step 2

After generating English chunks, proceed normally:

```bash
python src/esia_extractor.py --chunks document_chunks.jsonl --output facts.json
```

The extractor will receive English-only chunks and work more efficiently!

---

## Provider Comparison

| Feature | Google | LibreTranslate |
|---------|--------|----------------|
| Accuracy | Excellent | Good |
| Speed | Fast | Slower |
| Cost | Possible | Free |
| Setup | API key needed | None |
| Offline | No | Yes (self-hosted) |

---

## Full CLI Options

```bash
python step1_docling_hybrid_chunking.py INPUT_FILE [OPTIONS]

Translation Options:
  --translate-to-english              Enable translation (default: disabled)
  --translation-provider {google|libretranslate}
                                     Provider to use (default: google)

Other Options:
  -o, --output-dir DIR               Output directory
  --gpu-mode {auto|cuda|cpu}        GPU mode
  --chunk-max-tokens N               Tokens per chunk
  --enable-images                    Extract images
  --disable-tables                   Disable table extraction
  --output-markdown                  Export markdown
  --verbose                          Verbose output
```

---

For detailed documentation, see: `TRANSLATION_IMPLEMENTATION.md`
