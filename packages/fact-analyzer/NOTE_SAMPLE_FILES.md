# Sample Files Note

## About ESIA_Report_Final_Elang_AMNT_review.html

**Status:** Sample file (generated with v2.0, before removals)
**Date Modified:** November 27, 2024 (before threshold removal)

### Important

The HTML file in the repository is a **sample output** from an earlier version (v2.0) that still included the IFC Threshold Compliance section.

## Updated Code

The current code (`analyze_esia_v2.py`) has been updated to remove the threshold section:

✅ **What's been removed from the code:**
- IFC Threshold Compliance HTML section
- Threshold Compliance Excel sheet
- Threshold stat card from dashboard
- Threshold checks from analysis pipeline
- Threshold console output

✅ **What's been refactored:**
- CLI parameters (now uses `./data/analysis_inputs/` by default)
- Input/output folder structure
- Help text with examples

## Regenerating Sample Files

If you want to regenerate sample output files with the current code:

```bash
# 1. Place sample input files
mkdir -p ./data/analysis_inputs
cp /path/to/sample_chunks.jsonl ./data/analysis_inputs/chunks.jsonl
cp /path/to/sample_meta.json ./data/analysis_inputs/meta.json

# 2. Run the analysis
python analyze_esia_v2.py

# 3. New files generated in ./data/analysis_outputs/
```

## Sample File State

| File | Status | Version | Notes |
|------|--------|---------|-------|
| `ESIA_Report_Final_Elang_AMNT_review.html` | Old | v2.0 | Still has IFC Threshold section (for reference) |
| `ESIA_Report_Final_Elang_AMNT_review.xlsx` | Old | v2.0 | Still has Threshold Compliance sheet (for reference) |
| Code in `analyze_esia_v2.py` | Current | v2.0.1 | No threshold sections |

## What to Expect

When you run the current code with input files, you'll get:

**HTML Dashboard:**
- 4 stat cards (not 5)
  - Chunks Analyzed
  - Consistency Issues
  - Unit Variations
  - Content Gaps

- 3 main sections (not 4)
  - Consistency Issues
  - Unit Standardization
  - Content Coverage
  - Gap Analysis

**Excel Workbook:**
- 5 sheets (not 6)
  - Summary
  - Fact Categories
  - Consistency Issues
  - Unit Standardization
  - Gap Analysis

## To Update Sample Files

**Option 1: Delete old samples**
```bash
rm ESIA_Report_Final_Elang_AMNT_review.*
```
New samples will be generated when you run analysis.

**Option 2: Keep them for reference**
The old samples are useful to see what v2.0 looked like. They won't affect the tool's operation.

## Recommendation

The old sample files serve as documentation of v2.0 output format. They don't need to be deleted or updated - they're just reference materials. When you run the tool with your own data, it will generate new files with the current code (v2.0.1).

---

**Version:** 2.0.1
**Date:** November 28, 2024
**Code Status:** Current - No threshold sections
**Sample Files:** Old - Still have threshold sections (for reference)
