#!/usr/bin/env python3
"""
Debug LLM Extraction - Shows Raw Prompts and Responses

This script provides maximum visibility into LLM interactions to diagnose
why fact extraction is failing.

Usage:
    python test_llm_debug.py <markdown_file>
    python test_llm_debug.py docling_output/test_docling.md
"""

import sys
import json
import re
from pathlib import Path
from typing import List, Dict

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import dspy
from pydantic import BaseModel, Field
from saas.core.extractor import (
    configure_llm,
    chunk_markdown,
    Fact,
    slugify,
    normalize_unit,
    ExtractedFact,
    FactExtractionSignature
)


class DebugFactExtractor:
    """
    Debug version of FactExtractor using JSON string output
    """

    def __init__(self):
        # Create few-shot examples
        self._add_examples()

        # Use ChainOfThought for better reasoning about fact extraction
        self.extractor = dspy.ChainOfThought(FactExtractionSignature)

        # Set demonstrations
        if hasattr(self, 'examples') and self.examples:
            self.extractor.demos = self.examples
            print(f"Loaded {len(self.examples)} few-shot examples\n")

    def _add_examples(self):
        """Add few-shot examples with structured text output"""
        try:
            # Example 1: Quantitative facts
            example1_text = "The proposed mining project will cover an area of 500 hectares in the northern region. The total investment is estimated at $50 million. Annual coal production is expected to reach 2 million tonnes per year. The project manager is John Smith."

            example1_output = """FACT: Project area
TYPE: quantity
VALUE: 500
VALUE_NUM: 500
UNIT: hectares
EVIDENCE: The proposed mining project will cover an area of 500 hectares
---
FACT: Annual coal production
TYPE: quantity
VALUE: 2 million
VALUE_NUM: 2000000
UNIT: tonnes/year
EVIDENCE: Annual coal production is expected to reach 2 million tonnes per year
---
FACT: Total investment
TYPE: quantity
VALUE: 50 million
VALUE_NUM: 50000000
UNIT: $
EVIDENCE: The total investment is estimated at $50 million
---"""

            example1 = dspy.Example(
                text=example1_text,
                output=example1_output
            ).with_inputs("text")

            self.examples = [example1]

        except Exception as e:
            print(f"Warning: Could not add few-shot examples: {e}")
            self.examples = []

    def _parse_structured_output(self, text_output: str) -> List[Dict[str, str]]:
        """Parse structured text format into fact dictionaries"""
        facts_list = []
        blocks = text_output.split('---')

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            fact_dict = {}
            lines = block.split('\n')

            for line in lines:
                line = line.strip()
                if ':' not in line:
                    continue

                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()

                if key == 'fact':
                    fact_dict['name'] = value
                elif key == 'type':
                    fact_dict['type'] = value.lower()
                elif key == 'value':
                    fact_dict['value'] = value
                elif key == 'value_num':
                    try:
                        fact_dict['value_num'] = float(value) if value else 0
                    except ValueError:
                        fact_dict['value_num'] = 0
                elif key == 'unit':
                    fact_dict['unit'] = value
                elif key == 'evidence':
                    fact_dict['evidence'] = value

            if 'name' in fact_dict and 'type' in fact_dict:
                fact_dict.setdefault('value', '')
                fact_dict.setdefault('value_num', 0)
                fact_dict.setdefault('unit', '')
                fact_dict.setdefault('evidence', '')
                fact_dict.setdefault('aliases', [])
                facts_list.append(fact_dict)

        return facts_list

    def extract_from_chunk(self, text: str, page: int, chunk_id: int) -> List[Fact]:
        """Extract facts with detailed debugging using structured text output"""

        print(f"\n{'='*80}")
        print(f"EXTRACTING FROM CHUNK {chunk_id}")
        print(f"{'='*80}\n")

        print(f"📄 Input text preview ({len(text)} chars):")
        print("-" * 80)
        print(text[:500] + "..." if len(text) > 500 else text)
        print("-" * 80)

        try:
            # Call DSPy extractor
            print("\n⚙️  Calling DSPy ChainOfThought extractor...")
            print("  Method: ChainOfThought (adds reasoning)")
            print("  Input field: 'text' (document chunk)")
            print("  Output field: 'output' (JSON string)")

            result = self.extractor(text=text)

            print("\n✅ DSPy call completed")

            # Show the result object
            print(f"\n🔍 Result object type: {type(result)}")
            print(f"   Has 'output' attribute: {hasattr(result, 'output')}")

            # Get the structured text output
            print(f"\n📤 Raw Output:")
            print("-" * 80)

            text_output = result.output
            print(f"Type: {type(text_output)}")
            print(f"Length: {len(text_output) if text_output else 0} chars")
            print(f"Preview: {text_output[:300] if text_output else 'None'}...")
            print("-" * 80)

            if not text_output or text_output.strip() == "":
                print("  ⚠️  No output from LLM")
                return []

            # Parse structured text output
            print("\n📋 Parsing structured text output...")
            try:
                facts_list = self._parse_structured_output(text_output)

                if not facts_list:
                    print(f"⚠️  No facts could be parsed from output")
                    print(f"  Output was: {text_output[:200]}")
                    return []

                print(f"✅ Parsing complete")
                print(f"   Found {len(facts_list)} fact(s)")

            except Exception as e:
                print(f"❌ Parse Error: {type(e).__name__}: {e}")
                return []

            # Process each fact
            print(f"\n✅ Processing {len(facts_list)} fact(s)")
            facts = []
            for i, fact_dict in enumerate(facts_list):
                try:
                    print(f"\n  Processing fact {i+1}:")
                    print(f"    Raw: {fact_dict}")

                    # Validate against Pydantic model
                    extracted_fact = ExtractedFact(**fact_dict)

                    print(f"    Type: {type(extracted_fact)}")
                    print(f"    Name: {extracted_fact.name}")
                    print(f"    Value: {extracted_fact.value} {extracted_fact.unit}")
                    print(f"    Value (numeric): {extracted_fact.value_num}")
                    print(f"    Type: {extracted_fact.type}")
                    print(f"    Aliases: {extracted_fact.aliases}")
                    print(f"    Evidence: {extracted_fact.evidence[:60]}...")

                    # Create Fact object from Pydantic model
                    fact = Fact(
                        name=extracted_fact.name,
                        type=extracted_fact.type,
                        value=extracted_fact.value,
                        value_num=extracted_fact.value_num,
                        unit=extracted_fact.unit,
                        aliases=extracted_fact.aliases,
                        evidence=extracted_fact.evidence,
                        page=page,
                        chunk_id=chunk_id
                    )

                    # Canonicalize
                    fact.signature = slugify(fact.name)

                    # Normalize units
                    fact.normalized_value, fact.normalized_unit = normalize_unit(
                        fact.value_num, fact.unit
                    )

                    print(f"    ✓ Created Fact: {fact.name} = {fact.value} {fact.unit}")
                    print(f"      Normalized: {fact.normalized_value} {fact.normalized_unit}")
                    print(f"      Signature: {fact.signature}")

                    facts.append(fact)
                except Exception as e:
                    print(f"    ❌ Error processing fact: {e}")
                    continue

            print(f"\n✅ Successfully extracted {len(facts)} fact(s)")
            return facts

        except Exception as e:
            print(f"\n❌ Extraction Error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return []


def test_with_simple_prompt():
    """Test with a very simple prompt to verify LLM is working"""
    print("\n" + "="*80)
    print("SIMPLE LLM TEST")
    print("="*80 + "\n")

    print("Testing if LLM can respond to basic prompts...")

    try:
        lm = configure_llm()

        # Test 1: Simple text generation
        print("\nTest 1: Simple text generation")
        print("-" * 80)
        test_prompt = "What is 2+2? Answer with just the number."
        print(f"Prompt: {test_prompt}")

        response = lm(test_prompt)
        print(f"Response: {response}")
        print(f"Response type: {type(response)}")

        # Test 2: JSON generation
        print("\n\nTest 2: JSON generation")
        print("-" * 80)
        json_prompt = """Return a JSON array with one fact about the following text:
"The project area is 500 hectares."

Return ONLY valid JSON in this exact format:
[{"name": "Project area", "type": "quantity", "value": "500", "value_num": 500, "unit": "ha", "evidence": "The project area is 500 hectares."}]
"""
        print(f"Prompt: {json_prompt}")

        response = lm(json_prompt)
        print(f"Response: {response}")
        print(f"Response type: {type(response)}")

        # Try to parse it
        try:
            parsed = json.loads(response)
            print(f"✅ Valid JSON! Parsed: {parsed}")
        except:
            print(f"❌ Not valid JSON")

    except Exception as e:
        print(f"❌ Error in simple test: {e}")
        import traceback
        traceback.print_exc()


class TeeOutput:
    """Write to both console and file"""
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, 'w', encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def close(self):
        self.log.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_llm_debug.py <markdown_file>")
        print("\nExample:")
        print("  python test_llm_debug.py docling_output/test_docling.md")
        print("\nOr run simple LLM test:")
        print("  python test_llm_debug.py --test")
        sys.exit(1)

    if sys.argv[1] == "--test":
        # Run simple LLM test
        test_with_simple_prompt()
        return

    markdown_file = sys.argv[1]

    # Setup output file
    output_file = "llm_debug_output.txt"
    tee = TeeOutput(output_file)
    sys.stdout = tee

    print("="*80)
    print("LLM EXTRACTION DEBUG TEST")
    print("="*80)
    print(f"\nInput file: {markdown_file}")
    print(f"Output also saved to: {output_file}\n")

    # Read markdown
    markdown_path = Path(markdown_file)
    if not markdown_path.exists():
        print(f"❌ File not found: {markdown_file}")
        return

    with open(markdown_path, 'r', encoding='utf-8') as f:
        text = f.read()

    print(f"✓ Loaded {len(text):,} characters")

    # Configure LLM
    print("\n" + "="*80)
    print("CONFIGURING LLM")
    print("="*80 + "\n")

    import os
    print(f"OLLAMA_MODEL: {os.getenv('OLLAMA_MODEL', 'qwen2.5:7b-instruct')}")
    print(f"OLLAMA_BASE_URL: {os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}")
    print(f"LLM_TEMPERATURE: {os.getenv('LLM_TEMPERATURE', '0.2')}")
    print(f"LLM_MAX_TOKENS: {os.getenv('LLM_MAX_TOKENS', '2048')}")

    lm = configure_llm()
    print(f"\n✓ LLM configured")

    # Chunk text
    print("\n" + "="*80)
    print("CHUNKING TEXT")
    print("="*80 + "\n")

    chunks = chunk_markdown(text, max_chars=4000)
    print(f"Created {len(chunks)} chunks")

    # Create debug extractor
    extractor = DebugFactExtractor()

    # Process first chunk only (for detailed debugging)
    print("\n" + "="*80)
    print("PROCESSING FIRST CHUNK ONLY (for detailed output)")
    print("="*80)

    facts = extractor.extract_from_chunk(chunks[0], page=1, chunk_id=0)

    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80 + "\n")

    if facts:
        print(f"✅ SUCCESS: Extracted {len(facts)} fact(s)")
        for i, fact in enumerate(facts):
            print(f"\nFact {i+1}:")
            print(f"  Name: {fact.name}")
            print(f"  Value: {fact.value} {fact.unit}")
            print(f"  Normalized: {fact.normalized_value} {fact.normalized_unit}")
            print(f"  Evidence: {fact.evidence[:100]}...")
    else:
        print("❌ FAILED: No facts extracted")
        print("\nTroubleshooting steps:")
        print("1. Run simple LLM test: python test_llm_debug.py --test")
        print("2. Check Ollama: ollama list")
        print("3. Test model directly: ollama run qwen2.5:7b-instruct")
        print("4. Check the markdown content has extractable facts")

    # Close the output file
    tee.close()
    sys.stdout = tee.terminal

    print(f"\n✓ Full debug output saved to: {output_file}")


if __name__ == "__main__":
    main()
