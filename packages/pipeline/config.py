"""
Configuration management for ESIA Pipeline.

Loads configuration from environment variables and config files.
Uses project root .env.local as SINGLE SOURCE OF TRUTH.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv  # Optional - gracefully handles if not installed


class Config:
    """Configuration loader for ESIA Pipeline."""

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize configuration.

        Args:
            config_dir: Directory to look for .env file (defaults to project root)
        """
        if config_dir is None:
            config_dir = Path(__file__).parent

        self.config_dir = config_dir

        # Use project root .env.local as SINGLE SOURCE OF TRUTH
        # Path: esia-workspace/packages/pipeline/ -> go up 3 levels to esia-ai/
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        self.env_file = project_root / ".env.local"
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from .env file and environment variables."""
        # Try to load .env file (override=False: don't override parent process env)
        if self.env_file.exists():
            try:
                load_dotenv(self.env_file, override=False)
            except NameError:
                # dotenv not installed, try manual loading
                self._load_env_file()

    def _load_env_file(self) -> None:
        """Manually load .env file (fallback if python-dotenv not installed)."""
        if not self.env_file.exists():
            return

        with open(self.env_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return os.environ.get(key, default)

    def get_pipeline_config(self) -> Dict[str, Any]:
        """
        Get pipeline-specific configuration.

        Returns:
            Dictionary with pipeline settings
        """
        return {
            "extractor_dir": self.config_dir / "esia-fact-extractor-pipeline",
            "analyzer_dir": self.config_dir / "esia-fact-analyzer",
            "pdf_stem": self.get("PDF_STEM", "ESIA_Report_Final_Elang AMNT"),
            "verbose": self.get("VERBOSE", "false").lower() == "true",
        }

    def get_api_keys(self) -> Dict[str, Optional[str]]:
        """
        Get API keys for LLM providers.

        Returns:
            Dictionary with API keys (may contain None values)
        """
        return {
            "google_api_key": self.get("GOOGLE_API_KEY"),
            "openrouter_api_key": self.get("OPENROUTER_API_KEY"),
        }

    def validate_required_keys(self) -> bool:
        """
        Validate that required configuration is present.

        Returns:
            True if valid, False otherwise
        """
        # At least one API key should be present for extraction
        api_keys = self.get_api_keys()
        return any(api_keys.values())

    @staticmethod
    def create_sample_env(output_path: Path) -> None:
        """
        Create a sample .env file for reference.

        Args:
            output_path: Path where to write sample .env file
        """
        sample_content = """# ESIA Pipeline Configuration

# API Keys for LLM Providers
GOOGLE_API_KEY=your_google_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Pipeline Configuration
PDF_STEM=ESIA_Report_Final_Elang AMNT
VERBOSE=false

# Optional: Custom paths (if needed)
# EXTRACTOR_DIR=./esia-fact-extractor-pipeline
# ANALYZER_DIR=./esia-fact-analyzer
"""
        with open(output_path, "w") as f:
            f.write(sample_content)


def get_config(config_dir: Optional[Path] = None) -> Config:
    """
    Get or create configuration instance.

    Args:
        config_dir: Optional configuration directory

    Returns:
        Config instance
    """
    return Config(config_dir)
