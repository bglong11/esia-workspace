"""
Unit normalization and validation functions.
"""

import re
from typing import Tuple, List

from .constants import UNIT_CONVERSIONS


def normalize_unit(unit: str) -> Tuple[str, float]:
    """
    Normalize unit to base unit and return conversion factor.

    Args:
        unit: The unit string to normalize

    Returns:
        Tuple of (base_unit, conversion_factor)
    """
    unit_clean = unit.strip().lower()

    # Direct lookup
    for u, conv in UNIT_CONVERSIONS.items():
        if unit_clean == u.lower() or unit_clean == u:
            return conv['base'], conv['factor']

    # Partial match for compound units
    for u, conv in UNIT_CONVERSIONS.items():
        if u.lower() in unit_clean:
            return conv['base'], conv['factor']

    return unit, 1.0


def is_unit_valid_for_context(unit: str, valid_units: List[str]) -> bool:
    """
    Check if a unit is valid for a given context. Uses strict matching.

    Args:
        unit: The unit string to validate
        valid_units: List of valid unit strings for the context

    Returns:
        True if the unit is valid for the context
    """
    unit_lower = unit.lower().strip()

    # Normalize common variations
    unit_normalized = unit_lower
    unit_normalized = re.sub(r'\s+', '', unit_normalized)  # Remove spaces
    unit_normalized = unit_normalized.replace('²', '2')  # Normalize superscript
    unit_normalized = unit_normalized.replace('³', '3')

    for valid_u in valid_units:
        if valid_u == '':
            continue  # Empty means dimensionless numbers OK

        valid_lower = valid_u.lower().strip()
        valid_normalized = re.sub(r'\s+', '', valid_lower)
        valid_normalized = valid_normalized.replace('²', '2').replace('³', '3')

        # Strict equality check
        if unit_normalized == valid_normalized:
            return True

        # Handle plural forms (hectares vs hectare)
        if unit_normalized.rstrip('s') == valid_normalized.rstrip('s'):
            return True

        # Handle compound units like dB(A) vs dBA
        if 'db' in unit_normalized and 'db' in valid_normalized:
            return True

    return False
