"""
Test script to verify all DSPy signatures are properly imported and available.
Part of Phase 4 Production Hardening - Task 2.
"""

import sys
import re
from typing import List, Dict, Set

def get_all_signatures_from_file(file_path: str) -> Set[str]:
    """Extract all signature class names from generated_signatures.py"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        signatures = set(re.findall(r'^class (\w+Signature)\(dspy\.Signature\):', content, re.MULTILINE))
    return signatures

def get_imported_signatures_from_file(file_path: str) -> Set[str]:
    """Extract all imported signature class names from esia_extractor.py"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        signatures = set(re.findall(r'^\s+(\w+Signature),?\s*$', content, re.MULTILINE))
    return signatures

def categorize_signatures(signatures: List[str]) -> Dict[str, List[str]]:
    """Categorize signatures by sector"""
    categories = {
        'Core ESIA': [],
        'Energy': [],
        'Infrastructure': [],
        'Agriculture': [],
        'Manufacturing': [],
        'Real Estate': [],
        'Financial': [],
        'Mining': [],
        'Technical/Environmental': [],
        'Project Management': [],
        'Other': []
    }

    for sig in sorted(signatures):
        if any(x in sig for x in ['Energy', 'Solar', 'Wind', 'Hydro', 'Geothermal', 'Coal', 'Nuclear', 'Grid', 'Transmission']):
            categories['Energy'].append(sig)
        elif any(x in sig for x in ['Infrastructure', 'Bridge', 'Tunnel', 'Ports', 'Pipeline']):
            categories['Infrastructure'].append(sig)
        elif 'Agriculture' in sig:
            categories['Agriculture'].append(sig)
        elif 'Manufacturing' in sig:
            categories['Manufacturing'].append(sig)
        elif 'RealEstate' in sig:
            categories['Real Estate'].append(sig)
        elif 'Financial' in sig:
            categories['Financial'].append(sig)
        elif any(x in sig for x in ['Mine', 'Mineral', 'Alumina', 'Nickel']):
            categories['Mining'].append(sig)
        elif any(x in sig for x in ['Noise', 'Vibration', 'Electromagnetic', 'Visual', 'Landscape', 'Avian', 'Bat', 'Process', 'Emissions', 'Hazardous', 'Hydrocarbon', 'Well', 'Drilling']):
            categories['Technical/Environmental'].append(sig)
        elif any(x in sig for x in ['ProjectDescription', 'ExecutiveSummary', 'Introduction', 'Baseline', 'Impact', 'Mitigation', 'ESMP', 'GRM', 'Gender', 'Consultation', 'Decommissioning', 'Closure', 'Cumulative', 'Conclusion', 'References', 'Annexes']):
            categories['Core ESIA'].append(sig)
        else:
            categories['Other'].append(sig)

    # Remove empty categories
    return {k: v for k, v in categories.items() if v}

def test_dynamic_signature_retrieval():
    """Test that signatures can be dynamically retrieved by the extractor"""
    try:
        from src.esia_extractor import ESIAExtractor
        import src.generated_signatures as gen_sigs

        extractor = ESIAExtractor()

        # Test some key signatures
        test_domains = [
            'infrastructure_ports',
            'manufacturing_general',
            'agriculture_crops',
            'financial_intermediary_esms',
            'energy_nuclear',
            'real_estate_commercial'
        ]

        results = []
        for domain in test_domains:
            sig_class = extractor._get_signature_class(domain)
            if sig_class:
                results.append((domain, sig_class.__name__, 'OK'))
            else:
                results.append((domain, None, 'FAILED'))

        return results
    except Exception as e:
        return [('error', None, str(e))]

def main():
    import io
    import sys
    # Force UTF-8 encoding for stdout to handle Unicode characters on Windows
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 80)
    print("PHASE 4 PRODUCTION HARDENING - TASK 2: SIGNATURE IMPORT VERIFICATION")
    print("=" * 80)
    print()

    # 1. Get all signatures from generated_signatures.py
    print("1. CHECKING GENERATED SIGNATURES FILE...")
    all_signatures = get_all_signatures_from_file('src/generated_signatures.py')
    print(f"   Found {len(all_signatures)} signatures in generated_signatures.py")
    print()

    # 2. Get imported signatures from esia_extractor.py
    print("2. CHECKING IMPORTED SIGNATURES...")
    imported_signatures = get_imported_signatures_from_file('src/esia_extractor.py')
    print(f"   Found {len(imported_signatures)} signatures imported in esia_extractor.py")
    print()

    # 3. Compare and find missing
    print("3. COMPARING SIGNATURES...")
    missing = sorted(all_signatures - imported_signatures)
    extra = sorted(imported_signatures - all_signatures)

    if missing:
        print(f"   ❌ MISSING IMPORTS ({len(missing)}):")
        for sig in missing:
            print(f"      - {sig}")
    else:
        print(f"   ✓ All signatures properly imported!")

    if extra:
        print(f"   ⚠️  EXTRA IMPORTS ({len(extra)} - these are imported but don't exist):")
        for sig in extra:
            print(f"      - {sig}")
    print()

    # 4. Categorize signatures
    print("4. SIGNATURE CATEGORIES...")
    categories = categorize_signatures(list(all_signatures))
    for category, sigs in categories.items():
        print(f"   {category} ({len(sigs)}):")
        for sig in sigs:
            status = "✓" if sig in imported_signatures else "✗"
            print(f"      {status} {sig}")
    print()

    # 5. Test dynamic retrieval
    print("5. TESTING DYNAMIC SIGNATURE RETRIEVAL...")
    retrieval_results = test_dynamic_signature_retrieval()
    for domain, sig_class, status in retrieval_results:
        if status == 'OK':
            print(f"   ✓ {domain} → {sig_class}")
        else:
            print(f"   ✗ {domain} → {status}")
    print()

    # 6. Summary
    print("=" * 80)
    print("SUMMARY:")
    print("=" * 80)
    print(f"Total signatures in generated_signatures.py: {len(all_signatures)}")
    print(f"Total signatures imported in esia_extractor.py: {len(imported_signatures)}")
    print(f"Missing imports: {len(missing)}")
    print(f"Extra imports: {len(extra)}")
    print()

    if missing or extra:
        print("❌ STATUS: FAILED - Import mismatch detected")
        return 1
    else:
        print("✓ STATUS: PASSED - All signatures properly imported and available")
        return 0

if __name__ == "__main__":
    sys.exit(main())
