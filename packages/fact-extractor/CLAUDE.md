# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference for Claude

**For detailed understanding of DSPy and LLM integration patterns, see `llms.txt`** - This file contains comprehensive documentation on:
- DSPy framework architecture (Signatures, Modules, Predictors)
- Language model programming concepts
- Retrieval-Augmented Generation patterns
- Best practices for composable LLM systems

The `llms.txt` file is optimized for Claude's understanding and can be referenced when working on DSPy-related enhancements.

## Project Overview

ESIA Fact Extractor is a Python-based tool that uses DSPy with OpenRouter API to automatically extract quantitative and categorical facts from Environmental and Social Impact Assessment (ESIA) documents. The system normalizes units, detects conflicts, and generates structured CSV outputs with checkpoint/resume capability. Switch between any LLM model on OpenRouter with a simple `.env` configuration change.

## Commands

### Development and Testing

```bash
# Run extraction on a document
python esia_extractor.py <input.md> <output_dir>

# Example with sample document
python esia_extractor.py sample_esia.md ./output

# Run with alternative model via step2_extract_facts.py
python step2_extract_facts.py markdown_outputs/your_test.md ./output --model anthropic/claude-haiku-4-5-20251001
```

### Dependencies

```bash
# Install required Python packages
pip install dspy-ai pandas tqdm
```

### Checkpoint Management

```bash
# Delete checkpoint to restart extraction
rm output/.checkpoint.pkl  # Linux/Mac
del output\.checkpoint.pkl  # Windows
```

## Architecture

### Core Pipeline Flow

The extraction system follows a 9-stage pipeline:

1. **LLM Configuration** - Loads OpenRouter API configuration from `.env` and configures DSPy
2. **Document Loading** - Reads markdown file
3. **Text Chunking** - Splits document into 4000-character chunks (paragraph-aware)
4. **Fact Extraction** - Uses DSPy Predict to extract facts from each chunk via OpenRouter API
5. **Clustering** - Groups facts by signature (slugified fact name)
6. **Fact Categorization** - Uses DSPy Predict with FactCategorizer to assign facts to 8 categories/32 subcategories
7. **Output Generation** - Creates DataFrames for CSV export
8. **Factsheet Generation** - Organizes categorized facts into project factsheet
9. **Checkpoint Cleanup** - Removes checkpoint file on successful completion

### Key Components

**esia_extractor.py** - Single monolithic file containing:

- **DSPy Configuration** (lines 39-96): OpenRouter API configuration for any LLM model
- **DSPy Signatures** (lines 190-278):
  - `FactExtraction`: Defines extraction input/output schema for LLM
  - `FactCategorizationSignature`: Defines categorization schema with Literal type constraints for 8 categories/32 subcategories
- **Fact Data Model** (lines 285-240): Dataclass representing extracted facts with normalization fields
- **Unit Conversions** (lines 247-355): Dictionary mapping 80+ units to canonical forms with conversion factors
- **Canonicalization** (lines 383-389): `slugify()` converts fact names to stable signature identifiers
- **Text Chunking** (lines 392-427): Splits by paragraphs, respecting max_chars boundary
- **FactExtractor Class** (lines 512-646): Main extraction logic using dspy.Predict with structured text parsing
- **FactCategorizer Class** (lines 653-810): Categorizes facts using dspy.Predict with:
  - 8 diverse few-shot examples (covers different project types)
  - **Caching mechanism** to avoid redundant LLM calls for duplicate facts (37-80% hit rate expected)
  - Cache statistics tracking (hits, misses, hit rate)
  - Error handling with graceful degradation for individual facts
  - Progress bar with tqdm for visual feedback
- **FactsheetGenerator Class** (lines 850-961): Aggregates categorized facts into project factsheet with category ordering
- **Clustering** (lines 793-806): Groups facts by signature for consolidation
- **Conflict Detection** (lines 809-843): Identifies value discrepancies (2% tolerance, detects ×10 errors)
- **Output Generation** (lines 968-1022): Creates DataFrames for CSV export (including factsheet)
- **Checkpoint System** (lines 1030-1080): Pickle-based resume capability (saves every 5 chunks)
- **Main Pipeline** (lines 1090-1290): Orchestrates 9-step workflow with progress tracking

### Data Flow

```
Input Markdown → chunk_markdown() → List[str]
                                      ↓
                      FactExtractor.extract_from_chunk() → List[Fact]
                                      ↓
                               normalize_unit() → (normalized_value, canonical_unit)
                                      ↓
                              cluster_facts() → Dict[signature, List[Fact]]
                                      ↓
                            detect_conflicts() → (has_conflict, description)
                                      ↓
                      FactCategorizer() → {category, subcategory, confidence, rationale}
                      (uses cache for duplicate facts - 37-80% hit rate)
                                      ↓
                          FactsheetGenerator() → Organized facts by category/subcategory
                                      ↓
                    generate_*_table() → DataFrame → CSV files (4 total)
```

### Output Files

1. **esia_mentions.csv** - All fact occurrences with evidence quotes and page numbers
2. **esia_consolidated.csv** - Unique facts with occurrence counts, value ranges, and conflict flags
3. **esia_replacement_plan.csv** - Regex patterns for document editing/replacement
4. **project_factsheet.csv** - Facts organized by LLM-categorized project sections (8 categories, 32 subcategories)

## Factsheet Categorization

The system uses LLM-based categorization for intelligent fact organization:

### FactCategorizationSignature
- Type-safe signature using `Literal` type constraints
- 8 primary categories: Project Overview, Project Description, Environmental Impacts, Social Impacts, Economic Impacts, Health & Safety, Governance & Management, Risks & Issues
- 32 subcategories for detailed organization
- Confidence scores (high/medium/low) for categorization certainty
- Rationale field for audit trail

### FactCategorizer Module
- Uses `dspy.Predict` for straightforward fact-to-category mapping
- 8 diverse few-shot examples covering different project types and confidence levels
- Handles both quantitative (with units) and categorical facts
- LLM-based approach handles ambiguous cases better than keyword matching
- **Caching mechanism** (NEW):
  - Cache key: (fact_name.lower(), fact_unit.lower()) - ignores value to allow variations
  - Avoids redundant LLM calls for the same fact type across multiple occurrences
  - Expected hit rate: 37-80% on typical ESIA documents (37.5% on test with 3 duplicates)
  - Statistics tracked: hits, misses, hit_rate, cache_size
  - Can significantly reduce LLM API costs and processing time for documents with repeated facts
- **Error handling** (NEW):
  - Try-except wrapper for individual fact categorization
  - Failed facts logged with error details
  - Pipeline continues even if some facts fail to categorize
  - Summary report of failed facts shown at end
- **Progress tracking** (NEW):
  - tqdm progress bar during categorization showing fact count and speed

### FactsheetGenerator Aggregator
- Groups facts by category and subcategory
- Maintains consistent category ordering in output
- Generates summary statistics (by_category, confidence_breakdown)
- Supports optional confidence filtering

## Important Patterns

### Unit Normalization

The system uses a conversion dictionary to normalize all units to canonical forms:
- Mass: All converted to `kg` (tonnes × 1000, g × 0.001)
- Area: All converted to `ha` (km² × 100, m² × 0.0001)
- Power: All converted to `MW`
- Energy: All converted to `MWh`

When adding custom units, edit `UNIT_CONVERSIONS` (lines 83-191):
```python
UNIT_CONVERSIONS = {
    'your_unit': ('canonical_unit', conversion_factor),
}
```

### Checkpoint/Resume System

- Checkpoints saved automatically every 5 chunks (configurable at line 626)
- Stored as `.checkpoint.pkl` in output directory
- Contains: `{'facts': List[Fact], 'processed_chunks': int, 'timestamp': str}`
- Auto-deleted on successful completion
- User prompted to resume or restart if checkpoint exists

### JSON Repair Logic

The LLM sometimes produces malformed JSON. The `repair_json()` method (line 295) fixes common issues:
- Missing closing quotes on field names: `{"name: → {"name":`
- Regex pattern: `r'([\{,]\s*)"([a-zA-Z_][a-zA-Z0-9_]*)\s*:' → r'\1"\2":'`

### Conflict Detection

Two-tier conflict detection (lines 397-431):
1. **Relative difference threshold** - 2% tolerance (configurable)
2. **Order-of-magnitude detection** - Flags if ratio is ~10× or ~0.1× (catches decimal point errors)

### Fact Signature Generation

Facts are clustered by signature using `slugify()` (lines 219-242):
- Unicode normalization → ASCII
- Lowercase conversion
- Remove special characters
- Replace spaces/hyphens with underscores
- Example: "Coal production (annual)" → "coal_production_annual"

## Configuration

### Adjustable Parameters

**Chunk size** (line 595):
```python
chunks = chunk_markdown(text, max_chars=4000)  # Reduce for memory constraints
```

**Checkpoint frequency** (line 626):
```python
if (i + 1) % 5 == 0:  # Change 5 to save more/less frequently
    save_checkpoint(...)
```

**Conflict tolerance** (line 397):
```python
def detect_conflicts(cluster, tolerance=0.02):  # 2% default
```

**LLM temperature** (line 39):
```python
temperature=0.2,  # Low for consistent JSON, increase for creativity
```

**Max tokens** (line 40):
```python
max_tokens=2048  # Reduce if memory constrained
```

## Error Handling

**Common issues and solutions:**

1. **"OPENROUTER_API_KEY not set"** → Add your API key to `.env` file
2. **"Connection refused"** → Check internet connection and OpenRouter API status
3. **"Model not found"** → Verify model name in `.env` or command line (e.g., `openai/gpt-4o`)
4. **JSON parsing errors** → Handled by `repair_json()` with graceful degradation
5. **Keyboard interrupt (Ctrl+C)** → Auto-saves checkpoint for resume
6. **Checkpoint corruption** → Delete `.checkpoint.pkl` and restart

## Performance Characteristics

Processing time depends on document size and selected model:
- 50 KB (~12 chunks): 1-3 minutes
- 100 KB (~25 chunks): 3-6 minutes
- 200 KB (~50 chunks): 6-15 minutes
- 500 KB (~125 chunks): 15-35 minutes

Bottleneck: OpenRouter API inference time per chunk (~5-15 seconds/chunk for fast models like gpt-4o-mini)

## Development Notes

### When modifying extraction logic:

1. Test with `sample_esia.md` first (small test document)
2. Verify JSON schema compatibility with DSPy signature
3. Check unit normalization for new unit types
4. Test checkpoint/resume after changes to data models
5. Validate conflict detection doesn't produce false positives

### When adding unit support:

1. Add to `UNIT_CONVERSIONS` dictionary (lines 83-191)
2. Use canonical unit that already exists if possible
3. Test conversion accuracy with known values
4. Document in README if adding new unit category

### DSPy-specific considerations:

- The system uses `dspy.ChainOfThought` wrapper (line 293) for reasoning
- LLM output must be valid JSON array or `{"facts": [...]}`
- Field names in `FactExtraction` signature must match expected JSON schema
- Temperature affects JSON consistency - keep low (0.2) for production
