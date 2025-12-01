# -*- coding: utf-8 -*-
"""
Output Organizer - Folder-Based Output Structure Management

Organizes all pipeline outputs into a single folder structure based on sanitized filename.

Structure created:
    SANITIZED_NAME/
    ├── markdown/
    │   └── document.md          (converted markdown)
    ├── facts/
    │   ├── esia_mentions.csv    (all fact occurrences)
    │   ├── esia_consolidated.csv (unique facts)
    │   ├── esia_replacement_plan.csv
    │   └── project_factsheet.csv (categorized facts)
    ├── reports/
    │   └── verification_report.md
    └── checkpoints/
        └── .checkpoint.pkl      (resume capability)
"""

from pathlib import Path
from typing import Optional, Dict
from file_sanitizer import sanitize_path_component


class OutputOrganizer:
    """Manages organized folder structure for pipeline outputs."""

    # Subfolder names
    MARKDOWN_DIR = "markdown"
    FACTS_DIR = "facts"
    REPORTS_DIR = "reports"
    CHECKPOINTS_DIR = "checkpoints"

    def __init__(self, base_name: str, root_dir: str = "."):
        """
        Initialize output organizer.

        Args:
            base_name: Base name for the project (will be sanitized)
            root_dir: Root directory to create project folder in (default: current dir)

        Example:
            organizer = OutputOrganizer("NATARBORA PESIA as submitted 2025-02-10")
            # Creates: NATARBORA_PESIA_as_submitted_2025-02-10/
        """
        # Sanitize the base name
        self.sanitized_name = sanitize_path_component(base_name)

        # Create root project directory
        self.root_dir = Path(root_dir)
        self.project_dir = self.root_dir / self.sanitized_name

        # Create subdirectories
        self.markdown_dir = self.project_dir / self.MARKDOWN_DIR
        self.facts_dir = self.project_dir / self.FACTS_DIR
        self.reports_dir = self.project_dir / self.REPORTS_DIR
        self.checkpoints_dir = self.project_dir / self.CHECKPOINTS_DIR

    def create_folders(self) -> Path:
        """
        Create the entire folder structure.

        Returns:
            Path to the project directory

        Example:
            project_dir = organizer.create_folders()
            # Creates all subdirectories and returns Path object
        """
        # Create all directories
        self.markdown_dir.mkdir(parents=True, exist_ok=True)
        self.facts_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)

        return self.project_dir

    def get_markdown_dir(self) -> Path:
        """
        Get the markdown directory path.

        Returns:
            Path to markdown directory

        Example:
            markdown_dir = organizer.get_markdown_dir()
            # Returns: project_dir/markdown
        """
        return self.markdown_dir

    def get_markdown_path(self, filename: str) -> Path:
        """
        Get path for markdown file.

        Args:
            filename: Name of markdown file (e.g., "document.md")

        Returns:
            Full path to markdown file
        """
        return self.markdown_dir / filename

    def get_facts_path(self, filename: str) -> Path:
        """
        Get path for facts CSV file.

        Args:
            filename: Name of CSV file (e.g., "esia_mentions.csv")

        Returns:
            Full path to facts file
        """
        return self.facts_dir / filename

    def get_report_path(self, filename: str) -> Path:
        """
        Get path for report file.

        Args:
            filename: Name of report file (e.g., "verification_report.md")

        Returns:
            Full path to report file
        """
        return self.reports_dir / filename

    def get_checkpoint_path(self) -> Path:
        """
        Get path for checkpoint file.

        Returns:
            Path to checkpoint pickle file
        """
        return self.checkpoints_dir / ".checkpoint.pkl"

    def get_all_output_files(self) -> Dict[str, Path]:
        """
        Get paths to all expected output files.

        Returns:
            Dictionary with file descriptions and paths
        """
        return {
            "markdown": self.get_markdown_path("document.md"),
            "facts_mentions": self.get_facts_path("esia_mentions.csv"),
            "facts_consolidated": self.get_facts_path("esia_consolidated.csv"),
            "facts_replacement": self.get_facts_path("esia_replacement_plan.csv"),
            "facts_factsheet": self.get_facts_path("project_factsheet.csv"),
            "report": self.get_report_path("verification_report.md"),
            "checkpoint": self.get_checkpoint_path(),
        }

    def print_structure(self) -> None:
        """Print the folder structure to console."""
        print("\n" + "=" * 80)
        print("OUTPUT FOLDER STRUCTURE")
        print("=" * 80)
        print(f"\nRoot: {self.project_dir.absolute()}\n")

        structure = f"""
{self.sanitized_name}/
├── markdown/
│   └── document.md                    (Converted markdown from PDF)
├── facts/
│   ├── esia_mentions.csv              (All fact occurrences with evidence)
│   ├── esia_consolidated.csv          (Unique facts with statistics)
│   ├── esia_replacement_plan.csv      (Regex patterns for document editing)
│   └── project_factsheet.csv          (Categorized facts by section)
├── reports/
│   └── verification_report.md         (Data quality report)
└── checkpoints/
    └── .checkpoint.pkl                (Extraction checkpoint for resume)
"""
        print(structure)
        print("=" * 80 + "\n")

    def get_project_dir(self) -> Path:
        """Get the project directory path."""
        return self.project_dir

    def get_sanitized_name(self) -> str:
        """Get the sanitized project name."""
        return self.sanitized_name


class LegacyOutputOrganizer:
    """
    Compatibility wrapper for legacy output structure.

    Maps old flat structure to new organized structure while maintaining compatibility.
    """

    def __init__(self, output_dir: str):
        """
        Initialize with legacy output directory.

        Args:
            output_dir: Existing output directory path
        """
        self.output_dir = Path(output_dir)

    def get_facts_csv(self, filename: str) -> Path:
        """Get path to facts CSV (legacy: at root level)."""
        return self.output_dir / filename

    def get_checkpoint_path(self) -> Path:
        """Get path to checkpoint (legacy: at root level)."""
        return self.output_dir / ".checkpoint.pkl"


def create_output_structure(base_name: str, root_dir: str = ".") -> OutputOrganizer:
    """
    Factory function to create and initialize output organizer.

    Args:
        base_name: Base name for project folder
        root_dir: Root directory for project folder

    Returns:
        OutputOrganizer instance with folders created

    Example:
        organizer = create_output_structure("NATARBORA PESIA 2025-02-10")
        print(organizer.get_facts_path("esia_mentions.csv"))
        # Output: NATARBORA_PESIA_2025-02-10/facts/esia_mentions.csv
    """
    organizer = OutputOrganizer(base_name, root_dir)
    organizer.create_folders()
    return organizer


def migrate_to_organized_structure(legacy_dir: Path, base_name: str) -> OutputOrganizer:
    """
    Migrate legacy flat output to organized structure.

    Moves files from legacy flat structure to new organized structure.

    Args:
        legacy_dir: Path to legacy output directory
        base_name: Base name for new project folder

    Returns:
        OutputOrganizer with migrated files

    Example:
        # Before: output_NATARBORA_PESIA/
        #   ├── esia_mentions.csv
        #   ├── esia_consolidated.csv
        #   └── .checkpoint.pkl
        #
        # After: NATARBORA_PESIA/
        #   ├── facts/
        #   │   ├── esia_mentions.csv
        #   │   └── esia_consolidated.csv
        #   └── checkpoints/
        #       └── .checkpoint.pkl
    """
    import shutil

    legacy_path = Path(legacy_dir)
    if not legacy_path.exists():
        raise ValueError(f"Legacy directory not found: {legacy_path}")

    # Create new organized structure
    organizer = create_output_structure(base_name, legacy_path.parent)

    # Migrate CSV files
    csv_files = ["esia_mentions.csv", "esia_consolidated.csv",
                 "esia_replacement_plan.csv", "project_factsheet.csv"]
    for csv_file in csv_files:
        legacy_file = legacy_path / csv_file
        if legacy_file.exists():
            new_file = organizer.get_facts_path(csv_file)
            shutil.move(str(legacy_file), str(new_file))
            print(f"  Migrated: {csv_file} → facts/")

    # Migrate markdown if exists
    markdown_files = legacy_path.glob("*.md")
    for md_file in markdown_files:
        if md_file.name != "verification_report.md":
            new_file = organizer.get_markdown_path(md_file.name)
            shutil.move(str(md_file), str(new_file))
            print(f"  Migrated: {md_file.name} → markdown/")

    # Migrate checkpoint if exists
    checkpoint_file = legacy_path / ".checkpoint.pkl"
    if checkpoint_file.exists():
        new_checkpoint = organizer.get_checkpoint_path()
        shutil.move(str(checkpoint_file), str(new_checkpoint))
        print(f"  Migrated: .checkpoint.pkl → checkpoints/")

    # Migrate report if exists
    report_file = legacy_path / "verification_report.md"
    if report_file.exists():
        new_report = organizer.get_report_path("verification_report.md")
        shutil.move(str(report_file), str(new_report))
        print(f"  Migrated: verification_report.md → reports/")

    # Remove legacy directory if empty
    try:
        legacy_path.rmdir()
        print(f"  Removed legacy directory: {legacy_path.name}")
    except OSError:
        # Directory not empty or other error - leave it
        pass

    return organizer
