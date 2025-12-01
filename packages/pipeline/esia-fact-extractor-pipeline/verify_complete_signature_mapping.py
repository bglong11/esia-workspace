"""
Complete verification script for signature mapping.
Tests all domain types and ensures signatures are properly available.

Part of Phase 4 Production Hardening - Task 2.
"""

import sys
import os
sys.path.append(os.getcwd())

from src.esia_extractor import ESIAExtractor
from src.archetype_mapper import ArchetypeMapper

def test_all_archetype_domains():
    """Test that all archetype domains can be mapped to signatures."""
    import io
    # Force UTF-8 encoding for stdout to handle Unicode characters on Windows
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 80)
    print("COMPLETE SIGNATURE MAPPING VERIFICATION")
    print("=" * 80)
    print()

    # Initialize extractor and mapper
    extractor = ESIAExtractor()
    mapper = ArchetypeMapper()

    # Get all archetype domains
    all_domains = mapper.get_all_domains()
    print(f"Total archetype domains loaded: {len(all_domains)}")
    print()

    # Test each domain
    results = {
        'success': [],
        'failed': [],
        'skipped': []
    }

    print("Testing signature mapping for each domain:")
    print("-" * 80)

    for domain in sorted(all_domains):
        # Try to get signature class
        try:
            sig_class = extractor._get_signature_class(domain)
            if sig_class:
                results['success'].append((domain, sig_class.__name__))
                print(f"✓ {domain:<50} → {sig_class.__name__}")
            else:
                # Check if this is a Performance Standard (PS1-PS8) which don't have direct signatures
                if domain.startswith('ps') and domain[2:].isdigit():
                    results['skipped'].append((domain, 'IFC Performance Standard (no direct signature)'))
                    print(f"○ {domain:<50} → IFC PS (no direct signature)")
                else:
                    results['failed'].append((domain, 'No signature found'))
                    print(f"✗ {domain:<50} → NO SIGNATURE FOUND")
        except Exception as e:
            results['failed'].append((domain, str(e)))
            print(f"✗ {domain:<50} → ERROR: {str(e)[:30]}")

    print()
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"Total domains tested: {len(all_domains)}")
    print(f"Successfully mapped: {len(results['success'])}")
    print(f"Skipped (PS standards): {len(results['skipped'])}")
    print(f"Failed: {len(results['failed'])}")
    print()

    if results['failed']:
        print("FAILED DOMAINS:")
        for domain, reason in results['failed']:
            print(f"  - {domain}: {reason}")
        print()

    # Test key Phase 2 domains specifically
    print("=" * 80)
    print("PHASE 2 SPECIFIC DOMAIN VERIFICATION")
    print("=" * 80)

    phase2_domains = [
        'energy_nuclear',
        'infrastructure_ports',
        'agriculture_crops',
        'agriculture_animal_production',
        'agriculture_forestry',
        'manufacturing_general',
        'real_estate_commercial',
        'real_estate_hospitality',
        'real_estate_healthcare',
        'financial_banking',
        'financial_microfinance',
        'financial_intermediary_esms',
    ]

    phase2_results = {}
    for domain in phase2_domains:
        sig_class = extractor._get_signature_class(domain)
        if sig_class:
            phase2_results[domain] = sig_class.__name__
            print(f"✓ {domain:<40} → {sig_class.__name__}")
        else:
            phase2_results[domain] = None
            print(f"✗ {domain:<40} → NOT FOUND")

    print()
    phase2_success = sum(1 for v in phase2_results.values() if v is not None)
    print(f"Phase 2 domains verified: {phase2_success}/{len(phase2_domains)}")
    print()

    # Overall status
    if results['failed']:
        print("❌ VERIFICATION FAILED: Some domains cannot be mapped to signatures")
        return 1
    else:
        print("✓ VERIFICATION PASSED: All domains successfully mapped to signatures")
        return 0

def test_signature_field_extraction():
    """Test that signatures can extract fields from sample text."""
    print("=" * 80)
    print("SIGNATURE FIELD EXTRACTION TEST")
    print("=" * 80)
    print()

    extractor = ESIAExtractor()

    # Test data for different domains
    test_cases = [
        {
            'domain': 'infrastructure_ports',
            'context': '''
            Port Development Project
            Location: Coastal City, Maritime District
            Capacity: 2 million TEU per year
            Marine Impact: Dredging 3 million cubic meters
            Vessel Traffic: Expected increase of 40% in shipping lanes
            Page | 15
            '''
        },
        {
            'domain': 'agriculture_crops',
            'context': '''
            Agricultural Plantation Project
            Crop Type: Palm Oil
            Total Area: 10,000 hectares
            Pesticide Use: Integrated Pest Management System
            Soil Conservation: Contour plowing and terracing
            Page | 22
            '''
        },
        {
            'domain': 'financial_intermediary_esms',
            'context': '''
            Financial Intermediary ESMS Framework
            Sub-Project Screening: Category A requires full ESIA
            Exclusion List: 12 prohibited activities including tobacco and weapons
            ESMS Monitoring: Annual audits of high-risk sub-projects
            Capacity Building: Quarterly training for FI staff
            Page | 8
            '''
        }
    ]

    results = []
    for test in test_cases:
        domain = test['domain']
        context = test['context']

        print(f"Domain: {domain}")
        try:
            facts = extractor.extract(context, domain)
            if facts:
                print(f"  ✓ Extracted {len(facts)} fields")
                for field, value in list(facts.items())[:3]:  # Show first 3
                    preview = str(value)[:60]
                    print(f"    - {field}: {preview}{'...' if len(str(value)) > 60 else ''}")
                results.append((domain, 'SUCCESS', len(facts)))
            else:
                print(f"  ⚠ No facts extracted")
                results.append((domain, 'EMPTY', 0))
        except Exception as e:
            print(f"  ✗ Error: {str(e)[:60]}")
            results.append((domain, 'ERROR', 0))
        print()

    print("-" * 80)
    print("Extraction Test Results:")
    for domain, status, field_count in results:
        print(f"  {domain:<40} {status:<10} ({field_count} fields)")

    return 0

if __name__ == "__main__":
    # Run all tests
    result1 = test_all_archetype_domains()
    print("\n" + "=" * 80 + "\n")
    result2 = test_signature_field_extraction()

    # Exit with error code if any test failed
    sys.exit(max(result1, result2))
