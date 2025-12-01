"""
Full Pipeline Test: Test complete extraction with Docling

Tests the entire pipeline from document upload through fact extraction.
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from core.extractor import process_document


def test_full_pipeline(file_path: str):
    """Test complete extraction pipeline"""
    print("=" * 80)
    print("Full Pipeline Test (with Docling)")
    print("=" * 80)
    print()

    file_path_obj = Path(file_path)

    # Validate file
    if not file_path_obj.exists():
        print(f"✗ File not found: {file_path}")
        return False

    print(f"Testing with: {file_path}")
    print(f"File type: {file_path_obj.suffix}")
    print()

    # Test extraction
    try:
        print("Starting extraction pipeline...")
        print("-" * 80)

        def progress_callback(current, total, status):
            """Print progress updates"""
            print(f"  [{current}%] {status}")

        # Run extraction
        results = process_document(
            file_path=file_path,
            progress_callback=progress_callback
        )

        print("-" * 80)
        print()

        # Display results
        print("✓ Extraction completed successfully!")
        print()
        print("Results:")
        print(f"  Total facts extracted: {results['stats']['total_facts']}")
        print(f"  Unique facts: {results['stats']['unique_facts']}")
        print(f"  Conflicts detected: {results['stats']['conflicts']}")
        print(f"  Total chunks processed: {results['total_chunks']}")
        print()

        # Show sample facts
        if results['consolidated_facts']:
            print("Sample extracted facts (first 5):")
            print("-" * 80)
            for i, fact in enumerate(results['consolidated_facts'][:5], 1):
                print(f"{i}. {fact.name}")
                print(f"   Value: {fact.normalized_value} {fact.normalized_unit}")
                print(f"   Type: {fact.type}")
                if fact.has_conflict:
                    print(f"   ⚠️  Conflict: {fact.conflict_description}")
                print()

        print("=" * 80)
        print("✓ Full pipeline test PASSED!")
        print("=" * 80)
        return True

    except Exception as e:
        print(f"\n✗ Pipeline test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Test full extraction pipeline with Docling'
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
        '--md',
        type=str,
        help='Path to Markdown file for testing'
    )

    args = parser.parse_args()

    # Determine which file to test
    test_file = args.pdf or args.docx or args.md

    if not test_file:
        print("Error: Please provide a file to test")
        print()
        print("Usage:")
        print("  python test_full_pipeline.py --pdf test.pdf")
        print("  python test_full_pipeline.py --docx test.docx")
        print("  python test_full_pipeline.py --md test.md")
        return False

    # Run test
    success = test_full_pipeline(test_file)
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
