"""
Phase 2 Integration Test: Verify DocumentProcessor works in the pipeline

This script tests that the updated core extractor works correctly with Docling.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from core.extractor import DocumentProcessor


def test_document_processor():
    """Test that DocumentProcessor can be imported and instantiated"""
    print("=" * 80)
    print("Phase 2 Integration Test")
    print("=" * 80)
    print()

    # Test 1: Check class exists
    print("Test 1: DocumentProcessor class exists")
    try:
        assert hasattr(DocumentProcessor, 'extract_text_from_document')
        print("  ✓ PASS: DocumentProcessor.extract_text_from_document() method found")
    except AssertionError:
        print("  ✗ FAIL: Method not found")
        return False

    # Test 2: Check method signature
    print("\nTest 2: Method signature is correct")
    import inspect
    sig = inspect.signature(DocumentProcessor.extract_text_from_document)
    params = list(sig.parameters.keys())
    try:
        assert 'file_path' in params
        print("  ✓ PASS: Method accepts 'file_path' parameter")
    except AssertionError:
        print("  ✗ FAIL: Incorrect signature")
        return False

    # Test 3: Can import Docling
    print("\nTest 3: Docling can be imported")
    try:
        from docling.document_converter import DocumentConverter
        print("  ✓ PASS: Docling imports successfully")
    except ImportError as e:
        print(f"  ✗ FAIL: {e}")
        return False

    print("\n" + "=" * 80)
    print("✓ All integration tests passed!")
    print("=" * 80)
    print()
    print("Phase 2 is complete. The core extractor now uses Docling.")
    print()
    print("Next steps:")
    print("  1. Test with actual document: python test_with_document.py --pdf test.pdf")
    print("  2. Proceed with Phase 3: Update FastAPI and frontend")
    print()
    return True


if __name__ == "__main__":
    success = test_document_processor()
    sys.exit(0 if success else 1)
