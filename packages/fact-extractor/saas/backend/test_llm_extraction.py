#!/usr/bin/env python3
"""
Test LLM Fact Extraction with Detailed Debug Output

This script reads a markdown file (from Docling output) and extracts facts
using the LLM, showing all intermediate results for debugging.

Usage:
    python test_llm_extraction.py <markdown_file>
    python test_llm_extraction.py docling_output/test_docling.md
"""

import sys
import json
from pathlib import Path
from pprint import pprint

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from saas.core.extractor import (
    configure_llm,
    chunk_markdown,
    FactExtractor,
    Fact
)

def print_section(title: str):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_chunk_preview(chunk: str, max_chars: int = 500):
    """Print preview of chunk content"""
    if len(chunk) <= max_chars:
        print(chunk)
    else:
        print(chunk[:max_chars])
        print(f"\n... [truncated, total {len(chunk):,} characters]")


def test_llm_extraction(markdown_file: str):
    """
    Test LLM extraction with detailed debugging output

    Args:
        markdown_file: Path to markdown file to process
    """

    print_section("LLM FACT EXTRACTION TEST")
    print(f"Input file: {markdown_file}")

    # Read markdown file
    print_section("1. READING MARKDOWN FILE")

    markdown_path = Path(markdown_file)
    if not markdown_path.exists():
        print(f"❌ Error: File not found: {markdown_file}")
        return

    with open(markdown_path, 'r', encoding='utf-8') as f:
        text = f.read()

    print(f"✓ File loaded successfully")
    print(f"  Total characters: {len(text):,}")
    print(f"  Total lines: {text.count(chr(10)) + 1:,}")
    print(f"\nFirst 500 characters:")
    print("-" * 80)
    print_chunk_preview(text, 500)

    # Configure LLM
    print_section("2. CONFIGURING LLM")

    try:
        import os
        print("Environment variables:")
        print(f"  OLLAMA_MODEL: {os.getenv('OLLAMA_MODEL', 'qwen2.5:7b-instruct')} (default)")
        print(f"  OLLAMA_BASE_URL: {os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')} (default)")
        print(f"  LLM_TEMPERATURE: {os.getenv('LLM_TEMPERATURE', '0.2')} (default)")
        print(f"  LLM_MAX_TOKENS: {os.getenv('LLM_MAX_TOKENS', '2048')} (default)")

        lm = configure_llm()
        print(f"\n✓ LLM configured successfully")
        print(f"  Model: {lm.model}")
        print(f"  Base URL: {lm.base_url}")

    except Exception as e:
        print(f"❌ Error configuring LLM: {e}")
        import traceback
        traceback.print_exc()
        return

    # Chunk text
    print_section("3. CHUNKING TEXT")

    max_chars = 4000
    print(f"Chunk size: {max_chars:,} characters")

    chunks = chunk_markdown(text, max_chars=max_chars)
    print(f"\n✓ Text chunked successfully")
    print(f"  Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i}: {len(chunk):,} characters")

    # Create extractor
    print_section("4. CREATING FACT EXTRACTOR")

    try:
        extractor = FactExtractor()
        print("✓ FactExtractor created successfully")
    except Exception as e:
        print(f"❌ Error creating extractor: {e}")
        import traceback
        traceback.print_exc()
        return

    # Extract facts from each chunk
    print_section("5. EXTRACTING FACTS FROM CHUNKS")

    all_facts = []

    for chunk_idx, chunk in enumerate(chunks):
        print("\n" + "-" * 80)
        print(f"PROCESSING CHUNK {chunk_idx + 1}/{len(chunks)}")
        print("-" * 80)

        print(f"\n📄 Chunk content ({len(chunk):,} characters):")
        print("~" * 80)
        print_chunk_preview(chunk, 800)
        print("~" * 80)

        # Show the prompt that will be sent
        print(f"\n🔍 DSPy Signature:")
        print("  Input field: 'document_chunk' (the chunk text above)")
        print("  Output field: 'facts' (expected JSON array)")
        print("  Method: ChainOfThought (includes reasoning step)")

        # Extract facts
        print(f"\n⚙️  Calling LLM...")

        try:
            # Call the extraction method
            facts = extractor.extract_from_chunk(chunk, chunk_idx)

            print(f"✓ LLM call completed")
            print(f"  Facts extracted: {len(facts)}")

            if facts:
                print(f"\n📊 Extracted facts:")
                for i, fact in enumerate(facts):
                    print(f"\n  Fact {i + 1}:")
                    print(f"    Name: {fact.name}")
                    print(f"    Value: {fact.value}")
                    print(f"    Unit: {fact.unit}")
                    print(f"    Normalized value: {fact.normalized_value}")
                    print(f"    Canonical unit: {fact.canonical_unit}")
                    print(f"    Evidence: {fact.evidence[:100]}..." if len(fact.evidence) > 100 else f"    Evidence: {fact.evidence}")
                    print(f"    Page: {fact.page_number}")
                    print(f"    Chunk: {fact.chunk_number}")

                all_facts.extend(facts)
            else:
                print("  ⚠️  No facts extracted from this chunk")

        except Exception as e:
            print(f"\n❌ Error extracting facts from chunk {chunk_idx}:")
            print(f"  Error type: {type(e).__name__}")
            print(f"  Error message: {e}")
            import traceback
            traceback.print_exc()

            # Try to get more details about the LLM response
            print("\n🔬 Attempting to inspect raw LLM response...")
            try:
                # Access DSPy internals to see what happened
                import dspy
                print("  DSPy configuration:")
                print(f"    Language model: {dspy.settings.lm}")

                # Try a raw LLM call to see the response
                print("\n  Testing raw LLM call with simplified prompt...")
                test_prompt = "Extract facts from this text: The project area is 500 hectares."

                try:
                    response = lm(test_prompt)
                    print(f"  Raw LLM response type: {type(response)}")
                    print(f"  Raw LLM response:")
                    print("  " + "-" * 76)
                    print(f"  {response}")
                    print("  " + "-" * 76)
                except Exception as inner_e:
                    print(f"  Raw LLM call also failed: {inner_e}")

            except Exception as inspect_error:
                print(f"  Could not inspect LLM internals: {inspect_error}")

    # Summary
    print_section("6. EXTRACTION SUMMARY")

    print(f"Total chunks processed: {len(chunks)}")
    print(f"Total facts extracted: {len(all_facts)}")

    if all_facts:
        print("\n✅ SUCCESS: Facts were extracted!")
        print("\nAll facts:")
        for i, fact in enumerate(all_facts):
            print(f"\n{i + 1}. {fact.name}")
            print(f"   Value: {fact.value} {fact.unit}")
            print(f"   Normalized: {fact.normalized_value} {fact.canonical_unit}")
            print(f"   From chunk: {fact.chunk_number}")
    else:
        print("\n❌ PROBLEM: No facts were extracted from any chunks")
        print("\nPossible issues:")
        print("  1. LLM not returning valid JSON")
        print("  2. LLM not finding any facts in the content")
        print("  3. Prompt format incompatible with model")
        print("  4. Model not loaded or connection issue")
        print("\nNext steps:")
        print("  - Check Ollama is running: ollama list")
        print("  - Test model directly: ollama run qwen2.5:7b-instruct")
        print("  - Check LLM temperature (lower = more consistent JSON)")
        print("  - Verify chunk content has extractable facts")


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_llm_extraction.py <markdown_file>")
        print("\nExample:")
        print("  python test_llm_extraction.py docling_output/test_docling.md")
        sys.exit(1)

    markdown_file = sys.argv[1]
    test_llm_extraction(markdown_file)


if __name__ == "__main__":
    main()
