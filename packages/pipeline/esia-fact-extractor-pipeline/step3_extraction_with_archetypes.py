#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 3: ESIA Fact Extraction with Archetype-Based Section Mapping

Processes chunks from Step 1 and extracts domain-specific facts using:
- Intelligent archetype-based section mapping
- Multi-domain extraction per section
- IFC Performance Standard alignment
- 50+ project type support

Usage:
    python step3_extraction_with_archetypes.py
    python step3_extraction_with_archetypes.py --sample 10
    python step3_extraction_with_archetypes.py --verbose
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Load environment variables from project root .env.local (SINGLE SOURCE OF TRUTH)
try:
    from dotenv import load_dotenv
    # Load from project root: esia-ai/.env.local
    # Path: esia-workspace/packages/pipeline/esia-fact-extractor-pipeline/ -> go up 4 levels
    root_env = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.env.local')
    load_dotenv(root_env, override=False)  # Don't override parent process env
except ImportError:
    pass  # dotenv not required, use system env vars

sys.path.append(os.getcwd())

from src.esia_extractor import ESIAExtractor
from src.archetype_mapper import ArchetypeMapper


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


def process_single_section(
    section_name: str,
    section_chunks: List[Dict],
    mapper: 'ArchetypeMapper',
    extractor: 'ESIAExtractor',
    section_idx: int,
    total_sections: int,
    verbose: bool = False,
    print_lock: threading.Lock = None
) -> Optional[Dict[str, Any]]:
    """
    Process a single section with domain mapping and extraction.

    This function is designed to be called in parallel by ThreadPoolExecutor.

    Args:
        section_name: Name of the section
        section_chunks: List of chunks for this section
        mapper: ArchetypeMapper instance
        extractor: ESIAExtractor instance
        section_idx: Index of this section (for logging)
        total_sections: Total number of sections
        verbose: Enable verbose logging
        print_lock: Thread lock for synchronized printing

    Returns:
        Section data dict if facts were extracted, None otherwise
    """
    def safe_print(*args, **kwargs):
        """Thread-safe print function."""
        if print_lock:
            with print_lock:
                print(*args, **kwargs)
        else:
            print(*args, **kwargs)

    # Check if section should be processed
    if not mapper.should_process_section(section_name):
        if verbose:
            safe_print(f"[{section_idx}/{total_sections}] SKIP: {section_name}")
        return None

    # Map section to domains
    domain_matches = mapper.map_section(section_name, top_n=3)
    if not domain_matches:
        if verbose:
            safe_print(f"[{section_idx}/{total_sections}] WARN: No archetype match for {section_name}")
        return None

    # Filter domains by confidence threshold
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
    domain_matches_filtered = [m for m in domain_matches if m['confidence'] >= CONFIDENCE_THRESHOLD]

    if not domain_matches_filtered:
        if verbose:
            safe_print(f"[{section_idx}/{total_sections}] SKIP: No domains above confidence {CONFIDENCE_THRESHOLD}")
        return None

    domain_matches = domain_matches_filtered

    safe_print(f"[{section_idx}/{total_sections}] {section_name}")

    # Combine text from all chunks in this section
    combined_text = ' '.join([c['text'] for c in section_chunks])

    section_data = {
        'section': section_name,
        'page_start': section_chunks[0]['page'],
        'page_end': section_chunks[-1]['page'],
        'chunk_count': len(section_chunks),
        'archetype_matches': [],
        'extracted_facts': {}
    }

    # Try to extract facts from matched domains
    domains_with_facts = 0
    errors = []

    # Check if batching is enabled
    enable_batching = os.getenv("EXTRACTION_BATCH_DOMAINS", "true").lower() == "true"
    max_batch_size = int(os.getenv("EXTRACTION_MAX_BATCH_SIZE", "3"))

    # Decide whether to use batched or individual extraction
    domains_to_extract = [m['domain'] for m in domain_matches]
    use_batching = enable_batching and len(domains_to_extract) >= 2 and len(domains_to_extract) <= max_batch_size

    if use_batching:
        # BATCHED EXTRACTION: Extract all domains in single API call
        safe_print(f"  [BATCH] Processing {len(domains_to_extract)} domains together")

        try:
            # Extract all domains at once
            all_facts = extractor.extract_batched(combined_text, domains_to_extract)

            # Process results
            for i, match in enumerate(domain_matches, 1):
                domain = match['domain']
                confidence = match['confidence']

                # Store match info
                section_data['archetype_matches'].append({
                    'domain': domain,
                    'confidence': confidence,
                    'subsection': match.get('subsection'),
                    'matching_keywords': match.get('matching_keywords', [])
                })

                # Check if facts were extracted for this domain
                if domain in all_facts and all_facts[domain]:
                    section_data['extracted_facts'][domain] = all_facts[domain]
                    domains_with_facts += 1
                    safe_print(f"    [{i}] {domain} (conf: {confidence}) - {len(all_facts[domain])} fields")
                else:
                    safe_print(f"    [{i}] {domain} (conf: {confidence}) - No facts")

        except Exception as e:
            error_msg = f"Section '{section_name}' (batched): {str(e)[:80]}"
            errors.append(error_msg)
            safe_print(f"      [ERR] Batched extraction failed: {str(e)[:60]}")

    else:
        # INDIVIDUAL EXTRACTION: Extract domains one by one (original behavior)
        for i, match in enumerate(domain_matches, 1):
            domain = match['domain']
            confidence = match['confidence']

            safe_print(f"  [{i}] {domain} (confidence: {confidence})")

            try:
                # Extract facts using this domain
                facts = extractor.extract(combined_text, domain)

                if facts:
                    section_data['extracted_facts'][domain] = facts
                    domains_with_facts += 1
                    safe_print(f"      [OK] Extracted {len(facts)} fields")
                else:
                    safe_print(f"      - No facts found for this domain")

            except Exception as e:
                error_msg = f"Section '{section_name}' ({domain}): {str(e)[:80]}"
                errors.append(error_msg)
                safe_print(f"      [ERR] {str(e)[:60]}")

            # Store match info
            section_data['archetype_matches'].append({
                'domain': domain,
                'confidence': confidence,
                'subsection': match.get('subsection'),
                'matching_keywords': match.get('matching_keywords', [])
            })

    safe_print()

    # Return section data if facts were extracted
    if domains_with_facts > 0:
        section_data['_errors'] = errors
        section_data['_multi_domain'] = len(domain_matches) > 1
        return section_data

    return None


def extract_facts(chunks: List[Dict], verbose: bool = False, max_workers: int = None) -> Dict[str, Any]:
    """Extract facts from chunks using archetype-based mapping."""

    # Initialize components
    print("Initializing archetype mapper...")
    mapper = ArchetypeMapper()
    mapper_stats = mapper.get_statistics()
    print(f"[OK] Loaded {mapper_stats['total_archetypes']} archetypes with {mapper_stats['total_subsections']} subsections")
    print()

    print("Initializing DSPy extractor...")
    # ESIAExtractor will use config defaults from .env.local (LLM_PROVIDER, model for that provider)
    extractor = ESIAExtractor()
    print(f"[OK] Extractor initialized (provider: {extractor.provider}, model: {extractor.model})")
    print()

    results = {
        'document': Path(chunks[0]['metadata']['origin']['filename']).name if chunks else 'unknown',
        'extraction_date': datetime.now().isoformat(),
        'total_chunks': len(chunks),
        'sections_processed': 0,
        'sections_skipped': 0,
        'sections_with_facts': 0,
        'multi_domain_sections': 0,
        'mapper_statistics': mapper_stats,
        'sections': {},
        'errors': []
    }

    # Group chunks by section
    sections = {}
    for chunk in chunks:
        section = chunk.get('section') or 'Unknown'
        if section not in sections:
            sections[section] = []
        sections[section].append(chunk)

    print(f"Found {len(sections)} unique sections")
    print("=" * 70)
    print()

    # Determine number of workers from environment or parameter
    if max_workers is None:
        max_workers = int(os.getenv("EXTRACTION_MAX_WORKERS", "4"))

    print(f"Using parallel processing with {max_workers} workers")
    print()

    # Create thread lock for synchronized printing
    print_lock = threading.Lock()

    # Prepare section processing jobs
    section_items = list(sorted(sections.items()))

    # Process sections in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all section processing jobs
        future_to_section = {}
        for idx, (section_name, section_chunks) in enumerate(section_items, 1):
            future = executor.submit(
                process_single_section,
                section_name,
                section_chunks,
                mapper,
                extractor,
                idx,
                len(sections),
                verbose,
                print_lock
            )
            future_to_section[future] = section_name

        # Collect results as they complete
        for future in as_completed(future_to_section):
            section_name = future_to_section[future]
            results['sections_processed'] += 1

            try:
                section_data = future.result()

                if section_data is None:
                    # Section was skipped
                    results['sections_skipped'] += 1
                else:
                    # Extract and remove temporary fields
                    errors = section_data.pop('_errors', [])
                    is_multi_domain = section_data.pop('_multi_domain', False)

                    # Add to results
                    results['sections'][section_name] = section_data
                    results['sections_with_facts'] += 1
                    results['errors'].extend(errors)

                    if is_multi_domain:
                        results['multi_domain_sections'] += 1

            except Exception as e:
                # Catch any unexpected errors from the worker
                error_msg = f"Unexpected error processing '{section_name}': {str(e)[:80]}"
                results['errors'].append(error_msg)
                results['sections_skipped'] += 1
                with print_lock:
                    print(f"[ERROR] {error_msg}")

    print()
    print(f"[OK] Parallel processing completed: {results['sections_processed']} sections processed")
    print()

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Step 3: Extract ESIA facts from chunks with archetype-based mapping'
    )
    parser.add_argument(
        '--chunks',
        required=True,
        help='Path to chunks JSONL file from Step 1 (e.g., ../data/outputs/document_chunks.jsonl)'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output file for extraction results (e.g., ../data/outputs/document_facts.json)'
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
    parser.add_argument(
        '--max-workers',
        type=int,
        default=None,
        help='Number of parallel workers (default: 4, or EXTRACTION_MAX_WORKERS env var)'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("STEP 3: ESIA FACT EXTRACTION WITH ARCHETYPE-BASED MAPPING")
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
    print("Extracting facts with archetype-based section mapping...")
    print()
    results = extract_facts(chunks, verbose=args.verbose, max_workers=args.max_workers)

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
    print(f"Multi-domain sections: {results['multi_domain_sections']}")
    print()

    print("Archetype Coverage:")
    print(f"  Total archetypes: {results['mapper_statistics']['total_archetypes']}")
    print(f"  Total subsections: {results['mapper_statistics']['total_subsections']}")
    print()

    if results['sections']:
        print("Top sections by fact extraction:")
        section_scores = []
        for section_name, section_data in results['sections'].items():
            fact_count = sum(len(facts) for facts in section_data['extracted_facts'].values())
            section_scores.append((section_name, fact_count, len(section_data['extracted_facts'])))

        for section_name, fact_count, domain_count in sorted(section_scores, key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - {section_name}")
            print(f"    Domains: {domain_count}, Fields: {fact_count}")

    if results['errors']:
        print(f"\nErrors: {len(results['errors'])}")
        for error in results['errors'][:3]:
            print(f"  - {error}")

    print()
    print("[OK] Step 3 extraction complete!")


if __name__ == '__main__':
    main()
