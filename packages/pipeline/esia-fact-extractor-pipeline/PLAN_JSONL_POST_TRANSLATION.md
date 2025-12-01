# Implementation Plan: Post-JSONL Translation for Absolute Page Number Certainty

## Overview

**User Requirement**: "you MUST translate after the conversion i.e. translate the jsonl file BECAUSE PAGE NUMBERS MAY BE AFFECTED AND PAGE NUMBER PROVENENCE IS CRITICAL. THIS CAN ONLY BE ENSURED IF THE TRANSALATION IS DONE AFTER THE DOCLING CONVERSION."

**Goal**: Refactor translation logic to happen AFTER the original JSONL file is completely written, providing absolute certainty that page numbers from Docling provenance are preserved.

**Deliverables**:
- ✅ Original JSONL file (document_chunks.jsonl) - no translation
- ✅ English JSONL file (document_chunks_english.jsonl) - translated from original JSONL
- ✅ Same page numbers in both files (guaranteed by post-JSONL translation)
- ✅ Same chunk structure and metadata (only text field differs)

---

## Current State Analysis

### Current Implementation (Lines 754-833 of step1_docling_hybrid_chunking.py)

**Approach**: Streaming translation during chunk extraction
- Opens both original and English JSONL files simultaneously
- Writes to both files during the chunk streaming loop
- Translation happens for each chunk as it's being extracted

**Page Number Preservation**: ✅ Currently works correctly because:
1. Docling conversion is complete (lines 713-724)
2. Page numbers extracted from provenance metadata BEFORE translation (lines 510-517)
3. Page numbers stored in chunk.page field (independent of text content)
4. Translation modifies only the text field (lines 793-807)
5. Both JSONL files have identical page numbers

**Why User Wants Change**:
"THIS CAN ONLY BE ENSURED IF THE TRANSALATION IS DONE AFTER THE DOCLING CONVERSION"

The user wants MAXIMUM CERTAINTY by having translation happen on the complete, final JSONL file. This provides:
- Clear temporal separation of concerns (no simultaneous dual writes)
- Absolute guarantee that original JSONL is complete before translation touches it
- Easier to verify page number preservation (compare both files after both phases complete)
- Simpler debugging if page numbers ever become an issue

---

## Proposed Architecture

### Phase Separation

```
PDF/DOCX Document
    ↓
[PHASE 1: Document Parsing & Chunking]
    ├─ Docling conversion (complete document)
    ├─ HybridChunker extraction (semantic chunks)
    ├─ Page number extraction from provenance
    └─ Output: ORIGINAL JSONL ONLY
       ✓ document_chunks.jsonl (complete, 100% original)
    ↓
[PHASE 2: Translation (Optional)]
    ├─ IF --translate-to-english flag set:
    │  ├─ Read original JSONL file (complete)
    │  ├─ Detect language (from first chunk)
    │  ├─ Translate each chunk's text
    │  ├─ Preserve all metadata and page numbers
    │  └─ Write: ENGLISH JSONL
    │     ✓ document_chunks_english.jsonl (translated, same structure/pages)
    └─ IF NOT set: Skip Phase 2 (no English file created)
    ↓
[Output]
├─ document_chunks.jsonl (original language, original pages)
├─ document_chunks_english.jsonl (English text, SAME pages)
└─ document_meta.json (metadata including translation status)
```

**Key Difference from Current**:
- Current: Simultaneous dual writes during streaming (lines 754-833)
- Proposed: Sequential phases (original JSONL first, then optional English translation)

---

## Implementation Approach

### Step 1: Refactor process_document() Function

**Current Flow (Lines 754-843)**:
```python
# Open both files
if config.translate_to_english:
    f_english = open(...)

with open(jsonl_path, 'w') as f:
    for chunk in chunk_gen:
        # Write original
        f.write(json.dumps(chunk_original) + '\n')

        # Translate and write English
        if f_english:
            translated_chunk = translate(chunk)
            f_english.write(json.dumps(translated_chunk) + '\n')
```

**Proposed Flow**:
```python
# PHASE 1: Write original JSONL only (lines 754-???)
with open(jsonl_path, 'w') as f:
    for chunk in chunk_gen:
        # NO translation here
        f.write(json.dumps(chunk_original) + '\n')

# PHASE 2: Post-JSONL translation (new function, called after Phase 1)
if config.translate_to_english:
    translate_jsonl_to_english(jsonl_path, output_dir, config)
```

### Step 2: Create New Function - translate_jsonl_to_english()

**Location**: Lines 844+ in step1_docling_hybrid_chunking.py (after process_document returns)

**Function Signature**:
```python
def translate_jsonl_to_english(
    original_jsonl_path: Path,
    output_dir: Path,
    config: ProcessingConfig,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Translate a complete JSONL chunks file from original language to English.

    This function:
    1. Reads the original JSONL file (completely written)
    2. Detects language from first chunk
    3. Translates text field of each chunk
    4. Preserves all other fields (page, section, metadata, etc.)
    5. Writes English JSONL file with identical structure

    Args:
        original_jsonl_path: Path to original chunks JSONL file
        output_dir: Directory for output files
        config: ProcessingConfig with translation_provider setting
        verbose: Print progress messages

    Returns:
        Translation metadata dict with source_language, provider, error status
    """

    translation_metadata = {
        'source_language': None,
        'translated': False,
        'provider': config.translation_provider,
        'error': None,
        'chunks_translated': 0
    }

    # Derive English JSONL path from original
    english_jsonl_path = Path(str(original_jsonl_path).replace('_chunks.jsonl', '_chunks_english.jsonl'))

    if verbose:
        print(f"\n[POST] Translating chunks to English...")
        print(f"  Input:  {original_jsonl_path.name}")
        print(f"  Output: {english_jsonl_path.name}")

    try:
        chunks = []

        # PHASE 2.1: Read original JSONL into memory
        if verbose:
            print(f"  [2.1/3] Loading original chunks...")

        with open(original_jsonl_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f):
                try:
                    chunk_dict = json.loads(line.strip())
                    chunks.append(chunk_dict)
                except json.JSONDecodeError as e:
                    if verbose:
                        print(f"    ⚠ Skipping malformed chunk at line {line_num}: {e}")
                    continue

        if verbose:
            print(f"    ✓ Loaded {len(chunks)} chunks")

        # PHASE 2.2: Detect language from first chunk
        if verbose:
            print(f"  [2.2/3] Detecting language...")

        if chunks:
            first_chunk_text = chunks[0].get('text', '')
            source_lang = detect_language(first_chunk_text)
            translation_metadata['source_language'] = source_lang

            if verbose and source_lang:
                print(f"    ✓ Detected: {source_lang}")
            elif verbose:
                print(f"    ⚠ Could not detect language, skipping translation")
                return translation_metadata
        else:
            if verbose:
                print(f"    ⚠ No chunks found, skipping translation")
            return translation_metadata

        # PHASE 2.3: Translate chunks and write English JSONL
        if verbose:
            print(f"  [2.3/3] Translating and writing English JSONL...")

        with open(english_jsonl_path, 'w', encoding='utf-8') as f_english:
            for chunk_idx, chunk_dict in enumerate(chunks):
                try:
                    # Translate text field only
                    original_text = chunk_dict.get('text', '')

                    translated_text, _ = translate_text_to_english(
                        original_text,
                        provider=config.translation_provider,
                        verbose=False  # Don't log each chunk
                    )

                    # Create translated chunk with same structure
                    chunk_translated = {
                        **chunk_dict,  # Keep all original fields
                        'text': translated_text  # Only replace text field
                    }

                    # Write to English JSONL (preserve order, structure, metadata)
                    f_english.write(json.dumps(chunk_translated, ensure_ascii=False) + '\n')

                    translation_metadata['chunks_translated'] += 1

                    if verbose and chunk_idx == 0:
                        print(f"    ✓ Translating chunks (0/{len(chunks)})")

                except Exception as e:
                    if verbose:
                        print(f"    ⚠ Translation failed for chunk {chunk_idx}: {e}")
                    translation_metadata['error'] = str(e)
                    # Continue with remaining chunks

        translation_metadata['translated'] = True

        if verbose:
            print(f"    ✓ Translated {translation_metadata['chunks_translated']} chunks")
            print(f"    ✓ English JSONL: {english_jsonl_path.name}")

    except Exception as e:
        translation_metadata['error'] = f"Post-JSONL translation failed: {str(e)}"
        if verbose:
            print(f"    ✗ Error: {translation_metadata['error']}")

    return translation_metadata
```

### Step 3: Modify process_document() - Remove Streaming Translation

**Lines to Modify**: 754-833 (streaming translation during chunk extraction)

**Changes**:
1. Remove opening of English JSONL file (lines 758-760)
2. Remove chunk translation logic (lines 776-820)
3. Write ONLY original chunks to original JSONL
4. Remove closing of English JSONL file (lines 830-833)
5. Keep all chunk extraction logic unchanged

**Simplified Pseudo-code**:
```python
try:
    # ONLY open original JSONL
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        chunk_gen = extract_chunks_with_pages(doc, chunker, tokenizer, config.verbose)

        for chunk in chunk_gen:
            # Create chunk with original text only
            chunk_original = DocumentChunk(
                chunk_id=chunk.chunk_id,
                page=chunk.page,
                section=chunk.section,
                text=chunk.text,  # Original text
                token_count=chunk.token_count,
                metadata=chunk.metadata
            )

            # Write to original JSONL ONLY
            f.write(json.dumps(chunk_original.to_dict(), ensure_ascii=False) + '\n')

            # Update stats
            chunk_stats['count'] += 1
            chunk_stats['total_tokens'] += chunk_original.token_count
            # ...

    if config.verbose:
        print(f"  ✓ Streamed {chunk_stats['count']} chunks to {jsonl_path.name}")

except Exception as e:
    print(f"✗ Error streaming chunks: {e}")
    sys.exit(1)

# PHASE 2: Post-JSONL Translation (NEW - after original JSONL is complete)
if config.translate_to_english:
    translation_metadata = translate_jsonl_to_english(
        jsonl_path,
        output_dir,
        config,
        verbose=config.verbose
    )
else:
    translation_metadata = {
        'source_language': None,
        'translated': False,
        'provider': None,
        'error': None
    }
```

### Step 4: Update process_document() Return Value

**Current Return** (line ~880): Returns metadata dict with translation metadata nested

**New Return**: Same structure, but translation_metadata now comes from Phase 2 function (lines 854+)

---

## Files to Modify

### 1. step1_docling_hybrid_chunking.py

**Changes Summary**:

| Section | Lines | Change | Purpose |
|---------|-------|--------|---------|
| New Function | 844-950 | Add `translate_jsonl_to_english()` | Post-JSONL translation logic |
| process_document() | 758-833 | Simplify/remove streaming translation | Only write original JSONL |
| process_document() | 833-840 | Add Phase 2 call | Call translate_jsonl_to_english() |
| Imports | Top | No changes needed | Use existing translation functions |
| Config | 103-105 | No changes needed | Existing config already has translate_to_english |

**Code Locations**:

- **Remove** (lines 758-760): English file opening
  ```python
  if config.translate_to_english:
      jsonl_english_path = output_dir / f"{pdf_path.stem}_chunks_english.jsonl"
      f_english = open(jsonl_english_path, 'w', encoding='utf-8')
  ```

- **Simplify** (lines 776-820): Remove all translation logic from streaming loop
  - Keep only original chunk creation (lines 767-774)
  - Remove translation detection/translation (lines 776-813)

- **Remove** (lines 830-833): English file closing
  ```python
  if f_english:
      f_english.close()
      if config.verbose:
          print(f"  ✓ Translated chunks: {jsonl_english_path.name}")
  ```

- **Add** (after line 843, after streaming loop completes): Call Phase 2
  ```python
  # PHASE 2: Post-JSONL Translation
  if config.translate_to_english:
      translation_metadata = translate_jsonl_to_english(
          jsonl_path,
          output_dir,
          config,
          verbose=config.verbose
      )
  ```

---

## Benefits of This Approach

### 1. Absolute Page Number Certainty ✅
- Original JSONL written FIRST (100% complete before any translation)
- Translation reads from complete file
- Page numbers from Docling provenance never touched
- Clear separation of concerns

### 2. Verifiable Quality ✅
- Can validate original JSONL before translation
- Can compare both files to verify identical pages/structure
- Easier to debug if page numbers ever differ

### 3. Clearer Code Flow ✅
- No simultaneous dual file writes
- Two distinct phases: Parsing, then (optionally) Translation
- Easier to understand and maintain

### 4. Better Error Handling ✅
- If original JSONL fails → stop before translation attempt
- If translation fails → original JSONL already safe
- Independent error recovery for each phase

### 5. Backward Compatible ✅
- No translation flag required → works as before (Phase 1 only)
- With flag → Phase 1 + Phase 2 (no breaking changes)
- All CLI arguments unchanged

### 6. Performance ✅
- Phase 1 (chunking): Unchanged performance
- Phase 2 (translation): Same speed as current streaming approach
- Total time identical to current implementation

---

## Implementation Steps

### Step 1: Add translate_jsonl_to_english() Function
- Add new function after process_document() completes
- Lines 844-950 (approx 100 lines)
- Implements 3-phase logic: load → detect → translate

### Step 2: Simplify process_document() Streaming Loop
- Remove lines 758-760 (English file opening)
- Remove lines 776-820 (streaming translation logic)
- Simplify to write original chunks only
- Keep all chunking logic unchanged

### Step 3: Call Phase 2 After Original JSONL Complete
- After line 843, add conditional call to translate_jsonl_to_english()
- Passes jsonl_path, output_dir, config
- Captures translation_metadata for output summary

### Step 4: Update process_document() Summary Output
- Show Phase 1 completion: "✓ Original JSONL: document_chunks.jsonl"
- Show Phase 2 completion: "✓ English JSONL: document_chunks_english.jsonl" (if enabled)
- Keep existing summary structure

### Step 5: Test and Verify
- Test with non-English ESIA (verify both JSONL files created)
- Test with English ESIA (verify no English file created if not flagged)
- Verify page numbers identical in both files
- Verify chunk structure identical (only text differs)

---

## Verification Checklist

After implementation, verify:

- [ ] Original JSONL created (Phase 1)
- [ ] English JSONL created only if `--translate-to-english` flag used (Phase 2)
- [ ] Both files have same chunk count
- [ ] Both files have same page numbers (jq '.page' comparison)
- [ ] Both files have same structure/metadata
- [ ] Only text field differs between files
- [ ] Page numbers from Docling provenance preserved
- [ ] Backward compatible (works without translation flag)
- [ ] No breaking changes to existing workflows
- [ ] CLI help text still accurate

---

## Timeline & Dependencies

**No External Dependencies**: Uses existing functions:
- `detect_language()` - already exists (line 282)
- `translate_text_to_english()` - already exists (line 319)
- JSON reading/writing - standard library

**Estimated Changes**: ~150 lines total
- New function: ~100 lines
- Modified function: ~20 lines
- Function calls: ~5 lines
- Comments/docstrings: ~25 lines

**No Database Changes**: Works with existing JSONL format

---

## Documentation Updates

### Files to Update:
1. **TRANSLATION_ARCHITECTURE.md** - Update architecture diagram to show two phases
2. **TRANSLATION_IMPLEMENTATION.md** - Update with new post-JSONL translation flow
3. **README.md** - Clarify that English JSONL is created after original JSONL

### New Documentation (Optional):
- **TRANSLATION_PHASES.md** - Detailed explanation of two-phase translation

---

## Summary

**Goal**: Refactor translation to happen AFTER original JSONL is complete

**Why**: Provides absolute certainty that page numbers from Docling provenance are preserved

**How**:
1. Phase 1: Extract chunks, write original JSONL (no translation)
2. Phase 2: Read original JSONL, translate, write English JSONL

**Benefit**: Clear separation of concerns, easier to verify, absolute page number certainty

**Impact**: ~150 lines of code changes, fully backward compatible, no breaking changes

---

## Ready for User Approval

This plan provides:
✅ Detailed architecture changes
✅ Step-by-step implementation approach
✅ Exact code locations to modify
✅ New function specifications
✅ Verification procedures
✅ Benefits analysis

**Status**: Ready for user instruction to proceed with implementation.
