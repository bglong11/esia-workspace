# Step 2: ESIA Fact Extraction with DSPy

## Overview

Step 2 processes the semantic chunks from Step 1 and extracts domain-specific facts using DSPy with LLM (Google Gemini or OpenRouter).

**Input**: `*_chunks.jsonl` from Step 1
**Output**: `esia_facts_extracted.json` with extracted facts

## Pipeline Steps

1. **Load Chunks** - Read JSONL file with semantic chunks
2. **Initialize DSPy** - Set up LLM provider (using .env configuration)
3. **Extract Facts** - Apply 40+ domain-specific signatures to each section
4. **Merge Results** - Combine facts by section and domain
5. **Save Output** - Write results to JSON file

## Running Step 2

### Basic Extraction (All Chunks)
```bash
python step2_simple_extraction.py
```

**What it does**:
- Processes all 117 chunks
- Groups chunks by document section
- Extracts facts from each section
- Saves results to `./data/outputs/esia_facts_extracted.json`

### Test Run (Sample Chunks)
```bash
python step2_simple_extraction.py --sample 5
```

**Use cases**:
- Testing the pipeline (faster)
- Debugging issues
- Verifying configuration

### Verbose Output
```bash
python step2_simple_extraction.py --verbose
```

**Shows**:
- Detailed extraction progress
- Fact extraction counts
- Errors and warnings

### Custom Output File
```bash
python step2_simple_extraction.py \
  --output ./my_output/facts.json
```

## Configuration

Step 2 uses the `.env` file settings:

| Variable | Purpose | Example |
|----------|---------|---------|
| `LLM_PROVIDER` | Which API to use | `openrouter` |
| `OPENROUTER_MODEL` | Model for extraction | `google/gemini-2.0-flash-exp:free` |
| `GOOGLE_MODEL` | Google model name | `gemini-2.0-flash-exp` |
| `OPENROUTER_API_KEY` | API key for OpenRouter | `sk-or-v1-...` |
| `GOOGLE_API_KEY` | API key for Google | `AIzaSy...` |

### Using OpenRouter (Free Gemini)
Current setup uses OpenRouter with the free Google Gemini model - **no cost!**

### Using Google Gemini Directly
```python
# Modify initialization in step2_simple_extraction.py
extractor = ESIAExtractor(model="gemini-2.0-flash-exp", provider="google")
```

## Output Format

### File Structure
```json
{
  "document": "TL_IPP_Supp_ESIA_2025-09-15.pdf",
  "extraction_date": "2025-11-27T01:30:00.000000",
  "total_chunks": 117,
  "sections": {
    "Project Description": {
      "section": "Project Description",
      "page_start": 1,
      "page_end": 5,
      "chunk_count": 3,
      "facts": {
        "ProjectDescriptionSignature": {...facts...},
        "ProjectTypeSignature": {...facts...},
        ...
      }
    },
    ...more sections...
  },
  "errors": [
    "Section 'Name': error message",
    ...
  ]
}
```

### Fact Structure

Each section contains facts extracted by different domain signatures:

```json
"facts": {
  "ProjectDescriptionSignature": {
    "project_name": "Laleia Solar IPP",
    "project_type": "Solar Energy",
    "location": "Timor-Leste",
    ...
  },
  "EnvironmentalImpactSignature": {
    "environmental_impacts": [...],
    "mitigation_measures": [...],
    ...
  },
  ...
}
```

## Processing Time

**Estimated times** (depending on LLM latency):

| Scenario | Chunks | Time |
|----------|--------|------|
| Sample test | 2 | 10-15 sec |
| Small doc | 5-10 | 1-2 min |
| Medium doc | 50-100 | 10-20 min |
| Full doc | 117+ | 20-40 min |

**Factors affecting speed**:
- LLM API response time (OpenRouter or Google)
- Number of chunks to process
- Number of unique sections
- Complexity of content

## Understanding Extraction

### What Gets Extracted?

The DSPy extractors look for:
- **Project Information**: Name, type, location, client
- **Environmental Impacts**: Climate, water, biodiversity
- **Social Impacts**: Community, labor, resettlement
- **Mitigation Measures**: Proposed solutions, management plans
- **Compliance**: Legal framework, permits, policies
- **Domain-Specific**: Solar-specific, mining-specific, etc.

### What About Sections with No Facts?

Some sections (like Acronyms, Table of Contents) may not have extractable facts. This is **normal and expected**.

Sections that successfully extract facts:
- Project Description
- Environmental & Social Impact Assessment
- Mitigation & Enhancement Measures
- Project-Specific Impacts (Solar, Hydro, etc.)
- Management Plans
- Conclusions & Recommendations

## Advanced Usage

### Combining with Project Classification

After extracting facts, you can classify the project type:

```bash
# Step 2 extracts facts
python step2_simple_extraction.py

# Step 3 would classify project (requires file search setup)
# python src/project_type_classifier.py ./data/outputs/esia_facts_extracted.json
```

### Batch Processing Multiple Documents

```bash
# Process each PDF
for pdf in ./data/inputs/pdfs/*.pdf; do
    echo "Processing: $pdf"
    python step1_docling_hybrid_chunking.py "$pdf" -o ./data/outputs
    python step2_simple_extraction.py
done
```

### Integration with Downstream Systems

The output JSON is suitable for:
- **Vector Databases**: Convert facts to embeddings
- **Data Warehouses**: Load for analysis
- **Dashboards**: Visualize extracted metrics
- **Search Systems**: Index by domain and section

## Troubleshooting

### "API Key not found" Error

**Solution**: Check `.env` file exists and has keys:
```bash
cat .env
# Should show: OPENROUTER_API_KEY=sk-or-v1-...
```

### "Rate limit exceeded" Error

**Solution**: Wait a moment and retry:
```bash
# OpenRouter free tier has limits
# Wait 30-60 seconds and run again
sleep 60
python step2_simple_extraction.py
```

### "No facts extracted" for All Sections

**Possible causes**:
1. Chunks contain only metadata/headings (not content)
2. LLM not finding relevant facts in text
3. Section names don't match domain signatures

**Solution**: Check chunk content:
```bash
python -c "
import json
with open('./data/outputs/TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl') as f:
    chunk = json.loads(f.readline())
    print(f'Section: {chunk[\"section\"]}')
    print(f'Text (first 200 chars): {chunk[\"text\"][:200]}')
    print(f'Token count: {chunk[\"token_count\"]}')
"
```

### JSON Decoding Error

**Solution**: Verify output format:
```bash
python -c "
import json
with open('./data/outputs/esia_facts_extracted.json') as f:
    data = json.load(f)
print(f'Successfully loaded {len(data[\"sections\"])} sections')
"
```

## Performance Optimization

### Process Only High-Value Chunks

Modify script to skip low-value sections:

```python
# In step2_simple_extraction.py
skip_sections = {'Acronyms', 'Table of Contents', 'Glossary'}

for section_name in sections:
    if section_name in skip_sections:
        continue
    # ...extract facts...
```

### Parallel Processing

For multiple documents:

```bash
# Process up to 3 documents in parallel
parallel python step2_simple_extraction.py --chunks {} ::: ./data/outputs/*_chunks.jsonl
```

## Next Steps After Step 2

### Step 3: Project Type Classification
Classify the ESIA project into categories:
- Energy type (Solar, Hydro, Coal, Wind, Geothermal)
- Mining type (Gold, Copper, Coal, etc.)
- Infrastructure type (Road, Dam, Port, etc.)
- Other (Manufacturing, Agriculture, etc.)

### Step 4: Results Analysis
- Analyze extracted facts
- Identify missing information
- Validate against source documents
- Export to dashboard or database

### Step 5: Integration
- Combine facts from multiple documents
- Build knowledge graphs
- Create impact assessments
- Generate reports

## Files Generated

**Step 2 produces:**
```
./data/outputs/
├── esia_facts_extracted.json      (Main output)
├── esia_facts_metadata.json       (Statistics)
└── extraction_report.txt           (Summary)
```

**All previous outputs preserved:**
```
./data/outputs/
├── TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl     (Step 1)
├── TL_IPP_Supp_ESIA_2025-09-15_meta.json        (Step 1)
├── project_classification.json                   (Step 3, if run)
└── ...
```

## Quick Reference

| Task | Command |
|------|---------|
| Run full extraction | `python step2_simple_extraction.py` |
| Test with samples | `python step2_simple_extraction.py --sample 5` |
| Verbose output | `python step2_simple_extraction.py --verbose` |
| Custom output | `python step2_simple_extraction.py --output ./my_facts.json` |
| Check results | `python -c "import json; print(json.load(open('./data/outputs/esia_facts_extracted.json')))"`|

---

**Status**: Step 2 ready for production
**Current Setup**: OpenRouter with free Google Gemini 2.0 Flash
**Next Step**: Run full extraction on all 117 chunks
