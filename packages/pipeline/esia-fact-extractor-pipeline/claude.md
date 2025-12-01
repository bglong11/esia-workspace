# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Purpose**: Multi-step ESIA (Environmental and Social Impact Assessment) document intelligence pipeline:
- **Step 1**: Convert PDF/DOCX to token-aware semantic chunks (`step1_docling_hybrid_chunking.py`)
- **Step 2**: Extract domain-specific facts from chunks using DSPy (`src/esia_extractor.py`)
- **Supporting**: Configuration, LLM management, validation, and archetype analysis

**Type**: Python multi-module project with single-file Step 1 script

**Key Technologies**: Docling, HybridChunker, DSPy, tiktoken, Gemini API, OpenRouter

## Architecture at a Glance

```
PDF/DOCX Documents
    ↓
[Step 1: Document Chunking]
    step1_docling_hybrid_chunking.py
    • DOCX → PDF conversion (temp)
    • GPU-accelerated document parsing (Docling)
    • Token-aware semantic chunking (HybridChunker)
    • Real page number extraction
    • Table/Image extraction
    Output: _chunks.jsonl, _meta.json
    ↓
[Step 2: Fact Extraction]
    src/esia_extractor.py (DSPy pipeline)
    • Load chunks from JSONL
    • Apply 40+ domain-specific extractors
    • Use LLM (Gemini, OpenRouter)
    • Generate structured facts
    Output: JSON with extracted facts
    ↓
[Quality Assurance]
    src/validator.py
    • Verify extraction completeness
    • Check fact validity
    ↓
[Domain Analysis]
    src/project_type_classifier.py
    src/archetype_merger.py
    • Classify project type
    • Merge domain-specific insights
```

## File Organization

### Core Pipeline Files

| File | Lines | Purpose |
|------|-------|---------|
| `step1_docling_hybrid_chunking.py` | 660 | Document chunking with page tracking |
| `src/esia_extractor.py` | 400+ | DSPy-based fact extraction |
| `src/config.py` | 30 | API keys and configuration |
| `src/llm_manager.py` | 150 | LLM provider abstraction (Gemini, OpenRouter) |

### Supporting Files

| File | Purpose |
|------|---------|
| `src/validator.py` | Quality checks for extracted facts |
| `src/project_type_classifier.py` | Classify ESIA project type (solar, hydro, coal, etc.) |
| `src/archetype_merger.py` | Merge insights across domain extractors |
| `src/generated_signatures.py` | 40+ DSPy Signatures for domain extraction (auto-generated) |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | User-facing documentation |
| `DSPY_INTEGRATION.md` | How chunks.jsonl/meta.json are used in DSPy |
| `claude.md` | This file |

## Key Implementation Details

### Step 1: Document Chunking (`step1_docling_hybrid_chunking.py`)

**Core Concept**: Convert messy documents into clean, token-counted chunks with precise page tracking.

**Why DOCX → PDF Conversion** (Lines 113-166):
- DOCX is XML-based with no inherent page structure
- PDF conversion enables page boundary detection
- Provides consistent input for Docling parser
- Temporary PDF cleaned up after processing

**Token-Aware Chunking** (Lines 232-280):
- Uses HybridChunker with tiktoken for exact token counts
- Default: 2,500 tokens per chunk (configurable)
- Respects semantic boundaries (sections, paragraphs)
- Optional peer merging to prevent small fragments

**Real Page Numbers** (Lines 282-330):
- Extracted from Docling's `doc_items[0].prov[0].page_no`
- Not guessed or interpolated
- Enables precise source attribution in Step 2

**Streaming Output** (Lines 515-535):
- JSONL format: one complete JSON object per line
- Memory-efficient for large documents (100+ MB)
- Each chunk is self-contained and independently valid

### Step 2: Fact Extraction (`src/esia_extractor.py`)

**Core Concept**: Use DSPy with domain-specific signatures to extract structured facts from chunks.

**Architecture**:
```python
ESIAExtractor
├── __init__: Initialize LLM provider + DSPy config
├── _configure_dspy(): Wrap LLMManager as DSPy LM
├── extract_section(): Load chunks, apply signature, extract facts
└── 40+ domain signatures (generated_signatures.py)
    ├── ProjectDescriptionSignature
    ├── EnvironmentalAndSocialImpactAssessmentSignature
    ├── MitigationAndEnhancementMeasuresSignature
    ├── SolarSpecificImpactsSignature
    └── ... (one signature per domain section)
```

**LLM Provider Abstraction** (`src/llm_manager.py`):
- Supports Gemini API (default, requires GOOGLE_API_KEY)
- Supports OpenRouter (alternative, requires OPENROUTER_API_KEY)
- Configurable temperature, max_tokens per signature
- Handles API errors gracefully

**Signature Generation** (`src/generated_signatures.py`):
- 40+ DSPy Signature classes, auto-generated from domain knowledge
- Each signature targets one ESIA section (e.g., "Solar Specific Impacts")
- Signature normalizes domain names for matching chunks by section

**Domain Normalization**:
```python
# Example: ESIAExtractor.normalize_domain_name()
"1. Project Description" → "Project Description"
"ESMP" → "Environmental And Social Management Plan Esmp"
```

### Configuration & Secrets (`src/config.py`)

**Required Environment Variables**:
```bash
GOOGLE_API_KEY=...       # For Gemini API (Step 2)
OPENROUTER_API_KEY=...   # Optional, for OpenRouter fallback
```

**Not in code**: API keys should be in `.env` file, never committed.

### Quality Assurance (`src/validator.py`)

Validates extracted facts:
- Check required fields are present
- Verify data types
- Cross-check facts against tables (optional)

### Project Type Classification (`src/project_type_classifier.py`)

Identifies project category from document text:
- Solar IPP
- Hydropower
- Coal Power
- Geothermal
- Wind
- Mining operations
- etc.

Used to select appropriate domain extractors.

## Common Development Tasks

### Running Step 1 (Document Chunking)

```bash
# Basic: Process PDF with defaults
python step1_docling_hybrid_chunking.py document.pdf

# DOCX with GPU acceleration
python step1_docling_hybrid_chunking.py document.docx --gpu-mode cuda

# Custom chunk size with image extraction
python step1_docling_hybrid_chunking.py document.pdf --chunk-max-tokens 3000 --enable-images

# CPU-only mode (debugging)
python step1_docling_hybrid_chunking.py document.pdf --gpu-mode cpu --verbose

# All output options
python step1_docling_hybrid_chunking.py document.pdf \
  -o ./output \
  --output-markdown \
  --enable-images \
  --verbose
```

**Output**:
- `document_chunks.jsonl` - Semantic chunks, one JSON per line
- `document_meta.json` - Metadata, statistics, tables
- `document.md` - (optional) Markdown version

### Windows PowerShell - Setting API Keys

**IMPORTANT**: Windows PowerShell uses different syntax than Linux/Mac. Always use `$env:` prefix:

```powershell
# Windows PowerShell (CORRECT)
$env:GOOGLE_API_KEY="your-api-key"
$env:OPENROUTER_API_KEY="your-api-key"

# NOT bash/Linux/Mac (WRONG in PowerShell)
# export GOOGLE_API_KEY="your-api-key"  ← This will NOT work in PowerShell
```

**Complete Example - PowerShell**:
```powershell
# Set API key
$env:GOOGLE_API_KEY="your-google-api-key"

# Run Step 1 with translation
python step1_docling_hybrid_chunking.py document.pdf --translate-to-english --verbose

# Or in one line
$env:GOOGLE_API_KEY="your-key"; python step1_docling_hybrid_chunking.py document.pdf --translate-to-english --verbose
```

**Verify API Key is Set**:
```powershell
$env:GOOGLE_API_KEY  # Should display your key
```

### Running Step 2 (Fact Extraction)

```bash
# Process chunks with DSPy
python src/esia_extractor.py --chunks document_chunks.jsonl --output facts.json

# With custom model
python src/esia_extractor.py --chunks document_chunks.jsonl --model gpt-4o --provider openrouter
```

**Prerequisites**:
- `document_chunks.jsonl` from Step 1
- API key in `.env` file
- `pip install -r requirements.txt`

### Testing

```bash
# Run validation on extracted facts
python src/validator.py facts.json

# Check project type classification
python src/project_type_classifier.py document_meta.json
```

### Debugging

**Step 1 Issues**:
```bash
# Verbose output to see processing details
python step1_docling_hybrid_chunking.py document.pdf --verbose

# Check if CUDA available
python -c "import torch; print(torch.cuda.is_available())"

# Test DOCX conversion standalone
python -c "from src.esia_extractor import convert_docx_to_pdf; convert_docx_to_pdf('file.docx')"
```

**Step 2 Issues**:
```bash
# Test LLM connection
python -c "from src.llm_manager import LLMManager; print(LLMManager().test_connection())"

# Run single signature test
python -c "from src.esia_extractor import ESIAExtractor; e = ESIAExtractor(); print(e.extract_section('chunks.jsonl', 'Project Description'))"
```

## Data Formats

### Chunks JSONL Format (`_chunks.jsonl`)

Each line is a complete JSON object:
```json
{
  "chunk_id": 0,
  "page": 1,
  "section": "Project Description",
  "text": "Project: Laleia Solar IPP...",
  "token_count": 2450,
  "metadata": {
    "headings": ["ESIA", "Project Description"],
    "captions": [],
    "doc_items_count": 4,
    "origin": {"filename": "...", ...}
  }
}
```

**Key Fields**:
- `chunk_id`: Sequential ID (0, 1, 2, ...)
- `page`: Exact page number from document provenance
- `section`: Top-level heading/section from document
- `text`: Semantic chunk of content (respects token limit)
- `token_count`: Exact token count using tiktoken
- `metadata.headings`: Breadcrumb of section hierarchy

### Metadata JSON Format (`_meta.json`)

```json
{
  "document": {
    "original_filename": "ESIA_2025.pdf",
    "total_pages": 77,
    "processed_at": "2025-11-26T21:01:18.450711"
  },
  "files": {
    "chunks": "ESIA_2025_chunks.jsonl",
    "format": "jsonl"
  },
  "tables": [
    {
      "table_id": 0,
      "page": 5,
      "position": "table_0_page_5",
      "content": "| Col1 | Col2 |...",
      "caption": "Table Title",
      "metadata": {"bbox": {...}}
    }
  ],
  "statistics": {
    "total_chunks": 117,
    "avg_tokens_per_chunk": 176.6,
    "total_tokens": 20664,
    "pages_with_chunks": 77
  }
}
```

**Use Cases**:
- Validate processing completed (total_chunks)
- Estimate API costs (total_tokens)
- Cross-reference facts against tables
- Find chunks by page number

## Configuration System

### Step 1 CLI Arguments

```bash
python step1_docling_hybrid_chunking.py input_file [OPTIONS]

Options:
  -o, --output-dir DIR           Output directory (default: hybrid_chunks_output)
  --gpu-mode {auto,cuda,cpu}     GPU mode (default: auto)
  --chunk-max-tokens N           Max tokens per chunk (default: 2500)
  --tokenizer-model MODEL        Tiktoken model (default: gpt-4o)
  --no-merge-peers               Disable small chunk merging
  --enable-images                Extract images with metadata
  --disable-tables               Disable table extraction
  --output-markdown              Export markdown version
  --no-json                      Disable JSON metadata output
  -v, --verbose                  Verbose output
```

### Step 2 Configuration

Set in `.env` or environment:
```bash
GOOGLE_API_KEY=...              # Required for Gemini
OPENROUTER_API_KEY=...          # Optional for OpenRouter
```

Configure LLM in `src/esia_extractor.py`:
```python
extractor = ESIAExtractor(
    model="gpt-4o",
    provider="google"  # or "openrouter"
)
```

## Error Handling & Troubleshooting

### Step 1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "CUDA requested but not available" | GPU not installed or TensorFlow not compatible | Use `--gpu-mode cpu` |
| "DOCX conversion failed" | Docling not installed | `pip install --upgrade docling docling-core` |
| "Token counting failed" | Tiktoken model mismatch | Verify `--tokenizer-model gpt-4o` |
| Out of memory | Document too large | Reduce `--chunk-max-tokens` or enable streaming |

### Step 2 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "API key not found" | .env missing or wrong path | Create `.env` with `GOOGLE_API_KEY=...` |
| "Failed to extract section" | Chunks don't match signature domain | Run with `--verbose` to see domain matching |
| "Rate limit exceeded" | API quota exhausted | Wait or switch to OpenRouter |

### Debugging Checklist

1. **Verify input file**: `file document.pdf` (ensure valid PDF/DOCX)
2. **Check dependencies**: `pip list | grep -E "docling\|torch\|dspy\|tiktoken"`
3. **Test API connection**: `python -c "from src.llm_manager import LLMManager; LLMManager().test()"`
4. **Run verbose**: Add `--verbose` to Step 1, check output for specific failures
5. **Check logs**: Look for temporary files in `tempfile.gettempdir()`

## Integration Points

### Step 1 → Step 2 Data Flow

```python
# Step 1 output
step1_docling_hybrid_chunking.py "document.pdf"
# Creates: document_chunks.jsonl, document_meta.json

# Step 2 input
esia_extractor.extract_sections("document_chunks.jsonl")
# Loads chunks line-by-line
# Matches chunk.section to domain signatures
# Extracts facts using DSPy
# Returns: facts_by_domain.json
```

### With Vector Databases

Chunks can be directly embedded:
```python
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('document_chunks.jsonl') as f:
    for line in f:
        chunk = json.loads(line)
        embedding = model.encode(chunk['text'])
        # Store: embedding + chunk['page'] + chunk['chunk_id']
```

### With External APIs

JSONL format integrates with:
- LangChain document loaders
- Pinecone/Weaviate vector stores
- OpenAI API for embeddings
- Custom RAG pipelines

## Dependencies & Requirements

```
docling>=1.0.0                        # PDF/DOCX parsing
docling-core[chunking-openai]>=1.0.0 # HybridChunker + tokenizer
tiktoken>=0.5.0                       # OpenAI token counting
torch>=2.0.0                          # GPU detection
tqdm>=4.65.0                          # Progress bars
dspy-ai                               # DSPy framework (Step 2)
google-genai                          # Gemini API
openrouter                            # OpenRouter API (optional)
python-dotenv                         # .env loading
```

Install all: `pip install -r requirements.txt`

## Code Patterns & Conventions

### Step 1 (Procedural)
- Single script with data classes and generator functions
- Uses dataclasses for structured data (DocumentChunk, TableData, ImageData)
- Generator pattern for chunk extraction (streaming, memory-efficient)
- Error handling: early exits with user-friendly messages

### Step 2 (Object-Oriented)
- Class-based design (ESIAExtractor, LLMManager)
- DSPy Signatures for declarative fact extraction
- Custom DSPy LM adapter wrapping LLMManager
- Domain normalization for flexible section matching

### Naming Conventions
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Signatures: `[Domain]Signature` (e.g., `SolarSpecificImpactsSignature`)

### Type Hints
- Used throughout both scripts
- Optional for return types
- Enables IDE autocomplete and type checking

## Performance Characteristics

### Step 1 Performance

| Document Size | Processing Time | GPU Speedup |
|---|---|---|
| 1-10 pages | < 1 sec | 1x |
| 10-100 pages | 1-10 sec | 3-5x |
| 100+ pages | 10-60 sec | 3-5x |

**Memory**: Streaming JSONL keeps peak memory constant regardless of document size.

### Step 2 Performance

| Documents | Chunks | LLM Calls | Time (Gemini) |
|---|---|---|---|
| 1 | 117 | ~40 | 30-60 sec |
| 10 | 1,170 | ~400 | 5-10 min |

**Bottleneck**: LLM API latency dominates. Batch processing with OpenRouter can reduce costs.

## File Modification Quick Reference

### Change Default Chunk Size
File: `step1_docling_hybrid_chunking.py:94`
```python
chunk_max_tokens: int = 3000  # Change from 2500
```

### Add New Domain Signature
File: `src/generated_signatures.py`
```python
class YourNewDomainSignature(dspy.Signature):
    """Extract facts about your domain"""
    context = dspy.InputField(desc="Document chunk text")
    your_field_1 = dspy.OutputField(desc="What to extract")
    your_field_2 = dspy.OutputField(desc="Another field")
```

Then add to `src/esia_extractor.py` imports and extraction logic.

### Switch LLM Provider
File: `src/esia_extractor.py:__init__`
```python
extractor = ESIAExtractor(
    model="gpt-4o",
    provider="openrouter"  # Change from "google"
)
```

### Modify Token Counting Model
File: `step1_docling_hybrid_chunking.py` CLI argument:
```bash
python step1_docling_hybrid_chunking.py doc.pdf --tokenizer-model cl100k_base
```

## Limitations & Known Issues

### Step 1
- DOCX conversion may lose formatting (acceptable for text extraction)
- Complex table formatting doesn't always convert to Markdown perfectly
- Page layout analysis quality depends on document clarity
- OCR disabled by default (enable with `--do-ocr` if needed)

### Step 2
- LLM extraction quality varies by section complexity
- No built-in hallucination detection (validate with `src/validator.py`)
- Rate limits on free tier APIs (use OpenRouter for higher quotas)
- Signature quality tied to domain knowledge in `generated_signatures.py`

## Future Enhancement Opportunities

1. **Multi-format Support**: PPTX, HTML, RTF input formats for Step 1
2. **Parallel Processing**: Process multiple documents concurrently
3. **Caching**: Cache converted PDFs for repeated DOCX processing
4. **Streaming API**: HTTP endpoint for document processing
5. **Fact Validation**: Built-in cross-checking and hallucination detection
6. **Batch Extraction**: Parallel LLM calls for faster Step 2
7. **Custom Chunking**: Pluggable chunking strategies
8. **Vector Integration**: Direct integration with embedding models
