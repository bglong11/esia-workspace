"""
Numeric value extraction and parameter context identification.
"""

import re
from typing import List, Dict

from .constants import PARAMETER_CONTEXTS
from .units import normalize_unit, is_unit_valid_for_context


def extract_numeric_values(text: str) -> List[Dict]:
    """
    Extract numeric values with units from text.

    Args:
        text: The text to extract values from

    Returns:
        List of dicts with keys: value, unit, normalized_value, base_unit, raw
    """
    # More specific patterns to avoid false matches
    # Note: Order matters - more specific patterns first
    patterns = [
        # Concentration units
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(mg/[Ll]|µg/m³|ug/m3|mg/m³|mg/Nm³|ppm|ppb)',
        # Noise/sound
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(dB\s*\(?A\)?|dBA|decibels?)',
        # Temperature
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(°C|degrees?\s*C)',
        # Area units (specific)
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(km²|km2|square\s*kilometers?|sq\s*km)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(hectares?|ha)\b',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(m²|m2|sq\s*m|sqm|square\s*met(?:er|re)s?)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(acres?)',
        # Volume
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(ML|megalit(?:er|re)s?)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(kL|kiloliti(?:er|re)s?)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(m³|m3|cubic\s*met(?:er|re)s?)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(L/s|lit(?:er|re)s?\s*per\s*second)',
        # Emissions (specific)
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(tCO2e|tCO2|t\s*CO2\s*e?)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(Mt|megatonnes?)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(kt|kilotonnes?)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(tonnes?|t/y|t/yr|t/year)\b',
        # Power
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(GW|gigawatts?)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(MW|megawatts?)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(kW|kilowatts?)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(GWh|MWh)',
        # Distance (require word boundary to avoid matching 'm' in words)
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(kilometers?|km)\b',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(met(?:er|re)s?|m)\b(?!\s*[²³/])',  # m but not m², m³, m/
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(mm|millimeters?)',
        # Mass
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(kg|kilograms?)',
        # Percentage
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(%)',
        # Multipliers with units
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(million|thousand)?\s*(hectares?|square\s+kilometers?|people|persons?|households?)',
    ]

    results = []
    seen_positions = set()  # Avoid duplicate extractions

    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            start_pos = match.start()

            # Skip if we've already extracted a value at this position
            if start_pos in seen_positions:
                continue

            groups = match.groups()
            value = groups[0].replace(',', '')
            unit = ' '.join(g for g in groups[1:] if g).strip()

            try:
                num_value = float(value)

                # Handle multipliers
                if 'million' in unit.lower():
                    num_value *= 1000000
                    unit = re.sub(r'\s*million\s*', '', unit, flags=re.IGNORECASE).strip()
                elif 'thousand' in unit.lower():
                    num_value *= 1000
                    unit = re.sub(r'\s*thousand\s*', '', unit, flags=re.IGNORECASE).strip()

                # Skip if unit is empty or just whitespace
                if not unit or not unit.strip():
                    continue

                base_unit, factor = normalize_unit(unit)
                normalized_value = num_value * factor

                results.append({
                    "value": num_value,
                    "unit": unit,
                    "normalized_value": normalized_value,
                    "base_unit": base_unit,
                    "raw": match.group()
                })

                seen_positions.add(start_pos)

            except ValueError:
                pass

    return results


def identify_parameter_context(text: str, unit: str = None) -> List[str]:
    """
    Identify which parameter context(s) a text snippet belongs to, optionally validating unit.

    Args:
        text: The text to analyze
        unit: Optional unit string to validate against context

    Returns:
        List of matching context names
    """
    text_lower = text.lower()
    unit_lower = (unit or '').lower().strip()
    contexts = []

    for ctx_name, ctx_data in PARAMETER_CONTEXTS.items():
        patterns = ctx_data['patterns']
        valid_units = ctx_data['valid_units']

        # Check if text matches the context pattern
        pattern_matched = False
        for pattern in patterns:
            if re.search(pattern, text_lower):
                pattern_matched = True
                break

        if pattern_matched:
            # If unit is provided, validate it's appropriate for this context
            if unit_lower:
                unit_valid = is_unit_valid_for_context(unit_lower, valid_units)

                if unit_valid:
                    contexts.append(ctx_name)
            else:
                # No unit provided, just check pattern
                contexts.append(ctx_name)

    return contexts if contexts else []
