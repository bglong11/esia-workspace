"""
Test Docling Installation and Extraction
Phase 1: Verify Docling works with PDF and DOCX files

Run this script to test Docling before integrating into the pipeline.
"""

import sys
from pathlib import Path
import time


def test_installation():
    """Test if Docling is installed correctly"""
    print("=" * 80)
    print("Phase 1: Testing Docling Installation")
    print("=" * 80)
    print()

    try:
        from docling.document_converter import DocumentConverter
        print("✓ Docling imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import Docling: {e}")
        print()
        print("Installation instructions:")
        print("  pip install docling")
        return False


def test_pdf_extraction(pdf_path: str = None):
    """Test PDF extraction with Docling"""
    print("\n" + "-" * 80)
    print("Test 1: PDF Extraction")
    print("-" * 80)

    from docling.document_converter import DocumentConverter

    # Use sample file if provided, otherwise create a test message
    if pdf_path and Path(pdf_path).exists():
        print(f"Testing with: {pdf_path}")

        try:
            start_time = time.time()

            # Create converter
            converter = DocumentConverter()
            print("  Converter created...")

            # Convert document
            print("  Converting document...")
            result = converter.convert(pdf_path)

            # Export to markdown
            print("  Exporting to markdown...")
            markdown_text = result.document.export_to_markdown()

            elapsed = time.time() - start_time

            # Display results
            print(f"\n✓ PDF extraction successful!")
            print(f"  Time: {elapsed:.2f} seconds")
            print(f"  Characters extracted: {len(markdown_text):,}")
            print(f"  Lines: {markdown_text.count(chr(10)):,}")

            # Show preview
            print("\nPreview (first 500 characters):")
            print("-" * 40)
            print(markdown_text[:500])
            print("-" * 40)

            return True, markdown_text

        except Exception as e:
            print(f"\n✗ PDF extraction failed: {e}")
            return False, None
    else:
        print(f"⚠ No PDF file provided or file not found: {pdf_path}")
        print("  Skipping PDF test")
        return None, None


def test_docx_extraction(docx_path: str = None):
    """Test DOCX extraction with Docling"""
    print("\n" + "-" * 80)
    print("Test 2: DOCX Extraction")
    print("-" * 80)

    from docling.document_converter import DocumentConverter

    if docx_path and Path(docx_path).exists():
        print(f"Testing with: {docx_path}")

        try:
            start_time = time.time()

            # Create converter
            converter = DocumentConverter()
            print("  Converter created...")

            # Convert document
            print("  Converting document...")
            result = converter.convert(docx_path)

            # Export to markdown
            print("  Exporting to markdown...")
            markdown_text = result.document.export_to_markdown()

            elapsed = time.time() - start_time

            # Display results
            print(f"\n✓ DOCX extraction successful!")
            print(f"  Time: {elapsed:.2f} seconds")
            print(f"  Characters extracted: {len(markdown_text):,}")
            print(f"  Lines: {markdown_text.count(chr(10)):,}")

            # Show preview
            print("\nPreview (first 500 characters):")
            print("-" * 40)
            print(markdown_text[:500])
            print("-" * 40)

            return True, markdown_text

        except Exception as e:
            print(f"\n✗ DOCX extraction failed: {e}")
            return False, None
    else:
        print(f"⚠ No DOCX file provided or file not found: {docx_path}")
        print("  Skipping DOCX test")
        return None, None


def test_markdown_quality(markdown_text: str):
    """Verify markdown structure and quality"""
    print("\n" + "-" * 80)
    print("Test 3: Markdown Quality Check")
    print("-" * 80)

    if not markdown_text:
        print("⚠ No markdown text to check")
        return False

    checks = []

    # Check 1: Has content
    has_content = len(markdown_text) > 100
    checks.append(("Has substantial content", has_content))

    # Check 2: Has headers
    has_headers = "#" in markdown_text
    checks.append(("Contains markdown headers", has_headers))

    # Check 3: Has paragraphs
    has_paragraphs = "\n\n" in markdown_text
    checks.append(("Contains paragraph breaks", has_paragraphs))

    # Check 4: Not just whitespace
    is_meaningful = len(markdown_text.strip()) > 50
    checks.append(("Contains meaningful text", is_meaningful))

    # Display results
    all_passed = True
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"  {status} {check_name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n✓ Markdown quality check passed!")
    else:
        print("\n⚠ Some quality checks failed")

    return all_passed


def create_sample_files():
    """Create sample test files if they don't exist"""
    print("\n" + "-" * 80)
    print("Creating Sample Test Files")
    print("-" * 80)

    # Note: We can't actually create PDF/DOCX files here without dependencies
    # This is just a placeholder
    print("⚠ Sample file creation not implemented")
    print("  Please provide your own PDF or DOCX files for testing")
    print()
    print("Suggested test files:")
    print("  - sample_esia.md (convert to PDF)")
    print("  - Any ESIA document in PDF format")
    print("  - Any ESIA document in DOCX format")


def main():
    """Main test runner"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Test Docling installation and extraction'
    )
    parser.add_argument(
        '--pdf',
        type=str,
        help='Path to PDF file for testing'
    )
    parser.add_argument(
        '--docx',
        type=str,
        help='Path to DOCX file for testing'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Optional: Save extracted text to file'
    )

    args = parser.parse_args()

    # Test 1: Installation
    if not test_installation():
        print("\n" + "=" * 80)
        print("FAILED: Docling is not installed correctly")
        print("=" * 80)
        return False

    # Test 2: PDF extraction
    pdf_success, pdf_text = test_pdf_extraction(args.pdf)

    # Test 3: DOCX extraction
    docx_success, docx_text = test_docx_extraction(args.docx)

    # Test 4: Quality check
    if pdf_text:
        test_markdown_quality(pdf_text)
    elif docx_text:
        test_markdown_quality(docx_text)

    # Save output if requested
    if args.output and (pdf_text or docx_text):
        output_text = pdf_text or docx_text
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"\n✓ Extracted text saved to: {args.output}")

    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)

    results = []
    results.append(("Docling Installation", True))
    if pdf_success is not None:
        results.append(("PDF Extraction", pdf_success))
    if docx_success is not None:
        results.append(("DOCX Extraction", docx_success))

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {test_name}")

    all_passed = all(result[1] for result in results if result[1] is not None)

    if all_passed:
        print("\n" + "=" * 80)
        print("✓ All tests passed! Docling is ready to use.")
        print("=" * 80)
        print("\nNext steps:")
        print("  1. Proceed with Phase 2: Update core extractor")
        print("  2. Say 'implement phase 2' to continue")
    else:
        print("\n" + "=" * 80)
        print("⚠ Some tests failed. Please address issues before proceeding.")
        print("=" * 80)

    return all_passed


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
