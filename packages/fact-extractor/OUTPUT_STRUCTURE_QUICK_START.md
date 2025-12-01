# Output Folder Structure - Quick Start

## The Change

All pipeline outputs are now organized in a single project folder by document name.

### Before (Old)
```
├── markdown_outputs/
│   └── NATARBORA_PESIA_..._20251116.md
└── output_NATARBORA_PESIA/
    ├── esia_mentions.csv
    ├── esia_consolidated.csv
    └── esia_replacement_plan.csv
```

### After (New)
```
NATARBORA_PESIA_as_submitted_2025-02-10/
├── NATARBORA_PESIA_..._20251116.md           ← Markdown in root
├── facts/
│   ├── esia_mentions.csv
│   ├── esia_consolidated.csv
│   └── esia_replacement_plan.csv
├── reports/
│   └── verification_report.md
└── checkpoints/
    └── .checkpoint.pkl
```

## How to Use

Just run normally - organization is automatic:

```bash
python run_data_pipeline.py "My Document.pdf"
```

The script creates:
```
My_Document/
├── my_document_20251116_103053.md  ← Converted PDF (in root)
├── facts/         ← All extracted data
├── reports/       ← Analysis results
└── checkpoints/   ← Resume capability
```

## What's in Each Location

| Location | Contents |
|----------|----------|
| **Root** | Converted markdown file from PDF |
| **facts/** | 4 CSV files with extracted facts |
| **reports/** | Data quality verification report |
| **checkpoints/** | Progress file for resuming |

## File Locations

### CSV Files (Facts)
```
DOCUMENT_NAME/facts/
├── esia_mentions.csv          ← All occurrences
├── esia_consolidated.csv      ← Unique facts
├── esia_replacement_plan.csv  ← Find/replace patterns
└── project_factsheet.csv      ← Categorized facts
```

### Reports
```
DOCUMENT_NAME/reports/
└── verification_report.md     ← Quality analysis
```

### Markdown
```
DOCUMENT_NAME/
└── document_TIMESTAMP.md      ← Converted PDF (in root)
```

## Examples

### Processing One Document
```bash
python run_data_pipeline.py "Environmental Assessment 2025.pdf"

# Creates: Environmental_Assessment_2025/
```

### Processing Multiple Documents
```bash
for pdf in *.pdf; do
    python run_data_pipeline.py "$pdf"
done

# Creates:
# Environmental_Assessment_2025/
# Social_Impact_Study/
# Technical_Report/
# ... one folder per document
```

### Finding Results
```bash
# All results for one document:
cd NATARBORA_PESIA_as_submitted_2025-02-10

# View extracted facts:
cat facts/esia_consolidated.csv

# View quality report:
cat reports/verification_report.md

# View original markdown:
cat markdown/*.md
```

## Backward Compatibility

✅ Old method still works:
```bash
# This still uses flat structure (no subfolders):
python step2_extract_facts.py markdown.md ./my_output_dir
```

✅ New method (recommended):
```bash
# This uses organized structure with subfolders:
python run_data_pipeline.py document.pdf
```

## Resuming from Checkpoint

If extraction was interrupted:

```bash
# New structure - automatic resume:
python run_data_pipeline.py "document.pdf"
# Finds checkpoint in: DOCUMENT_NAME/checkpoints/.checkpoint.pkl
# Resumes from where it left off

# Legacy structure:
python step2_extract_facts.py markdown.md ./output_dir
# Finds checkpoint in: output_dir/.checkpoint.pkl
```

## Accessing Files Programmatically

```python
from output_organizer import OutputOrganizer

# Create organizer
organizer = OutputOrganizer("My Document 2025")
organizer.create_folders()

# Get file paths
markdown = organizer.get_markdown_path("document.md")
facts = organizer.get_facts_path("esia_mentions.csv")
report = organizer.get_report_path("verification_report.md")
checkpoint = organizer.get_checkpoint_path()

# Use them
import pandas as pd
df = pd.read_csv(facts)
```

## Folder Naming

Project folder names are sanitized for safety:

| Input | Output Folder |
|-------|---|
| `My Document.pdf` | `My_Document` |
| `Project & Impact 2025.pdf` | `Project_Impact_2025` |
| `NATARBORA PESIA as submitted 2025-02-10.pdf` | `NATARBORA_PESIA_as_submitted_2025-02-10` |

- Spaces → underscores
- Special chars → removed
- Safe for all operating systems

## Tips

1. **Use `run_data_pipeline.py`** - Automatically creates organized structure
2. **One folder per document** - Easy to find and manage
3. **Archiving** - Zip entire folder for backup:
   ```bash
   zip -r NATARBORA_PESIA.zip NATARBORA_PESIA_as_submitted_2025-02-10/
   ```
4. **Batch processing** - Run on multiple PDFs, get organized results
5. **Share results** - Give entire folder to colleagues

## Common Tasks

### Find all facts for a document
```bash
cat DOCUMENT_NAME/facts/esia_consolidated.csv
```

### Find specific fact
```bash
grep "project area" DOCUMENT_NAME/facts/esia_consolidated.csv
```

### Check extraction quality
```bash
cat DOCUMENT_NAME/reports/verification_report.md
```

### Resume interrupted extraction
```bash
# Automatic if checkpoint exists
python run_data_pipeline.py "document.pdf"
```

### Migrate old results to new structure
```bash
# If you have old flat structure:
# output_NATARBORA_PESIA/esia_mentions.csv
# output_NATARBORA_PESIA/.checkpoint.pkl

# Run migration:
python -c "
from output_organizer import migrate_to_organized_structure
from pathlib import Path
migrate_to_organized_structure(
    Path('output_NATARBORA_PESIA'),
    'NATARBORA PESIA'
)
"
```

## Storage Structure for Teams

### Personal Projects
```
MY_PROJECT_NAME/
├── DOCUMENT_1/
├── DOCUMENT_2/
└── DOCUMENT_3/
```

### Multiple Documents
```
NATARBORA_2025/              ← One document
├── markdown/
├── facts/
├── reports/
└── checkpoints/

ENVIRONMENTAL_STUDY_2025/    ← Another document
├── markdown/
├── facts/
├── reports/
└── checkpoints/
```

## What Changed

✅ **Better organization** - All files together
✅ **Easier to find** - Clear folder structure
✅ **Scale better** - Manage many documents
✅ **Professional** - Looks organized
✅ **Automatic** - No manual setup needed

## Need Help?

See [OUTPUT_STRUCTURE.md](OUTPUT_STRUCTURE.md) for detailed documentation.

---

**TL;DR**: Run `python run_data_pipeline.py "document.pdf"` and your results go in `DOCUMENT_NAME/` with organized subfolders. That's it!
