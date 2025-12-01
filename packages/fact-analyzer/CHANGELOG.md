# Changelog

## Version 2.0.1 (November 27, 2024)

### Removed Features

**IFC Threshold Compliance Section** - Removed from both HTML and Excel outputs

#### What Was Removed:

1. **HTML Dashboard Section**
   - "IFC Threshold Compliance" section (formerly with badge "EHS Guidelines")
   - Table showing parameter, measured value, IFC limit, status, and page references
   - Featured parameters: PM10, PM2.5, SO2, NO2 (air quality), Noise, pH, BOD, COD, TSS (water quality)

2. **Excel Workbook Sheet**
   - Removed "Threshold Compliance" sheet from workbook (was sheet #5)
   - Columns: Parameter, Category, Value, Threshold, Unit, Status, Page, Source
   - Color-coded status rows: Red (EXCEEDANCE), Yellow (APPROACHING), Green (COMPLIANT)

3. **Dashboard Statistics Card**
   - Removed stat card showing "Threshold Issues" count from top metrics grid
   - Was showing exceedances of IFC limits

4. **Analysis Pipeline**
   - Removed `check_thresholds()` method call from main analysis pipeline
   - Method still exists in code but no longer executed
   - Removed threshold check print message from console output

5. **Documentation**
   - Removed IFC Thresholds section from SKILL_v2.md
   - Updated workflow documentation to remove threshold validation step
   - Updated output interpretation guide

### Updated Files

| File | Changes |
|------|---------|
| `analyze_esia_v2.py` | Removed ~107 lines (threshold HTML, Excel export, pipeline call, console output) |
| `SKILL_v2.md` | Removed IFC thresholds reference table, updated workflow docs |
| `README.md` | Updated feature list and pipeline description |
| `ANALYSIS_EXAMPLE.md` | Already did not include threshold analysis |

### Functionality Preserved

The following features remain unchanged:

✓ Fact Categorization
✓ Context-Aware Consistency Checking
✓ Unit Standardization Analysis
✓ Gap Analysis with Content Extraction
✓ HTML Dashboard
✓ Excel Workbook (5 sheets instead of 6)

### Output Changes

**HTML Dashboard:**
- Now shows 4 stat cards instead of 5 (removed Threshold Issues card)
- Dashboard animation delays adjusted (delay-4 now points to Content Gaps)

**Excel Workbook:**
- Sheets reduced from 6 to 5
- New sheet order:
  1. Summary
  2. Fact Categories
  3. Consistency Issues
  4. Unit Standardization
  5. Gap Analysis *(was #6, now #5)*

**Console Output:**
- Removed threshold exceedance line from final summary
- Summary now shows:
  - Document name
  - Chunks analyzed
  - Consistency issues
  - Unit standardization issues
  - Content gaps

### Code Stability

✓ Script remains fully functional
✓ No dependencies affected
✓ No breaking changes to input/output formats
✓ Backward compatible with existing JSONL inputs
✓ `check_thresholds()` method preserved (not used)

### Future Considerations

If threshold compliance checking is needed again:
1. Method `check_thresholds()` still exists in code
2. Reference data: IFC EHS threshold standards still available in skill directory
3. To re-enable: Add `check_thresholds()` call back to `run_analysis()` pipeline
4. Restore Excel sheet creation and HTML section as needed

---

## Version 2.0 (Initial Release)

### Features

- Fact Categorization (ESIA taxonomy mapping)
- Context-Aware Consistency Checking (17 parameter contexts)
- Unit Standardization Analysis (80+ unit conversions)
- IFC Threshold Compliance (air quality, noise, water, GHG)
- Gap Analysis (30+ expected content items across 6 sections)
- Interactive HTML Dashboard (dark theme, responsive)
- Detailed Excel Workbook (6 sheets, styled)

### Key Improvements from v1.0

- Like-for-like comparison prevents false positives
- Unit validation per context
- Content extraction with page references
- Modern UI design
- Comprehensive reporting

---

**Removal Date:** November 27, 2024
**Reason:** User request to focus on core analysis (consistency, units, gaps)
**Status:** Complete - All threshold checks removed from user-facing output
