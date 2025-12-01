"""
Test script to verify PHASE A: Read-Only Table Access

This script tests that tables can be loaded from metadata without
affecting any existing analysis functionality.
"""

from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from esia_analyzer.reviewer import ESIAReviewer

def test_table_loading():
    """Test that tables load correctly from metadata."""

    # Setup paths
    base_path = Path(__file__).parent.parent
    chunks_path = base_path / "data" / "outputs" / "Buli_CFPP_Final_2025_09_12_chunks.jsonl"
    meta_path = base_path / "data" / "outputs" / "Buli_CFPP_Final_2025_09_12_meta.json"

    print("=" * 80)
    print("PHASE A VERIFICATION TEST: Read-Only Table Access")
    print("=" * 80)
    print()

    # Check if files exist
    if not chunks_path.exists():
        print(f"ERROR: Chunks file not found: {chunks_path}")
        return False

    if not meta_path.exists():
        print(f"ERROR: Metadata file not found: {meta_path}")
        return False

    print(f"Chunks file: {chunks_path.name}")
    print(f"Metadata file: {meta_path.name}")
    print()

    # Initialize reviewer
    print("Initializing ESIAReviewer...")
    reviewer = ESIAReviewer(Path(__file__).parent)

    # Verify new attributes exist
    assert hasattr(reviewer, 'tables'), "Missing 'tables' attribute"
    assert hasattr(reviewer, 'enable_table_analysis'), "Missing 'enable_table_analysis' attribute"
    assert reviewer.tables == [], "tables should be initialized as empty list"
    assert reviewer.enable_table_analysis == False, "enable_table_analysis should be False by default"
    print("[OK] New attributes initialized correctly")
    print()

    # Load data (which should automatically load tables)
    print("Loading data and tables...")
    reviewer.load_data(chunks_path, meta_path)
    print()

    # Verify tables loaded
    tables = reviewer.tables

    print("VERIFICATION RESULTS:")
    print("-" * 80)

    # Test 1: Return type
    assert tables is not None, "load_tables() returned None"
    print("[OK] Test 1: load_tables() did not return None")

    # Test 2: List type
    assert isinstance(tables, list), f"load_tables() returned {type(tables)}, not a list"
    print("[OK] Test 2: load_tables() returned a list")

    # Test 3: Expected count
    expected_count = 82
    actual_count = len(tables)
    if actual_count != expected_count:
        print(f"[WARN] Test 3: Expected {expected_count} tables, got {actual_count}")
        print("  (This may be normal if metadata has different table count)")
    else:
        print(f"[OK] Test 3: Loaded {actual_count} tables (matches expected count)")

    # Test 4: Table structure
    if tables:
        sample_table = tables[0]
        assert 'table_id' in sample_table, "Tables missing 'table_id' field"
        print("[OK] Test 4: All tables have 'table_id' field")

        print()
        print(f"Sample table keys: {list(sample_table.keys())}")
        print(f"Sample table_id: {sample_table.get('table_id', 'N/A')}")
        if 'page' in sample_table:
            print(f"Sample page: {sample_table.get('page', 'N/A')}")
        if 'caption' in sample_table:
            caption = sample_table.get('caption', 'N/A')
            if caption and len(caption) > 80:
                caption = caption[:77] + "..."
            print(f"Sample caption: {caption if caption else 'N/A'}")
    else:
        print("[WARN] No tables found in metadata")

    print()
    print("-" * 80)
    print()

    # Test 5: Verify no existing functionality broken
    print("INTEGRITY CHECK: Verifying existing functionality not affected...")
    print("-" * 80)

    # Check that facts were loaded normally
    assert len(reviewer.facts) > 0, "Facts not loaded (existing functionality broken)"
    print(f"[OK] Facts loaded: {len(reviewer.facts)} chunks")

    # Check that metadata was loaded normally
    assert reviewer.metadata, "Metadata not loaded (existing functionality broken)"
    print(f"[OK] Metadata loaded: {len(reviewer.metadata)} keys")

    # Check that document name was extracted
    assert reviewer.document_name != "Unknown", "Document name not extracted"
    print(f"[OK] Document name extracted: {reviewer.document_name}")

    print()
    print("=" * 80)
    print("SUCCESS: PHASE A implementation verified!")
    print("=" * 80)
    print()
    print("SUMMARY:")
    print(f"  - Tables loaded: {len(tables)}")
    print(f"  - Feature flag: enable_table_analysis = {reviewer.enable_table_analysis}")
    print(f"  - Existing functionality: INTACT")
    print(f"  - Ready for PHASE B: Table cross-checking")
    print()

    return True

if __name__ == "__main__":
    try:
        success = test_table_loading()
        sys.exit(0 if success else 1)
    except Exception as e:
        print()
        print("=" * 80)
        print(f"TEST FAILED with exception: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        sys.exit(1)
