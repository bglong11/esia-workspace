---
name: esia-reviewer
description: Analyzes JSONL output from ESIA fact extraction to organize facts for internal QA and external reviewer compliance (IFC, ADB, World Bank). Features context-aware consistency checking, unit standardization analysis, IFC threshold validation, gap analysis with content extraction, and a modern dark-themed dashboard. Trigger with "activate esia reviewer" or when user needs to review extracted ESIA facts.
---

# ESIA Reviewer v2.0

Analyze extracted ESIA facts for internal quality assurance and external lender/regulator compliance review.

## What's New in v2.0

### Context-Aware Consistency Checking
- **Like-for-like comparisons**: Only compares values within the same parameter context (e.g., study area vs study area, not any area value)
- **Normalized values**: Converts all units to base units for accurate comparison
- **17 parameter contexts**: study_area, concession_area, disturbance_area, buffer_zone, population, affected_households, workforce, water_consumption, power_capacity, emissions_ghg, noise_level, air_quality_pm, rainfall, temperature, etc.

### Unit Standardization Analysis
- **Detects mixed units**: Identifies when the same parameter is reported using different units (e.g., study area as 1.2 ha AND 12,000 m²)
- **Recommendations**: Suggests which base unit to standardize to
- **80+ unit conversions**: Supports area (ha, km², m², acres), length (km, m), volume (ML, kL, L, m³), mass/emissions (t, tCO2e), concentrations, power (MW, GW), and more

### Enhanced Gap Analysis
- **Collapsible section headings**: Project Description, Physical Baseline, Biological Baseline, Social Baseline, Impact Assessment, Mitigation & Management
- **Coverage indicators**: Shows "X/Y found" for each section
- **Sub-section column**: Lists specific expected content items
- **Content extraction**: Shows actual text found in the document
- **Page references**: Content displayed with page numbers in square brackets [p.XX]
- **Expanded checks**: 30+ expected content items across 6 categories

### Redesigned Dashboard
- **Dark theme**: Modern, professional appearance with high contrast
- **Typography**: Instrument Serif for headings, Space Mono for data, DM Sans for body text
- **Animated elements**: Subtle fade-in animations for sections
- **Responsive design**: Adapts to desktop, tablet, and mobile
- **Card-based layout**: Unit standardization issues displayed as actionable cards

## Workflow

### Step 1: Prepare Input Files

Place your input files in the `./data/analysis_inputs` folder:

```bash
# Create the input folder if it doesn't exist
mkdir -p ./data/analysis_inputs

# Copy your files there:
# - chunks.jsonl (required)
# - meta.json (optional)
```

### Step 2: Run Analysis

**Option A: Use default folder**
```bash
python analyze_esia_v2.py
```
Automatically looks for:
- `./data/analysis_inputs/chunks.jsonl`
- `./data/analysis_inputs/meta.json` (optional)

**Option B: Custom input folder**
```bash
python analyze_esia_v2.py --input-dir /path/to/your/data
```

**Option C: Custom filenames**
```bash
python analyze_esia_v2.py \
    --input-dir ./data/analysis_inputs \
    --chunks my_chunks.jsonl \
    --meta my_metadata.json
```

**Option D: Custom output folder**
```bash
python analyze_esia_v2.py --output-dir ./my_results
```

The script performs:
1. **Fact categorization** - Maps facts to ESIA taxonomy
2. **Context-aware consistency checking** - Detects inconsistent values only for the same parameter type
3. **Unit standardization analysis** - Identifies parameters reported with mixed units
4. **Gap analysis with content extraction** - Identifies missing content and extracts found content with page references

### Step 3: Review Outputs

Two output files generated in `./data/analysis_outputs` (or custom `--output-dir`):
- `{basename}_review.html` - Interactive dark-themed dashboard with collapsible sections
- `{basename}_review.xlsx` - Detailed workbook with enhanced Gap Analysis sheet

### Step 4: Interpret Results

**Gap Analysis Section:**
- Click section headers (📋 Project Description, 🌍 Physical Baseline, etc.) to expand/collapse
- Coverage pill shows how many items found vs expected (e.g., "5/7 found")
- Sub-section column lists the specific expected content
- Content Found column shows actual extracted text with page references [p.XX]
- Status badges: PRESENT (green) or MISSING (red)

**Consistency Issues Section:**
- Shows only like-for-like comparisons
- Values displayed in original units AND normalized to base unit
- Percentage difference calculated on normalized values

**Unit Standardization Section:**
- Lists parameters where multiple units are used
- Shows examples with page references
- Provides recommended standard unit

## Gap Analysis Categories

| Section | Sub-sections Checked |
|---------|---------------------|
| Project Description | Location Coordinates, Project Area, Workforce Numbers, Water Consumption, Power Consumption, Project Duration, Capital Cost |
| Physical Baseline | Ambient Air Quality, Noise Measurements, Water Quality Data, Rainfall Data, Seismic Assessment, Climate Data, Topography |
| Biological Baseline | Species Lists, IUCN Status, Protected Areas, Critical Habitat, Endemic Species |
| Social Baseline | Population Data, Household Data, Livelihood Sources, Vulnerable Groups, Land Tenure, Indigenous Peoples |
| Impact Assessment | Significance Criteria, Cumulative Impacts, Transboundary Impacts |
| Mitigation & Management | ESMP Reference, Monitoring Plan, Emergency Response |

## Parameter Contexts

| Context | Patterns Matched |
|---------|------------------|
| study_area | study area, project area, assessment area, survey area |
| concession_area | concession area, mining area, license area, permit area |
| disturbance_area | disturbance area, clearing area, footprint, impact area |
| buffer_zone | buffer zone, exclusion zone, setback |
| population | population, residents, inhabitants |
| affected_households | affected households, displaced households, impacted households |
| workforce | workforce, employees, workers, staff, personnel |
| water_consumption | water consumption, water demand, water use |
| power_capacity | power capacity, installed capacity, generation capacity |
| emissions_ghg | GHG emissions, greenhouse gas, carbon emissions, tCO2e |

## Unit Conversions

**Area → sq m:**
- 1 ha = 10,000 sq m
- 1 km² = 1,000,000 sq m
- 1 acre = 4,046.86 sq m

**Volume → L:**
- 1 ML = 1,000,000 L
- 1 kL = 1,000 L
- 1 m³ = 1,000 L

**Emissions → t:**
- 1 kt = 1,000 t
- 1 Mt = 1,000,000 t

## Dependencies

Required: Python 3.8+
Optional (for Excel export): pandas, openpyxl

```bash
pip install pandas openpyxl --break-system-packages
```

## Output Interpretation

**Severity Levels:**
- HIGH: Likely to cause rejection by lenders (fix before submission)
- MEDIUM: May require clarification (address if time permits)
- LOW: Minor quality issues (note for future)

**Coverage Status (Gap Analysis):**
- Green pill (teal): All items found
- Amber pill: Some items missing
- Red pill (coral): Most items missing

**Unit Standardization Status:**
- Shows count of different units used for each parameter
- Highlights normalized values for comparison
- Provides recommended base unit
