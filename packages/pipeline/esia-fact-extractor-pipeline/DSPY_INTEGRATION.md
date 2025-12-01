# DSPy Integration Guide: Which File to Use

## Quick Answer

**`_chunks.jsonl` is the PRIMARY input for DSPy**

The `_meta.json` is OPTIONAL and serves as supporting/reference information.

---

## File Purposes

### `_chunks.jsonl` (REQUIRED for DSPy)

**Contains:** The actual content chunks ready for fact extraction

```json
{
  "chunk_id": 0,
  "page": 1,
  "section": "ENVIRONMENTAL AND SOCIAL IMPACT ASSESSMENT FOR THE PROJECT",
  "text": "Project: Laleia Solar Independent Power Producer (IPP) Project\nClient: EDF Renewables & Itochu Corporation\nProject Number: 2025-TL-03\nDate: 15 September 2025",
  "token_count": 21,
  "metadata": {
    "headings": ["ENVIRONMENTAL AND SOCIAL IMPACT ASSESSMENT FOR THE PROJECT"],
    "captions": [],
    "doc_items_count": 4,
    "origin": {"filename": "TL_IPP_Supp_ESIA_2025-09-15.pdf", ...}
  }
}
```

**Why DSPy uses this:**
- **Text content** - What DSPy actually processes for fact extraction
- **Page number** - Trace facts back to original document location
- **Section** - Understand content context
- **Token count** - Know input size for cost/performance calculations

**Usage in DSPy:**
```python
import json

# Load chunks for DSPy
chunks = []
with open('TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl') as f:
    for line in f:
        chunk = json.loads(line)
        chunks.append({
            'context': chunk['text'],
            'page': chunk['page'],
            'section': chunk['section'],
            'chunk_id': chunk['chunk_id']
        })

# Process each chunk with DSPy
for chunk in chunks:
    result = dspy_pipeline.forward(
        context=chunk['context'],
        page=chunk['page'],
        section=chunk['section']
    )
    # Extract facts, save results, etc.
```

---

### `_meta.json` (OPTIONAL, Supporting)

**Contains:** Metadata, index, and statistics about the document

```json
{
  "document": {
    "original_filename": "...",
    "total_pages": 77,
    "processed_at": "2025-11-26T21:01:18.450711"
  },
  "files": {
    "chunks": "TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl"
  },
  "tables": [
    {
      "table_id": 0,
      "page": 2,
      "content": "| AEP | Annual Exceedance Probability | ...",
      "metadata": {"bbox": {...}}
    }
  ],
  "statistics": {
    "total_chunks": 117,
    "avg_tokens_per_chunk": 176.62,
    "total_tokens": 20664
  }
}
```

**Why you might use this with DSPy:**
- **Quality assurance** - Verify processing completed successfully
- **Table extraction** - If your facts need to be validated against tables
- **Cross-referencing** - Link extracted facts to original page locations
- **Cost estimation** - Calculate processing costs before running DSPy
- **Document tracking** - Know when document was processed and what version
- **Metadata filtering** - Filter chunks before processing (e.g., only process pages 10-40)

**Usage scenarios:**

```python
import json

meta = json.load(open('TL_IPP_Supp_ESIA_2025-09-15_meta.json'))

# Use case 1: Cost estimation before running DSPy
tokens = meta['statistics']['total_tokens']
estimated_cost = tokens * 0.00002  # OpenAI API pricing
print(f"Processing cost estimate: ${estimated_cost:.2f}")

# Use case 2: Validate against extracted tables
tables = meta['tables']
for table in tables:
    print(f"Table on page {table['page']}: {table['content'][:50]}...")

# Use case 3: Filter chunks before processing
with open('chunks.jsonl') as f:
    # Only process chunks from pages with content
    pages_with_content = set(t['page'] for t in meta['tables'])
    for line in f:
        chunk = json.loads(line)
        if chunk['page'] in pages_with_content:
            # Process this chunk
            pass

# Use case 4: Quality check
stats = meta['statistics']
if stats['total_chunks'] != count_lines_in_jsonl:
    print("WARNING: Chunk count mismatch!")
```

---

## Data Flow Comparison

### Minimal DSPy Pipeline (Chunks Only)

```
PDF Document
    ↓
[Step 1: Enhanced Docling Convertor]
    ├→ chunks.jsonl  (✓ USED)
    └→ meta.json     (✗ IGNORED)
    ↓
[Step 2: DSPy Pipeline]
    ├→ Load chunks.jsonl
    ├→ Iterate through each chunk
    ├→ Extract facts from chunk.text
    └→ Save results with page/section context
```

### Complete DSPy Pipeline (With Meta Support)

```
PDF Document
    ↓
[Step 1: Enhanced Docling Convertor]
    ├→ chunks.jsonl  (✓ USED - for actual content)
    └→ meta.json     (✓ USED - for validation & context)
    ↓
[Step 2: DSPy Pipeline with Quality Checks]
    ├→ Load meta.json
    ├→ Validate: chunk count matches
    ├→ Estimate: processing cost
    ├→ Filter: select relevant pages (optional)
    ├→ Load chunks.jsonl
    ├→ For each chunk:
    │  ├→ Extract facts from chunk.text
    │  ├→ Add context: page, section
    │  ├→ Cross-reference: validate against tables (optional)
    │  └→ Save results with full lineage
    ├→ Quality check: all chunks processed
    └→ Report: document processed, X facts extracted
```

---

## Real-World DSPy Examples

### Example 1: Basic Fact Extraction (Minimal)

```python
import dspy
import json

# Initialize DSPy
dspy.configure(lm=dspy.OpenAI(model="gpt-4o"))

class FactExtractor(dspy.ChainOfThought):
    """Extract key facts from environmental impact document"""
    def forward(self, context, page, section):
        return dspy.ChainOfThought('context, page, section -> facts')(
            context=context,
            page=page,
            section=section
        )

# Load ONLY chunks.jsonl
facts_by_page = {}
with open('TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl') as f:
    for line in f:
        chunk = json.loads(line)

        # Extract facts
        result = FactExtractor().forward(
            context=chunk['text'],
            page=chunk['page'],
            section=chunk['section']
        )

        # Organize by page
        if chunk['page'] not in facts_by_page:
            facts_by_page[chunk['page']] = []
        facts_by_page[chunk['page']].append({
            'chunk_id': chunk['chunk_id'],
            'section': chunk['section'],
            'facts': result.facts
        })

# Save results
with open('extracted_facts.json', 'w') as f:
    json.dump(facts_by_page, f, indent=2)
```

### Example 2: Fact Extraction with Quality Validation (Complete)

```python
import dspy
import json

# Load and validate metadata first
meta = json.load(open('TL_IPP_Supp_ESIA_2025-09-15_meta.json'))
print(f"Processing: {meta['document']['original_filename']}")
print(f"Total chunks: {meta['statistics']['total_chunks']}")
print(f"Estimated tokens: {meta['statistics']['total_tokens']}")

# Cost estimation
cost = meta['statistics']['total_tokens'] * 0.00002
print(f"Estimated API cost: ${cost:.2f}")

# Continue with extraction
dspy.configure(lm=dspy.OpenAI(model="gpt-4o"))

class EnvironmentalFactExtractor(dspy.ChainOfThought):
    def forward(self, context):
        return dspy.ChainOfThought('context -> environmental_impacts, climate_risks, mitigation_measures')(
            context=context
        )

# Process chunks with cross-reference to tables
facts_with_validation = []
table_pages = {t['page']: t['content'][:200] for t in meta['tables']}

with open('TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl') as f:
    for i, line in enumerate(f):
        chunk = json.loads(line)

        # Extract facts
        result = EnvironmentalFactExtractor().forward(context=chunk['text'])

        # Validate against tables if available
        table_context = table_pages.get(chunk['page'], None)

        facts_with_validation.append({
            'chunk_id': chunk['chunk_id'],
            'page': chunk['page'],
            'section': chunk['section'],
            'facts': result,
            'has_supporting_table': table_context is not None,
            'tokens': chunk['token_count']
        })

        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{meta['statistics']['total_chunks']} chunks")

# Final validation
if len(facts_with_validation) == meta['statistics']['total_chunks']:
    print(f"✓ Validation passed: All {len(facts_with_validation)} chunks processed")
else:
    print(f"✗ ERROR: Expected {meta['statistics']['total_chunks']} chunks, got {len(facts_with_validation)}")

# Save results
with open('environmental_facts.json', 'w') as f:
    json.dump(facts_with_validation, f, indent=2)
```

### Example 3: Selective Processing Using Meta (Advanced)

```python
import dspy
import json

# Load meta to understand document structure
meta = json.load(open('TL_IPP_Supp_ESIA_2025-09-15_meta.json'))

# Find pages with environmental impact tables
impact_pages = set()
for table in meta['tables']:
    if 'Impact' in table['content'] or 'Environmental' in table['content']:
        impact_pages.add(table['page'])

print(f"Found {len(impact_pages)} pages with environmental impact information")
print(f"Pages: {sorted(impact_pages)}")

# ONLY process chunks from those pages
dspy.configure(lm=dspy.OpenAI(model="gpt-4o"))

class ImpactAssessmentExtractor(dspy.ChainOfThought):
    def forward(self, context):
        return dspy.ChainOfThought('context -> impacts, mitigation_strategies')(
            context=context
        )

impact_facts = []
with open('TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl') as f:
    for line in f:
        chunk = json.loads(line)

        # Skip chunks not on impact pages
        if chunk['page'] not in impact_pages:
            continue

        # Extract facts from relevant chunks only
        result = ImpactAssessmentExtractor().forward(context=chunk['text'])

        impact_facts.append({
            'page': chunk['page'],
            'section': chunk['section'],
            'impacts': result.impacts,
            'mitigations': result.mitigation_strategies
        })

print(f"Extracted impacts from {len(impact_facts)} relevant chunks")

with open('impact_assessment_facts.json', 'w') as f:
    json.dump(impact_facts, f, indent=2)
```

---

## Decision Tree: Which File to Use?

```
Do you want to extract facts from text content?
    └─→ YES: Use chunks.jsonl (REQUIRED)

Do you need to validate results against tables?
    └─→ YES: Use meta.json (OPTIONAL)

Do you want quality assurance checks?
    └─→ YES: Use meta.json (OPTIONAL)

Do you want to estimate costs before running?
    └─→ YES: Use meta.json (OPTIONAL)

Do you want to filter to specific pages?
    └─→ YES: Use meta.json (OPTIONAL)

Do you want to trace facts back to original locations?
    └─→ YES: Use both (chunks.jsonl for text, meta.json for page/table info)

Minimum needed for DSPy?
    └─→ chunks.jsonl only
```

---

## Summary Table

| Need | File | Required? | Why |
|------|------|-----------|-----|
| Fact extraction | chunks.jsonl | ✓ YES | Contains actual text to process |
| Page reference | chunks.jsonl | ✓ YES | Page number in each chunk |
| Section context | chunks.jsonl | ✓ YES | Section heading in each chunk |
| Cost estimation | meta.json | Optional | Statistics for API cost calculation |
| Quality validation | meta.json | Optional | Verify all chunks processed |
| Table cross-reference | meta.json | Optional | Validate facts against tables |
| Document tracking | meta.json | Optional | Know when/what was processed |
| Selective processing | meta.json | Optional | Filter chunks by page/table |

---

## Best Practices

### For Simple Fact Extraction
- Use **only** `chunks.jsonl`
- Lighter processing, faster iteration
- Page/section info already included

### For Production Systems
- Use **both** files:
  - `chunks.jsonl` for actual processing
  - `meta.json` for validation and cost estimation
- Implement quality checks
- Cross-reference facts against tables when applicable

### For Quality Assurance
1. Check meta.json statistics match actual chunks processed
2. Validate that total_chunks = lines in chunks.jsonl
3. Verify token counts are reasonable
4. Cross-reference any extracted facts with tables in meta.json

---

## File Size Comparison

For your document:

| File | Size | What It Contains |
|------|------|------------------|
| chunks.jsonl | 184 KB | 117 chunks of actual content |
| meta.json | 52 KB | Metadata + full table content + statistics |

**Total:** 236 KB to represent a 77-page PDF document
- **Compression ratio:** ~99% (original PDF is likely several MB)
- **Processing efficiency:** Entire document fits in memory easily

---

## Conclusion

**For DSPy:**
- **Must use:** `chunks.jsonl` (the actual content)
- **Should consider:** `meta.json` (for validation, cost estimation, table cross-reference)

The chunks.jsonl is self-contained with everything you need (text, page, section).
The meta.json is optional but recommended for production pipelines for quality control and optimization.
