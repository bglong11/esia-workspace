#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Step 3: Fact Analysis and Verification Checklist Generation

Analyzes the extracted facts from an ESIA to find inconsistencies and generates
a human-friendly verification report in Markdown format.

Usage:
    python step3_analyze_facts.py <input_dir_from_step2> [--provider PROVIDER]

Example:
    python step3_analyze_facts.py ./pipeline_test_openai
"""

import sys
import io
import os
import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd
import dspy
from dotenv import load_dotenv

# Configure UTF-8 output for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def print_header(title):
    print(f"\n{'=' * 80}\n{title}\n{'=' * 80}\n")


def print_step(step_num, title):
    print(f"\n[{step_num}] {title}\n{'-' * 80}")


class CategorizeAndConsolidateFacts(dspy.Signature):
    """
    Consolidates fact mentions and groups them into logical ESIA categories.
    """

    raw_facts = dspy.InputField(
        desc="A string containing raw fact data from a CSV, including name, value, page, and evidence."
    )
    consolidated_factsheet = dspy.OutputField(
        desc="A comprehensive factsheet in Markdown format, grouping all mentions of each unique fact."
    )


class GenerateVerificationChecklist(dspy.Signature):
    """
    Identifies contradictions, inconsistencies, and data quality issues to produce a checklist.
    """

    consolidated_factsheet = dspy.InputField(
        desc="A factsheet in Markdown format with consolidated and categorized facts from an ESIA."
    )
    verification_checklist = dspy.OutputField(
        desc="A prioritized, actionable checklist in Markdown format for human reviewers."
    )


class ESIAFactChecker(dspy.Module):
    """DSPy module that runs the consolidation and checklist signatures sequentially."""

    def __init__(self):
        super().__init__()
        self.consolidator = dspy.ChainOfThought(CategorizeAndConsolidateFacts)
        self.checker = dspy.ChainOfThought(GenerateVerificationChecklist)

    def forward(self, esia_data):
        print("  → Consolidating and categorizing facts...")
        consolidation_result = self.consolidator(raw_facts=esia_data)

        print("  → Analyzing factsheet and generating checklist...")
        checklist_result = self.checker(
            consolidated_factsheet=consolidation_result.consolidated_factsheet
        )

        return dspy.Prediction(
            consolidated_factsheet=consolidation_result.consolidated_factsheet,
            verification_checklist=checklist_result.verification_checklist
        )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Step 3: Fact Analysis and Verification Checklist Generation.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python %(prog)s ./pipeline_test_openai
  python %(prog)s ./pipeline_test_gemini --provider gemini
        """
    )

    parser.add_argument("input_dir", type=Path, help="Directory produced by step2_extract_facts.py.")
    parser.add_argument(
        "--provider",
        type=str,
        choices=["openai", "ollama", "anthropic", "gemini"],
        help="Override the LLM provider for this analysis."
    )
    parser.add_argument(
        "--dump-raw",
        action="store_true",
        help="Write the raw fact input sent to DSPy to <input_dir>/dspy_input.txt"
    )

    return parser.parse_args()


def configure_dspy(provider: str):
    provider = provider.lower()
    print(f"  → Preparing DSPy for provider: {provider.upper()}")

    if provider == "ollama":
        model = os.getenv("OLLAMA_MODEL", "mistral:latest")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        temperature = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))
        max_tokens = int(os.getenv("OLLAMA_MAX_TOKENS", "4096"))

        print(f"    Using Ollama model {model} @ {base_url}")
        print(f"    Max tokens: {max_tokens}")
        lm = dspy.LM(
            model=f"ollama_chat/{model}",
            api_base=base_url,
            api_key="",
            temperature=temperature,
            max_tokens=max_tokens
        )
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment.")

        model = os.getenv("OPENAI_MODEL", "gpt-5")
        temperature = float(os.getenv("OPENAI_TEMPERATURE", "1"))
        max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "16000"))

        print(f"    Using OpenAI model {model}")
        print(f"    Max tokens: {max_tokens}")
        lm = dspy.LM(
            model=f"openai/{model}",
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in the environment.")

        model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
        temperature = float(os.getenv("ANTHROPIC_TEMPERATURE", "0.1"))
        max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", "4096"))

        print(f"    Using Anthropic model {model}")
        print(f"    Max tokens: {max_tokens}")
        lm = dspy.LM(
            model=f"anthropic/{model}",
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in the environment.")

        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.1"))
        max_tokens = int(os.getenv("GEMINI_MAX_TOKENS", "4096"))

        print(f"    Using Gemini model {model}")
        print(f"    Max tokens: {max_tokens}")
        lm = dspy.LM(
            model=f"gemini/{model}",
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    dspy.configure(lm=lm)
    print(f"  ✓ DSPy configured for LLM Provider: {provider.upper()}")
    return lm


def main():
    print_header("STEP 3: FACT ANALYSIS & VERIFICATION CHECKLIST")

    args = parse_arguments()
    input_dir = args.input_dir
    provider_override = args.provider

    load_dotenv()
    llm_provider = (provider_override or os.getenv("LLM_PROVIDER", "openai")).lower()

    try:
        configure_dspy(llm_provider)
    except Exception as exc:
        print(f"  ✗ Error configuring DSPy LM: {exc}")
        return

    print_step(1, "LOADING EXTRACTED FACTS")
    mentions_file = input_dir / "esia_mentions.csv"

    if not mentions_file.exists():
        print(f"  ✗ Error: esia_mentions.csv not found in {input_dir}")
        return

    try:
        df = pd.read_csv(mentions_file)
        columns = ["name", "value_raw", "page", "evidence"]
        present_columns = [col for col in columns if col in df.columns]
        raw_facts_string = df[present_columns].to_string(index=False)
        print(f"  ✓ Loaded {len(df)} fact mentions from {mentions_file.name}")
    except Exception as exc:
        print(f"  ✗ Error reading CSV file: {exc}")
        return

    if args.dump_raw:
        debug_path = input_dir / "dspy_input.txt"
        try:
            debug_path.write_text(raw_facts_string, encoding="utf-8")
            print(f"  ✓ Dumped DSPy input to {debug_path.name}")
        except Exception as exc:
            print(f"  ⚠️ Failed to dump DSPy input: {exc}")

    print_step(2, "RUNNING DSPY ANALYSIS MODULE")
    try:
        fact_checker = ESIAFactChecker()
        result = fact_checker(esia_data=raw_facts_string)
        print("  ✓ DSPy module execution complete.")
    except Exception as exc:
        print(f"  ✗ DSPy module failed: {exc}")
        return

    verification_checklist = result.verification_checklist or (
        "⚠️ DSPy did not return a verification checklist. "
        "This often happens when the LLM response is truncated; "
        "consider increasing the provider max_tokens setting."
    )
    if result.verification_checklist is None:
        print("  ⚠️ DSPy did not produce a checklist, so a placeholder text is being used.")
    consolidated_factsheet = result.consolidated_factsheet or (
        "⚠️ DSPy did not return a consolidated factsheet. "
        "Please re-run with a larger max_tokens value or check the LLM logs."
    )
    if result.consolidated_factsheet is None:
        print("  ⚠️ DSPy did not produce a consolidated factsheet; using fallback text.")

    print_step(3, "GENERATING VERIFICATION REPORT")
    report_path = input_dir / "verification_report.md"

    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# ESIA Verification Report\n\n")
            f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Source Directory:** `{input_dir.absolute()}`\n\n")
            f.write("## 1. Actionable Verification Checklist\n\n")
            f.write("This checklist highlights potential inconsistencies and issues found in the ESIA data. Please review each item and make corrections in the source document.\n\n")
            f.write(verification_checklist)
            f.write("\n\n---\n\n")
            f.write("## 2. Comprehensive Factsheet\n\n")
            f.write("This is a consolidated list of all unique facts extracted from the document for reference.\n\n")
            f.write(consolidated_factsheet)

        print("  ✓ Verification report successfully generated.")
        print_header("STEP 3 COMPLETE")
        print(f"Success! Review the final report at:\n  {report_path.absolute()}")
    except Exception as exc:
        print(f"  ✗ Failed to write report file: {exc}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nFact analysis interrupted by user")
        sys.exit(1)
    except Exception as exc:
        print(f"\nFatal error: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
