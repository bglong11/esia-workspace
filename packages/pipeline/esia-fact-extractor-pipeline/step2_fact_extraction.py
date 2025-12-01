#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 2: DSPy-Based ESIA Fact Extraction

Processes chunks from Step 1 and extracts domain-specific facts using DSPy
with LLM (Google Gemini or OpenRouter).

Features:
- Processes chunks line-by-line from JSONL
- Uses 40+ domain-specific DSPy signatures
- Supports Google Gemini and OpenRouter APIs
- Extracts facts organized by document section
- Generates comprehensive results with metadata

Usage:
    python step2_fact_extraction.py
    python step2_fact_extraction.py --verbose
    python step2_fact_extraction.py --sample 10  # Test with 10 chunks
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import traceback

# Add project root to path
sys.path.append(os.getcwd())

import dspy
from src.esia_extractor import ESIAExtractor



def get_english_chunks_if_available(chunks_file: str, verbose: bool = False) -> str:
    """
    Auto-detect if English chunks are available and preferentially use them.

    If the provided chunks file is in the original language, this function checks
    if a corresponding *_chunks_english.jsonl file exists. If it does, recommends
    using the English version for consistent fact extraction.

    Args:
        chunks_file: Path to chunks JSONL file
        verbose: Print recommendation if English version found

    Returns:
        str: Path to English chunks if available and recommended, otherwise original path
    """
    chunks_path = Path(chunks_file)

    # Check if this is already an English chunks file
    if '_chunks_english.jsonl' in str(chunks_path):
        return chunks_file

    # Generate path for English chunks
    english_chunks_path = chunks_path.parent / f"{chunks_path.stem}_english.jsonl"

    # Check if English chunks exist
    if english_chunks_path.exists():
        if verbose:
            print(f"\n⚠️  English chunks file detected: {english_chunks_path.name}")
            print(f"    Using English chunks for consistent fact extraction")
            print(f"    (Original: {chunks_path.name})")
        return str(english_chunks_path)

    return chunks_file


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


def extract_facts_from_chunks(chunks: List[Dict], extractor: ESIAExtractor, verbose: bool = False) -> Dict[str, Any]:
    """Extract facts from chunks using DSPy signatures."""

    results = {
        'document': Path(chunks[0]['metadata']['origin']['filename']).name if chunks else 'unknown',
        'extraction_date': datetime.now().isoformat(),
        'total_chunks': len(chunks),
        'chunks_processed': 0,
        'chunks_with_facts': 0,
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

    total_sections = len(sections)

    print(f"\nFound {total_sections} unique sections in document")
    print("=" * 70)

    # Process each section
    for section_idx, (section_name, section_chunks) in enumerate(sections.items(), 1):
        print(f"[{section_idx}/{total_sections}] Processing section: {section_name}")
        print(f"  Chunks in section: {len(section_chunks)}")

        section_facts = {
            'section': section_name,
            'page_start': section_chunks[0]['page'],
            'page_end': section_chunks[-1]['page'],
            'chunk_count': len(section_chunks),
            'facts_extracted': 0,
            'facts': []
        }

        # Extract facts from first few chunks of this section (to avoid rate limiting)
        chunks_to_process = min(2, len(section_chunks))  # Process max 2 chunks per section

        for chunk_idx, chunk in enumerate(section_chunks[:chunks_to_process]):
            try:
                if verbose:
                    print(f"    Chunk {chunk_idx + 1}: Processing (page {chunk['page']})")

                # Extract facts from chunk using the normalized section name
                facts = extractor.extract_section(
                    chunk['text'],
                    section_name,
                    chunk['page']
                )

                if facts:
                    section_facts['facts_extracted'] += 1
                    section_facts['facts'].append({
                        'chunk_id': chunk['chunk_id'],
                        'page': chunk['page'],
                        'facts': facts
                    })
                    results['chunks_with_facts'] += 1

                    if verbose:
                        print(f"      [OK] Facts extracted: {len(facts) if isinstance(facts, dict) else 1}")

                results['chunks_processed'] += 1

            except Exception as e:
                error_msg = f"Section '{section_name}', Chunk {chunk['chunk_id']}: {str(e)}"
                results['errors'].append(error_msg)
                if verbose:
                    print(f"      [ERR] Error: {str(e)}")

        # Add section results if any facts were extracted
        if section_facts['facts_extracted'] > 0:
            results['sections'][section_name] = section_facts
            print(f"  [OK] Extracted {section_facts['facts_extracted']} fact sets from {chunks_to_process} chunks")
        else:
            print(f"  - No facts extracted for this section")

    return results


def save_results(results: Dict[str, Any], output_file: str) -> None:
    """Save extraction results to JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)

    print(f"\nResults saved to: {output_file}")


def print_summary(results: Dict[str, Any]) -> None:
    """Print extraction summary."""
    print("\n" + "=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)
    print(f"Document: {results['document']}")
    print(f"Total chunks: {results['total_chunks']}")
    print(f"Chunks processed: {results['chunks_processed']}")
    print(f"Chunks with facts: {results['chunks_with_facts']}")
    print(f"Sections with facts: {len(results['sections'])}")

    if results['errors']:
        print(f"\nErrors encountered: {len(results['errors'])}")
        for error in results['errors'][:5]:  # Show first 5 errors
            print(f"  - {error}")

    print("\nSections processed:")
    for section_name, section_data in results['sections'].items():
        print(f"  • {section_name}")
        print(f"    Pages: {section_data['page_start']}-{section_data['page_end']}")
        print(f"    Facts extracted: {section_data['facts_extracted']}")


def main():
    parser = argparse.ArgumentParser(
        description='Step 2: Extract ESIA facts from chunks using DSPy',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
IMPORTANT: For consistent fact extraction across languages, this step REQUIRES
English-language chunks. If your document was processed with --translate-to-english,
use the *_chunks_english.jsonl file.

Example:
  # For multilingual ESIAs (use English version for consistency)
  python step2_fact_extraction.py --chunks document_chunks_english.jsonl

  # For English-only ESIAs (original chunks are fine)
  python step2_fact_extraction.py --chunks document_chunks.jsonl
        """
    )
    parser.add_argument(
        '--chunks',
        default='./data/outputs/TL_IPP_Supp_ESIA_2025-09-15_chunks.jsonl',
        help='Path to chunks JSONL file from Step 1 (MUST BE ENGLISH for consistent extraction)'
    )
    parser.add_argument(
        '--output',
        default='./data/outputs/esia_facts.json',
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
    print("STEP 2: DSPy FACT EXTRACTION")
    print("=" * 70)
    print()

    # Auto-detect and prefer English chunks if available
    preferred_chunks_file = get_english_chunks_if_available(args.chunks, verbose=True)
    if preferred_chunks_file != args.chunks:
        args.chunks = preferred_chunks_file

    # Check if chunks file exists
    if not os.path.exists(args.chunks):
        print(f"Error: Chunks file not found: {args.chunks}")
        sys.exit(1)

    # Load chunks
    print(f"Loading chunks from: {args.chunks}")
    chunks = load_chunks(args.chunks, args.sample)
    print(f"[OK] Loaded {len(chunks)} chunks")

    # Initialize extractor
    print("\nInitializing DSPy extractor...")
    extractor = ESIAExtractor(verbose=args.verbose)
    print("[OK] Extractor initialized")

    # Extract facts
    print("\nExtracting facts from chunks...")
    results = extract_facts_from_chunks(chunks, extractor, verbose=args.verbose)

    # Save results
    print("\nSaving results...")
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    save_results(results, args.output)

    # Print summary
    print_summary(results)

    print("\n[OK] Step 2 extraction complete!")


if __name__ == '__main__':
    main()
