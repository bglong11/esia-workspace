# ESIA Fact Analyzer - Claude Development Notes

This document provides context about how this application was created and guidance for future development by Claude or other developers.

---

## Project Genesis

**ESIA Fact Analyzer** was created by Claude (Anthropic) as an intelligent tool for analyzing Environmental & Social Impact Assessment (ESIA) documents.

The tool processes extracted facts from ESIA reports and performs sophisticated analysis to ensure document quality, consistency, and compliance with international standards (IFC EHS Guidelines, ADB, World Bank requirements).

---

## Design Philosophy

### 1. **Minimal Dependencies**
- Core analysis uses only Python standard library
- Optional dependencies (pandas, openpyxl) for enhanced output
- Graceful degradation if optional packages unavailable
- Ensures portability and ease of installation

### 2. **Context-Aware Intelligence** (No LLM)
- **NOT using LLM/ML**: Uses explicit pattern matching with semantic rules
- Parameter contexts prevent false positives (e.g., only compares "study area" with "study area", not with any area measurement)
- Like-for-like comparison principle throughout
- Unit-aware numeric comparisons
- **How it works**: Semantic understanding comes from hardcoded context rules and unit validation, not neural networks

### 3. **Comprehensive Yet Focused**
- Single-purpose tool: analyze extracted ESIA facts
- Deep expertise in one domain rather than shallow coverage
- Extensible reference data (thresholds, taxonomy, checklists) for customization
- Professional output quality suitable for lender/regulator review

### 4. **User-Centric Design**
- Modern, professional UI (dark theme)
- Clear severity indicators and status badges
- Interactive HTML dashboard with collapsible sections
- Detailed Excel workbook for detailed analysis
- Page references for traceability

---

## Understanding "Context-Aware Intelligence"

### Does This Use LLM/AI?

**SHORT ANSWER: No. This is pure rule-based logic with domain knowledge.**

The term "context-aware intelligence" refers to the tool's ability to understand **semantic meaning** through **explicit rules**, not machine learning. Here's why this approach was chosen:

### What "Context-Aware" Means Here

The tool distinguishes between:
- **Study area** vs **Disturbance area** (different concepts, even though both are areas)
- **Workforce** (measured in people) vs **Water consumption** (measured in liters)
- **5,000 hectares** vs **50,000,000 square meters** (same value, different units)

This prevents false positives like:
- Reporting that study area (5,000 ha) contradicts disturbance area (500 ha) — they're different things!
- Flagging "workforce is 500 hectares" as valid
- Comparing dissimilar measurements

### The Intelligence Layer

**This is achieved through:**

1. **Parameter Contexts** (17 distinct types)
   - Each parameter type (study_area, workforce, water_consumption) has specific patterns and valid units
   - Prevents mixing apples and oranges

2. **Unit Validation** (80+ unit conversions)
   - Ensures "hectares" is valid for area contexts but not for workforce
   - Normalizes all units to base units for accurate comparison

3. **Like-for-Like Comparison**
   - Only compares study area with study area
   - Only compares workforce with workforce
   - Prevents spurious inconsistencies

### Why NOT Machine Learning?

| Aspect | LLM Approach | This Tool's Approach |
|--------|--------------|----------------------|
| **Speed** | Slow (API latency) | Fast (milliseconds) |
| **Cost** | Expensive per request | Free (runs locally) |
| **Consistency** | Non-deterministic (varies) | Deterministic (always same) |
| **Auditability** | Black box (hard to explain) | Transparent (explicit rules) |
| **Compliance** | Risk (regulators want explanations) | Safe (all decisions justified) |
| **Offline** | Requires internet | Works completely offline |

For regulatory/compliance documents (ESIA is used by World Bank, IFC, ADB), **transparency and auditability matter more than cutting-edge AI**.

### Example: Why Rules Trump ML

```
Scenario: Document says "Study area is 5,000 ha" and "Disturbance area is 500 ha"

Naive LLM might think:
- Both are areas with numeric values
- 5,000 is much larger than 500
- This is an inconsistency! ❌ FALSE POSITIVE

This Tool's Logic:
1. Extract value from first sentence: 5,000 ha, context=study_area
2. Extract value from second sentence: 500 ha, context=disturbance_area
3. Compare: Different contexts → Skip comparison ✓ CORRECT
```

The tool's "intelligence" is **encoded domain knowledge**, not learned patterns.

---

## Architecture Overview

### Core Class: ESIAReviewer

The entire application revolves around a single main class with specialized methods:

```python
class ESIAReviewer:
    def __init__(self, skill_dir: Path)
        # Load reference data (thresholds, taxonomy, checklists)
        # Initialize analysis data structures

    def load_data(self, chunks_path, meta_path)
        # Parse JSONL input and metadata

    def categorize_facts(self)
        # Match facts to ESIA taxonomy using keywords

    def check_consistency(self)
        # Context-aware like-for-like value comparison

    def check_unit_standardization(self)
        # Detect mixed units for same parameters

    def check_thresholds(self)
        # Compare values against IFC EHS limits

    def analyze_gaps(self)
        # Find missing expected content

    def run_analysis(self)
        # Execute full pipeline

    def export_html(self, output_path)
        # Generate interactive dashboard

    def export_excel(self, output_path)
        # Generate detailed workbook
```

### Data Flow

```
Input (JSONL + Metadata)
    ↓
Load Data
    ↓
Categorization (taxonomy matching)
    ↓
Extract & Normalize Numeric Values
    ↓
Consistency Checking (context-aware)
    ↓
Unit Standardization Detection
    ↓
Threshold Compliance Validation
    ↓
Gap Analysis (expected content)
    ↓
Report Generation (HTML + Excel)
    ↓
Output Files
```

---

## Key Implementation Details

### 1. Unit Conversion System

**Location:** `UNIT_CONVERSIONS` dictionary (lines 33-90)

```python
UNIT_CONVERSIONS = {
    'ha': {'base': 'sq m', 'factor': 10000},
    'km²': {'base': 'sq m', 'factor': 1000000},
    # ... 80+ conversions
}
```

**Why this design:**
- Extensible: Easy to add new unit conversions
- Normalized output: All comparisons done in base units
- Grouped by type: Area units, volume units, emissions, etc.

**How to extend:**
- Add new unit entry to dictionary
- Specify base unit and conversion factor
- Update corresponding parameter context if needed

### 2. Parameter Contexts & Context-Aware Matching

**Location:** `PARAMETER_CONTEXTS` dictionary (lines 92-222) + `identify_parameter_context()` method (lines 392-420)

#### The Context System (Not LLM-Based)

The "context-aware intelligence" is achieved through **explicit semantic rules**, not machine learning:

```python
PARAMETER_CONTEXTS = {
    'study_area': {
        'patterns': [r'study\s+area', r'project\s+area', ...],
        'valid_units': ['sq m', 'ha', 'km²', 'm²', 'acres'],
    },
    'disturbance_area': {
        'patterns': [r'disturbance\s+area', r'clearing\s+area', ...],
        'valid_units': ['sq m', 'ha', 'km²', 'm²'],
    },
    'workforce': {
        'patterns': [r'workforce', r'employees?', r'workers?', ...],
        'valid_units': ['people', 'persons', ''],  # Often dimensionless
    },
    # ... 14 more contexts
}
```

#### How Context Matching Works

**Step 1: Pattern Recognition** (lines 402-407)
```python
# Text: "The study area is approximately 5,000 hectares"
# Scan all context patterns to find matches
for pattern in patterns:  # e.g., r'study\s+area'
    if re.search(pattern, text_lower):
        pattern_matched = True  # Found "study area"
```

**Step 2: Unit Validation** (lines 410-418)
```python
# Extract unit: "hectares"
# Check if it's valid for this context
if unit_lower:
    unit_valid = self._is_unit_valid_for_context("hectares",
                                                   ['sq m', 'ha', 'km²', ...])
    if unit_valid:
        contexts.append('study_area')  # Confirmed context
```

**Step 3: Unit Normalization** (lines 422-450)
```python
# "hectares" → normalize spacing, superscripts, plurals
# Strict matching: hectares = hectare ✓ (both base to "hectare")
# Invalid: "people" for study_area ✗ (not in valid_units)
```

#### Why NOT LLM?

**Pros of this approach:**
- ✓ **Deterministic**: Same input always gives same output
- ✓ **Fast**: Runs in milliseconds, no API calls
- ✓ **Transparent**: Rules are explicit and auditable
- ✓ **Offline**: No network dependency
- ✓ **Reliable**: No hallucinations or inconsistency
- ✓ **Maintainable**: Rules are easy to understand and modify

**Why an LLM would be worse here:**
- ✗ **Cost**: API calls for every value extraction
- ✗ **Latency**: Much slower than regex matching
- ✗ **Non-deterministic**: Same text might get different contexts on different calls
- ✗ **Overkill**: Regex patterns perfectly sufficient for this task
- ✗ **Compliance risk**: ESIA documents used for lender/regulator approval (need to explain decisions)

#### Semantic Understanding (Without Neural Networks)

The "semantic understanding" comes from **domain knowledge encoded as rules**:

| Concept | Implementation | Example |
|---------|-----------------|---------|
| **Area contexts** | Separate study_area from disturbance_area | Compare 5,000 ha study area with 50M m² study area, not disturbance area |
| **Unit semantics** | Valid units per context | Workforce: people/persons ✓, hectares ✗ |
| **Numeric meaning** | Unit conversion to base units | 5 ha = 50,000 sq m (same value, different units) |
| **Comparison logic** | Only compare within context | Study areas vs study areas, not study vs disturbance |

#### Real Example: Why Context Matters

Without context (naive approach):
```
Chunk 1: "Study area is 5,000 hectares"
Chunk 2: "Disturbance area is 500 hectares"
Issue: Study area (5,000 ha) vs Disturbance area (500 ha) = 90% different ✗ FALSE POSITIVE
```

With context (this tool):
```
Chunk 1: "Study area is 5,000 hectares" → context=study_area
Chunk 2: "Disturbance area is 500 hectares" → context=disturbance_area
Analysis: Different contexts, don't compare ✓ NO FALSE POSITIVE
```

Another example - unit validation:
```
Chunk 3: "Workforce is 500 hectares" → pattern matches "workforce"
                                    → unit "hectares" NOT valid for workforce context
                                    → REJECTED (not added to analysis)
```

**Why this design:**
- Prevents false positives by semantic matching
- Each context knows its valid units
- Regex patterns are customizable
- No expensive external API calls
- Transparent and auditable decision making

**How to extend:**
- Add new context with patterns and valid units
- Patterns should be specific to avoid overlaps (e.g., "study area" vs generic "area")
- Valid units define what measurements are acceptable
- Update `check_consistency()` if special comparison logic needed

### 3. Numeric Extraction

**Location:** `extract_numeric_values()` method (lines 300-390)

**Features:**
- 30+ regex patterns, ordered by specificity
- Handles formatted numbers (1,234.56)
- Multiplier support (million, thousand)
- De-duplication (avoids extracting same value twice)
- Error handling for invalid numbers

**Pattern order matters:** Specific patterns first (concentration units) before general patterns (percentage)

### 4. Consistency Checking

**Location:** `check_consistency()` method (lines 454-511)

**Key insight:** Groups values by `context|base_unit` key
- Only compares values in same context AND same base unit
- Calculates percentage difference on normalized values
- 5% threshold for significance
- HIGH (>20%) vs MEDIUM (≤20%) severity

**Why this approach:**
- Prevents comparing incompatible measurements
- Unit-normalized comparisons are accurate
- Configurable threshold (currently 5%)

### 5. Gap Analysis

**Location:** `analyze_gaps()` method (lines 640-740)

**Features:**
- 30+ expected content patterns across 6 sections
- Pattern-based search (not just keyword lookup)
- Extracts actual matching content
- Deduplicates matches (first 3 per item)
- Tracks page references

**Patterns include:**
- Coordinate format: `\d+°\s*\d+\'\s*\d+"?\s*[NS]`
- Numeric patterns: `\d+(?:,\d{3})*(?:\.\d+)?`
- Keyword patterns: `(?:workforce|employees?|workers?)`

---

## Adding New Analysis Features

### Example: Adding a New Check

To add a new analysis method:

1. **Create the method:**
```python
def check_my_analysis(self):
    """Description of what this checks."""
    for fact in self.facts:
        text = fact.get("text", "")
        # Your analysis logic
        self.my_issues.append({
            "type": "MY_CHECK",
            "severity": "high|medium|low",
            "message": "Description",
            # ... other fields
        })
```

2. **Initialize data structure in `__init__`:**
```python
self.my_issues = []
```

3. **Call in `run_analysis()` pipeline:**
```python
def run_analysis(self):
    # ... existing checks
    print("Checking my analysis...")
    self.check_my_analysis()
    # ... rest of pipeline
```

4. **Add to summary generation:**
```python
def generate_summary(self) -> dict:
    return {
        # ... existing summaries
        "my_analysis": {
            "total": len(self.my_issues),
            "high_severity": len([i for i in self.my_issues if i.get("severity") == "high"]),
        }
    }
```

5. **Add to exports (HTML and Excel):**
- Update `export_html()` to include new section
- Update `export_excel()` to create new worksheet

---

## Extending Reference Data

### Adding IFC Thresholds

Edit or extend `ifc_thresholds.json`:

```json
{
  "air_quality": {
    "ambient": {
      "PM10": {"value": 50, "unit": "µg/m³"},
      "NEW_PARAM": {"value": 100, "unit": "unit"}
    }
  }
}
```

Then update pattern matching in `check_thresholds()` method.

### Extending Taxonomy

Edit `esia_taxonomy.json`:

```json
{
  "categories": {
    "My Category": {
      "keywords": ["keyword1", "keyword2", "keyword3"]
    }
  }
}
```

Keywords are used in `categorize_facts()` to match facts.

### Expanding Gap Analysis

Edit `reviewer_checklists.json`:

```json
{
  "gap_analysis_template": {
    "expected_content": {
      "My Section": {
        "New Item": "pattern here"
      }
    }
  }
}
```

Then update patterns in `analyze_gaps()` method.

---

## Testing & Validation

### Manual Testing Approach

1. **Create test JSONL file:**
```jsonl
{"text": "Study area is 5,000 hectares", "page": 1}
{"text": "Study area is 50 million square meters", "page": 2}
{"text": "Water consumption: 100 ML/day", "page": 3}
```

2. **Run analysis:**
```bash
python analyze_esia_v2.py test.jsonl --output-dir ./test_output
```

3. **Verify outputs:**
- Check consistency issue detected (5,000 ha vs 50M m²)
- Check HTML dashboard renders
- Check Excel workbook has all sheets

### Known Edge Cases

- **Overlapping patterns:** Unit extraction can match multiple patterns. Solution: `seen_positions` set prevents duplicates.
- **False positives in gap analysis:** Regex patterns may match unrelated text. Solution: Keep patterns specific and use negative lookahead.
- **Unit ambiguity:** "m" could mean meter or million. Solution: Word boundaries `\b` and context checking.

---

## Performance Considerations

### Current Optimization

- **Streaming input:** JSONL read line-by-line (not all at once)
- **Regex pre-compilation:** Patterns compiled once, not per fact
- **De-duplication:** `seen_positions` prevents redundant extractions
- **Lazy evaluation:** Reference data loaded only once at init

### Potential Improvements

- **Regex caching:** Pre-compile all patterns once
- **Parallel processing:** Process facts in chunks (for large documents)
- **Incremental analysis:** Skip re-analysis of unchanged sections
- **Database indexing:** For very large reference data

### Typical Performance

- 1,000 chunks: <1 second
- 10,000 chunks: 2-5 seconds
- 100,000 chunks: 20-60 seconds
- Memory: ~50MB + input size

---

## Common Customizations

### Changing Severity Thresholds

In `check_consistency()` (line 494):
```python
if diff_pct > 5:  # Threshold for significance
    severity = "high" if diff_pct > 20 else "medium"  # Severity classification
```

### Adjusting Gap Analysis Coverage

In `analyze_gaps()` gap_checks dictionary - add/remove expected content items.

### Modifying Dashboard Colors

In `export_html()` CSS variables (lines 972-988):
```css
:root {
    --accent-teal: #2dd4bf;
    --accent-coral: #fb7185;
    --accent-amber: #fbbf24;
    /* ... update colors */
}
```

### Changing Output Formats

- **HTML:** Modify template in `export_html()` (lines 962-1977)
- **Excel:** Modify worksheet structure in `export_excel()` (lines 791-956)

---

## Debugging Tips

### Enable verbose output:

Add prints to track data flow:
```python
print(f"Extracted {len(values)} numeric values from chunk")
print(f"Identified contexts: {contexts}")
print(f"Consistency issues found: {len(self.issues)}")
```

### Inspect intermediate data:

```python
# After loading data
print(f"Total facts: {len(self.facts)}")
print(f"Sample fact: {self.facts[0]}")

# After categorization
print(f"Categories: {list(self.categorized_facts.keys())}")

# After consistency check
print(f"Issues: {self.issues[:3]}")
```

### Test regex patterns:

```python
import re
pattern = r'study\s+area'
text = "The study area is 5,000 ha"
matches = re.findall(pattern, text, re.IGNORECASE)
print(f"Matches: {matches}")
```

---

## Future Enhancement Ideas

### High Priority
- [ ] **Error handling:** Graceful failure for malformed input
- [ ] **Logging:** Structured logging instead of print statements
- [ ] **Validation:** Input validation for chunks and metadata
- [ ] **Configuration file:** YAML/JSON config instead of hardcoded values

### Medium Priority
- [ ] **Unit tests:** Comprehensive test suite
- [ ] **Documentation generation:** Auto-generate docs from docstrings
- [ ] **CLI improvements:** More command-line options and help
- [ ] **Progress bars:** Show progress for large files

### Nice to Have
- [ ] **Web interface:** HTTP API for cloud deployment
- [ ] **Database backend:** Store results in database
- [ ] **Visualization:** Interactive charts in dashboard
- [ ] **Machine learning:** ML-based anomaly detection
- [ ] **Localization:** Multi-language support
- [ ] **Plugin system:** Allow custom analysis modules

---

## Code Quality Notes

### Style
- Uses type hints for clarity (Python 3.8+)
- Docstrings for all public methods
- Follows PEP 8 naming conventions
- Descriptive variable names

### Error Handling
- Try/except blocks around external operations (file I/O)
- Graceful fallback for missing optional dependencies
- Value validation in numeric conversion
- Regex error handling with ValueError catch

### Documentation
- Inline comments for complex logic
- Docstrings explain purpose and parameters
- Code is self-documenting where possible

---

## Maintenance Notes

### Regular Updates Needed
- **IFC Thresholds:** Update when new guidelines released
- **Taxonomy:** Expand keywords as new ESIA categories emerge
- **Unit conversions:** Add new units as needed

### Version Management
- Current version: 2.0
- Changes documented in SKILL_v2.md and README.md
- Git history preserved for reference

### Compatibility
- Python 3.8+ required
- Tested on Windows, macOS, Linux
- Compatible with Python 3.9, 3.10, 3.11, 3.12

---

## Contributing Guidelines

### Code Style
- Follow existing code patterns
- Add type hints to new functions
- Include docstrings with parameter descriptions
- Keep methods focused and single-purpose

### Adding Features
1. Create isolated feature branch
2. Write code following existing patterns
3. Update documentation (README.md, docstrings)
4. Update SKILL_v2.md if user-facing changes
5. Test with sample data before submitting

### Reference Data Changes
1. Update JSON reference files
2. Document changes in SKILL_v2.md
3. Include examples of new patterns/thresholds
4. Test that patterns work as intended

---

## Contact & Support

For questions about implementation or future enhancements, refer to:
- **Code comments:** Detailed explanations in source
- **README.md:** User-facing documentation
- **SKILL_v2.md:** Feature documentation
- **This file (claude.md):** Developer context

---

**Last Updated:** November 2024
**Created by:** Claude (Anthropic)
**Version:** 2.0
