#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 2: ESIA Fact Extraction with Section Mapping

Processes chunks from Step 1 and extracts domain-specific facts using DSPy
with intelligent section-to-domain mapping.

Usage:
    python step2_extraction_with_mapping.py
    python step2_extraction_with_mapping.py --verbose
    python step2_extraction_with_mapping.py --sample 10
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

sys.path.append(os.getcwd())

from src.esia_extractor import ESIAExtractor
from src.section_mapper import SectionMapper


def load_chunks(chunks_file: str, sample_size: Optional[int] = None) -> List[Dict[str, Any]]:
    """Load chunks from JSONL file."""
    chunks = []
    try:
        with open(chunks_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if sample_size and i >= sample_size:
                    break
                try:
                    chunk = json.loads(line.strip())
                    chunks.append(chunk)
                except json.JSONDecodeError as e:
                    print(f"Warning: Could not parse chunk {i}: {e}")
                    continue
    except FileNotFoundError:
        raise FileNotFoundError(f"Chunks file not found: {chunks_file}")

    return chunks


def extract_facts(chunks: List[Dict], verbose: bool = False) -> Dict[str, Any]:
    """Extract facts from chunks using DSPy with section mapping."""

    # Initialize extractor
    print("Initializing DSPy extractor...")
    extractor = ESIAExtractor()
    print("[OK] Extractor initialized")
    print()

    results = {
        'document': Path(chunks[0]['metadata']['origin']['filename']).name if chunks else 'unknown',
        'extraction_date': datetime.now().isoformat(),
        'total_chunks': len(chunks),
        'sections_processed': 0,
        'sections_skipped': 0,
        'sections_with_facts': 0,
        'mapping_stats': SectionMapper.get_statistics(),
        'sections': {},
        'errors': []
    }

    # Group chunks by section
    sections = {}
    for chunk in chunks:
        section = chunk.get('section', 'Unknown')
        if section not in sections:
            sections[section] = []
        sections[section].append(chunk)

    print(f"Found {len(sections)} unique sections")
    print("=" * 70)
    print()

    section_idx = 0
    for section_name, section_chunks in sorted(sections.items()):
        section_idx += 1

        # Check if section should be processed
        if not SectionMapper.should_process_section(section_name):
            if verbose:
                print(f"[{section_idx}/{len(sections)}] SKIP: {section_name}")
            results['sections_skipped'] += 1
            continue

        # Map section to domain
        mapped_domain = SectionMapper.map_section(section_name)
        if not mapped_domain:
            if verbose:
                print(f"[{section_idx}/{len(sections)}] WARN: No mapping for {section_name}")
            results['sections_skipped'] += 1
            continue

        print(f"[{section_idx}/{len(sections)}] {section_name}")
        print(f"  Domain: {mapped_domain}")

        # Combine text from all chunks in this section
        combined_text = ' '.join([c['text'] for c in section_chunks])

        section_data = {
            'section': section_name,
            'mapped_domain': mapped_domain,
            'page_start': section_chunks[0]['page'],
            'page_end': section_chunks[-1]['page'],
            'chunk_count': len(section_chunks),
            'facts': {}
        }

        try:
            if verbose:
                print(f"  Extracting from {len(section_chunks)} chunks...")

            # Extract facts using the mapped domain
            facts = extractor.extract(combined_text, mapped_domain)

            if facts:
                section_data['facts'] = facts
                results['sections'][section_name] = section_data
                results['sections_with_facts'] += 1

                if verbose:
                    print(f"  [OK] Facts extracted from {mapped_domain}")
                else:
                    print(f"  [OK] Facts extracted")

            else:
                print(f"  - No facts found in this section")

            results['sections_processed'] += 1

        except Exception as e:
            error_msg = f"Section '{section_name}' ({mapped_domain}): {str(e)}"
            results['errors'].append(error_msg)
            print(f"  [ERR] {str(e)[:80]}")

        print()

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Step 2: Extract ESIA facts from chunks with section mapping'
    )
    parser.add_argument(
        '--chunks',
        default='./data/outputs/TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl',
        help='Path to chunks JSONL file from Step 1'
    )
    parser.add_argument(
        '--output',
        default='./data/outputs/esia_facts_with_mapping.json',
        help='Output file for extraction results'
    )
    parser.add_argument(
        '--sample',
        type=int,
        default=None,
        help='Process only first N chunks (for testing)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("STEP 2: ESIA FACT EXTRACTION WITH SECTION MAPPING")
    print("=" * 70)
    print()

    # Check chunks file
    if not os.path.exists(args.chunks):
        print(f"Error: Chunks file not found: {args.chunks}")
        sys.exit(1)

    # Load chunks
    print(f"Loading chunks from: {args.chunks}")
    chunks = load_chunks(args.chunks, args.sample)
    print(f"[OK] Loaded {len(chunks)} chunks")

    if args.sample:
        print(f"     (Using sample of {args.sample} chunks for testing)")

    print()

    # Extract facts
    print("Extracting facts with section mapping...")
    print()
    results = extract_facts(chunks, verbose=args.verbose)

    # Save results
    print()
    print("=" * 70)
    print("SAVING RESULTS")
    print("=" * 70)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)

    print(f"[OK] Results saved to: {args.output}")

    # Print summary
    print()
    print("=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)
    print(f"Document: {results['document']}")
    print(f"Total chunks: {results['total_chunks']}")
    print(f"Sections processed: {results['sections_processed']}")
    print(f"Sections skipped: {results['sections_skipped']}")
    print(f"Sections with facts: {results['sections_with_facts']}")

    if results['sections']:
        print("\nSections with extracted facts:")
        for section_name, section_data in results['sections'].items():
            print(f"  - {section_name}")
            print(f"    Domain: {section_data['mapped_domain']}")
            print(f"    Pages: {section_data['page_start']}-{section_data['page_end']}")
            if section_data['facts']:
                print(f"    Facts: {len(section_data['facts'])} fields")

    if results['errors']:
        print(f"\nErrors: {len(results['errors'])}")
        for error in results['errors'][:3]:
            print(f"  - {error}")

    print()
    print("[OK] Step 2 extraction complete!")


if __name__ == '__main__':
    main()
