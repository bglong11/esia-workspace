"""
Threshold checking against IFC EHS Guidelines.
"""

import re
from typing import List, Dict, Optional


# Threshold patterns for extracting values from text
THRESHOLD_PATTERNS = {
    "air_quality": {
        "PM10": [r'PM\s*10.*?(\d+(?:\.\d+)?)\s*(?:µg/m³|ug/m3)', r'(\d+(?:\.\d+)?)\s*(?:µg/m³|ug/m3).*PM\s*10'],
        "PM2.5": [r'PM\s*2\.?5.*?(\d+(?:\.\d+)?)\s*(?:µg/m³|ug/m3)'],
        "SO2": [r'SO\s*2.*?(\d+(?:\.\d+)?)\s*(?:µg/m³|ug/m3|mg/m3)'],
        "NO2": [r'NO\s*2.*?(\d+(?:\.\d+)?)\s*(?:µg/m³|ug/m3|mg/m3)'],
    },
    "noise": {
        "noise_level": [r'(\d+(?:\.\d+)?)\s*dB\s*\(?A\)?', r'noise.*?(\d+(?:\.\d+)?)\s*dB'],
    },
    "water": {
        "pH": [r'\bpH\s*(?:of\s+)?(\d+(?:\.\d+)?)', r'(\d+(?:\.\d+)?)\s*pH'],
        "BOD": [r'BOD.*?(\d+(?:\.\d+)?)\s*mg/[Ll]'],
        "COD": [r'COD.*?(\d+(?:\.\d+)?)\s*mg/[Ll]'],
        "TSS": [r'TSS.*?(\d+(?:\.\d+)?)\s*mg/[Ll]'],
    }
}


def get_threshold(thresholds: Dict, category: str, param: str) -> Optional[Dict]:
    """
    Get threshold value from IFC thresholds dictionary.

    Args:
        thresholds: Dictionary of threshold values
        category: Category name (air_quality, noise, water)
        param: Parameter name (PM10, noise_level, pH, etc.)

    Returns:
        Threshold info dict or None if not found
    """
    if category == "air_quality":
        return thresholds.get("air_quality", {}).get("ambient", {}).get(param)
    elif category == "noise":
        return thresholds.get("noise", {}).get("residential_day")
    elif category == "water":
        return thresholds.get("water_quality", {}).get("effluent_general", {}).get(param)
    return None


def compare_threshold(value: float, threshold_info: Dict) -> str:
    """
    Compare value against threshold.

    Args:
        value: The measured value
        threshold_info: Dict with 'value', 'min', 'max' keys

    Returns:
        Status string: EXCEEDANCE, APPROACHING, COMPLIANT, or UNKNOWN
    """
    if "min" in threshold_info and "max" in threshold_info:
        if value < threshold_info["min"] or value > threshold_info["max"]:
            return "EXCEEDANCE"
        return "COMPLIANT"
    elif "value" in threshold_info:
        if value > threshold_info["value"]:
            return "EXCEEDANCE"
        elif value > threshold_info["value"] * 0.8:
            return "APPROACHING"
        return "COMPLIANT"
    return "UNKNOWN"


def check_thresholds(facts: List[Dict], thresholds: Dict) -> List[Dict]:
    """
    Check extracted values against IFC thresholds.

    Args:
        facts: List of fact dictionaries with text and page keys
        thresholds: Dictionary of IFC threshold values

    Returns:
        List of threshold check result dictionaries
    """
    threshold_checks = []

    for fact in facts:
        text = fact.get("text", "")
        page = fact.get("page", "?")

        for category, params in THRESHOLD_PATTERNS.items():
            for param, patterns in params.items():
                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        try:
                            value = float(match)
                            threshold_info = get_threshold(thresholds, category, param)
                            if threshold_info:
                                status = compare_threshold(value, threshold_info)
                                threshold_checks.append({
                                    "parameter": param,
                                    "category": category,
                                    "value": value,
                                    "threshold": threshold_info.get("value"),
                                    "unit": threshold_info.get("unit"),
                                    "status": status,
                                    "page": page,
                                    "source": threshold_info.get("source", "IFC EHS Guidelines")
                                })
                        except (ValueError, TypeError):
                            pass

    return threshold_checks
