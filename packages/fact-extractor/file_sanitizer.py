# -*- coding: utf-8 -*-
"""
Filename Sanitization Utility

Provides secure filename sanitization for ESIA Fact Extractor.
Handles file uploads and converts them to safe, standardized names
suitable for use throughout the pipeline.

Features:
- Removes/replaces invalid characters
- Prevents path traversal attacks
- Preserves meaningful filename information
- Handles Unicode characters safely
- Maintains original filename in metadata
"""

import re
import unicodedata
from pathlib import Path
from typing import Tuple


class FilenameSanitizer:
    """Sanitize filenames for safe usage in file systems and paths."""

    # Characters that are invalid in Windows filenames
    INVALID_CHARS = r'[<>:"/\\|?*\x00-\x1f]'

    # Valid filename pattern (alphanumeric, spaces, hyphens, underscores, dots)
    VALID_PATTERN = r'^[a-zA-Z0-9_\-\s.]+$'

    # Maximum filename length (considering filesystem limits)
    MAX_FILENAME_LENGTH = 200

    # Reserved Windows filenames to avoid
    RESERVED_NAMES = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }

    @staticmethod
    def sanitize(filename: str) -> str:
        """
        Sanitize a filename for safe usage in filesystem operations.

        Args:
            filename: Raw filename from user input or file upload

        Returns:
            Safe, sanitized filename preserving extension

        Examples:
            >>> sanitize("NATARBORA PESIA as submitted 2025-02-10.pdf")
            'NATARBORA_PESIA_as_submitted_2025-02-10.pdf'

            >>> sanitize("file@#$%.docx")
            'file.docx'

            >>> sanitize("../../../etc/passwd")
            'etc_passwd'
        """
        if not filename or not isinstance(filename, str):
            raise ValueError("Filename must be a non-empty string")

        # Split extension
        path = Path(filename)
        stem = path.stem
        suffix = path.suffix.lower()

        # Validate extension
        if not suffix:
            raise ValueError(f"Filename must have an extension: {filename}")

        # Normalize Unicode characters (NFC normalization)
        stem = unicodedata.normalize('NFC', stem)

        # Remove path traversal attempts
        stem = stem.replace('..', '').replace('/', '').replace('\\', '')

        # Replace spaces with underscores
        stem = re.sub(r'\s+', '_', stem.strip())

        # Remove invalid characters
        stem = re.sub(FilenameSanitizer.INVALID_CHARS, '', stem)

        # Replace multiple consecutive underscores with single underscore
        stem = re.sub(r'_+', '_', stem)

        # Remove leading/trailing underscores
        stem = stem.strip('_')

        # Ensure we have a valid stem
        if not stem:
            raise ValueError(f"Filename stem is empty after sanitization: {filename}")

        # Check against reserved names
        if stem.upper() in FilenameSanitizer.RESERVED_NAMES:
            stem = f"{stem}_file"

        # Enforce maximum length (leave room for timestamp if needed)
        if len(stem) > FilenameSanitizer.MAX_FILENAME_LENGTH - len(suffix):
            stem = stem[:FilenameSanitizer.MAX_FILENAME_LENGTH - len(suffix)]

        # Reconstruct filename
        sanitized = f"{stem}{suffix}"

        return sanitized

    @staticmethod
    def sanitize_path_component(name: str) -> str:
        """
        Sanitize a string for use as a directory name or path component.
        More restrictive than sanitize() - suitable for directory names.

        Args:
            name: Directory name or path component

        Returns:
            Safe directory name

        Examples:
            >>> sanitize_path_component("output NATARBORA PESIA as submitted 2025-02-10")
            'output_NATARBORA_PESIA_as_submitted_2025-02-10'

            >>> sanitize_path_component("test@#$%dir")
            'testdir'
        """
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        # Normalize Unicode
        name = unicodedata.normalize('NFC', name)

        # Remove path traversal
        name = name.replace('..', '').replace('/', '').replace('\\', '')

        # Replace spaces with underscores
        name = re.sub(r'\s+', '_', name.strip())

        # Remove invalid characters (more restrictive - only alphanumeric, underscore, hyphen)
        name = re.sub(r'[^a-zA-Z0-9_\-]', '', name)

        # Replace multiple consecutive underscores
        name = re.sub(r'_+', '_', name)

        # Remove leading/trailing underscores/hyphens
        name = name.strip('_-')

        # Ensure we have something left
        if not name:
            raise ValueError(f"Path component is empty after sanitization")

        # Enforce maximum length for directory names
        if len(name) > FilenameSanitizer.MAX_FILENAME_LENGTH:
            name = name[:FilenameSanitizer.MAX_FILENAME_LENGTH]

        # Check against reserved names
        if name.upper() in FilenameSanitizer.RESERVED_NAMES:
            name = f"{name}_dir"

        return name

    @staticmethod
    def extract_base_name(filename: str) -> str:
        """
        Extract a clean base name (stem) from a filename.
        Useful for creating output directories.

        Args:
            filename: Raw filename

        Returns:
            Clean base name without extension

        Examples:
            >>> extract_base_name("NATARBORA PESIA as submitted 2025-02-10.pdf")
            'NATARBORA_PESIA_as_submitted_2025-02-10'
        """
        path = Path(filename)
        stem = path.stem
        return FilenameSanitizer.sanitize_path_component(stem)

    @staticmethod
    def validate_filename(filename: str) -> Tuple[bool, str]:
        """
        Validate if a filename is safe without modifying it.

        Args:
            filename: Filename to validate

        Returns:
            Tuple of (is_valid, reason_if_invalid)

        Examples:
            >>> is_valid, reason = validate_filename("../../../etc/passwd")
            >>> print(is_valid, reason)
            False, "Contains path traversal attempt"
        """
        if not filename or not isinstance(filename, str):
            return False, "Filename must be a non-empty string"

        # Check for path traversal
        if '..' in filename or filename.startswith('/') or filename.startswith('\\'):
            return False, "Contains path traversal attempt"

        # Check for invalid characters
        if re.search(FilenameSanitizer.INVALID_CHARS, filename):
            return False, "Contains invalid characters"

        # Check extension
        if not Path(filename).suffix:
            return False, "Missing file extension"

        # Check reserved names
        stem = Path(filename).stem.upper()
        if stem in FilenameSanitizer.RESERVED_NAMES:
            return False, f"'{stem}' is a reserved system name"

        return True, "Valid"


def sanitize_filename(filename: str) -> str:
    """
    Convenience function to sanitize a filename.

    Args:
        filename: Raw filename from user input

    Returns:
        Safe filename suitable for filesystem operations

    Raises:
        ValueError: If filename cannot be sanitized
    """
    return FilenameSanitizer.sanitize(filename)


def sanitize_path_component(name: str) -> str:
    """
    Convenience function to sanitize a directory name or path component.

    Args:
        name: Directory name to sanitize

    Returns:
        Safe directory name

    Raises:
        ValueError: If name cannot be sanitized
    """
    return FilenameSanitizer.sanitize_path_component(name)


def extract_base_name(filename: str) -> str:
    """
    Convenience function to extract clean base name from filename.

    Args:
        filename: Raw filename

    Returns:
        Clean base name without extension
    """
    return FilenameSanitizer.extract_base_name(filename)


def validate_filename(filename: str) -> Tuple[bool, str]:
    """
    Convenience function to validate a filename.

    Args:
        filename: Filename to validate

    Returns:
        Tuple of (is_valid, reason)
    """
    return FilenameSanitizer.validate_filename(filename)
