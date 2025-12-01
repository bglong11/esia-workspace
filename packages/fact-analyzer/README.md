# ESIA Fact Analyzer

**A comprehensive Environmental & Social Impact Assessment (ESIA) document review tool** that analyzes extracted facts from ESIA reports for quality assurance and lender/regulator compliance.

Built by Claude to provide intelligent, context-aware analysis of ESIA documents with professional reporting dashboards.

---

## What It Does

The ESIA Fact Analyzer processes extracted facts from ESIA documents and performs sophisticated analysis:

- **Fact Categorization** - Organizes facts into ESIA taxonomy categories
- **Context-Aware Consistency Checking** - Detects inconsistent values within the same parameter type (e.g., study area reported differently in multiple locations)
- **Unit Standardization Analysis** - Identifies when the same parameter is reported using different units
- **Gap Analysis** - Identifies missing expected content from the ESIA with extraction of found content and page references
- **Professional Reporting** - Generates interactive HTML dashboards and detailed Excel workbooks

---

## Quick Start

### Prerequisites

- Python 3.8+
- Input: JSONL chunks file from ESIA fact extraction pipeline
- Optional: Metadata JSON file

### Installation

```bash
# Install optional dependencies for Excel export (recommended)
pip install pandas openpyxl

# Or with system packages flag if needed
pip install pandas openpyxl --break-system-packages
```

### Basic Usage

**Default (uses `./data/analysis_inputs` folder):**
```bash
python analyze_esia_v2.py
```
Expects files:
- `./data/analysis_inputs/chunks.jsonl` (required)
- `./data/analysis_inputs/meta.json` (optional)

**Custom input folder:**
```bash
python analyze_esia_v2.py --input-dir ./my_data
```

**Custom output folder:**
```bash
python analyze_esia_v2.py --output-dir ./my_results
```

**Override specific filenames:**
```bash
python analyze_esia_v2.py --chunks my_chunks.jsonl --meta my_metadata.json
```

**Full control:**
```bash
python analyze_esia_v2.py \
    --input-dir ./data/analysis_inputs \
    --output-dir ./data/analysis_outputs \
    --skill-dir /path/to/skill
```

**Parameters:**
- `--input-dir` / `-i` - Input directory (default: `./data/analysis_inputs`)
- `--chunks` - Override chunks filename (default: `chunks.jsonl`)
- `--meta` - Override metadata filename (default: `meta.json`)
- `--output-dir` / `-o` - Output directory (default: `./data/analysis_outputs`)
- `--skill-dir` - Path to skill directory containing reference data

### Output Files

The tool generates two files:
1. **`{basename}_review.html`** - Interactive dark-themed dashboard with collapsible sections
2. **`{basename}_review.xlsx`** - Detailed workbook with 6 analysis sheets

---

## How It Works

### Architecture

The tool is built around a single main class: **`ESIAReviewer`**

```
ESIAReviewer
├── load_data()                      # Load JSONL chunks & metadata
├── categorize_facts()               # Map facts to taxonomy
├── check_consistency()              # Context-aware value comparison
├── check_unit_standardization()    # Detect mixed units
├── check_thresholds()              # IFC compliance validation
├── analyze_gaps()                  # Identify missing content
├── run_analysis()                  # Execute full pipeline
└── export_html() / export_excel()  # Generate reports
```

### Analysis Pipeline

```
1. Load Input Files
   └─ Read JSONL chunks and optional metadata

2. Categorization
   └─ Match facts to ESIA taxonomy keywords

3. Consistency Analysis
   ├─ Extract numeric values with units
   ├─ Identify parameter contexts (study area, workforce, etc.)
   ├─ Normalize units to base units
   └─ Compare like-for-like values (>5% difference = issue)

4. Unit Standardization
   ├─ Group by parameter context
   ├─ Detect different units used for same parameter
   └─ Recommend standard unit

5. Gap Analysis
   ├─ Search for 30+ expected content items
   ├─ Extract found content with page references
   └─ Classify as PRESENT or MISSING

6. Report Generation
   ├─ Generate HTML dashboard
   └─ Generate Excel workbook
```

---

## Key Features

### 1. Context-Aware Consistency Checking

Only compares values within the same parameter context using intelligent pattern matching:

- **17 Parameter Contexts**: study_area, concession_area, disturbance_area, buffer_zone, population, affected_households, workforce, water_consumption, power_capacity, emissions_ghg, noise_level, air_quality_pm, rainfall, temperature, etc.
- **Like-for-Like Comparison**: Study area vs study area, not study area vs any area
- **Unit Normalization**: All values converted to base units for accurate comparison
- **Severity Levels**: HIGH (>20% difference) or MEDIUM (≤20% difference)

**Example:**
```
Study area mentioned as both "5,000 ha" and "50,000,000 m²"
→ Normalized: 50,000,000 sq m vs 50,000,000 sq m = 0% difference ✓
```

### 2. Unit Standardization Analysis

Detects when the same parameter is reported using different units:

- **80+ Unit Conversions** supporting:
  - Area: ha, km², m², acres → sq m
  - Volume: ML, kL, L, m³ → L
  - Emissions: t, tCO2e, kt, Mt → tonnes
  - Power: MW, GW, kW → MW
  - Concentration: mg/L, µg/m³
  - And more...

**Example:**
```
Water consumption reported as:
  - 500 ML [p.15]
  - 500,000,000 L [p.42]
→ Recommendation: Standardize to liters (L)
```

### 3. IFC Threshold Compliance

Validates measured values against International Finance Corporation (IFC) Environmental, Health & Safety Guidelines:

**Air Quality (Ambient):**
- PM10: 50 µg/m³ (24-hr), 20 µg/m³ (annual)
- PM2.5: 25 µg/m³ (24-hr), 10 µg/m³ (annual)
- SO2, NO2, and other pollutants

**Noise:**
- Residential day: 55 dB(A)
- Residential night: 45 dB(A)
- Industrial areas: 70 dB(A)

**Water Quality (Effluent):**
- BOD: 50 mg/L
- COD: 250 mg/L
- TSS: 50 mg/L
- pH: 6-9

**Status Indicators:**
- EXCEEDANCE: Value exceeds IFC limit (red)
- APPROACHING: Value >80% of limit (amber)
- COMPLIANT: Within acceptable range (green)

### 4. Enhanced Gap Analysis

Systematically checks for 30+ expected content items across 6 sections:

| Section | Expected Items |
|---------|-----------------|
| **Project Description** | Location Coordinates, Project Area, Workforce Numbers, Water Consumption, Power Consumption, Project Duration, Capital Cost |
| **Physical Baseline** | Ambient Air Quality, Noise Measurements, Water Quality Data, Rainfall Data, Seismic Assessment, Climate Data, Topography |
| **Biological Baseline** | Species Lists, IUCN Status, Protected Areas, Critical Habitat, Endemic Species |
| **Social Baseline** | Population Data, Household Data, Livelihood Sources, Vulnerable Groups, Land Tenure, Indigenous Peoples |
| **Impact Assessment** | Significance Criteria, Cumulative Impacts, Transboundary Impacts |
| **Mitigation & Management** | ESMP Reference, Monitoring Plan, Emergency Response |

**Features:**
- Extracts actual content found in document
- Page references for found content [p.XX]
- Collapsible sections with coverage indicators (X/Y found)
- Status badges: PRESENT (green) or MISSING (red)

### 5. Modern Dashboard UI

**HTML Dashboard Features:**
- Dark theme with professional design
- Custom typography (Instrument Serif, Space Mono, DM Sans)
- Animated stat cards with color-coded metrics
- Collapsible sections for gap analysis
- Responsive design (desktop, tablet, mobile)
- Color-coded badges for severity/status

**Excel Workbook Sheets:**
1. **Summary** - Key statistics and counts
2. **Fact Categories** - Categorization breakdown
3. **Consistency Issues** - Detected inconsistencies with severity
4. **Unit Standardization** - Mixed unit issues and recommendations
5. **Gap Analysis** - Missing/present content with page references

---

## Input Data Format

### JSONL Chunks File

Newline-delimited JSON with extracted facts:

```jsonl
{"text": "The study area is 5,000 hectares...", "page": 15, "section": "Project Description", "metadata": {"headings": ["Study Area"]}}
{"text": "Workforce will be approximately 500 people...", "page": 22, "section": "Project Description"}
{"text": "Water consumption is 50 ML per day...", "page": 33, "section": "Inputs and Resources"}
```

**Required fields:**
- `text` - Fact text content
- `page` - Page number where found

**Optional fields:**
- `section` - Document section name
- `metadata` - Additional context (headings, etc.)

### Metadata JSON (Optional)

```json
{
  "document": {
    "original_filename": "ESIA_Report_Final.pdf",
    "total_pages": 450,
    "extraction_date": "2024-01-15"
  }
}
```

---

## Reference Data Files

The tool requires three JSON reference files in `{skill_dir}/references/`:

### 1. ifc_thresholds.json

IFC EHS Guidelines thresholds for various parameters:

```json
{
  "air_quality": {
    "ambient": {
      "PM10": {"value": 50, "unit": "µg/m³"},
      "PM2.5": {"value": 25, "unit": "µg/m³"}
    }
  },
  "noise": {
    "residential_day": {"value": 55, "unit": "dB(A)"}
  }
}
```

### 2. esia_taxonomy.json

Keyword-based categorization for facts:

```json
{
  "categories": {
    "Baseline - Physical": {
      "keywords": ["air quality", "noise", "water quality", "climate"]
    },
    "Impacts - Environmental": {
      "keywords": ["emissions", "effluent", "waste", "deforestation"]
    }
  }
}
```

### 3. reviewer_checklists.json

Expected content patterns for gap analysis:

```json
{
  "gap_analysis_template": {
    "expected_content": {
      "Project Description": {},
      "Physical Baseline": {}
    }
  }
}
```

---

## Output Interpretation

### Severity Levels

- **HIGH** - Likely to cause rejection by lenders (must fix before submission)
- **MEDIUM** - May require clarification (address if possible)
- **LOW** - Minor quality issues (note for future improvement)

### Coverage Status (Gap Analysis)

- **Green (Teal)** - All expected items found (✓)
- **Amber** - Some items missing (⚠)
- **Red (Coral)** - Most items missing (✗)

### Consistency Issues

Shows like-for-like comparisons with:
- Original units reported
- Normalized values (base unit)
- Percentage difference
- Page references for location

### Unit Standardization

Identifies parameters with mixed units:
- Lists all units found
- Shows examples with page references
- Recommends base unit to standardize to

### Threshold Compliance

Validates against IFC limits:
- EXCEEDANCE: Value exceeds limit
- APPROACHING: Value >80% of limit
- COMPLIANT: Within acceptable range

---

## Configuration & Customization

### Modifying Unit Conversions

Edit the `UNIT_CONVERSIONS` dictionary in `analyze_esia_v2.py`:

```python
UNIT_CONVERSIONS = {
    'ha': {'base': 'sq m', 'factor': 10000},
    'km²': {'base': 'sq m', 'factor': 1000000},
    # Add custom conversions here
}
```

### Adding Parameter Contexts

Edit the `PARAMETER_CONTEXTS` dictionary:

```python
PARAMETER_CONTEXTS = {
    'my_context': {
        'patterns': [r'my pattern', r'another pattern'],
        'valid_units': ['unit1', 'unit2'],
    },
    # Add custom contexts here
}
```

### Modifying Gap Analysis Checks

Edit the gap_checks dictionary in `analyze_gaps()` method to add/remove expected content items:

```python
"Project Description": {
    "New Item": r'regex pattern to search for',
}
```

---

## Technical Details

### Dependencies

**Core (no external dependencies):**
- Python standard library only for main analysis

**Optional (for Excel export):**
- `pandas` - Data transformation
- `openpyxl` - Excel file generation with styling

### Performance

- Processes thousands of text chunks efficiently
- Regex-based pattern matching for fact extraction
- Memory-efficient streaming of JSONL input
- Suitable for ESIA reports with 100-1000+ pages

### Browser Compatibility

HTML dashboard works in all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

---

## Project Structure

```
esia-fact-analyzer/
├── analyze_esia_v2.py          # Main analysis script
├── README.md                    # This file
├── SKILL_v2.md                 # Skill documentation
├── ESIA_Report_Final_*         # Sample outputs
└── .git/                       # Version control
```

---

## Example Workflow

```bash
# 1. Extract facts from ESIA PDF (separate tool)
# Output: sample_chunks.jsonl, sample_meta.json

# 2. Run analysis
python analyze_esia_v2.py sample_chunks.jsonl \
    --meta sample_meta.json \
    --output-dir ./results \
    --skill-dir /path/to/skill

# 3. Review outputs
# - Open results/sample_review.html in browser
# - Open results/sample_review.xlsx in spreadsheet

# 4. Interpret findings
# - Check consistency issues for contradictions
# - Review unit standardization for reporting consistency
# - Verify threshold compliance with IFC guidelines
# - Check gap analysis for missing content
```

---

## Troubleshooting

### Excel Export Not Working

```bash
# Install openpyxl
pip install openpyxl

# Check version
python -c "import openpyxl; print(openpyxl.__version__)"
```

### Missing Reference Files

Error: `FileNotFoundError: references/ifc_thresholds.json`

**Solution:** Ensure reference files exist in `{skill_dir}/references/`:
- `ifc_thresholds.json`
- `esia_taxonomy.json`
- `reviewer_checklists.json`

### No Issues/Gaps Detected

This is normal if the document is well-documented. Check:
1. Are facts being extracted correctly?
2. Are regex patterns in reference files comprehensive?
3. Try with different keyword patterns in taxonomy

---

## Version History

### v2.0 (Current)
- **Context-Aware Consistency Checking** - Like-for-like comparisons only
- **Unit Standardization Analysis** - Detect mixed units
- **Enhanced Gap Analysis** - Content extraction with page references
- **Modern Dashboard** - Dark theme, responsive design
- **6-Sheet Excel** - Comprehensive data workbook

### v1.0
- Basic fact categorization
- Simple value comparison
- Basic gap analysis

---

## License & Attribution

Built by Claude (Anthropic) as an AI-assisted ESIA analysis tool.

---

## Support & Documentation

- **SKILL_v2.md** - Detailed skill documentation
- **Sample outputs** - Review included ESIA_Report_Final_* examples
- **Code comments** - Source code includes detailed explanations

---

## Use Cases

### Internal QA
- Pre-submission document quality checks
- Consistency verification across document
- Missing content identification

### Lender/Regulator Compliance
- IFC EHS Guidelines compliance validation
- Environmental baseline adequacy assessment
- Impact assessment completeness review
- Social baseline data verification

### Document Management
- Fact extraction quality assurance
- Unit standardization reporting
- Content coverage metrics

---

## Key Concepts

### Parameter Context
A semantic categorization of measured values. Example: "Study area" is a context that can be measured in ha, km², or m². The tool only compares study area values with other study area values, not with disturbance area values.

### Like-for-Like Comparison
Comparing only similar items. The tool doesn't compare a "study area" value with a "disturbance area" value, even though both are areas. This prevents false positives.

### Normalized Values
Values converted to a standard base unit for comparison. Example: 5 ha normalized to 50,000 sq m.

### Coverage
The proportion of expected content items that were found in the document, expressed as "X/Y found" where X is found items and Y is total expected items.

---

## Contributing

This tool was created by Claude. Feedback and improvements are welcome.

---

**Last Updated:** November 2024
**Version:** 2.0
**Python:** 3.8+
