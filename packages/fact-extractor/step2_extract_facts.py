#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Step 2: Fact Extraction and Factsheet Generation
Extracts facts from markdown and generates categorized factsheet

Usage:
    python step2_extract_facts.py <input.md> <output_dir> [--model MODEL]
    python step2_extract_facts.py markdown_outputs/your_test_20250101_120000.md ./pipeline_test_default
    python step2_extract_facts.py markdown_outputs/your_test_20250101_120000.md ./pipeline_test_claude --model anthropic/claude-haiku-4-5-20251001

Available models through OpenRouter:
    - openai/gpt-4o (default)
    - openai/gpt-4o-mini (fast, cost-effective)
    - anthropic/claude-haiku-4-5-20251001 (fast)
    - anthropic/claude-sonnet-4-20250514 (balanced)
    - google/gemini-2.0-flash (multimodal)
"""

import sys
import io
import os
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Configure UTF-8 output for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def print_header(title):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}\n")


def print_step(step_num, title):
    """Print a step header."""
    print(f"\n[{step_num}] {title}")
    print("-" * 80)


def print_success(msg):
    """Print success message."""
    print(f"  ✓ {msg}")


def print_error(msg):
    """Print error message."""
    print(f"  ✗ {msg}")


def print_info(msg):
    """Print info message."""
    print(f"  → {msg}")


def parse_arguments():
    """Parse command-line arguments using argparse."""

    parser = argparse.ArgumentParser(
        description="Step 2: Fact Extraction and Factsheet Generation.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python %(prog)s markdown_outputs/your_test.md ./pipeline_test_default
  python %(prog)s markdown_outputs/your_test.md ./pipeline_test_claude --model anthropic/claude-haiku-4-5-20251001
  python %(prog)s markdown_outputs/your_test.md ./pipeline_test_gemini --model google/gemini-2.0-flash
        """
    )

    parser.add_argument("markdown_path", type=Path, help="Path to the input markdown file.")
    parser.add_argument("output_dir", type=Path, help="Directory to save the output files.")
    parser.add_argument(
        "--model",
        type=str,
        help="Override the LLM model specified in the .env file (e.g., 'openai/gpt-4o', 'anthropic/claude-haiku-4-5-20251001')"
    )

    args = parser.parse_args()
    return args.markdown_path, args.output_dir, args.model


def set_llm_model(model):
    """Set LLM model in environment variables."""
    if not model:
        return True  # Use default from .env

    # Validate model format (should be "provider/model-name")
    if "/" not in model:
        print_error(f"Invalid model format: {model}")
        print_info("Expected format: 'provider/model-name' (e.g., 'openai/gpt-4o', 'anthropic/claude-haiku-4-5-20251001')")
        return False

    # Check if OpenRouter API key is set
    if not os.getenv("OPENROUTER_API_KEY"):
        print_error("OPENROUTER_API_KEY not set in .env file")
        print_info("Get your API key from https://openrouter.ai/")
        return False

    # Set model in environment
    os.environ["OPENROUTER_MODEL"] = model
    return True


def main():
    """Run fact extraction and factsheet generation."""

    print_header("STEP 2: FACT EXTRACTION & FACTSHEET GENERATION")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Load .env file first
    load_dotenv()

    # Parse command-line arguments
    markdown_path, output_dir, model = parse_arguments()

    # Set LLM model if specified
    if model:
        if not set_llm_model(model):
            return False
        print_success(f"LLM Model override: {model}")

    # Check if markdown file exists
    if not markdown_path.exists():
        print_error(f"Markdown file not found: {markdown_path}")
        return False

    print_success(f"Found markdown: {markdown_path}")
    print_info(f"File size: {markdown_path.stat().st_size / 1024:.1f} KB")

    # ========================================================================
    # PHASE 1: CREATE OUTPUT DIRECTORY
    # ========================================================================

    print_step(1, "CREATING OUTPUT DIRECTORY")

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        print_success(f"Output directory ready: {output_dir.absolute()}")
    except Exception as e:
        print_error(f"Failed to create output directory: {e}")
        return False

    # ========================================================================
    # PHASE 2: FACT EXTRACTION & FACTSHEET GENERATION
    # ========================================================================

    print_step(2, "EXTRACTING FACTS & GENERATING FACTSHEET")

    # Check which LLM model is configured
    llm_model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

    print_info(f"LLM Provider: OpenRouter")
    print_info(f"Input Markdown: {markdown_path}")
    print_info(f"Output Directory: {output_dir}")
    print_info(f"\nStarting esia_extractor.py...")

    try:
        # Prepare environment for subprocess with LLM provider settings
        env = os.environ.copy()

        # Run esia_extractor.py as subprocess
        result = subprocess.run(
            [sys.executable, "esia_extractor.py", str(markdown_path), str(output_dir)],
            capture_output=True,
            text=True,
            timeout=1800,  # 30 minute timeout
            env=env  # Pass environment variables including LLM_PROVIDER
        )

        # Print extraction output
        print(result.stdout)

        if result.returncode != 0:
            print_error(f"Extraction failed with return code {result.returncode}")
            if result.stderr:
                print(f"STDERR:\n{result.stderr}")
            return False

        print_success("Fact extraction and factsheet generation completed")

    except subprocess.TimeoutExpired:
        print_error("Extraction timeout (exceeded 30 minutes)")
        print_info("The document is very large or the LLM provider is slow.")
        print_info("Consider using a local LLM (Ollama) or splitting the document.")
        return False
    except Exception as e:
        print_error(f"Subprocess execution failed: {e}")
        return False

    # ========================================================================
    # PHASE 3: VERIFY OUTPUT FILES
    # ========================================================================

    print_step(3, "VERIFYING OUTPUT FILES")

    expected_files = [
        "esia_mentions.csv",
        "esia_consolidated.csv",
        "esia_replacement_plan.csv",
        "project_factsheet.csv"
    ]

    all_exist = True
    file_sizes = {}

    for filename in expected_files:
        filepath = output_dir / filename
        if filepath.exists() and filepath.stat().st_size > 10:
            size = filepath.stat().st_size
            file_sizes[filename] = size
            print_success(f"{filename} ({size / 1024:.1f} KB)")
        else:
            if not filepath.exists():
                print_error(f"{filename} NOT FOUND")
            else:
                print_error(f"{filename} is empty or invalid (size: {filepath.stat().st_size} bytes)")
            all_exist = False

    if not all_exist:
        print_info(f"\nOutput directory contents:")
        for f in output_dir.glob("*"):
            print_info(f"  {f.name} ({f.stat().st_size / 1024:.1f} KB)")
        return False

    # ========================================================================
    # PHASE 4: GENERATE SUMMARY REPORT
    # ========================================================================

    print_step(4, "SUMMARY REPORT")

    print("\nPipeline Statistics:")
    print(f"  Markdown Input Size:      {markdown_path.stat().st_size / 1024:.1f} KB")

    # Count lines in factsheet to estimate facts
    try:
        factsheet_path = output_dir / "project_factsheet.csv"
        with open(factsheet_path, "r", encoding="utf-8") as f:
            factsheet_lines = len(f.readlines())
        facts_count = factsheet_lines - 1  # Subtract header
        print(f"  Facts Extracted:          {facts_count}")
    except:
        print(f"  Facts Extracted:          (see CSV files)")

    print("\nOutput Files Generated:")
    total_size = 0
    for filename, size in file_sizes.items():
        print(f"  {filename:35} {size / 1024:8.1f} KB")
        total_size += size
    print(f"  {'TOTAL':35} {total_size / 1024:8.1f} KB")

    # ========================================================================
    # FINAL STATUS
    # ========================================================================

    print_header("STEP 2 COMPLETE")
    print(f"Status: SUCCESS\n")
    print(f"Output Location: {output_dir.absolute()}\n")
    print(f"Generated Files:")
    print(f"  1. {output_dir}/esia_mentions.csv")
    print(f"  2. {output_dir}/esia_consolidated.csv")
    print(f"  3. {output_dir}/esia_replacement_plan.csv")
    print(f"  4. {output_dir}/project_factsheet.csv")
    print(f"\nNext Step:")
    print("  Run the analysis script to generate a prioritized verification report.")
    print(f"  python step3_analyze_facts.py \"{output_dir.absolute()}\"")
    print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nFact extraction interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
