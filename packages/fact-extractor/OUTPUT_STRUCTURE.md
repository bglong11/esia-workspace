# Output Folder Structure - Organized Organization

## Overview

The pipeline now organizes all output files in a clean folder structure based on the sanitized filename. Instead of scattered files and separate directories, everything related to one document is organized in a single project folder.

## New Folder Structure

### Before (Legacy - Scattered)
```
root/
├── markdown_outputs/
│   ├── NATARBORA_PESIA_..._20251116_103053.md
│   └── other_documents.md
├── output_NATARBORA_PESIA/
│   ├── esia_mentions.csv
│   ├── esia_consolidated.csv
│   ├── esia_replacement_plan.csv
│   └── project_factsheet.csv
└── run_data_pipeline.py
```

### After (New - Organized)
```
root/
└── NATARBORA_PESIA_as_submitted_2025-02-10/  ← Single project folder
    ├── NATARBORA_PESIA_as_submitted_2025-02-10_20251116_103053.md  ← Markdown in root
    ├── facts/
    │   ├── esia_mentions.csv
    │   ├── esia_consolidated.csv
    │   ├── esia_replacement_plan.csv
    │   └── project_factsheet.csv
    ├── reports/
    │   └── verification_report.md
    └── checkpoints/
        └── .checkpoint.pkl  (for resuming extraction)
```

## Benefits

✅ **Organized**: All files for one document in one place
✅ **Clean**: No scattered markdown_outputs directories
✅ **Scalable**: Easy to manage multiple documents
✅ **Safe**: Checkpoint files in dedicated subdir
✅ **Professional**: Clear folder hierarchy
✅ **Logical**: Grouped by file type (markdown, facts, reports)

## Folder Structure Details

### Project Root Folder
**Name**: Sanitized version of PDF/document filename
- Example: `NATARBORA_PESIA_as_submitted_2025-02-10`
- Spaces → underscores
- Special chars removed
- Length limited to 200 chars
- Safe for all operating systems

### Markdown File (In Root)
**Location**: Project root folder (not in a subdirectory)
- **File**: `DOCUMENT_NAME_TIMESTAMP.md`
- **Size**: Same as source PDF (in text form)
- **Purpose**: Converted markdown for extraction
- **Timestamp**: Ensures unique names if converted multiple times

**Example**:
```
NATARBORA_PESIA_as_submitted_2025-02-10/
├── NATARBORA_PESIA_as_submitted_2025-02-10_20251116_103053.md  ← Markdown here
├── facts/
├── reports/
└── checkpoints/
```

### facts/ Subdirectory
**Contents**: All extracted facts in CSV format
- **esia_mentions.csv** - All fact occurrences (with quotes and page #)
- **esia_consolidated.csv** - Unique facts (aggregated)
- **esia_replacement_plan.csv** - Regex patterns for document editing
- **project_factsheet.csv** - Facts organized by category/section

**Example**:
```
facts/
├── esia_mentions.csv              (10,000+ rows for large docs)
├── esia_consolidated.csv          (100-500 rows, unique facts)
├── esia_replacement_plan.csv      (Replacement patterns)
└── project_factsheet.csv          (Categorized facts)
```

### reports/ Subdirectory
**Contents**: Analysis and quality reports
- **verification_report.md** - Data quality assessment
- Markdown format for easy reading
- Includes statistics and error analysis

**Example**:
```
reports/
└── verification_report.md         (Summary, conflicts, errors)
```

### checkpoints/ Subdirectory
**Contents**: Progress checkpoints for resuming
- **.checkpoint.pkl** - Pickle file with extraction progress
- Created every 5 chunks during extraction
- Automatically deleted on successful completion
- Allows resume if extraction is interrupted

**Example**:
```
checkpoints/
└── .checkpoint.pkl                (Resume capability)
```

## File Descriptions

### esia_mentions.csv
All occurrences of extracted facts with evidence.

| Column | Content |
|--------|---------|
| name | Fact name (e.g., "Project area") |
| type | "quantity" or "categorical" |
| value | Extracted value |
| unit | Unit of measurement |
| normalized_value | Standardized numeric value |
| normalized_unit | Standardized unit (e.g., "ha", "MW") |
| evidence | Quote from document |
| page | Page number |
| chunk_id | Chunk identifier |
| signature | Slugified fact name (for grouping) |

### esia_consolidated.csv
Unique facts with occurrence statistics.

| Column | Content |
|--------|---------|
| signature | Fact identifier |
| name | Fact name |
| type | quantity or categorical |
| value | Primary value |
| unit | Primary unit |
| normalized_value | Standardized value |
| normalized_unit | Standardized unit |
| occurrences | How many times this fact appears |
| has_conflict | True if conflicting values found |
| conflict_description | Details of conflicts if found |

### esia_replacement_plan.csv
Regex patterns for finding and replacing facts in document.

| Column | Content |
|--------|---------|
| fact_name | Which fact this pattern is for |
| pattern | Regular expression to find |
| replacement_suggestion | Suggested replacement text |

### project_factsheet.csv
Facts organized by LLM-categorized project sections.

| Column | Content |
|--------|---------|
| signature | Fact identifier |
| name | Fact name |
| value | Extracted value |
| unit | Unit |
| category | Project section (e.g., "Environmental Impacts") |
| subcategory | Detailed category |
| confidence | "high", "medium", or "low" |
| rationale | Why this categorization was chosen |
| occurrences | How many times found |

## Usage Examples

### Example 1: Single Document Processing

```bash
# Input: NATARBORA PESIA as submitted 2025-02-10.pdf

python run_data_pipeline.py "NATARBORA PESIA as submitted 2025-02-10.pdf"

# Creates:
# NATARBORA_PESIA_as_submitted_2025-02-10/
# ├── NATARBORA_PESIA_as_submitted_2025-02-10_20251116_103053.md  ← Markdown in root
# ├── facts/
# │   ├── esia_mentions.csv
# │   ├── esia_consolidated.csv
# │   ├── esia_replacement_plan.csv
# │   └── project_factsheet.csv
# ├── reports/
# │   └── verification_report.md
# └── checkpoints/
#     └── .checkpoint.pkl
```

### Example 2: Batch Processing Multiple Documents

```bash
for pdf in *.pdf; do
    python run_data_pipeline.py "$pdf"
done

# Creates separate organized folders for each:
# NATARBORA_PESIA_2025-02-10/
# ENVIRONMENTAL_ASSESSMENT_2025/
# SOCIAL_IMPACT_STUDY_2024/
# ... etc
```

### Example 3: Finding Results for a Specific Document

```bash
# All results are in one place:
NATARBORA_PESIA/

# To find facts:
cat NATARBORA_PESIA/facts/esia_consolidated.csv

# To find report:
cat NATARBORA_PESIA/reports/verification_report.md

# To find original markdown:
cat NATARBORA_PESIA/markdown/NATARBORA*.md
```

## Backward Compatibility

✅ **Legacy structure still works**
- If you specify `--output-dir`, the old flat structure is used
- Checkpoints work with both old and new structures
- No breaking changes to existing workflows

```bash
# Old way (flat structure) still works:
python step2_extract_facts.py markdown_outputs/doc.md ./my_output_dir

# New way (organized structure - automatic):
python run_data_pipeline.py document.pdf
```

## How It Works

### Step 1: PDF to Markdown
```
Input: NATARBORA PESIA as submitted 2025-02-10.pdf
       ↓ (sanitize filename)
       NATARBORA_PESIA_as_submitted_2025-02-10
       ↓ (create project folder and subfolders)
       NATARBORA_PESIA_as_submitted_2025-02-10/markdown/
       ↓
Output: NATARBORA_PESIA_as_submitted_2025-02-10/markdown/NATARBORA_PESIA_..._20251116.md
```

### Step 2: Fact Extraction
```
Input: Markdown file from Step 1
       ↓
Process: Extract facts chunk by chunk
       ↓
       NATARBORA_PESIA_as_submitted_2025-02-10/facts/
       ↓
Outputs:
  - esia_mentions.csv
  - esia_consolidated.csv
  - esia_replacement_plan.csv
  - project_factsheet.csv
```

### Step 3: Analysis & Reporting
```
Input: Extracted facts from Step 2
       ↓
Process: Analyze quality, categorize, generate report
       ↓
       NATARBORA_PESIA_as_submitted_2025-02-10/reports/
       ↓
Output: verification_report.md
```

## Integration Points

### In run_data_pipeline.py
```python
from output_organizer import create_output_structure

# Create organized structure
organizer = create_output_structure(pdf_path.stem, root_dir=".")
output_dir = organizer.get_project_dir()

# All subsequent steps use output_dir
# Subdirectories created automatically
```

### In esia_extractor.py
```python
# Detects structure automatically
facts_dir = output_path / "facts"
if facts_dir.exists():
    # Using new organized structure
    csv_path = facts_dir / "esia_mentions.csv"
else:
    # Using legacy flat structure
    csv_path = output_path / "esia_mentions.csv"
```

### Checkpoint Support
```python
# Automatically uses correct location
checkpoint = output_path / "checkpoints" / ".checkpoint.pkl"  # New
# Or fallback to:
checkpoint = output_path / ".checkpoint.pkl"  # Legacy
```

## File Naming

### Project Folder Name
**Format**: Sanitized base filename
**Example**: `NATARBORA_PESIA_as_submitted_2025-02-10`

Rules:
- Spaces → underscores
- Special chars removed
- Lowercase conversion applied (except within name)
- Maximum 200 characters
- No path traversal characters (../)
- Safe on Windows, macOS, Linux

### Markdown File Name
**Format**: `SANITIZED_NAME_TIMESTAMP.md`
**Example**: `NATARBORA_PESIA_as_submitted_2025-02-10_20251116_103053.md`

- Timestamp ensures uniqueness
- Format: YYYYMMDD_HHMMSS
- One markdown per conversion (no overwrites)

### CSV File Names
**Fixed names**:
- `esia_mentions.csv` - All occurrences
- `esia_consolidated.csv` - Unique facts
- `esia_replacement_plan.csv` - Replacement patterns
- `project_factsheet.csv` - Categorized facts

## Accessing Files Programmatically

### Using OutputOrganizer

```python
from output_organizer import OutputOrganizer

organizer = OutputOrganizer("NATARBORA PESIA 2025-02-10")
organizer.create_folders()

# Get specific file paths
markdown = organizer.get_markdown_path("document.md")
facts = organizer.get_facts_path("esia_mentions.csv")
report = organizer.get_report_path("verification_report.md")
checkpoint = organizer.get_checkpoint_path()

# Get all files at once
all_files = organizer.get_all_output_files()
for file_type, path in all_files.items():
    print(f"{file_type}: {path}")
```

### Print Structure

```python
organizer = OutputOrganizer("My Document 2025")
organizer.create_folders()
organizer.print_structure()

# Output:
# =====================================
# OUTPUT FOLDER STRUCTURE
# =====================================
#
# Root: /path/to/My_Document_2025
#
# My_Document_2025/
# ├── markdown/
# │   └── document.md
# ...
```

## Migration from Legacy Structure

If you have existing output in legacy flat structure:

```python
from output_organizer import migrate_to_organized_structure

# Migrate old structure to new one
organizer = migrate_to_organized_structure(
    legacy_dir=Path("output_NATARBORA_PESIA"),
    base_name="NATARBORA PESIA"
)

# Files automatically moved:
# output_NATARBORA_PESIA/esia_mentions.csv → NATARBORA_PESIA/facts/esia_mentions.csv
# output_NATARBORA_PESIA/.checkpoint.pkl → NATARBORA_PESIA/checkpoints/.checkpoint.pkl
```

## Performance Impact

- **Negligible**: Extra folder creation has minimal overhead
- **Memory**: No additional memory required
- **Speed**: Same extraction speed (folder structure doesn't affect processing)
- **Disk**: Same disk space used (just organized differently)

## Troubleshooting

### Issue: Files scattered in multiple locations

**Solution**: Use `python run_data_pipeline.py` instead of running steps manually. This ensures organized structure.

### Issue: Can't find expected CSV files

**Solution**: Check if document was processed with new pipeline:
```bash
# New structure:
DOCUMENT_NAME/facts/esia_mentions.csv

# Old structure (if --output-dir was specified):
output_dir/esia_mentions.csv
```

### Issue: Resume doesn't work

**Solution**: Check checkpoint location:
```bash
# New structure:
ls DOCUMENT_NAME/checkpoints/.checkpoint.pkl

# Old structure:
ls output_dir/.checkpoint.pkl
```

## Best Practices

1. **Use run_data_pipeline.py** for full pipeline - creates organized structure automatically
2. **Don't manually move files** - organizer handles placement
3. **Keep project folders** - easy to find results later
4. **Archive complete projects** - zip entire folder for long-term storage
5. **Use relative paths** - easier to move projects around

## Summary

The new output structure provides:
✅ **Organization** - All files for one document together
✅ **Clarity** - Logical folder hierarchy
✅ **Scalability** - Easy to manage multiple documents
✅ **Compatibility** - Works with old structure too
✅ **Professionalism** - Clean, organized results

Simply use `python run_data_pipeline.py "document.pdf"` and everything is organized automatically!
