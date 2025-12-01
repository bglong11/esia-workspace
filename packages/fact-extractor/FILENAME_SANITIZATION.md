# Filename Sanitization Guide

## Overview

This document explains the filename sanitization implementation for the ESIA Fact Extractor. Sanitization ensures that uploaded PDF/DOCX files are processed safely throughout the pipeline, preventing security vulnerabilities and filesystem errors.

## Why Sanitization Matters

### Security Risks (Without Sanitization)
- **Path Traversal**: Filenames like `../../../etc/passwd` could access parent directories
- **Injection Attacks**: Special characters could be interpreted as commands
- **Filesystem Errors**: Reserved Windows filenames (CON, PRN, etc.) cause crashes
- **Special Characters**: Unicode and control characters cause encoding issues

### Before & After Examples

| Input Filename | Risk | Sanitized Output |
|---|---|---|
| `NATARBORA PESIA as submitted 2025-02-10.pdf` | Spaces in filenames | `NATARBORA_PESIA_as_submitted_2025-02-10.pdf` |
| `file@#$%.docx` | Invalid characters | `file.docx` |
| `../../../etc/passwd` | Path traversal | `etc_passwd` |
| `CON.pdf` | Reserved name | `CON_file.pdf` |
| `file<>.txt` | Invalid chars | `file.txt` |

## Architecture

### The `FilenameSanitizer` Class

Located in: [file_sanitizer.py](file_sanitizer.py)

#### Core Methods

##### 1. `sanitize(filename: str) -> str`
Sanitizes a filename while preserving the extension.

**Features:**
- Removes path traversal attempts (`..`, `/`, `\`)
- Replaces spaces with underscores
- Removes invalid characters: `< > : " / \ | ? * \x00-\x1f`
- Normalizes Unicode (NFC normalization)
- Removes leading/trailing underscores
- Checks against Windows reserved names
- Enforces max 200-character length

**Examples:**
```python
from file_sanitizer import sanitize_filename

# Spaces to underscores
sanitize_filename("my file.pdf")
# → "my_file.pdf"

# Remove special chars
sanitize_filename("file@#$.docx")
# → "file.docx"

# Path traversal blocked
sanitize_filename("../../../etc/passwd")
# → "etc_passwd"

# Unicode normalized
sanitize_filename("café.pdf")
# → "café.pdf" (NFC normalized)
```

##### 2. `sanitize_path_component(name: str) -> str`
More restrictive sanitization for directory names (no dots allowed).

**Features:**
- Only allows: alphanumeric, underscore, hyphen
- Removes all other characters
- Prevents directory traversal
- Useful for output directory names

**Examples:**
```python
from file_sanitizer import sanitize_path_component

# Convert to safe directory name
sanitize_path_component("output NATARBORA PESIA 2025-02-10")
# → "output_NATARBORA_PESIA_2025-02-10"
```

##### 3. `extract_base_name(filename: str) -> str`
Extracts a clean base name (stem) from filename for directory creation.

**Examples:**
```python
from file_sanitizer import extract_base_name

extract_base_name("NATARBORA PESIA as submitted 2025-02-10.pdf")
# → "NATARBORA_PESIA_as_submitted_2025-02-10"
```

##### 4. `validate_filename(filename: str) -> Tuple[bool, str]`
Validates filename without modification (used by API).

**Returns:** Tuple of (is_valid: bool, reason: str)

**Examples:**
```python
from file_sanitizer import validate_filename

is_valid, reason = validate_filename("normal_file.pdf")
# → (True, "Valid")

is_valid, reason = validate_filename("../../../passwd")
# → (False, "Contains path traversal attempt")
```

## Integration Points

### 1. PDF to Markdown Conversion
**File:** `step1_pdf_to_markdown.py`
**Change:** Uses `extract_base_name()` to sanitize PDF stem before creating markdown filename

```python
from file_sanitizer import extract_base_name

def generate_unique_markdown_filename(pdf_path):
    pdf_name = extract_base_name(pdf_path)  # Sanitized!
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{pdf_name}_{timestamp}.md"

# Input: "NATARBORA PESIA as submitted 2025-02-10.pdf"
# Output: "NATARBORA_PESIA_as_submitted_2025-02-10_20251116_103053.md"
```

### 2. Output Directory Creation
**Files:**
- `run_data_pipeline.py` (lines 120-127)
- `esia_extractor.py` (lines 1306-1309)

**Change:** Uses `sanitize_path_component()` for output directory names

```python
from file_sanitizer import sanitize_path_component

# Before
output_dir = Path(f"output_{pdf_path.stem}")  # May have spaces/special chars

# After
sanitized_name = sanitize_path_component(pdf_path.stem)
output_dir = Path(f"output_{sanitized_name}")
```

### 3. Backend API Upload Handlers
**Files:**
- `saas/backend/main.py` (lines 82-85)
- `saas/backend/main_with_celery.py` (lines 86-89)

**Change:** Added validation before file save

```python
from file_sanitizer import validate_filename

# Validate original filename
is_valid, reason = validate_filename(file.filename)
if not is_valid:
    raise HTTPException(status_code=400, detail=f"Invalid filename: {reason}")

# Still use UUID for actual file storage (secure)
session_id = str(uuid.uuid4())
unique_filename = f"{session_id}{Path(file.filename).suffix}"
```

## File Flow Through Pipeline

```
User uploads PDF/DOCX
        ↓
API validates filename with validate_filename()
        ↓
File stored as UUID (e.g., "a1b2c3d4.pdf") ← Secure!
        ↓
Original filename saved in database
        ↓
Step 1: PDF → Markdown
  Uses extract_base_name() to sanitize stem
  Creates: "NATARBORA_PESIA_as_submitted_2025-02-10_20251116_103053.md"
        ↓
Step 2: Extract Facts
  Receives sanitized markdown filename
  Creates output directory with sanitize_path_component()
  Output: "output_NATARBORA_PESIA_as_submitted_2025-02-10/"
        ↓
Step 3: Generate factsheets
  Uses sanitized directory names throughout
        ↓
Results saved with clean filenames
```

## Character Handling

### Invalid Characters (Removed)
```
< > : " / \ | ? * (and control chars \x00-\x1f)
```

Windows-forbidden characters that are removed.

### Safe Characters (Preserved)
```
a-z A-Z 0-9 _ - . (space → _ for filenames, removed for directories)
```

### Unicode Handling
Files are normalized using NFC (Canonical Decomposition, followed by Canonical Composition).

**Examples:**
```
café (é = e + combining acute) → café (precomposed é)
```

## Security Considerations

### What's Protected

✅ **Path Traversal:** `..` sequences removed
✅ **Directory Escape:** `/` and `\` removed
✅ **Reserved Names:** `CON`, `PRN`, `AUX`, `LPT1`, etc. rejected or prefixed
✅ **Invalid Characters:** Windows-forbidden chars removed
✅ **Length Limits:** Enforced 200-char max
✅ **Injection:** No shell metacharacters allowed

### What's NOT Protected (By Design)

- **Duplicate Prevention:** Multiple files with same name get overwritten
  - *Solution:* Pipeline uses timestamps (step1) and UUIDs (API)
- **Encoding Attacks:** Special Unicode normalization assumed
  - *Solution:* Uses standard NFC normalization

### API Security Model

The backend API uses a **defense-in-depth** approach:

1. **Validation Layer:** `validate_filename()` checks user input
2. **Storage Layer:** `UUID` naming prevents any filename attacks
3. **Database:** Original filename stored separately (for audit trail)
4. **Access:** File served via session_id lookup (not direct filename)

```
User provides: "NATARBORA PESIA as submitted 2025-02-10.pdf"
     ↓ (validate_filename checks this)
Stored as: "a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p.pdf"
     ↓ (UUID prevents tampering)
Database: original_filename = "NATARBORA PESIA as submitted 2025-02-10.pdf"
     ↓ (For audit/display purposes)
Retrieved via: /api/result/a1b2c3d4... (not by filename)
```

## Testing

### Unit Tests

```python
from file_sanitizer import FilenameSanitizer

# Test sanitization
assert FilenameSanitizer.sanitize("my file.pdf") == "my_file.pdf"
assert FilenameSanitizer.sanitize("file@#$.docx") == "file.docx"
assert FilenameSanitizer.sanitize("../../../etc/passwd") == "etc_passwd"

# Test validation
is_valid, reason = FilenameSanitizer.validate_filename("normal.pdf")
assert is_valid == True

is_valid, reason = FilenameSanitizer.validate_filename("../../../etc/passwd")
assert is_valid == False
assert "path traversal" in reason.lower()

# Test directory names
assert FilenameSanitizer.sanitize_path_component("output dir") == "output_dir"
assert FilenameSanitizer.sanitize_path_component("test@#$") == "test"
```

## Common Issues & Solutions

### Issue: Filename has spaces
**Problem:** Causes issues in command-line arguments
**Solution:** `extract_base_name()` converts spaces to underscores

### Issue: Special characters in PDF name
**Problem:** Prevents directory creation
**Solution:** `sanitize_path_component()` removes all invalid chars

### Issue: Reserved Windows names
**Problem:** OS prevents file/folder creation
**Solution:** Detected and prefixed with `_file` or `_dir`

### Issue: Very long filenames
**Problem:** Filesystem limits (usually 255 chars)
**Solution:** Limited to 200 chars with enforcement

## Migration Guide

If you have existing files with unsanitized names:

1. **Identify files:**
   ```bash
   # Find markdown files with spaces/special chars
   find markdown_outputs -name "*[[:space:]]*"
   find output_* -type d -name "*[[:space:]]*"
   ```

2. **Rename safely:**
   ```python
   from pathlib import Path
   from file_sanitizer import sanitize_path_component

   for dir_path in Path("output_*").glob("output_*"):
       if dir_path.is_dir():
           # Create sanitized name
           new_name = Path("output_") / sanitize_path_component(dir_path.name.replace("output_", ""))
           # Backup and move
           dir_path.rename(new_name)
   ```

3. **Update references:**
   - Update database records if storing paths
   - Re-run pipeline for critical documents

## Configuration

No configuration required! The sanitization is automatic in:
- `step1_pdf_to_markdown.py`
- `run_data_pipeline.py`
- `esia_extractor.py`
- Both API versions (`main.py` and `main_with_celery.py`)

## Performance Impact

- **Negligible:** Sanitization uses simple regex operations
- **Time:** < 1ms per filename
- **Memory:** No additional memory overhead
- **Batch Processing:** No performance impact on pipelines

## Future Enhancements

Potential improvements (not implemented yet):
- [ ] Configurable character allowlists
- [ ] Whitelist for additional reserved names (non-Windows)
- [ ] Collision detection and auto-renaming
- [ ] Audit logging of sanitization operations
- [ ] Custom sanitization profiles per environment

## References

- **File naming conventions:** [Wikipedia - Filename](https://en.wikipedia.org/wiki/Filename)
- **Windows reserved names:** [Microsoft Docs](https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file)
- **Unicode normalization:** [Unicode Standard](https://unicode.org/reports/tr15/)
- **Path traversal attacks:** [OWASP](https://owasp.org/www-community/attacks/Path_Traversal)

## Support

For issues with filename sanitization:
1. Check if filename contains invalid characters (< > : " / \ | ? *)
2. Verify filename length < 200 characters
3. Check against Windows reserved names list
4. Validate using `validate_filename()` function
5. Open issue with example filename and error message
