#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 2: Simple DSPy-Based ESIA Fact Extraction

Processes chunks from Step 1 and extracts domain-specific facts using DSPy.

Usage:
    python step2_simple_extraction.py
    python step2_simple_extraction.py --verbose
    python step2_simple_extraction.py --sample 3
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
    """Extract facts from chunks using DSPy."""

    # Initialize extractor (using environment LLM_PROVIDER)
    print("Initializing DSPy extractor...")
    extractor = ESIAExtractor()
    print("[OK] Extractor initialized")
    print()

    results = {
        'document': Path(chunks[0]['metadata']['origin']['filename']).name if chunks else 'unknown',
        'extraction_date': datetime.now().isoformat(),
        'total_chunks': len(chunks),
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

    # Process each section
    for section_idx, (section_name, section_chunks) in enumerate(sections.items(), 1):
        print(f"[{section_idx}/{len(sections)}] Section: {section_name}")

        # Combine text from all chunks in this section
        combined_text = ' '.join([c['text'] for c in section_chunks])

        section_data = {
            'section': section_name,
            'page_start': section_chunks[0]['page'],
            'page_end': section_chunks[-1]['page'],
            'chunk_count': len(section_chunks),
            'facts': {}
        }

        try:
            if verbose:
                print(f"  Extracting facts from {len(section_chunks)} chunks...")

            # Extract facts from all domains using DSPy
            facts = extractor.extract_all_domains(combined_text)

            if facts:
                section_data['facts'] = facts
                results['sections'][section_name] = section_data

                if verbose:
                    fact_count = sum(1 for v in facts.values() if v)
                    print(f"  [OK] Extracted facts from {fact_count} domains")
                else:
                    print(f"  [OK] Facts extracted")

            else:
                print(f"  - No facts extracted")

        except Exception as e:
            error_msg = f"Section '{section_name}': {str(e)}"
            results['errors'].append(error_msg)
            print(f"  [ERR] {str(e)[:100]}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Step 2: Extract ESIA facts from chunks using DSPy'
    )
    parser.add_argument(
        '--chunks',
        default='./data/outputs/TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl',
        help='Path to chunks JSONL file from Step 1'
    )
    parser.add_argument(
        '--output',
        default='./data/outputs/esia_facts_extracted.json',
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
    print("STEP 2: ESIA FACT EXTRACTION WITH DSPY")
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
    print("Extracting facts...")
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
    print(f"Sections processed: {len(results['sections'])}")

    if results['sections']:
        print("\nSections with extracted facts:")
        for section_name, section_data in results['sections'].items():
            fact_count = len(section_data['facts'])
            print(f"  - {section_name}")
            print(f"    Pages: {section_data['page_start']}-{section_data['page_end']}")
            if section_data['facts']:
                print(f"    Domains with facts: {fact_count}")

    if results['errors']:
        print(f"\nErrors: {len(results['errors'])}")
        for error in results['errors'][:3]:
            print(f"  - {error}")

    print()
    print("[OK] Step 2 extraction complete!")


if __name__ == '__main__':
    main()
