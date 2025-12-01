"""
ESIA Fact Analyzer Package

A tool for analyzing Environmental & Social Impact Assessment (ESIA) documents.
Performs consistency checking, unit standardization, threshold compliance,
gap analysis, and factsheet summary generation.
"""

from .reviewer import ESIAReviewer
from .constants import UNIT_CONVERSIONS, PARAMETER_CONTEXTS

__version__ = "2.0.0"
__all__ = ["ESIAReviewer", "UNIT_CONVERSIONS", "PARAMETER_CONTEXTS"]
