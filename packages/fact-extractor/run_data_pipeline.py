#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run_data_pipeline.py

Orchestrates the Docling conversion, fact extraction, and DSPy analysis steps so you
can run the entire pipeline with a single command.

Usage:
  python run_data_pipeline.py <input.pdf> --provider openai --model gpt-4o-mini
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

from step1_pdf_to_markdown import convert_pdf_to_markdown
from file_sanitizer import sanitize_path_component
from output_organizer import create_output_structure


def print_header(title: str):
    print(f"\n{'=' * 80}\n{title}\n{'=' * 80}\n")


def print_step(step_num: int, title: str):
    print(f"\n[{step_num}] {title}\n{'-' * 80}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run Steps 1-3 (Docling conversion → fact extraction → DSPy analysis).",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python %(prog)s your_test.pdf --provider openai --model gpt-4o-mini
  python %(prog)s your_test.pdf --provider ollama --model mistral:latest
        """
    )

    parser.add_argument("pdf_path", type=Path, help="Path to the input PDF or DOCX.")
    parser.add_argument(
        "--provider",
        choices=["openai", "ollama", "anthropic", "gemini"],
        default=os.getenv("LLM_PROVIDER", "ollama"),
        help="LLM provider to use for steps 2 and 3 (default reads from .env or defaults to ollama)."
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Explicit model name for the chosen provider (overrides env defaults)."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for step 2/3 outputs (defaults to output_<pdf_stem>)."
    )
    parser.add_argument(
        "--markdown-dir",
        type=Path,
        default=Path("markdown_outputs"),
        help="Directory where step 1 saves converted markdown files."
    )

    return parser.parse_args()


def run_subprocess(step_num, title, command, env):
    print_step(step_num, title)
    try:
        subprocess.run(command, check=True, env=env)
        return True
    except subprocess.CalledProcessError as exc:
        print(f"  ✗ Step failed: {exc}")
        return False


def configure_environment(provider: str, model: str | None) -> dict:
    env = os.environ.copy()
    env["LLM_PROVIDER"] = provider

    if model:
        var_name = {
            "openai": "OPENAI_MODEL",
            "ollama": "OLLAMA_MODEL",
            "anthropic": "ANTHROPIC_MODEL",
            "gemini": "GEMINI_MODEL"
        }.get(provider)
        if var_name:
            env[var_name] = model

    return env


def main():
    print_header("RUNNING ESIA DATA PIPELINE")

    args = parse_arguments()
    pdf_path = args.pdf_path
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}")
        sys.exit(1)

    load_dotenv()

    provider = args.provider
    model = args.model

    # Create organized output structure based on PDF filename BEFORE conversion
    if args.output_dir:
        # Legacy support: if custom output dir specified, use it directly
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        organizer = None
        markdown_dir = args.markdown_dir
    else:
        # Create organized folder structure
        organizer = create_output_structure(pdf_path.stem, root_dir=".")
        output_dir = organizer.get_project_dir()
        markdown_dir = organizer.get_markdown_dir()  # Get markdown folder from organizer
        organizer.print_structure()
        print(f"Project folder: {organizer.get_sanitized_name()}/")
        print(f"  ├── markdown/ (converted document)")
        print(f"  ├── facts/ (extracted data)")
        print(f"  ├── reports/ (analysis)")
        print(f"  └── checkpoints/ (resume capability)\n")

    print_step(1, f"CONVERTING {pdf_path.name}")
    try:
        markdown_path, _ = convert_pdf_to_markdown(pdf_path, markdown_dir=markdown_dir)
    except Exception as exc:
        print(f"  ✗ Conversion failed: {exc}")
        sys.exit(1)

    env = configure_environment(provider, model)

    step2_cmd = [
        sys.executable,
        "step2_extract_facts.py",
        str(markdown_path),
        str(output_dir)
    ]
    if not run_subprocess(2, "RUNNING STEP 2 (FACT EXTRACTION)", step2_cmd, env):
        sys.exit(1)

    step3_cmd = [
        sys.executable,
        "step3_analyze_facts.py",
        str(output_dir),
        "--provider",
        provider
    ]
    if not run_subprocess(3, "RUNNING STEP 3 (ANALYSIS & REPORT)", step3_cmd, env):
        sys.exit(1)

    report_path = output_dir / "verification_report.md"
    print_header("PIPELINE COMPLETE")
    print(f"Results saved in: {output_dir.absolute()}")
    print(f"Review the verification report: {report_path.absolute()}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPipeline interrupted by user")
        sys.exit(1)
