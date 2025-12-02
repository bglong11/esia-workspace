#!/usr/bin/env python3
"""
ESIA Pipeline CLI - Unified Document Processing and Analysis Workflow

This orchestrates a unified 3-step pipeline with single input/output directories:

INPUT:  ./data/pdfs/              (PDF/DOCX files to process)
OUTPUT: ./data/outputs/           (ALL pipeline outputs in one place)

The pipeline consists of three main steps:
1. Chunk PDF/DOCX into semantic chunks with page tracking
2. Extract domain-specific facts using archetype-based extraction
3. Analyze extracted facts for consistency and compliance

Filename sanitization happens first and is used consistently throughout.

Usage:
    python run-esia-pipeline.py <pdf_file>                    # Run all steps
    python run-esia-pipeline.py <pdf_file> --steps 1,3        # Run specific steps
    python run-esia-pipeline.py --help                        # Show help

Examples:
    python run-esia-pipeline.py data/pdfs/ESIA_Report.pdf
    python run-esia-pipeline.py "Project XYZ (Draft).pdf" --steps 1,2
"""

import argparse
import logging
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).parent

# Component directories
EXTRACTOR_DIR = ROOT / "esia-fact-extractor-pipeline"
ANALYZER_DIR = ROOT / "esia-fact-analyzer"

# UNIFIED I/O directories (single source of truth)
UNIFIED_OUTPUT_DIR = ROOT / "data" / "outputs"
UNIFIED_INPUT_DIR = ROOT / "data" / "pdfs"

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO


def sanitize_pdf_stem(pdf_path: str) -> str:
    """
    Extract and sanitize filename stem from a PDF/DOCX file path.

    This is the FIRST step - the sanitized stem is used consistently
    throughout the entire pipeline.

    Args:
        pdf_path: Path to the PDF/DOCX file

    Returns:
        Sanitized stem suitable for use in filenames

    Examples:
        "Project XYZ (Draft).pdf" → "Project_XYZ_Draft"
        "ESIA Report Final.docx" → "ESIA_Report_Final"
        "/path/to/file name.pdf" → "file_name"
    """
    path = Path(pdf_path)

    # Get filename without extension
    filename = path.stem

    # Replace spaces and special characters with underscores
    # Keep only alphanumeric characters, hyphens, and underscores
    sanitized = re.sub(r"[^\w\-]", "_", filename)

    # Replace multiple consecutive underscores with single underscore
    sanitized = re.sub(r"_+", "_", sanitized)

    # Remove leading/trailing underscores
    sanitized = sanitized.strip("_")

    # Replace hyphens with underscores for consistency
    sanitized = sanitized.replace("-", "_")

    if not sanitized:
        raise ValueError(f"Could not sanitize filename from: {pdf_path}")

    return sanitized


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else LOG_LEVEL
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    return logging.getLogger(__name__)


def validate_directories(logger: logging.Logger) -> None:
    """Validate that required component directories exist."""
    required_dirs = {
        "Extractor": EXTRACTOR_DIR,
        "Analyzer": ANALYZER_DIR,
    }

    for name, path in required_dirs.items():
        if not path.exists():
            logger.error(f"{name} directory not found: {path}")
            raise FileNotFoundError(f"{name} directory not found: {path}")
        logger.debug(f"OK - {name} directory found: {path}")


def validate_pdf_file(pdf_path: str, logger: logging.Logger) -> Path:
    """
    Validate that PDF file exists and is readable.

    Args:
        pdf_path: Path to the PDF/DOCX file
        logger: Logger instance

    Returns:
        Path object for the validated file

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(pdf_path)

    if not path.exists():
        logger.error(f"PDF file not found: {pdf_path}")
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if not path.is_file():
        logger.error(f"Path is not a file: {pdf_path}")
        raise FileNotFoundError(f"Path is not a file: {pdf_path}")

    # Check file extension
    suffix = path.suffix.lower()
    if suffix not in {".pdf", ".docx"}:
        logger.warning(f"File extension is {suffix}, expected .pdf or .docx")

    logger.debug(f"OK - PDF file validated: {path.absolute()}")
    return path


def run_chunking(pdf_path: str, pdf_stem: str, logger: logging.Logger) -> None:
    """
    Step 1: Run document chunking with Docling.

    Converts PDF/DOCX to semantic chunks with token counts and page numbers.
    All output goes to unified ./data/outputs/ directory.

    Args:
        pdf_path: Full path to PDF file
        pdf_stem: Sanitized PDF filename stem
        logger: Logger instance for output
    """
    logger.info("=" * 70)
    logger.info("STEP 1: Running Document Chunking")
    logger.info("=" * 70)
    logger.info(f"Input:  {pdf_path}")
    logger.info(f"Output stem: {pdf_stem}")

    # Convert to absolute path since step1 runs from different working directory
    pdf_path_abs = str(Path(pdf_path).absolute())

    cmd = [
        "python",
        "step1_docling_hybrid_chunking.py",
        pdf_path_abs,
        "--output-dir", str(UNIFIED_OUTPUT_DIR),
        "--gpu-mode", "cpu",
    ]

    logger.info(f"Command: {' '.join(cmd)}")
    logger.info(f"Working directory: {EXTRACTOR_DIR}")

    try:
        subprocess.run(
            cmd,
            cwd=EXTRACTOR_DIR,
            check=True,
            capture_output=False,
        )
        logger.info("SUCCESS - Chunking completed successfully")

        # Step 1 uses the original PDF stem (with spaces/special chars)
        # We need to rename outputs to use the sanitized stem
        original_stem = Path(pdf_path_abs).stem
        if original_stem != pdf_stem:
            logger.debug(f"Renaming outputs from '{original_stem}' to '{pdf_stem}'")

            # Rename chunks file
            original_chunks = UNIFIED_OUTPUT_DIR / f"{original_stem}_chunks.jsonl"
            sanitized_chunks = UNIFIED_OUTPUT_DIR / f"{pdf_stem}_chunks.jsonl"
            if original_chunks.exists():
                # Delete existing sanitized version if present (re-run scenario)
                if sanitized_chunks.exists():
                    sanitized_chunks.unlink()
                original_chunks.rename(sanitized_chunks)
                logger.debug(f"Renamed chunks: {original_stem} → {pdf_stem}")

            # Rename metadata file
            original_meta = UNIFIED_OUTPUT_DIR / f"{original_stem}_meta.json"
            sanitized_meta = UNIFIED_OUTPUT_DIR / f"{pdf_stem}_meta.json"
            if original_meta.exists():
                # Delete existing sanitized version if present (re-run scenario)
                if sanitized_meta.exists():
                    sanitized_meta.unlink()
                original_meta.rename(sanitized_meta)
                logger.debug(f"Renamed metadata: {original_stem} → {pdf_stem}")
    except subprocess.CalledProcessError as e:
        logger.error(f"FAILED - Chunking failed with exit code {e.returncode}")
        raise


def run_fact_extraction(pdf_stem: str, logger: logging.Logger) -> None:
    """
    Step 2: Run fact extraction using archetype-based mapping.

    Extracts domain-specific facts from chunks using DSPy signatures.
    Reads chunks from unified ./data/outputs/, writes facts there too.

    Args:
        pdf_stem: Sanitized PDF filename stem
        logger: Logger instance for output
    """
    logger.info("=" * 70)
    logger.info("STEP 2: Running Fact Extraction")
    logger.info("=" * 70)
    logger.info(f"Input stem: {pdf_stem}")

    chunks_file = UNIFIED_OUTPUT_DIR / f"{pdf_stem}_chunks.jsonl"
    output_file = UNIFIED_OUTPUT_DIR / f"{pdf_stem}_facts.json"

    # Verify input exists
    if not chunks_file.exists():
        logger.error(f"Chunks file not found: {chunks_file}")
        raise FileNotFoundError(f"Chunks file not found: {chunks_file}")

    cmd = [
        "python",
        "step3_extraction_with_archetypes.py",
        "--chunks", str(chunks_file),
        "--output", str(output_file),
    ]

    logger.info(f"Command: {' '.join(cmd)}")
    logger.info(f"Working directory: {EXTRACTOR_DIR}")

    try:
        subprocess.run(
            cmd,
            cwd=EXTRACTOR_DIR,
            check=True,
            capture_output=False,
        )
        logger.info("SUCCESS - Fact extraction completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"FAILED - Extraction failed with exit code {e.returncode}")
        raise


def run_analyzer(pdf_stem: str, logger: logging.Logger) -> None:
    """
    Step 3: Run quality analysis and report generation.

    Performs consistency checks, compliance validation, and gap analysis.
    Generates HTML dashboard and Excel workbook.
    Reads from unified ./data/outputs/, writes outputs there too.

    Args:
        pdf_stem: Sanitized PDF filename stem
        logger: Logger instance for output
    """
    logger.info("=" * 70)
    logger.info("STEP 3: Running ESIA Fact Analyzer")
    logger.info("=" * 70)
    logger.info(f"Input stem: {pdf_stem}")

    chunks_file = UNIFIED_OUTPUT_DIR / f"{pdf_stem}_chunks.jsonl"
    meta_file = UNIFIED_OUTPUT_DIR / f"{pdf_stem}_meta.json"

    # Verify inputs exist
    if not chunks_file.exists():
        logger.error(f"Chunks file not found: {chunks_file}")
        raise FileNotFoundError(f"Chunks file not found: {chunks_file}")

    cmd = [
        "python",
        "analyze_esia_v2.py",
        "--input-dir", str(UNIFIED_OUTPUT_DIR),
        "--output-dir", str(UNIFIED_OUTPUT_DIR),
        "--chunks", f"{pdf_stem}_chunks.jsonl",
        "--meta", f"{pdf_stem}_meta.json",
    ]

    logger.info(f"Command: {' '.join(cmd)}")
    logger.info(f"Working directory: {ANALYZER_DIR}")

    try:
        subprocess.run(
            cmd,
            cwd=ANALYZER_DIR,
            check=True,
            capture_output=False,
        )
        logger.info("SUCCESS - Analyzer completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"FAILED - Analyzer failed with exit code {e.returncode}")
        raise


def run_factsheet_generator(pdf_stem: str, logger: logging.Logger) -> None:
    """
    Step 4 (Optional): Generate ESIA review factsheet in Excel and HTML format.

    Creates comprehensive Excel workbook and HTML dashboard from extracted facts.
    Reads from unified ./data/outputs/, writes outputs there too.

    Args:
        pdf_stem: Sanitized PDF filename stem
        logger: Logger instance for output
    """
    logger.info("=" * 70)
    logger.info("STEP 4: Generating ESIA Review Factsheet")
    logger.info("=" * 70)
    logger.info(f"Input stem: {pdf_stem}")

    facts_file = UNIFIED_OUTPUT_DIR / f"{pdf_stem}_facts.json"
    meta_file = UNIFIED_OUTPUT_DIR / f"{pdf_stem}_meta.json"
    chunks_file = UNIFIED_OUTPUT_DIR / f"{pdf_stem}_chunks.jsonl"

    # Verify inputs exist
    if not facts_file.exists():
        logger.error(f"Facts file not found: {facts_file}")
        raise FileNotFoundError(f"Facts file not found: {facts_file}")

    if not meta_file.exists():
        logger.error(f"Meta file not found: {meta_file}")
        raise FileNotFoundError(f"Meta file not found: {meta_file}")

    # Create a temporary Python script to run the factsheet generator
    # This imports the module and executes it with the correct file paths
    # Convert paths to use forward slashes to avoid Windows backslash escape sequence issues
    root_path = str(ROOT).replace('\\', '/')
    facts_path_str = str(facts_file).replace('\\', '/')
    meta_path_str = str(meta_file).replace('\\', '/')
    chunks_path_str = str(chunks_file).replace('\\', '/')
    output_dir_str = str(UNIFIED_OUTPUT_DIR).replace('\\', '/')

    temp_script = f"""
import sys
sys.path.insert(0, '{root_path}')

from generate_esia_factsheet import load_inputs, build_project_summary, build_fact_categories
from generate_esia_factsheet import check_consistency, check_unit_standardization, check_thresholds
from generate_esia_factsheet import analyze_gaps, generate_excel, build_html_factsheet
from pathlib import Path

facts_path = Path('{facts_path_str}')
meta_path = Path('{meta_path_str}')
chunks_path = Path('{chunks_path_str}')
output_dir = Path('{output_dir_str}')

facts, meta, chunks = load_inputs(facts_path, meta_path, chunks_path)

if not facts:
    print("Error: Could not load facts file.")
    sys.exit(1)

project_summary = build_project_summary(facts)
categories = build_fact_categories(facts)
consistency_issues = check_consistency(facts)
unit_issues = check_unit_standardization(facts)
threshold_checks = check_thresholds(meta, facts)
gaps = analyze_gaps(facts)

data = {{
    'facts': facts,
    'meta': meta,
    'chunks': chunks,
    'project_summary': project_summary,
    'categories': categories,
    'consistency_issues': consistency_issues,
    'unit_issues': unit_issues,
    'threshold_checks': threshold_checks,
    'gaps': gaps,
}}

base_name = Path('{pdf_stem}')
excel_path = output_dir / f"{{base_name}}_review.xlsx"
html_path = output_dir / f"{{base_name}}_review.html"

generate_excel(excel_path, data)
build_html_factsheet(html_path, data)
"""

    cmd = [
        "python",
        "-c",
        temp_script,
    ]

    logger.info(f"Generating factsheet for: {pdf_stem}")

    try:
        subprocess.run(
            cmd,
            check=True,
            capture_output=False,
        )
        logger.info("SUCCESS - Factsheet generation completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"FAILED - Factsheet generation failed with exit code {e.returncode}")
        raise


def run_pipeline(pdf_path: str, steps: List[int], logger: logging.Logger) -> None:
    """
    Execute the ESIA pipeline for specified steps.

    The pipeline operates with:
    - Single input directory: ./data/pdfs/
    - Single output directory: ./data/outputs/
    - Unified sanitized stem used throughout

    Args:
        pdf_path: Path to the PDF/DOCX file
        steps: List of step numbers to execute (1, 2, or 3)
        logger: Logger instance for output
    """
    logger.info("ESIA Pipeline Starting")
    logger.info(f"Input file: {pdf_path}")
    logger.info(f"Steps to execute: {steps}")

    try:
        # STEP 0 (implicit): Sanitize PDF filename stem FIRST
        # This is done immediately and used consistently throughout
        pdf_stem = sanitize_pdf_stem(pdf_path)
        logger.info(f"Sanitized stem: {pdf_stem}")

        # Ensure unified output directory exists
        UNIFIED_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Unified output directory: {UNIFIED_OUTPUT_DIR}")

        # Execute requested steps
        if 1 in steps:
            run_chunking(pdf_path, pdf_stem, logger)

        if 2 in steps:
            run_fact_extraction(pdf_stem, logger)

        if 3 in steps:
            run_analyzer(pdf_stem, logger)
            # Automatically generate factsheet after Step 3 completes
            run_factsheet_generator(pdf_stem, logger)

        logger.info("=" * 70)
        logger.info("SUCCESS - ESIA Pipeline completed successfully!")
        logger.info(f"All outputs saved to: {UNIFIED_OUTPUT_DIR}")
        logger.info("=" * 70)

    except Exception as e:
        logger.error("=" * 70)
        logger.error(f"FAILED - Pipeline failed: {e}")
        logger.error("=" * 70)
        sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "pdf_file",
        help="Path to the PDF or DOCX file to process",
        metavar="PDF_FILE",
    )

    parser.add_argument(
        "--steps",
        type=str,
        default="1,2,3",
        help="Comma-separated list of steps to run (1=chunk, 2=extract, 3=analyze). "
             "Default: 1,2,3 (all steps)",
        metavar="STEPS",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose/debug logging output",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="ESIA Pipeline v2.0 (Unified Architecture)",
    )

    return parser.parse_args()


def validate_steps(steps_str: str) -> List[int]:
    """
    Parse and validate step numbers.

    Valid steps:
        1 = Document chunking
        2 = Fact extraction
        3 = Quality analysis

    Args:
        steps_str: Comma-separated string of step numbers

    Returns:
        List of validated step numbers

    Raises:
        ValueError: If steps are invalid
    """
    try:
        steps = [int(s.strip()) for s in steps_str.split(",")]
        valid_steps = {1, 2, 3}

        for step in steps:
            if step not in valid_steps:
                raise ValueError(f"Invalid step number: {step}. Valid steps: 1, 2, 3")

        # Return steps in order
        return sorted(list(set(steps)))

    except ValueError as e:
        raise ValueError(f"Error parsing steps '{steps_str}': {e}")


def main():
    """Main entry point for the CLI."""
    args = parse_arguments()
    logger = setup_logging(verbose=args.verbose)

    try:
        # Validate required directories
        validate_directories(logger)

        # Validate PDF file
        pdf_path = validate_pdf_file(args.pdf_file, logger)
        logger.debug(f"PDF file: {pdf_path.absolute()}")

        # Parse and validate steps
        steps = validate_steps(args.steps)
        logger.debug(f"Parsed steps: {steps}")

        # Run the pipeline with unified architecture
        run_pipeline(str(pdf_path), steps, logger)

    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\nPipeline interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
