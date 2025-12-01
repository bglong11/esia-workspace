"""
Example wrapper for your Docling standalone program

This shows how to structure your docling script to work with the ESIA SaaS.

Requirements:
1. Accept PDF path as command-line argument
2. Extract text using Docling
3. Output text to stdout (or save to file)

Usage:
    python docling_wrapper_example.py input.pdf
"""

import sys
import argparse
from pathlib import Path

# ============================================================================
# REPLACE THIS SECTION WITH YOUR ACTUAL DOCLING IMPORTS AND CODE
# ============================================================================

def extract_with_docling(pdf_path: str) -> str:
    """
    Replace this function with your actual docling extraction code

    Example (pseudo-code):
        from docling.document_converter import DocumentConverter

        converter = DocumentConverter()
        result = converter.convert(pdf_path)
        return result.document.export_to_markdown()

    Args:
        pdf_path: Path to PDF file

    Returns:
        Extracted text as string
    """

    # EXAMPLE: This is placeholder code - replace with your docling implementation
    print(f"[INFO] Processing: {pdf_path}", file=sys.stderr)

    # Your docling extraction here:
    # -----------------------------
    # from your_docling_module import extract_pdf
    # text = extract_pdf(pdf_path)
    # return text

    # Placeholder for demonstration:
    return f"""
# Extracted from {Path(pdf_path).name}

This is example text extracted from the PDF.
In your actual implementation, this would be the text extracted by Docling.

## Section 1
Content here...

## Section 2
More content...
"""

# ============================================================================
# END OF REPLACEMENT SECTION
# ============================================================================


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Extract text from PDF using Docling'
    )
    parser.add_argument(
        'pdf_path',
        type=str,
        help='Path to input PDF file'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Optional: Path to output text file (if not provided, prints to stdout)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Validate input
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"[ERROR] File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    if not pdf_path.suffix.lower() == '.pdf':
        print(f"[ERROR] Not a PDF file: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    try:
        # Extract text using docling
        if args.verbose:
            print(f"[INFO] Starting extraction...", file=sys.stderr)

        extracted_text = extract_with_docling(str(pdf_path))

        if args.verbose:
            print(f"[INFO] Extraction complete. Characters: {len(extracted_text)}", file=sys.stderr)

        # Output
        if args.output:
            # Save to file
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(extracted_text)

            if args.verbose:
                print(f"[INFO] Saved to: {output_path}", file=sys.stderr)
        else:
            # Print to stdout (for subprocess capture)
            print(extracted_text)

        sys.exit(0)

    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

"""
# Output to stdout (captured by subprocess):
python docling_wrapper_example.py input.pdf

# Save to file:
python docling_wrapper_example.py input.pdf -o output.txt

# With verbose logging:
python docling_wrapper_example.py input.pdf --verbose
"""

# ============================================================================
# INTEGRATION WITH TASKS.PY
# ============================================================================

"""
The tasks.py file calls this script like:

    result = subprocess.run(
        ['python', 'docling_wrapper_example.py', file_path],
        capture_output=True,
        text=True,
        timeout=600
    )
    extracted_text = result.stdout

Make sure your script:
1. Outputs text to stdout (not stderr)
2. Uses stderr for logging/errors only
3. Exits with code 0 on success, non-zero on error
4. Completes within timeout (default 10 minutes)
"""
