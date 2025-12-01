# ESIA Fact Analyzer - Setup & Usage Guide

## Quick Start

### 1. Prepare Your Data

Create the input folder and place your files:

```bash
# Create input folder
mkdir -p ./data/analysis_inputs

# Place your files here:
# - chunks.jsonl (required)
# - meta.json (optional)
```

### 2. Run the Analysis

```bash
# Use default folders
python analyze_esia_v2.py
```

Results will be saved to `./data/analysis_outputs/`

---

## File Structure

```
esia-fact-analyzer/
├── analyze_esia_v2.py                    # Main script
├── data/
│   ├── analysis_inputs/                  # Input folder
│   │   ├── chunks.jsonl                  # Required
│   │   └── meta.json                     # Optional
│   └── analysis_outputs/                 # Output folder
│       ├── {name}_review.html            # Dashboard
│       └── {name}_review.xlsx            # Excel report
├── README.md
├── SKILL_v2.md
└── ...
```

---

## Command Examples

### Basic Usage

```bash
# Default behavior (looks in ./data/analysis_inputs)
python analyze_esia_v2.py
```

Output: `./data/analysis_outputs/`

### Custom Input Folder

```bash
python analyze_esia_v2.py --input-dir ./my_data
```

Expects:
- `./my_data/chunks.jsonl`
- `./my_data/meta.json` (optional)

### Custom Output Folder

```bash
python analyze_esia_v2.py --output-dir ./results
```

### Custom Filenames

If your files have different names:

```bash
python analyze_esia_v2.py \
    --input-dir ./data/analysis_inputs \
    --chunks my_chunks.jsonl \
    --meta my_metadata.json
```

### Short Options

```bash
# -i for input directory
python analyze_esia_v2.py -i ./my_data

# -o for output directory
python analyze_esia_v2.py -o ./results

# Combined
python analyze_esia_v2.py -i ./input -o ./output
```

### Custom Skill Directory

```bash
python analyze_esia_v2.py --skill-dir /path/to/skill
```

---

## Parameter Reference

| Parameter | Short | Type | Default | Description |
|-----------|-------|------|---------|-------------|
| `--input-dir` | `-i` | Path | `./data/analysis_inputs` | Folder containing input files |
| `--chunks` | - | String | `chunks.jsonl` | Chunks filename in input folder |
| `--meta` | - | String | `meta.json` | Metadata filename in input folder |
| `--output-dir` | `-o` | Path | `./data/analysis_outputs` | Folder for output reports |
| `--skill-dir` | - | Path | Parent dir | Location of reference data |
| `--help` | `-h` | - | - | Show help message |

---

## Error Messages

### "Chunks file not found"

**Error:**
```
ERROR: Chunks file not found: ./data/analysis_inputs/chunks.jsonl
Expected to find 'chunks.jsonl' in: ./data/analysis_inputs
```

**Solution:**
1. Check if `./data/analysis_inputs/` exists
2. Verify `chunks.jsonl` is in that folder
3. Use `--chunks` to specify a different filename

### "Permission denied"

**Error:**
```
PermissionError: [Errno 13] Permission denied: './data/analysis_outputs'
```

**Solution:**
1. Check folder permissions
2. Use a different output folder: `--output-dir ./my_results`
3. Create the folder manually: `mkdir -p ./data/analysis_outputs`

---

## Input File Format

### chunks.jsonl (Required)

Newline-delimited JSON with extracted facts:

```jsonl
{"text": "The study area is 5,000 hectares...", "page": 15, "section": "Project Description"}
{"text": "Workforce will be approximately 500 people...", "page": 22, "section": "Project Description"}
```

**Required fields:**
- `text` - Fact content
- `page` - Page number (can be "?" if unknown)

**Optional fields:**
- `section` - Document section
- `metadata` - Additional context

### meta.json (Optional)

Document metadata:

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

## Output Files

### HTML Report: `{name}_review.html`

Interactive dashboard with:
- **4 Stat Cards**: Chunks analyzed, consistency issues, unit variations, content gaps
- **Consistency Issues**: Like-for-like comparison with normalized values
- **Unit Standardization**: Mixed unit detection and recommendations
- **Content Coverage**: Taxonomy breakdown with progress bars
- **Gap Analysis**: Collapsible sections for 6 ESIA categories

Open in any web browser.

### Excel Report: `{name}_review.xlsx`

5-sheet workbook:
1. **Summary** - Key statistics
2. **Fact Categories** - Categorization breakdown
3. **Consistency Issues** - Detected inconsistencies
4. **Unit Standardization** - Mixed unit issues
5. **Gap Analysis** - Missing/present content

---

## Troubleshooting

### Python not found

```bash
# Check Python installation
python --version

# On some systems, use python3
python3 analyze_esia_v2.py
```

### Missing dependencies

```bash
# Install required packages
pip install pandas openpyxl
```

### Syntax errors

```bash
# Verify the script is valid
python -m py_compile analyze_esia_v2.py
```

---

## Workflow Examples

### Example 1: Standard Analysis

```bash
# Setup
mkdir -p ./data/analysis_inputs
cp my_chunks.jsonl ./data/analysis_inputs/chunks.jsonl
cp my_metadata.json ./data/analysis_inputs/meta.json

# Run
python analyze_esia_v2.py

# Results in ./data/analysis_outputs/
```

### Example 2: Multiple Projects

```bash
# Project A
mkdir -p ./projects/project_a/inputs
cp project_a_chunks.jsonl ./projects/project_a/inputs/chunks.jsonl
python analyze_esia_v2.py -i ./projects/project_a/inputs -o ./projects/project_a/outputs

# Project B
mkdir -p ./projects/project_b/inputs
cp project_b_chunks.jsonl ./projects/project_b/inputs/chunks.jsonl
python analyze_esia_v2.py -i ./projects/project_b/inputs -o ./projects/project_b/outputs
```

### Example 3: Custom Filenames

```bash
mkdir -p ./data/analysis_inputs
cp elang_facts.jsonl ./data/analysis_inputs/
cp elang_meta.json ./data/analysis_inputs/

python analyze_esia_v2.py \
    --chunks elang_facts.jsonl \
    --meta elang_meta.json
```

---

## Features

The analysis includes:

✅ **Fact Categorization** - 11 ESIA categories
✅ **Consistency Checking** - 17 parameter contexts
✅ **Unit Standardization** - 80+ unit conversions
✅ **Gap Analysis** - 30+ expected content items
✅ **Professional Reports** - HTML & Excel

See [README.md](README.md) and [SKILL_v2.md](SKILL_v2.md) for detailed documentation.

---

## Questions?

See the examples in the help:

```bash
python analyze_esia_v2.py --help
```

Or refer to:
- **README.md** - Comprehensive documentation
- **SKILL_v2.md** - Feature documentation
- **ANALYSIS_EXAMPLE.md** - Real-world example

---

**Version:** 2.0.1
**Last Updated:** November 28, 2024
