"""
Consistency checking functions for ESIA analysis.
"""

from collections import defaultdict
from typing import List, Dict

from .extraction import extract_numeric_values, identify_parameter_context


def check_consistency(facts: List[Dict]) -> List[Dict]:
    """
    Check for internal consistency issues with context-aware comparison.

    Args:
        facts: List of fact dictionaries with text, page, section keys

    Returns:
        List of consistency issue dictionaries
    """
    # Group values by parameter context AND base unit
    context_values = defaultdict(list)

    for fact in facts:
        text = fact.get("text", "")
        page = fact.get("page", "?")
        section = fact.get("section", "Unknown")

        # Extract numeric values
        values = extract_numeric_values(text)

        for v in values:
            # Identify parameter contexts WITH unit validation
            contexts = identify_parameter_context(text, v['unit'])

            for ctx in contexts:
                # Create context-specific key
                key = f"{ctx}|{v['base_unit']}"
                context_values[key].append({
                    "value": v["value"],
                    "unit": v["unit"],
                    "normalized_value": v["normalized_value"],
                    "base_unit": v["base_unit"],
                    "page": page,
                    "section": section,
                    "context": ctx,
                    "text_snippet": text[:300]
                })

    issues = []

    # Check for inconsistent values within same context
    for key, mentions in context_values.items():
        if len(mentions) > 1:
            # Compare normalized values
            norm_values = [m["normalized_value"] for m in mentions]

            if max(norm_values) != min(norm_values) and min(norm_values) > 0:
                diff_pct = (max(norm_values) - min(norm_values)) / min(norm_values) * 100

                if diff_pct > 5:  # >5% difference is significant
                    ctx_name = key.split('|')[0]
                    base_unit = key.split('|')[1]

                    # Format the values for display with original units AND page numbers
                    value_displays = [f"{m['value']} {m['unit']} [p. {m['page']}]" for m in mentions[:5]]

                    issues.append({
                        "type": "INCONSISTENCY",
                        "severity": "high" if diff_pct > 20 else "medium",
                        "context": ctx_name.replace('_', ' ').title(),
                        "base_unit": base_unit,
                        "values": value_displays,
                        "normalized_values": [round(v, 2) for v in norm_values[:5]],
                        "diff_percent": round(diff_pct, 1),
                        "mentions": mentions[:5],
                        "message": f"{ctx_name.replace('_', ' ').title()} reported with inconsistent values: {', '.join(value_displays[:3])} ({diff_pct:.1f}% difference when normalized)"
                    })

    return issues


def check_unit_standardization(facts: List[Dict]) -> List[Dict]:
    """
    Check for same parameter reported in different units.

    Args:
        facts: List of fact dictionaries with text, page, section keys

    Returns:
        List of unit standardization issue dictionaries
    """
    # Group by context and find different units used
    context_units = defaultdict(lambda: defaultdict(list))

    for fact in facts:
        text = fact.get("text", "")
        page = fact.get("page", "?")
        section = fact.get("section", "Unknown")

        values = extract_numeric_values(text)

        for v in values:
            # Get contexts with unit validation
            contexts = identify_parameter_context(text, v['unit'])

            for ctx in contexts:
                # Only track if base_unit matches (same type of measurement)
                context_units[ctx][v['base_unit']].append({
                    "value": v["value"],
                    "unit": v["unit"],
                    "normalized_value": v["normalized_value"],
                    "page": page,
                    "section": section,
                    "text_snippet": text[:200]
                })

    unit_issues = []

    # Find contexts where multiple different units are used
    for ctx, units_data in context_units.items():
        for base_unit, mentions in units_data.items():
            # Get unique original units used
            unique_units = list(set(m['unit'].lower() for m in mentions))

            if len(unique_units) > 1:
                # Multiple units for same parameter context
                unit_examples = []
                for unit in unique_units[:3]:
                    example = next((m for m in mentions if m['unit'].lower() == unit), None)
                    if example:
                        unit_examples.append({
                            "value": example["value"],
                            "unit": example["unit"],
                            "page": example["page"],
                            "normalized": round(example["normalized_value"], 2)
                        })

                unit_issues.append({
                    "context": ctx.replace('_', ' ').title(),
                    "base_unit": base_unit,
                    "units_used": unique_units,
                    "examples": unit_examples,
                    "count": len(mentions),
                    "severity": "medium",
                    "message": f"{ctx.replace('_', ' ').title()} reported using {len(unique_units)} different units: {', '.join(unique_units)}"
                })

    return unit_issues
