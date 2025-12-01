# Complete Pipeline: PDF → Markdown → Facts → Factsheet

This document describes the complete end-to-end pipeline from PDF document to categorized factsheet output.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    COMPLETE ESIA EXTRACTION PIPELINE                │
└─────────────────────────────────────────────────────────────────────┘

INPUT DOCUMENTS (PDF, DOCX, Markdown)
         ↓
    [DOCLING]
    PDF/DOCX → Markdown conversion
         ↓
    [TEXT CHUNKING]
    Split markdown into 4000-char chunks
         ↓
    [FACT EXTRACTION - DSPy]
    LLM extracts quantitative + categorical facts
         ↓
    [CLUSTERING]
    Group facts by signature (slugified names)
         ↓
    [CONFLICT DETECTION]
    Identify inconsistencies in fact values
         ↓
    [FACT CATEGORIZATION - DSPy] ← NEW
    LLM assigns facts to categories using Literal types
         ↓
    [FACTSHEET GENERATION] ← NEW
    Organize facts by category/subcategory
         ↓
OUTPUT CSV FILES (4 total)
├── esia_mentions.csv (all occurrences)
├── esia_consolidated.csv (unique facts)
├── esia_replacement_plan.csv (editing patterns)
└── project_factsheet.csv ← NEW (categorized facts)
```

---

## Stage-by-Stage Breakdown

### Stage 1: Document Input & Docling Conversion

**Input**: PDF, DOCX, or Markdown file
**Tool**: Docling (DocumentProcessor)
**Output**: Markdown string

```python
# Docling converts any document format to markdown
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("document.pdf")
markdown_text = result.document.export_to_markdown()
```

**What Docling Does**:
- Extracts text from PDF or DOCX files
- Preserves document structure (headings, lists, tables)
- Converts to clean markdown format
- Output saved to `saas/backend/docling_output/` for inspection

**Performance**: ~30-60 seconds per 100-page document

---

### Stage 2: Text Chunking

**Input**: Raw markdown string
**Tool**: `chunk_markdown()` function
**Output**: List of text chunks

```
Configuration:
- Chunk size: 4000 characters
- Strategy: Paragraph-aware (splits at paragraph boundaries)
- Max chunks for 100KB ESIA: ~25 chunks
```

**Why Chunking?**
- LLMs have context limits
- Smaller chunks = better extraction focus
- Enables progress tracking and checkpointing

**Example**:
```
Original: 99,276 characters
Split into: 25 chunks of ~4000 chars each
```

---

### Stage 3: Fact Extraction (DSPy Predict)

**Input**: Single text chunk (4000 chars)
**Tool**: FactExtractor (dspy.Predict)
**Output**: List of extracted facts

```python
class FactExtractor(dspy.Module):
    def __init__(self):
        self.extract = dspy.Predict(FactExtractionSignature)
        self._add_examples()  # 8 diverse examples

    def forward(self, text: str):
        result = self.extract(text=text)
        return parse_structured_output(result.output)
```

**What It Extracts**:
- **Quantitative facts**: Value + unit (e.g., "500 MW", "1200 hectares")
- **Categorical facts**: Classifications (e.g., "coal-fired", "open-pit mining")

**Fact Structure**:
```
FACT: Project area
TYPE: quantity
VALUE: 500
VALUE_NUM: 500
UNIT: hectares
EVIDENCE: The project will cover an area of 500 hectares
---
```

**Facts Extracted Per Chunk**: 3-5 facts average
**Total for 100KB ESIA**: ~100-150 facts

---

### Stage 4: Clustering

**Input**: All extracted facts (with duplicates)
**Tool**: `cluster_facts()` function
**Output**: Dictionary mapping signature → List[facts]

```python
# Cluster facts by signature
clusters = defaultdict(list)
for fact in all_facts:
    signature = slugify(fact.name)  # "Coal production (annual)" → "coal_production_annual"
    clusters[signature].append(fact)
```

**Why Clustering?**
- Same fact mentioned multiple times gets one row in output
- Detects duplicate mentions
- Enables occurrence counting

**Result**: ~100-150 facts → ~100-107 unique signatures

---

### Stage 5: Conflict Detection

**Input**: Clusters of facts
**Tool**: `detect_conflicts()` function
**Output**: (has_conflict: bool, description: str)

```python
def detect_conflicts(cluster, tolerance=0.02):
    """Detect value inconsistencies"""
    values = [f.normalized_value for f in cluster]

    # Check 1: Relative difference threshold (2%)
    if max(values) / min(values) > 1.02:
        return True, f"Values differ by {diff}%"

    # Check 2: Order-of-magnitude detection
    if max(values) / min(values) > 10:
        return True, "Potential ×10 error detected"

    return False, ""
```

**Examples**:
- ✗ Conflict: "500 MW" vs "5000 MW" (×10 error - likely decimal point mistake)
- ✗ Conflict: "500 MW" vs "510 MW" (>2% difference)
- ✓ OK: "500 MW" vs "505 MW" (<2% difference)

---

### Stage 6: Fact Categorization (DSPy Predict) ← NEW

**Input**: Single unique fact (signature, name, value, unit)
**Tool**: FactCategorizer (dspy.Predict with Literal types + caching)
**Output**: Categorization result

```python
class FactCategorizer(dspy.Module):
    def __init__(self):
        self.categorizer = dspy.Predict(FactCategorizationSignature)
        self._cache = {}  # Cache to avoid redundant LLM calls
        self._add_examples()  # 8 diverse examples

    def forward(self, fact_name: str, fact_value: str, fact_unit: str):
        # Check cache first (key: fact_name + unit, ignores value)
        cache_key = (fact_name.lower().strip(), fact_unit.lower().strip())
        if cache_key in self._cache:
            return self._cache[cache_key]  # Cache hit!

        # Cache miss - call LLM
        result = self.categorizer(...)
        categorization = {
            "category": result.category,        # 8 options
            "subcategory": result.subcategory,  # 32 options
            "confidence": result.confidence,    # high/medium/low
            "rationale": result.rationale
        }

        # Store in cache for next occurrence
        self._cache[cache_key] = categorization
        return categorization
```

**Caching Mechanism** (NEW):
- **Cache Key**: (fact_name.lower(), fact_unit.lower()) - ignores value variations
- **Purpose**: Avoid redundant LLM calls when same fact type appears multiple times
- **Expected Hit Rate**: 37-80% on typical ESIA documents (varies by document structure)
- **Benefits**:
  - Reduces LLM API costs significantly
  - Speeds up categorization for documents with repeated fact types
  - Maintains consistency for identical facts
- **Statistics**: Tracks hits, misses, hit_rate, and cache_size
- **Example**: If "Annual CO2 emissions" appears 5 times with different values:
  - 1st call: Cache miss → LLM API call
  - 2-5 calls: Cache hits → No API calls (4× cost savings!)

**Categories (8 primary)**:
1. Project Overview
2. Project Description
3. Environmental Impacts
4. Social Impacts
5. Economic Impacts
6. Health & Safety
7. Governance & Management
8. Risks & Issues

**Subcategories (32 total)**:
```
Project Overview:         Basic Info, Timeline
Project Description:      Financing, Capacity/Scale, Technology, Infrastructure, Location
Environmental Impacts:    Water, Air, Land, Biodiversity, Waste, Emissions
Social Impacts:           Employment, Resettlement, Community, Cultural
Economic Impacts:         Investment, Revenue, Local Procurement
Health & Safety:          Occupational, Public Health, Emergency
Governance & Management:  Institutional, Monitoring, Engagement
Risks & Issues:           Identified Risks, Uncertainties, Conflicts
```

**Confidence Levels**:
- **high**: Clear fit (e.g., "Annual CO2 emissions" → Environmental Impacts → Emissions)
- **medium**: Reasonable fit but could be interpreted differently
- **low**: Ambiguous and could belong to multiple categories

**Processing**: ~1-2 seconds per fact (depends on LLM)
**For 100 facts**: ~2-3 minutes additional time

---

### Stage 7: Output Generation

**Input**: All facts, clusters, categorizations
**Tool**: 3 DataFrame generators
**Output**: 3 DataFrames ready for CSV export

```python
# Three types of output tables
facts_df = generate_facts_table(all_facts)              # Every mention
consolidated_df = generate_consolidated_table(clusters) # Unique facts
replacement_df = generate_replacement_plan(clusters)    # Editing instructions
```

---

### Stage 8: Factsheet Generation (NEW)

**Input**: Categorized facts (from stage 6)
**Tool**: FactsheetGenerator
**Output**: DataFrame organized by category/subcategory

```python
class FactsheetGenerator:
    def __init__(self, categorized_facts):
        self.organized_facts = self._organize_by_category()

    def generate_factsheet_df(self):
        """Create DataFrame ordered by category then subcategory"""
        rows = []
        for category in CATEGORY_ORDER:
            for subcategory in sorted(subcategories[category]):
                for fact in facts:
                    rows.append({
                        'category': category,
                        'subcategory': subcategory,
                        'fact_name': fact['name'],
                        'value': fact['value'],
                        'unit': fact['unit'],
                        'occurrences': fact['occurrences'],
                        'has_conflict': fact['has_conflict'],
                        'confidence': fact['confidence'],
                        'rationale': fact['rationale'],
                        'signature': fact['signature']
                    })
        return pd.DataFrame(rows)
```

**Output Structure**:
```
category | subcategory | fact_name | value | unit | occurrences | has_conflict | confidence | rationale
---------|-------------|-----------|-------|------|-------------|------------|-----------|----------
Project Description | Capacity/Scale | Installed capacity | 500 | MW | 3 | False | high | Core descriptor
Environmental Impacts | Emissions | Annual CO2 | 250000 | tonnes/yr | 2 | False | high | Direct measure
```

---

### Stage 9: CSV Export

**Output Files** (4 total):

1. **esia_mentions.csv** (All occurrences)
   - Rows: Every mention of every fact
   - Use: Trace where facts come from, verify evidence

2. **esia_consolidated.csv** (Unique facts)
   - Rows: One per unique fact signature
   - Columns: Value range, occurrence count, conflict flag
   - Use: Summary of extracted facts

3. **esia_replacement_plan.csv** (Editing patterns)
   - Rows: One per unique fact
   - Columns: Regex patterns to find text, replacement rules
   - Use: Document editing/updating

4. **project_factsheet.csv** (Categorized facts) ← NEW
   - Rows: One per unique fact, organized by category
   - Columns: Category, subcategory, confidence, rationale
   - Use: Client deliverables, factsheet reports

---

## Two Implementation Paths

### Path A: CLI Script (Standalone)

**File**: `esia_extractor.py` (root directory)
**Entry Point**: Command line
**Supports**: Markdown input only

```bash
python esia_extractor.py input.md ./output
```

**Pipeline in Code**:
```
[1/9] Configure LLM
[2/9] Load markdown
[3/9] Chunk text
[4/9] Extract facts
[5/9] Cluster facts
[6/9] Categorize facts ← NEW
[7/9] Generate output tables
[8/9] Generate factsheet ← NEW
[9/9] Save CSV files
```

**Advantages**:
- Simple, standalone script
- No dependencies beyond DSPy, pandas
- Quick testing and verification

---

### Path B: SaaS Backend (Full-Featured)

**Directory**: `saas/core/extractor.py`
**Entry Point**: Python function
**Supports**: PDF, DOCX, Markdown input

```python
from saas.core.extractor import process_document

results = process_document(
    file_path="document.pdf",
    progress_callback=lambda curr, total, status: print(f"{curr}% {status}")
)
```

**Pipeline in Code**:
```
[0%] Configure LLM
[5%] Load document (with Docling conversion)
[10%] Chunk text
[15%] Extract facts
[90%] Cluster and detect conflicts
[100%] Return results
```

**Advantages**:
- Handles PDF/DOCX automatically via Docling
- Progress callback for web integration
- Returns Python objects, not just CSVs
- Ready for SaaS deployment

**Note**: Does NOT include factsheet generation yet (can be added)

---

## Performance Characteristics

### Time Breakdown (for 100KB ESIA with Claude 3 Sonnet)

| Stage | Time | Notes |
|-------|------|-------|
| 1. Docling conversion | 30-60s | PDF → Markdown (varies by complexity) |
| 2. Chunking | <1s | Fast, just string splitting |
| 3. Fact extraction | 3-8 min | 1-2s per chunk × 25 chunks |
| 4. Clustering | <1s | Simple grouping operation |
| 5. Conflict detection | <1s | Quick comparison |
| 6. Categorization | 1-2 min | ~1.2s per fact (with cache hits: 1s/fact → 0.3s/fact) |
| 7. Output generation | <1s | DataFrame creation |
| 8. Factsheet generation | <1s | Simple reorganization |
| 9. CSV export | <1s | Pandas to_csv() |
| **TOTAL** | **5-10 minutes** | Depends on document complexity and cache hit rate |

**Categorization Speedup**:
- Without cache: 1-2 seconds per fact = 2-3 minutes for 100 facts
- With cache (37-80% hit rate): 0.5-1.2 seconds per fact = 0.5-2 minutes for 100 facts
- **Savings**: 30-60% faster categorization with caching enabled

### Cost Breakdown (Claude 3 Sonnet)

**Without Caching**:
- ~100 chunks × ~500 tokens each = 50,000 input tokens ≈ $0.0015
- ~100 facts × ~100 tokens each = 10,000 input tokens ≈ $0.0003
- **Total cost**: ~$0.002 per document (~0.2 cents)

**With Caching (50% hit rate)**:
- Extraction: 50,000 input tokens ≈ $0.0015
- Categorization: ~50 facts × 100 tokens = 5,000 input tokens ≈ $0.00015
- **Total cost**: ~$0.00165 per document (17% cost reduction)

**With Caching (80% hit rate)**:
- Extraction: 50,000 input tokens ≈ $0.0015
- Categorization: ~20 facts × 100 tokens = 2,000 input tokens ≈ $0.00006
- **Total cost**: ~$0.00156 per document (22% cost reduction)

---

## Data Structures

### Fact Object

```python
@dataclass
class Fact:
    name: str                    # "Annual CO2 emissions"
    type: str                    # "quantity" or "categorical"
    value: str                   # "250000"
    value_num: float             # 250000.0
    unit: str                    # "tonnes/yr"
    aliases: List[str]           # ["CO2 emissions", "Carbon emissions"]
    evidence: str                # Source text quote
    page: int                    # Chunk number
    chunk_id: int                # Position
    signature: str               # "annual_co2_emissions" (slugified)
    normalized_value: float      # 250000.0 (converted to canonical unit)
    normalized_unit: str         # "tonnes/yr"
    # Added during processing:
    has_conflict: bool           # True if values differ >2%
    conflict_description: str    # "Values range from 250000 to 260000"
```

### Categorization Object

```python
categorization = {
    "category": "Environmental Impacts",      # 8 options (Literal)
    "subcategory": "Emissions",               # 32 options (Literal)
    "confidence": "high",                     # high/medium/low (Literal)
    "rationale": "CO2 is direct environmental impact"
}
```

---

## Error Handling & Recovery

### Graceful Degradation

If categorization fails:
- First 3 CSV files still generated (mentions, consolidated, replacement plan)
- `project_factsheet.csv` not created
- Warning printed to console
- Extraction continues successfully

### Checkpoint System (CLI Only)

- Saves every 5 chunks to `.checkpoint.pkl`
- Automatically resumes on re-run
- Useful for large documents

---

## How to Run Locally

### Quick Start (Markdown Input)

```powershell
# 1. Navigate to project
cd M:\GitHub\esia-fact-extractor

# 2. Ensure latest code
git fetch origin
git checkout claude/create-new-feature-011CV2gkmrffTaTiRnpMkrvk

# 3. Run extraction
python esia_extractor.py saas/backend/docling_output/test_simple.md ./my_results
```

### With PDF Input (Requires Docling)

```powershell
# 1. Install docling
pip install docling

# 2. Convert PDF in SaaS backend
cd saas/backend
python -c "
from core.extractor import process_document
results = process_document('your_document.pdf')
print(f'Extracted {results[\"stats\"][\"total_facts\"]} facts')
"

# 3. Generated markdown saved to saas/backend/docling_output/
```

---

## Configuration

### Key Environment Variables

```ini
# LLM Provider selection
LLM_PROVIDER=anthropic

# Extraction parameters
CHUNK_SIZE=4000
CHECKPOINT_FREQUENCY=5
CONFLICT_TOLERANCE=0.02

# Factsheet parameters (NEW)
SKIP_FACTSHEET_GENERATION=False
FACTSHEET_MIN_CONFIDENCE=medium
```

---

## Next Steps

1. **Test the pipeline locally**: Run on test_simple.md
2. **Verify factsheet output**: Check project_factsheet.csv for categorization accuracy
3. **Try with real PDF**: Use Docling to convert your ESIA documents
4. **Review categorizations**: Look for "low" confidence items needing manual review
5. **Provide feedback**: Report any miscategorizations or improvements

---

## Related Files

- `esia_extractor.py` - CLI script with all 9 pipeline stages
- `saas/core/extractor.py` - SaaS backend (stages 1-5 only)
- `saas/backend/test_full_pipeline.py` - Test runner for SaaS
- `saas/backend/test_docling.py` - Docling setup verification
- `FACTSHEET_IMPLEMENTATION_PLAN.md` - Design details
- `README.md` - User documentation
- `CLAUDE.md` - Development notes for Claude AI

