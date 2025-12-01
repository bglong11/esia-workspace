# Filename Sanitization - Quick Start

## TL;DR

All filenames in the ESIA pipeline are now automatically sanitized. This prevents security issues and filesystem errors.

## What Changed?

✅ **Before:** Filenames with spaces/special chars caused issues
```
NATARBORA PESIA as submitted 2025-02-10.pdf
├── markdown_outputs/NATARBORA PESIA as submitted 2025-02-10_20251116_103053.md
└── output_NATARBORA PESIA as submitted 2025-02-10/
    └── esia_mentions.csv
```

✅ **After:** All filenames are clean and safe
```
NATARBORA PESIA as submitted 2025-02-10.pdf
├── markdown_outputs/NATARBORA_PESIA_as_submitted_2025-02-10_20251116_103053.md
└── output_NATARBORA_PESIA_as_submitted_2025-02-10/
    └── esia_mentions.csv
```

## How to Use

### No Changes Needed!

The sanitization is automatic. Just use the pipeline as normal:

```bash
# All filenames are automatically sanitized
python run_data_pipeline.py "My File With Spaces & Special.pdf"

# Works with API
curl -X POST -F "file=@My File.pdf" http://localhost:8000/api/upload
```

## Supported Conversions

| Input | Output |
|-------|--------|
| Spaces | `_` (underscores) |
| `file@#$.pdf` | `file.pdf` |
| `../../../etc/passwd` | `etc_passwd` |
| `café.pdf` | `café.pdf` (normalized) |

## If You Need to Sanitize Manually

```python
from file_sanitizer import (
    sanitize_filename,           # For files
    sanitize_path_component,     # For directories
    extract_base_name,           # For output directories
    validate_filename            # For validation
)

# Sanitize a filename
clean_name = sanitize_filename("my file.pdf")
# → "my_file.pdf"

# Sanitize a directory name
clean_dir = sanitize_path_component("output NATARBORA 2025")
# → "output_NATARBORA_2025"

# Extract clean base name
base = extract_base_name("NATARBORA PESIA as submitted 2025-02-10.pdf")
# → "NATARBORA_PESIA_as_submitted_2025-02-10"

# Validate a filename
is_valid, reason = validate_filename("../../../etc/passwd")
# → (False, "Contains path traversal attempt")
```

## Files Updated

1. **[file_sanitizer.py](file_sanitizer.py)** - Main sanitization module (NEW)
2. **[step1_pdf_to_markdown.py](step1_pdf_to_markdown.py)** - Uses `extract_base_name()`
3. **[run_data_pipeline.py](run_data_pipeline.py)** - Uses `sanitize_path_component()`
4. **[esia_extractor.py](esia_extractor.py)** - Uses `sanitize_path_component()`
5. **[saas/backend/main.py](saas/backend/main.py)** - Uses `validate_filename()`
6. **[saas/backend/main_with_celery.py](saas/backend/main_with_celery.py)** - Uses `validate_filename()`

## Security

✅ Path traversal blocked (e.g., `../../../etc/passwd`)
✅ Invalid characters removed (e.g., `< > : " / \ | ? *`)
✅ Reserved names handled (e.g., `CON`, `PRN`, `AUX`)
✅ Unicode normalized
✅ Length limits enforced

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Output directory has weird name | This is normal! Check the base PDF filename |
| Filename looks truncated | Max 200 chars enforced. Shorten your PDF name |
| "Invalid filename" error | File has path traversal or reserved name |

## Examples

### Example 1: Simple File
```
Input:  "report.pdf"
Output: "report.pdf"  (no change)
```

### Example 2: File with Spaces
```
Input:  "My Report 2025.pdf"
Output: "My_Report_2025.pdf"
```

### Example 3: File with Special Characters
```
Input:  "Q&A Summary (v2.0).pdf"
Output: "QA_Summary_v2.0.pdf"
```

### Example 4: Full Pipeline
```
Input:  "Environmental Assessment & Social Impact (2025).pdf"
  ↓
Step 1 creates: markdown_outputs/Environmental_Assessment_Social_Impact_2025_20251116_103053.md
  ↓
Step 2 creates: output_Environmental_Assessment_Social_Impact_2025/
  ├── esia_mentions.csv
  ├── esia_consolidated.csv
  ├── esia_replacement_plan.csv
  └── project_factsheet.csv
```

## API Upload

When uploading via the API:

```javascript
// JavaScript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('/api/upload', {
    method: 'POST',
    body: formData
})
.then(res => res.json())
.then(data => {
    console.log('Job ID:', data.job_id);
    // File is automatically validated and stored securely
});
```

The API will:
1. ✅ Validate the filename is safe
2. ✅ Store the file with a UUID name (e.g., `a1b2c3d4.pdf`)
3. ✅ Keep original filename in database
4. ✅ Proceed with sanitization in pipeline

## No Migration Needed

Existing files in your system will continue to work. New files will automatically use sanitized names.

To clean up old files with unsafe names:
```bash
# See which files need cleaning
find markdown_outputs -name "*[[:space:]]*"
find . -type d -name "output *"
```

## Questions?

See [FILENAME_SANITIZATION.md](FILENAME_SANITIZATION.md) for detailed documentation.

## Summary

- ✅ Automatic sanitization across entire pipeline
- ✅ Security hardened against path traversal and injection
- ✅ Backward compatible (old files still work)
- ✅ No configuration needed
- ✅ Transparent to users (just works!)
