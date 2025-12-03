"""
Command-line interface for ESIA Reviewer.
"""

import os
import sys
import argparse
from pathlib import Path

from .reviewer import ESIAReviewer


def _load_env_file():
    """Load environment variables from .env or .env.local file if it exists."""
    # Prioritized list of paths to check
    # 1. Workspace root .env.local (main config file)
    # 2. Workspace root .env
    # 3. Current working directory
    # 4. Package parent directory
    workspace_root = Path(__file__).parent.parent.parent.parent.parent  # esia-fact-analyzer -> pipeline -> packages -> esia-workspace

    paths_to_check = [
        workspace_root / '.env.local',  # Primary: workspace root .env.local
        workspace_root / '.env',         # Secondary: workspace root .env
        Path.cwd() / '.env.local',
        Path.cwd() / '.env',
        Path(__file__).parent.parent / '.env',
    ]

    env_path = None
    for p in paths_to_check:
        if p.exists():
            env_path = p
            break

    if env_path and env_path.exists():
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key and value and key not in os.environ:
                            os.environ[key] = value
        except Exception as e:
            print(f"Warning: Could not load .env file: {e}")


def main():
    """Main CLI entry point."""
    # Load environment variables from .env file
    _load_env_file()

    parser = argparse.ArgumentParser(
        description="ESIA Reviewer Analysis Tool v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default: reads from ../data/outputs/, outputs to ../data/outputs/
  python analyze_esia_v2.py

  # Custom input folder
  python analyze_esia_v2.py --input-dir ./my_data

  # Custom output folder
  python analyze_esia_v2.py --output-dir ./results

  # Custom filenames
  python analyze_esia_v2.py --chunks my_chunks.jsonl --meta my_meta.json

  # Full customization
  python analyze_esia_v2.py -i ../data/outputs -o ../data/outputs --chunks document_chunks.jsonl --meta document_meta.json
        """
    )
    parser.add_argument(
        "--input-dir", "-i",
        default="../data/outputs",
        help="Input directory containing chunks and metadata (default: ../data/outputs)"
    )
    parser.add_argument(
        "--chunks",
        help="Override chunks filename (default: first .jsonl file found)"
    )
    parser.add_argument(
        "--meta",
        help="Override metadata filename (default: matching .json file)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="../data/outputs",
        help="Output directory for HTML and Excel (default: ../data/outputs)"
    )
    parser.add_argument(
        "--skill-dir",
        help="Path to skill directory (for references)"
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Disable LLM-based factsheet summary generation"
    )
    args = parser.parse_args()

    # Setup input directory
    input_dir = Path(args.input_dir)
    input_dir.mkdir(parents=True, exist_ok=True)

    # Find chunks file
    if args.chunks:
        chunks_filename = args.chunks if args.chunks.endswith('.jsonl') else args.chunks + '.jsonl'
    else:
        # Auto-detect first .jsonl file
        jsonl_files = list(input_dir.glob('*.jsonl'))
        if not jsonl_files:
            print(f"ERROR: No .jsonl files found in {input_dir}")
            print(f"Expected to find 'chunks.jsonl' or similar .jsonl file")
            print(f"\nAvailable files in {input_dir}:")
            for f in sorted(input_dir.iterdir()):
                if f.is_file():
                    print(f"  - {f.name}")
            sys.exit(1)
        chunks_filename = jsonl_files[0].name

    chunks_path = input_dir / chunks_filename

    # Verify chunks file exists
    if not chunks_path.exists():
        print(f"ERROR: Chunks file not found: {chunks_path}")
        print(f"Expected to find '{chunks_filename}' in: {input_dir}")
        sys.exit(1)

    # Find metadata file
    if args.meta:
        meta_filename = args.meta if args.meta.endswith('.json') else args.meta + '.json'
        meta_path = input_dir / meta_filename
    else:
        # Auto-detect matching .json file
        base_name = chunks_path.stem.replace('_chunks', '')
        meta_path = input_dir / f"{base_name}.json"
        if not meta_path.exists():
            meta_path = input_dir / "meta.json"
            if not meta_path.exists():
                meta_path = None

    # Setup output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find skill directory
    if args.skill_dir:
        skill_dir = Path(args.skill_dir)
    else:
        # Try to find skill directory relative to this file
        skill_dir = Path(__file__).parent.parent

    # Print configuration
    print("\n" + "=" * 60)
    print("ESIA REVIEWER - CONFIGURATION")
    print("=" * 60)
    print(f"Input directory:  {input_dir}")
    print(f"Chunks file:      {chunks_path.name}")
    if meta_path:
        print(f"Metadata file:    {meta_path.name}")
    print(f"Output directory: {output_dir}")
    print(f"LLM enabled:      {not args.no_llm}")
    print("=" * 60 + "\n")

    # Run analysis
    reviewer = ESIAReviewer(skill_dir)
    reviewer.load_data(chunks_path, meta_path)
    summary = reviewer.run_analysis()

    # Generate outputs
    base_name = chunks_path.stem.replace("_chunks", "")
    html_path = output_dir / f"{base_name}_analysis.html"
    excel_path = output_dir / f"{base_name}_analysis.xlsx"

    reviewer.export_html(html_path)
    reviewer.export_excel(excel_path)

    # Print summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"Document: {summary['document']}")
    print(f"Chunks analyzed: {summary['total_chunks']}")
    print(f"Consistency issues: {summary['issues']['total']} ({summary['issues']['high_severity']} high severity)")
    print(f"Unit standardization issues: {summary['unit_issues']['total']}")
    print(f"Threshold exceedances: {summary['threshold_checks']['exceedances']}")
    print(f"Content gaps: {summary['gaps']['missing']} missing items")
    print("=" * 60)
    print(f"\nOutput files saved to: {output_dir}")
    print(f"  - {html_path.name}")
    print(f"  - {excel_path.name}")


if __name__ == "__main__":
    main()
