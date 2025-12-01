# Translation Feature - Architecture & Design

## Pipeline Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    ESIA Fact Extraction Pipeline                │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────┐
│   USER INPUT: PDF/DOCX Document  │
│   (Any language: ES, ID, FR...)  │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│  STEP 1: Document Processing     │
│  (step1_docling_hybrid_chunking)  │
└────────────┬─────────────────────┘
             │
             ├─▶ [1/5] GPU Converter Setup
             │
             ├─▶ [2/5] Docling Parsing (PDF/DOCX → Document Object)
             │
             ├─▶ [2b/5] 🔄 TRANSLATION (NEW!)
             │         ├─ Detect Language
             │         ├─ If non-English:
             │         │   └─ Call Translation API (Google/LibreTranslate)
             │         └─ Return: English Document + Metadata
             │
             ├─▶ [3/5] HybridChunker Setup
             │
             ├─▶ [4/5] Chunk Extraction (doc → chunks.jsonl)
             │         └─ All chunks now ENGLISH ✓
             │
             └─▶ [5/5] Table & Image Extraction
                      └─ metadata_meta.json
                         {translation: {...}}
             │
             ▼
┌──────────────────────────────────────────────────┐
│   OUTPUT: Dual Chunks (Original + English)       │
│  • xxx_chunks.jsonl (Original language)          │
│  • xxx_chunks_english.jsonl (English - use this!)│
│  • xxx_meta.json (with translation metadata)     │
└────────────┬─────────────────────────────────────┘
             │
             ▼ (Always use English version)
┌──────────────────────────────────────────────────┐
│  STEP 2: Fact Extraction (English-Only)          │
│  (step2_fact_extraction.py)                      │
│  • Auto-detects & uses English chunks            │
│  • DSPy Signatures (English-only, 40+ domains)   │
│  • Domain normalization (deterministic)          │
│  • LLM Processing (Gemini API, English context)  │
│  • Extraction Quality: Consistent & Reliable     │
└──────────────────────────────────────────────────┘
```

---

## ⚠️ CRITICAL REQUIREMENT: English-Only Input to Step 2

### Why English-Only for Fact Extraction?

Your DSPy signatures and extraction logic are designed exclusively in English:

1. **Domain Signatures**: All 40+ signatures assume English input
   ```python
   class ProjectDescriptionSignature(dspy.Signature):
       """Extract facts about PROJECT DESCRIPTION"""  # English
       project_name = dspy.OutputField(desc="...")   # English
   ```

2. **Domain Normalization**: Mapping sections to signatures requires English
   ```python
   normalize_domain_name("Project Description") → ProjectDescriptionSignature  # 100% match
   normalize_domain_name("Descripción del Proyecto") → ??? (unreliable)  # Fuzzy match
   ```

3. **LLM Consistency**: English prompts + English context = reliable extraction
   - Mixed language input degrades LLM response quality
   - Inconsistent extraction across different source languages
   - Non-deterministic results

### Architecture Decision: Language-Agnostic Pipeline

```
SOURCE DOCUMENTS (Any Language)
    ↓
[STEP 1: Translation/Chunking]  ← Handles any input language
    ├─ Detect language
    ├─ Translate if needed
    └─ Output: English chunks (guaranteed)
    ↓
[STEP 2: Fact Extraction]  ← Language-independent (English only)
    ├─ Normalize domain (English → Signature)
    ├─ Apply signatures (all in English)
    ├─ LLM processing (English prompts)
    └─ Output: Facts (consistent & reliable)
```

### Implementation in Step 2

**Auto-detection of English chunks** (`step2_fact_extraction.py`):
```python
# If you provide original chunks file, it auto-detects English version
preferred_chunks_file = get_english_chunks_if_available(args.chunks)
# Returns: chunks_english.jsonl if available, otherwise original
```

**Usage:**
```bash
# Automatic: uses English version if available
python step2_fact_extraction.py --chunks document_chunks.jsonl
# → Automatically switches to document_chunks_english.jsonl (if exists)

# Explicit: specify English version directly
python step2_fact_extraction.py --chunks document_chunks_english.jsonl

# Fallback: original chunks (only if English or no translation done)
python step2_fact_extraction.py --chunks document_chunks.jsonl
# → Uses original if English chunks don't exist
```

### Output Guarantee

**Both files have identical structure** (same page numbers, chunk IDs, sections):
- `document_chunks.jsonl` ← Original language (for reference/review)
- `document_chunks_english.jsonl` ← English (for consistent fact extraction)

**Step 2 MUST use the English version** to ensure:
- ✓ Signature matching is deterministic
- ✓ LLM extraction is consistent
- ✓ Results are reproducible
- ✓ No language-specific logic needed

---

## Translation Flow (Step 2b Detail)

```
┌─────────────────────────────────────────────────────────────────┐
│                STEP 2B: TRANSLATION SUBSYSTEM                  │
└─────────────────────────────────────────────────────────────────┘

Input: Docling Document (parsed PDF/DOCX)
       ├─ Content in original language (ES, ID, FR, etc.)
       ├─ Structure: Text blocks, tables, images
       └─ Metadata: Page numbers, headings

    │
    ▼
┌─────────────────────────────────┐
│  Is Translation Enabled?        │ ─── NO ──▶ Return doc unchanged
│  (--translate-to-english flag)  │
└────────┬────────────────────────┘
         │ YES
         ▼
┌─────────────────────────────────┐
│  Export Document as Markdown    │
│  (preserve structure, extract   │
│   all text content)             │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Detect Language                │
│  (langdetect library)           │
│  Input: First 1000 chars        │
│  Output: Language code (es, id) │
└────────┬────────────────────────┘
         │
         ├─ English detected? ──── YES ──▶ Return doc unchanged
         │ (source_lang = None)            (translation_metadata)
         │
         │ NO
         ▼
┌─────────────────────────────────┐
│  Select Translation Provider    │
│  • google (Gemini API)          │
│  • libretranslate (free API)    │
└────────┬────────────────────────┘
         │
         ├─────────────────────────────────┐
         │                                 │
         ▼ GOOGLE                         ▼ LIBRETRANSLATE
┌─────────────────────────┐      ┌─────────────────────────┐
│ Google Gemini API       │      │ LibreTranslate API      │
│ • Model: gemini-1.5-flask    │ • URL: libretranslate.de│
│ • Key: GOOGLE_API_KEY   │      │ • Free, no key needed   │
│ • Accuracy: Excellent   │      │ • Accuracy: Good        │
│ • Speed: Fast           │      │ • Speed: Slower         │
│ • Cost: Possible        │      │ • Cost: Free            │
└────────┬────────────────┘      └────────┬────────────────┘
         │                                 │
         └─────────────────┬───────────────┘
                           │
         ▼
┌─────────────────────────────────┐
│  Translation Result             │
│  Input: Markdown (original lang)│
│  Output: Markdown (English)     │
│  Status: Translated ✓           │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Return Translated Document     │
│  + Translation Metadata:        │
│    {                            │
│      source_language: "es",     │
│      translated: true,          │
│      provider: "google",        │
│      error: null                │
│    }                            │
└─────────────────────────────────┘

Output: Docling Document (now in ENGLISH) + Metadata
        ├─ Content in English
        ├─ Structure: Preserved
        ├─ Page numbers: Accurate
        └─ Metadata: Translation info included
```

---

## Translation Function Architecture

```
┌──────────────────────────────────────────────────────────────┐
│           TRANSLATION FUNCTION HIERARCHY                     │
└──────────────────────────────────────────────────────────────┘

                   translate_docling_document()
                    (Entry point for documents)
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
      detect_language()          (Extract markdown)
      (Check if needed)                   │
                 │                        │
                 │◄───────────────────────┘
                 │
                 ├─ Already English? ──► Return unchanged
                 │                       (metadata: translated=false)
                 │
                 │ Non-English detected
                 ▼
      translate_text_to_english()
      (Main translation dispatcher)
                 │
      ┌──────────┴──────────┐
      │                     │
      ▼                     ▼
_translate_with_google()  _translate_with_libretranslate()
   │                           │
   ├─ Try Google Cloud API     ├─ HTTP POST
   ├─ Fallback: Gemini API     ├─ JSON response
   ├─ API key from .env        └─ Parse translatedText
   └─ Return translated text       field
                 │                     │
                 └──────────┬──────────┘
                            │
                            ▼
                     Result: Translated text
                     + source_language code
```

---

## Data Flow: Before and After Translation

### WITHOUT Translation (Default)

```
PDF (Spanish)
    │
    ├─ Docling parsing
    │   └─ "El proyecto solar es importante..."
    │
    ├─ HybridChunker
    │   └─ chunk.text = "El proyecto solar es importante..."
    │
    └─ JSONL Output
        └─ SPANISH TEXT IN CHUNKS ✗

Step 2 receives Spanish chunks
→ DSPy signatures (designed for English) process Spanish
→ LLM API sent Spanish prompts
→ Extraction quality depends on LLM's Spanish capability
```

### WITH Translation (--translate-to-english)

```
PDF (Spanish)
    │
    ├─ Docling parsing
    │   └─ "El proyecto solar es importante..."
    │
    ├─ TRANSLATION (NEW!)
    │   ├─ Detect: Spanish (es)
    │   ├─ Call Google Gemini
    │   └─ "The solar project is important..."
    │
    ├─ HybridChunker
    │   └─ chunk.text = "The solar project is important..."
    │
    └─ JSONL Output
        └─ ENGLISH TEXT IN CHUNKS ✓
        └─ metadata: {source_language: "es", translated: true}

Step 2 receives English chunks
→ DSPy signatures (English-optimized) process English
→ LLM API sent English prompts (native capability)
→ Extraction quality: CONSISTENT & HIGH
```

---

## Decision Tree: Should Translation Happen?

```
                    User runs Step 1
                          │
                          ▼
                  --translate-to-english
                   flag present?
                    /            \
                  YES             NO
                   │               │
                   ▼               ▼
            Load language      Skip translation
            detection model    Return doc unchanged
                   │
                   ▼
            detect_language()
            (langdetect)
                   │
        ┌──────────┴──────────┐
        │                     │
      English           Non-English
        │                     │
        │                     ▼
        │              Which provider?
        │              /           \
        │          Google      LibreTranslate
        │             │             │
        │             ▼             ▼
        │        Call Gemini   Call HTTP API
        │             │             │
        └─────────────┴─────────────┘
                      │
                      ▼
              Return translated doc
              + metadata
```

---

## Error Handling Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              ERROR HANDLING STRATEGY                         │
└──────────────────────────────────────────────────────────────┘

                 translate_docling_document()
                          │
                   Try/Except block
                    /             \
            Success             Exception
              │                    │
              ▼                    ▼
          Return doc        Catch exception
          + metadata       (API error, etc.)
                               │
                               ▼
                        Log error to metadata
                        {error: "message"}
                               │
                               ▼
                        Return original doc
                        (graceful fallback)
                               │
                               ▼
                        Continue processing
                        (chunks from original)

Result: Pipeline never fails due to translation errors
        Original text used as fallback
        Errors logged for visibility
```

---

## State Machine: Document Language Journey

```
┌────────────────────────────────────────────────────┐
│        DOCUMENT STATE TRANSITIONS                 │
└────────────────────────────────────────────────────┘

           Input Document
           (Any language)
                 │
                 ▼
         ┌───────────────┐
         │ UNTRANSLATED  │ ◄────────── Fallback on error
         │ State         │
         └───────┬───────┘
                 │
                 ├─ Translation disabled?
                 │   └─▶ Stay UNTRANSLATED
                 │
                 ├─ Language = English?
                 │   └─▶ Mark as ALREADY_ENGLISH
                 │       (no translation needed)
                 │
                 └─ Language ≠ English?
                     └─▶ Attempt translation
                         │
                         ├─ Success
                         │  └─▶ TRANSLATED ✓
                         │
                         └─ Failure
                            └─▶ TRANSLATION_FAILED ✗
                                (use original, log error)

Final States:
  • ALREADY_ENGLISH: No action taken (already OK)
  • TRANSLATED: Translation successful (chunks now English)
  • TRANSLATION_FAILED: Error occurred, original used
  • UNTRANSLATED: Feature disabled, original used
```

---

## Integration Points with Rest of Pipeline

### Step 1 → Docling
```
process_document()
    ├─ GPU setup
    ├─ Docling conversion ◄─── Outputs: doc object
    └─ ────────────────────────▶ Input to translation function
```

### Docling → Translation (NEW)
```
translate_docling_document()
    ├─ Input: doc object (parsed, non-English)
    └─ ────────────────────────▶ Output: doc object (English or original)
                                        + metadata
```

### Translation → Chunking
```
extract_chunks_with_pages(doc, ...)
    ├─ Input: doc object (possibly translated)
    └─ ────────────────────────▶ Output: chunks (guaranteed English if translated)
```

### Chunking → JSONL Output
```
JSONL file (xxx_chunks.jsonl)
    ├─ English text ✓
    ├─ Metadata: translation info
    └─ ────────────────────────▶ Input to Step 2 (esia_extractor.py)
```

---

## Configuration Propagation

```
Command Line Args
    ├─ --translate-to-english ─────┐
    └─ --translation-provider     │
                                  ▼
            ProcessingConfig object
            {
              translate_to_english: bool
              translation_provider: str
            }
                                  │
                                  ▼
            process_document(config)
                                  │
                                  ├─▶ translate_docling_document(config)
                                  │   └─ Uses config.translate_to_english
                                  │   └─ Uses config.translation_provider
                                  │
                                  └─▶ extract_chunks_with_pages()
                                      └─ Processes translated doc
```

---

## Performance Characteristics

```
Pipeline Latency (in seconds)

Without Translation:
    PDF Parsing (Docling):     2-5 sec
    HybridChunking:            1-3 sec
    ─────────────────────────────────
    Total:                      3-8 sec

With Translation (Google):
    PDF Parsing (Docling):      2-5 sec
    Language Detection:         0.1 sec
    Translation API Call:       2-5 sec ◄── Variable, depends on doc size
    HybridChunking:             1-3 sec
    ─────────────────────────────────
    Total:                      5-13 sec

With Translation (LibreTranslate):
    PDF Parsing (Docling):      2-5 sec
    Language Detection:         0.1 sec
    Translation HTTP Call:      5-10 sec ◄── Slower, free API
    HybridChunking:             1-3 sec
    ─────────────────────────────────
    Total:                      8-18 sec

Memory Impact:
    • Markdown export: ~1-5MB overhead
    • Translation: In-place (minimal overhead)
    • Chunks: Same as before (not doubled)
```

---

## Security Considerations

```
┌────────────────────────────────────────────────────────────┐
│                 SECURITY ARCHITECTURE                      │
└────────────────────────────────────────────────────────────┘

1. API Keys
   • GOOGLE_API_KEY: Stored in .env or environment
   • LibreTranslate: No key needed (free)
   • Keys never logged or printed

2. Document Content
   • Sent to translation API over HTTPS
   • Document content passes through external API
   • Consider: Document sensitivity / data privacy
   • Solution: Use on-premises LibreTranslate if needed

3. Error Handling
   • Translation errors don't expose API details
   • Errors logged to metadata file only
   • Pipeline continues even if translation fails

4. Fallback
   • Original document always preserved
   • No data loss on translation failure
   • Users can retrieve original if needed
```

---

## Testing Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    TEST COVERAGE                           │
└────────────────────────────────────────────────────────────┘

Unit Tests (recommended):
    ├─ detect_language() with English
    ├─ detect_language() with Spanish
    ├─ translate_text_to_english() with Google
    ├─ translate_text_to_english() with LibreTranslate
    ├─ translate_docling_document() with translation disabled
    ├─ translate_docling_document() with already-English doc
    ├─ translate_docling_document() with non-English doc
    └─ translate_docling_document() with API error

Integration Tests:
    ├─ Full Step 1 without translation
    ├─ Full Step 1 with Google translation
    ├─ Full Step 1 with LibreTranslate translation
    ├─ Verify chunks are English
    ├─ Verify metadata has translation info
    └─ Verify Step 2 processes English chunks

End-to-End Tests:
    ├─ Spanish PDF → English chunks
    ├─ Indonesian PDF → English chunks
    └─ English PDF with translation enabled (skipped)
```

---

## Summary Diagram: The Complete System

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPLETE SYSTEM OVERVIEW                │
└─────────────────────────────────────────────────────────────┘

User Input Layer:
    • PDF/DOCX documents (any language)
    • CLI flags for translation

Processing Layer:
    [Docling] ──▶ [Translation] ──▶ [Chunking] ──▶ [Extraction]
    (Parse)      (NEW!)            (HybridChunker) (Tables/Images)

Output Layer:
    • chunks.jsonl (guaranteed English)
    • metadata.json (with translation info)

Consumption Layer:
    • Step 2: esia_extractor.py
    • Step 3: Fact validation and merging

Configuration Layer:
    • --translate-to-english flag
    • --translation-provider choice
    • GOOGLE_API_KEY environment variable

Error Handling Layer:
    • Graceful fallback to original
    • Error logging to metadata
    • Pipeline never fails

Monitoring Layer:
    • Translation metadata in output
    • Verbose logging available
    • Original language tracked
```

This architecture ensures:
✓ **Reliability**: Graceful fallback on errors
✓ **Flexibility**: Multiple providers supported
✓ **Transparency**: Translation tracked in metadata
✓ **Performance**: Single API call per document
✓ **Compatibility**: Fully backward compatible
