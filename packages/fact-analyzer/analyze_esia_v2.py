#!/usr/bin/env python3
"""
ESIA Reviewer Analysis Script v2

This is a backward-compatible wrapper that imports from the esia_analyzer package.
For new development, consider using the package directly:
    from esia_analyzer import ESIAReviewer
    or
    python -m esia_analyzer
"""

from esia_analyzer.cli import main

if __name__ == "__main__":
    main()
