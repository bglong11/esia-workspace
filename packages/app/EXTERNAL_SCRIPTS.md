# Integrating External Python Scripts

This guide shows how to configure and integrate Python scripts from separate folders into the ESIA pipeline.

## Quick Start

### 1. Update `pipeline.config.js`

Modify the `steps` array to point to your script locations. Support for both **relative** and **absolute** paths:

```javascript
steps: [
  {
    id: 'extract',
    name: 'Extract Text',
    script: '../extraction_module/extract.py',  // Relative path
    args: ['{PDF_FILE}', '{SANITIZED_NAME}'],
    timeout: 300000,
  },
  {
    id: 'validate',
    name: 'Validate ESIA',
    script: 'C:/Users/user/esia_tools/validate.py',  // Absolute path (Windows)
    args: ['{PDF_FILE}', '--strict'],
    timeout: 300000,
  },
]
```

## Path Types

### Relative Paths
Resolved relative to the project root (where `esv` application lives):

```javascript
// From esv/ to ../extraction_module/extract.py
script: '../extraction_module/extract.py'

// From esv/ to scripts/ subfolder
script: './scripts/extract.py'
```

### Absolute Paths
Full path to the script (no resolution):

```javascript
// Linux/Mac
script: '/home/user/esia_processing/extract.py'

// Windows
script: 'C:/Users/user/esia_processing/extract.py'
script: 'C:\\Users\\user\\esia_processing\\extract.py'
```

## Script Arguments

Your Python scripts receive arguments in the order specified in `args`. Three placeholders are automatically replaced:

| Placeholder | Replaced With | Example |
|---|---|---|
| `{PDF_FILE}` | Full path to uploaded PDF | `/path/to/data/pdfs/123456-report.pdf` |
| `{SANITIZED_NAME}` | Clean root name | `report` |
| `{ROOT_NAME}` | Alias for SANITIZED_NAME | `report` |

### Example Configuration

```javascript
{
  id: 'extract',
  script: '../esia_tools/extract_text.py',
  args: ['{PDF_FILE}', '{SANITIZED_NAME}', '--output', './output'],
}
```

### What Your Script Receives

```bash
python ../esia_tools/extract_text.py /absolute/path/to/data/pdfs/123456-report.pdf report --output ./output
```

### Environment Variables

Scripts also receive environment variables:

```python
import os

pdf_file = os.environ.get('PDF_FILE')  # /absolute/path/to/data/pdfs/123456-report.pdf
sanitized_name = os.environ.get('SANITIZED_NAME')  # report
root_name = os.environ.get('ROOT_NAME')  # report
```

## Writing Your Python Scripts

### Basic Template

```python
#!/usr/bin/env python3
import sys
import os

def main():
    # Get arguments from command line
    if len(sys.argv) < 2:
        print("Usage: extract.py <pdf_path> <sanitized_name>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    sanitized_name = sys.argv[2]

    # Or get from environment
    pdf_file = os.environ.get('PDF_FILE')
    sanitized = os.environ.get('SANITIZED_NAME')

    print(f"Processing: {pdf_path}")
    print(f"Output name: {sanitized_name}")

    # Your processing logic here

    # Exit with code 0 on success, non-zero on failure
    sys.exit(0)

if __name__ == '__main__':
    main()
```

### With Output Files

```python
import sys
import os
from pathlib import Path

def main():
    pdf_path = sys.argv[1]
    sanitized_name = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else './data/output'

    # Create output directory if needed
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Process PDF
    result = extract_text(pdf_path)

    # Save output
    output_file = Path(output_dir) / f"{sanitized_name}_extracted.txt"
    output_file.write_text(result)

    print(f"Extracted text saved to {output_file}")
    sys.exit(0)

def extract_text(pdf_path):
    # Your extraction logic
    return "extracted content"

if __name__ == '__main__':
    main()
```

## Example Configuration

### Scenario: Scripts in Different Folders

```
home/user/
├── esia_extraction/
│   └── extract.py
├── esia_validation/
│   └── validate.py
├── esia_tools/
│   └── sanitize.py
└── esv/  (this application)
    ├── pipeline.config.js
    └── pipelineExecutor.js
```

**pipeline.config.js:**

```javascript
steps: [
  {
    id: 'extract',
    name: 'Extract Text',
    script: '../esia_extraction/extract.py',
    args: ['{PDF_FILE}', '{SANITIZED_NAME}', '--output', './data/extracted'],
    timeout: 300000,
  },
  {
    id: 'validate',
    name: 'Validate ESIA',
    script: '../esia_validation/validate.py',
    args: ['{PDF_FILE}', '--strict', '--report', './data/validation/{SANITIZED_NAME}.json'],
    timeout: 300000,
  },
  {
    id: 'sanitize',
    name: 'Sanitize & Normalize',
    script: '../esia_tools/sanitize.py',
    args: ['{PDF_FILE}', '{SANITIZED_NAME}', '--format', 'json'],
    timeout: 300000,
  },
]
```

## Error Handling

Scripts should:
- **Exit with code 0** on success
- **Exit with non-zero code** on failure
- **Print error messages to stderr** for logging

```python
import sys

try:
    result = process_file(pdf_path)
except Exception as e:
    print(f"ERROR: {str(e)}", file=sys.stderr)
    sys.exit(1)

sys.exit(0)
```

## Troubleshooting

### Script Not Found

If you see: `Warning: Script not found at...`

Check:
1. Script path is correct (use absolute paths if unsure)
2. File exists at that location
3. Correct path separators for your OS (forward slash `/` works on all)

### Script Fails to Execute

Check:
1. Python is installed and accessible (`python --version`)
2. Script has execute permissions on Linux/Mac: `chmod +x script.py`
3. Script has required dependencies installed
4. Check server logs for error messages

### Script Times Out

Scripts have a 5-minute timeout by default. Increase if needed:

```javascript
{
  id: 'heavy_processing',
  script: '../tools/slow_process.py',
  timeout: 900000,  // 15 minutes
}
```

## Dependencies

If your scripts have Python dependencies, install them:

```bash
# In your script's directory
pip install -r requirements.txt

# Or install specific packages
pip install pdfplumber pandas numpy
```

## Testing Scripts Locally

Before integrating, test scripts standalone:

```bash
# Test extract script
python ../esia_extraction/extract.py ./data/pdfs/test.pdf test_output

# Test with environment variables
export PDF_FILE=./data/pdfs/test.pdf
export SANITIZED_NAME=test
python ../esia_extraction/extract.py
```

## Complete Example

### Python Script: `extract_text.py`

```python
#!/usr/bin/env python3
"""Extract text from PDF files."""

import sys
import os
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("ERROR: pdfplumber not installed. Run: pip install pdfplumber")
    sys.exit(1)

def extract_text(pdf_path, output_name, output_dir='./data/extracted'):
    """Extract text from PDF."""

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Extract text
    extracted_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            extracted_text.append(f"--- Page {i+1} ---\n{text}")

    # Save output
    output_file = Path(output_dir) / f"{output_name}.txt"
    output_file.write_text('\n\n'.join(extracted_text))

    print(f"Extracted {len(pdf.pages)} pages")
    print(f"Saved to {output_file}")

    return str(output_file)

def main():
    if len(sys.argv) < 2:
        print("Usage: extract_text.py <pdf_path> [output_name] [output_dir]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else 'extracted'
    output_dir = sys.argv[3] if len(sys.argv) > 3 else './data/extracted'

    try:
        extract_text(pdf_path, output_name, output_dir)
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### Configuration in `pipeline.config.js`

```javascript
{
  id: 'extract',
  name: 'Extract Text',
  script: '../esia_extraction/extract_text.py',
  args: ['{PDF_FILE}', '{SANITIZED_NAME}', './data/extracted'],
  timeout: 300000,
}
```

When user uploads `report.pdf`, this will run:
```bash
python ../esia_extraction/extract_text.py /absolute/path/to/report.pdf report ./data/extracted
```

And output will be saved to `./data/extracted/report.txt`

