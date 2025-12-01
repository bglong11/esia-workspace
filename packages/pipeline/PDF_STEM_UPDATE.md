# PDF Stem Sanitization - Update

## What Changed

The CLI has been updated to automatically extract and sanitize the PDF filename stem from the input PDF/DOCX file path, instead of requiring manual specification via `--pdf-stem` argument.

## Previous Usage (Old)

```bash
# Had to manually specify stem
python run-esia-pipeline.py --pdf-stem "ESIA_Report_Final_Elang AMNT"
```

## New Usage (Better)

```bash
# Stem is automatically extracted from filename
python run-esia-pipeline.py data/pdfs/ESIA_Report_Final_Elang_AMNT.pdf

# Works with any filename - automatically sanitized
python run-esia-pipeline.py "Project XYZ (Draft).pdf"
python run-esia-pipeline.py "/path/to/my esia report.pdf"
```

## Sanitization Examples

The `sanitize_pdf_stem()` function converts filenames to clean, safe stems:

| Input | Output |
|-------|--------|
| `ESIA Report Final.pdf` | `ESIA_Report_Final` |
| `Project XYZ (Draft).pdf` | `Project_XYZ_Draft` |
| `my-esia-report-v2.pdf` | `my_esia_report_v2` |
| `ESIA (Copy) 2024.pdf` | `ESIA_Copy_2024` |
| `/path/to/file name.pdf` | `file_name` |

## Sanitization Rules

The sanitization process:
1. Extracts filename without extension
2. Replaces spaces and special characters with underscores
3. Removes multiple consecutive underscores
4. Replaces hyphens with underscores (consistency)
5. Removes leading/trailing underscores
6. Result is safe for use in filenames across all operating systems

## CLI Changes

### New Required Argument

```bash
pdf_file          # Path to the PDF or DOCX file (REQUIRED)
```

### Removed Argument

```bash
--pdf-stem        # No longer needed (automatically derived)
```

### Still Available Arguments

```bash
--steps 1,2,3     # Which pipeline steps to run
--verbose/-v      # Enable debug logging
--help/-h         # Show help
--version         # Show version
```

## Usage Examples

### Basic Usage (All Steps)
```bash
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf
```

### Specific Steps
```bash
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 1
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 1,3
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 3
```

### Debug Mode
```bash
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --verbose
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf --steps 1 -v
```

### With Spaces and Special Characters
```bash
python run-esia-pipeline.py "Project ABC (Draft) v2.pdf"
python run-esia-pipeline.py "/path/to/my ESIA report.docx"
```

## Output Files

The output files will use the sanitized stem:

```
Input: "Project XYZ (Draft).pdf"
Sanitized stem: "Project_XYZ_Draft"

Output files:
├─ Project_XYZ_Draft_chunks.jsonl
├─ Project_XYZ_Draft_meta.json
├─ Project_XYZ_Draft_review.html
└─ Project_XYZ_Draft_review.xlsx
```

## Technical Details

### New Function: `sanitize_pdf_stem()`

Located in `run-esia-pipeline.py`

```python
def sanitize_pdf_stem(pdf_path: str) -> str:
    """
    Extract and sanitize filename stem from a PDF/DOCX file path.

    Converts:
    - Spaces → underscores
    - Special characters → underscores
    - Multiple underscores → single underscore
    - Hyphens → underscores (for consistency)

    Returns a safe filename stem.
    """
```

### PDF File Validation

The new `validate_pdf_file()` function ensures:
- File exists
- Path is a file (not directory)
- File extension is .pdf or .docx (warning if different)

```python
def validate_pdf_file(pdf_path: str, logger: logging.Logger) -> Path:
    """Validate that PDF file exists and is readable."""
```

## Implementation Details

### Modified Functions

1. **`run_extractor(pdf_stem, logger)`**
   - Now accepts `pdf_stem` parameter
   - Uses stem for output naming

2. **`sync_outputs_to_analyzer(pdf_stem, logger)`**
   - Now accepts `pdf_stem` parameter
   - Dynamically creates chunk/meta filenames from stem

3. **`run_pipeline(pdf_path, steps, logger)`**
   - Now accepts `pdf_path` parameter
   - Sanitizes the stem internally
   - Passes stem to steps 1 and 2

4. **`parse_arguments()`**
   - Changed from optional `--pdf-stem` to required positional `pdf_file` argument

5. **`main()`**
   - Validates PDF file exists
   - Extracts and sanitizes stem
   - Passes to pipeline

## Benefits

✅ **Easier to Use** - No manual stem specification needed
✅ **Error Reduction** - No mismatched filenames between steps
✅ **Automatic** - Works with any filename format
✅ **Consistent** - Sanitization rules ensure clean output names
✅ **Safer** - Special characters removed prevent file system issues
✅ **Flexible** - Handles spaces, parentheses, version numbers, etc.

## Backward Compatibility

⚠️ **Breaking Change**: Old usage with `--pdf-stem` will no longer work

```bash
# OLD (no longer works)
python run-esia-pipeline.py --pdf-stem "My_Stem"

# NEW (correct usage)
python run-esia-pipeline.py "My_Stem.pdf"
# or
python run-esia-pipeline.py "/path/to/My_Stem.pdf"
```

## Migration Guide

If you have existing scripts:

### Before
```bash
#!/bin/bash
python run-esia-pipeline.py --pdf-stem "ESIA_Report"
```

### After
```bash
#!/bin/bash
# If your PDF is at data/pdfs/ESIA_Report.pdf
python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf

# Or with the full path
python run-esia-pipeline.py "$(pwd)/data/pdfs/ESIA_Report.pdf"
```

## Edge Cases Handled

| Case | Input | Output | Notes |
|------|-------|--------|-------|
| Spaces | `my report.pdf` | `my_report` | ✓ Handled |
| Parentheses | `v(1.0).pdf` | `v_1_0` | ✓ Handled |
| Multiple spaces | `my   report.pdf` | `my_report` | ✓ De-duplicated |
| Leading spaces | ` report.pdf` | `report` | ✓ Trimmed |
| Special chars | `report!@#.pdf` | `report` | ✓ Removed |
| Hyphens | `my-report.pdf` | `my_report` | ✓ Converted |
| No stem | `-.pdf` | Error | ✗ Raises ValueError |
| Wrong extension | `report.txt` | `report` | ⚠️ Warning logged |

## Testing

### Test Basic Sanitization
```bash
python run-esia-pipeline.py "test document.pdf"
# Expected stem: "test_document"
```

### Test Complex Filename
```bash
python run-esia-pipeline.py "Project (Draft) v2.0 - Final.pdf"
# Expected stem: "Project_Draft_v2_0_Final"
```

### Test With Path
```bash
python run-esia-pipeline.py "/path/to/ESIA Report.pdf"
# Expected stem: "ESIA_Report"
```

### Test Validation
```bash
python run-esia-pipeline.py nonexistent.pdf
# Error: "PDF file not found: nonexistent.pdf"
```

## Logging Output

When you run the pipeline, you'll see:

```
2025-11-29 14:30:45 - INFO - Input file: data/pdfs/My Report (Draft).pdf
2025-11-29 14:30:45 - INFO - Sanitized stem: My_Report_Draft
2025-11-29 14:30:45 - DEBUG - ✓ PDF file validated: /absolute/path/My_Report_Draft.pdf
```

This shows you exactly how your filename was sanitized.

## Summary

- **Input**: PDF/DOCX file path
- **Automatic**: Filename is extracted and sanitized
- **Output**: Clean, safe filename stem for all outputs
- **Simple**: One command, no manual configuration needed

```bash
# Before
python run-esia-pipeline.py --pdf-stem "ESIA_Report_Final_Elang AMNT"

# After
python run-esia-pipeline.py "ESIA Report Final Elang AMNT.pdf"
```

Much simpler! 🎉
