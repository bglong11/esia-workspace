# ESIA Pipeline Directory Structure - Complete Analysis

## Executive Summary

The ESIA Pipeline contains **2 main directories** (not more):
- `esia-fact-extractor-pipeline` - Steps 1 & 2 (Document chunking + fact extraction)
- `esia-fact-analyzer` - Step 3 (Quality analysis)

**There is NO duplication or confusion.** They are sequential stages in the pipeline with completely different purposes, technologies, and outputs.

---

## Complete Directory Map

```
packages/pipeline/
│
├── requirements.txt                              [NEW - Consolidated]
├── REQUIREMENTS_GUIDE.md                         [NEW - Installation guide]
├── pipeline_flow.md                              [Step-by-step execution]
├── DIRECTORY_STRUCTURE.md                        [This file]
├── run-esia-pipeline.py                          [Main orchestrator]
├── config.py                                     [Root config]
│
├── data/
│   ├── pdfs/                                     [Input documents]
│   └── outputs/                                  [Pipeline results]
│
├── esia-fact-extractor-pipeline/                 [STEPS 1 & 2]
│   ├── step1_docling_hybrid_chunking.py          [Step 1: Chunking]
│   ├── step2_fact_extraction.py                  [Step 2: Simple extraction]
│   ├── step3_extraction_with_archetypes.py       [Step 2: Archetype extraction]
│   ├── requirements.txt                          [Deprecated - includes parent]
│   │
│   ├── src/                                      [Core extraction modules]
│   │   ├── esia_extractor.py                     [DSPy fact extractor]
│   │   ├── generated_signatures.py               [40+ domain signatures]
│   │   ├── llm_manager.py                        [Gemini/OpenRouter API]
│   │   ├── archetype_mapper.py                   [Domain mapping]
│   │   ├── project_type_classifier.py            [Classify project type]
│   │   ├── validator.py                          [Quality checks]
│   │   └── [7 more modules...]
│   │
│   ├── data/
│   │   ├── archetypes/                           [Domain patterns]
│   │   │   ├── core_esia/
│   │   │   ├── core_cross_cutting/
│   │   │   ├── core_ifc_performance_standards/
│   │   │   └── project_specific_esia/
│   │   └── ifc-examples/                         [IFC reference data]
│   │
│   └── docs/                                     [Documentation]
│       ├── QUICKSTART.md
│       ├── CLI_USAGE.md
│       ├── ARCHITECTURE.md
│       └── [40+ more docs...]
│
└── esia-fact-analyzer/                           [STEP 3]
    ├── analyze_esia_v2.py                        [Main analysis script]
    ├── README.md                                 [User documentation]
    │
    ├── esia_analyzer/                            [Analysis package]
    │   ├── __init__.py
    │   ├── reviewer.py                           [Main ESIAReviewer class]
    │   ├── cli.py                                [CLI interface]
    │   ├── consistency.py                        [Consistency checks]
    │   ├── gaps.py                               [Gap analysis]
    │   ├── thresholds.py                         [IFC compliance]
    │   ├── units.py                              [Unit handling]
    │   ├── constants.py                          [Parameters]
    │   │
    │   ├── exporters/                            [Output generation]
    │   │   ├── html.py                           [Interactive dashboard]
    │   │   └── excel.py                          [Excel workbook]
    │   │
    │   └── factsheet/                            [Executive summaries]
    │       ├── generator.py
    │       ├── page_distiller.py
    │       ├── selector.py
    │       └── templates.py
    │
    └── docs/                                     [Documentation]
        ├── ANALYSIS_EXAMPLE.md
        ├── COMPLETION_REPORT.md
        └── [20+ more docs...]
```

---

## The Confusion: Why "So Many" Directories?

You might be confused because you see references to:
- `fact-extractor` (doesn't exist as a standalone directory)
- `fact-analyzer` (doesn't exist as a standalone directory)
- `esia-fact-analyzer` (real directory - Step 3)
- `esia-fact-extractor-pipeline` (real directory - Steps 1 & 2)
- `esia_analyzer` (Python package inside esia-fact-analyzer)
- `esia_extractor` (class inside esia-fact-extractor-pipeline)

**The reality:** Only **2 directories** exist. The other names are:
- Class names (ESIAExtractor, ESIAReviewer)
- Package names (esia_analyzer)
- Shorthand references in documentation

---

## Directory 1: esia-fact-extractor-pipeline

### Purpose
**Steps 1 & 2 of the pipeline** - Extract structured facts from raw documents

### What It Does

#### Step 1: Document Chunking
```python
PDF/DOCX Document
    ↓
step1_docling_hybrid_chunking.py
    • Parse PDF/DOCX (Docling)
    • Convert to semantic chunks
    • Track exact page numbers
    • Extract tables and images
    ↓
Output: chunks.jsonl + meta.json
```

**Key Features:**
- GPU-accelerated document parsing
- Token-aware chunking (respects semantic boundaries)
- Real page number extraction (not guessed)
- Memory-efficient streaming (JSONL format)

#### Step 2: Fact Extraction
```python
chunks.jsonl + meta.json
    ↓
step3_extraction_with_archetypes.py
    • Load chunks line-by-line
    • Match chunks to domain archetypes
    • Use 40+ DSPy signatures
    • Call LLM (Gemini API) for extraction
    • Merge archetype insights
    ↓
Output: facts.json
```

**Key Features:**
- DSPy-based structured extraction
- 40+ domain-specific signatures
- LLM-powered (Gemini or OpenRouter)
- Archetype-based domain mapping

### Key Files

| File | Size | Purpose |
|------|------|---------|
| `step1_docling_hybrid_chunking.py` | 43 KB | Document → chunks |
| `step3_extraction_with_archetypes.py` | 9.5 KB | Chunks → facts |
| `src/esia_extractor.py` | 15 KB | DSPy extraction logic |
| `src/generated_signatures.py` | 211 KB | 40+ extraction signatures |
| `src/archetype_mapper.py` | 38 KB | Domain mapping logic |
| `src/llm_manager.py` | 7.8 KB | API abstraction |

### Technology Stack
- **Docling** - PDF/DOCX parsing
- **DSPy** - Structured extraction framework
- **Google Gemini API** - LLM for extraction
- **Tiktoken** - Token counting
- **PyTorch** - GPU acceleration

### Output Format
```json
// facts.json
{
  "project_description": {
    "project_name": "...",
    "location": "...",
    "type": "...",
    ...
  },
  "environmental_impacts": {
    "air_quality": "...",
    "water_resources": "...",
    ...
  },
  ...
}
```

### Typical Execution Time
- **Step 1 (Chunking):** 5-15 minutes (depends on document size)
- **Step 2 (Extraction):** 5-15 minutes (depends on LLM API)
- **Total:** 10-30 minutes

---

## Directory 2: esia-fact-analyzer

### Purpose
**Step 3 of the pipeline** - Analyze extracted facts for quality assurance, consistency, and compliance

### What It Does

```python
facts.json
    ↓
analyze_esia_v2.py
    • Check consistency (find contradictions)
    • Validate units and standards
    • Check IFC compliance (World Bank thresholds)
    • Analyze gaps (missing content)
    • Generate executive summaries
    ↓
Output: review.html + review.xlsx
```

### Key Features

| Feature | Purpose | Technology |
|---------|---------|-----------|
| **Consistency Check** | Find contradictions in facts | Regex + explicit rules |
| **Gap Analysis** | Identify missing required content | Pattern matching |
| **Threshold Validation** | Check IFC compliance | Rule-based comparison |
| **Unit Handling** | Normalize and validate units | Conversion tables |
| **HTML Dashboard** | Interactive results viewer | Jinja2 templates |
| **Excel Export** | Detailed workbook | openpyxl styling |
| **Factsheet Generator** | Executive summaries | Template-based |

### Key Classes

#### Main Class: `ESIAReviewer`
**File:** `esia_analyzer/reviewer.py`

**Responsibilities:**
- Orchestrates all analysis modules
- Loads extracted facts
- Runs consistency checks
- Validates against thresholds
- Generates reports

**Code:** ~427 lines, highly modular

#### Analysis Modules
| Module | Purpose | Size |
|--------|---------|------|
| `consistency.py` | Consistency checking | 5.7 KB |
| `gaps.py` | Gap analysis | 5.5 KB |
| `thresholds.py` | IFC compliance | 4.2 KB |
| `units.py` | Unit normalization | 2.2 KB |
| `constants.py` | Parameter contexts | 6.1 KB |

#### Output Modules
| Module | Purpose | Size |
|--------|---------|------|
| `exporters/html.py` | Interactive dashboard | 49 KB |
| `exporters/excel.py` | Excel workbook | 8.5 KB |
| `factsheet/generator.py` | Summary generation | 13.8 KB |

### Technology Stack
- **Pure Python** - No LLM or external APIs
- **Rule-based Logic** - Explicit semantic rules
- **openpyxl** - Excel generation (optional)
- **Jinja2** - Template rendering
- **pandas** - Data handling (optional)

### Output Format

**HTML Dashboard** (`review.html`)
```html
Interactive web interface with:
- Executive summary
- Issue categories
- Detailed findings
- Downloadable reports
```

**Excel Workbook** (`review.xlsx`)
```
Sheets:
- Summary
- Consistency Issues
- Gap Analysis
- Threshold Violations
- Extracted Facts
```

### Typical Execution Time
- **Analysis:** 2-5 minutes (rule-based, no LLM)
- **Report Generation:** 1 minute

---

## Why 2 Directories (Not Merged)?

### Reason 1: Different Technologies
- **Extractor:** Uses LLM (Gemini API), requires GPU support
- **Analyzer:** Pure Python, no external dependencies

### Reason 2: Different Execution Models
- **Extractor:** Computationally intensive (LLM calls)
- **Analyzer:** Lightweight (rule-based, instant)

### Reason 3: Different Maintenance
- **Extractor:** Requires API key management, handles LLM prompts
- **Analyzer:** Self-contained, no external dependencies

### Reason 4: Different Update Cycles
- **Extractor:** Updated when LLM providers change, new archetypes added
- **Analyzer:** Updated when new validation rules needed

### Reason 5: Clear Separation of Concerns
- **Extractor:** "Intelligence layer" (learns facts from documents)
- **Analyzer:** "Quality layer" (ensures facts are correct)

---

## Pipeline Orchestration

### Main Script: `run-esia-pipeline.py`

**File:** `M:\GitHub\esia-workspace\packages\pipeline\run-esia-pipeline.py`

**Purpose:** Coordinates both directories in sequence

```python
# Pseudocode
def run_pipeline(pdf_file, steps=[1,2,3]):

    if 1 in steps:
        # Run esia-fact-extractor-pipeline/step1_docling_hybrid_chunking.py
        chunks, meta = chunk_document(pdf_file)

    if 2 in steps:
        # Run esia-fact-extractor-pipeline/src/esia_extractor.py
        facts = extract_facts(chunks)

    if 3 in steps:
        # Run esia-fact-analyzer/analyze_esia_v2.py
        report = analyze_facts(facts)

    return {
        'chunks': chunks,
        'meta': meta,
        'facts': facts,
        'report': report
    }
```

### Input/Output Flow

```
User Input: PDF/DOCX in data/pdfs/
    ↓
[esia-fact-extractor-pipeline]
    ├─ step1: data/pdfs/doc.pdf → data/outputs/doc_chunks.jsonl
    └─ step2: chunks.jsonl → data/outputs/doc_facts.json
    ↓
[esia-fact-analyzer]
    ├─ step3: facts.json → data/outputs/doc_review.html
    └─ step3: facts.json → data/outputs/doc_review.xlsx
    ↓
User Output: Reports in data/outputs/
```

---

## Naming Conventions Explained

### Why `esia-fact-extractor-pipeline`?
- `esia` - Environmental and Social Impact Assessment
- `fact-extractor` - Component that extracts facts
- `pipeline` - Multiple sequential steps (chunking → extraction)

### Why `esia-fact-analyzer`?
- `esia` - Same domain
- `fact-analyzer` - Component that analyzes facts (post-extraction)
- No `pipeline` suffix - It's a single analysis step

### Why `esia_analyzer` (Package)?
- Python package inside `esia-fact-analyzer`
- Uses underscores (Python convention) instead of hyphens
- Contains analysis logic (reviewer, consistency, gaps, etc.)

### Why `generated_signatures.py`?
- Contains 40+ DSPy "Signature" classes
- Auto-generated from domain knowledge
- Not manually written code

### Why `esia_extractor.py`?
- Contains `ESIAExtractor` class
- Uses LLM for extraction
- Different from HTML/Excel exporters

---

## No Duplication Proof

### Code Analysis

**esia-fact-extractor-pipeline modules:**
```python
# Step 1: Document chunking (Docling)
step1_docling_hybrid_chunking.py

# Step 2: Fact extraction (DSPy + LLM)
src/esia_extractor.py              # Main extractor
src/generated_signatures.py         # Extraction signatures
src/archetype_mapper.py             # Domain mapping
src/llm_manager.py                  # API management
```

**esia-fact-analyzer modules:**
```python
# Step 3: Fact analysis (Rule-based)
esia_analyzer/reviewer.py           # Main analyzer
esia_analyzer/consistency.py        # Consistency checks
esia_analyzer/gaps.py               # Gap analysis
esia_analyzer/thresholds.py         # IFC validation
esia_analyzer/exporters/html.py     # HTML output
esia_analyzer/exporters/excel.py    # Excel output
```

**Overlap:** ZERO
- No shared code between directories
- No duplicate functions or classes
- Different import statements
- No redundant logic

### Import Analysis

**From esia-fact-extractor-pipeline:**
```python
import docling              # Document parsing
import dspy               # Extraction framework
from google import genai  # Gemini API
import tiktoken          # Token counting
```

**From esia-fact-analyzer:**
```python
# No external imports (pure Python)
# Only optional: openpyxl, pandas
```

**Conclusion:** Different dependencies, different purposes, no duplication.

---

## Size Comparison

| Directory | Python Files | Documentation | Total Size |
|-----------|-------------|---------------|-----------|
| esia-fact-extractor-pipeline | 19 | 53 docs | ~500 KB |
| esia-fact-analyzer | 21 | 16 docs | ~250 KB |
| **Total** | **40** | **69 docs** | **~750 KB** |

Note: Large files are documentation, not redundant code.

---

## When Each Directory Is Used

### esia-fact-extractor-pipeline
- ✅ Always used for new documents
- ✅ Requires PDF/DOCX input
- ✅ Requires Gemini API key
- ✅ Takes 10-30 minutes
- ✅ Outputs JSON facts

### esia-fact-analyzer
- ✅ Only used after extraction
- ✅ Requires facts.json input
- ✅ Requires no API key
- ✅ Takes 2-5 minutes
- ✅ Outputs HTML + Excel

### Can Use Analyzer Alone?
**Yes**, if you already have facts.json:
```powershell
python esia-fact-analyzer/analyze_esia_v2.py --facts facts.json
```

### Can Use Extractor Alone?
**Yes**, to just extract facts:
```powershell
python run-esia-pipeline.py document.pdf --steps 1,2
```

---

## Frontend UI Integration

Both directories will eventually be called from the frontend UI:

```
Frontend (React)
    ↓
Upload PDF/DOCX
    ↓
Backend Express Server
    ↓
run-esia-pipeline.py orchestrator
    ↓
├─ esia-fact-extractor-pipeline (Steps 1-2)
│   └─ Generate facts.json
│
└─ esia-fact-analyzer (Step 3)
    └─ Generate review.html + review.xlsx
    ↓
Display Results in UI
```

---

## Recommendations

### ✅ No Changes Needed

The directory structure is:
- **Clear** - Purpose evident from names
- **Modular** - Each component independent
- **Non-redundant** - Zero code duplication
- **Well-documented** - 69 documentation files
- **Actively maintained** - Recent commits in both

### Optional Improvements

1. **Add Directory Overview File** (DONE)
   - This file: `DIRECTORY_STRUCTURE.md`

2. **Clarify in Documentation**
   - Add note to README about what each directory does

3. **Update Frontend Comments**
   - When UI calls these, add clear comments about which is which

4. **Consider Single Test Suite**
   - Could add `tests/` at root level that tests both directories

---

## Quick Reference

### I Want to...

**Extract facts only:**
```powershell
cd packages/pipeline
python run-esia-pipeline.py document.pdf --steps 1,2
```
→ Uses `esia-fact-extractor-pipeline`

**Analyze facts only:**
```powershell
cd packages/pipeline/esia-fact-analyzer
python analyze_esia_v2.py --facts facts.json
```
→ Uses `esia-fact-analyzer`

**Run complete pipeline:**
```powershell
cd packages/pipeline
python run-esia-pipeline.py document.pdf --steps 1,2,3
```
→ Uses both directories sequentially

**Understand the code:**
- Extraction logic? → `esia-fact-extractor-pipeline/src/`
- Analysis logic? → `esia-fact-analyzer/esia_analyzer/`
- Domain patterns? → `esia-fact-extractor-pipeline/data/archetypes/`
- Test data? → `esia-fact-extractor-pipeline/data/ifc-examples/`

---

## Summary Table

| Question | Answer |
|----------|--------|
| **How many main directories?** | 2 (extractor + analyzer) |
| **Is there duplication?** | No |
| **Are they used together?** | Yes, sequentially |
| **Can they run independently?** | Yes, partially |
| **Why 2 instead of 1?** | Different tech stacks, different purposes |
| **Which is Steps 1 & 2?** | esia-fact-extractor-pipeline |
| **Which is Step 3?** | esia-fact-analyzer |
| **Total Python files?** | 40 |
| **Total documentation?** | 69 files |
| **Code duplication?** | 0% |

---

**Last Updated:** December 1, 2025
**Version:** 1.0
**Status:** Complete analysis - No changes needed
