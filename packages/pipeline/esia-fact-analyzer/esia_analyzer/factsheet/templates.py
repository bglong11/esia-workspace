"""
Static fallback templates for factsheet summary generation.

Used when LLM is unavailable or disabled.
"""

import re
from typing import Dict, List


def generate_static_summary(selected_facts: Dict[str, List[Dict]]) -> Dict[str, str]:
    """
    Generate factsheet summary using static templates.

    Args:
        selected_facts: Dictionary mapping domains to lists of facts

    Returns:
        Dictionary mapping section names to paragraph text
    """
    paragraphs = {}

    # Project Overview
    paragraphs['project_overview'] = _generate_project_overview(
        selected_facts.get('project_overview', [])
    )

    # Environmental & Social Baseline
    env_facts = selected_facts.get('env_baseline', [])
    social_facts = selected_facts.get('social_baseline', [])
    paragraphs['baseline'] = _generate_baseline(env_facts, social_facts)

    # Major Impacts
    paragraphs['impacts'] = _generate_impacts(
        selected_facts.get('major_impacts', [])
    )

    # Mitigation & Management
    paragraphs['mitigation'] = _generate_mitigation(
        selected_facts.get('mitigation_commitments', [])
    )

    # Residual Risks & Compliance
    paragraphs['residual_risks'] = _generate_compliance(
        selected_facts.get('compliance', [])
    )

    return paragraphs


def _generate_project_overview(facts: List[Dict]) -> str:
    """Generate project overview as bullet points."""
    if not facts:
        return "• Project overview information not available in extracted facts."

    bullets = []

    for fact in facts[:6]:
        text = fact['text'].strip()
        page = fact.get('page', '?')

        # Clean up and truncate text if needed
        if len(text) > 250:
            # Find a sentence break
            end_pos = text.find('. ', 150)
            if end_pos > 0:
                text = text[:end_pos + 1]
            else:
                text = text[:250] + '...'

        # Format as bullet point with page reference
        bullets.append(f"• {text} [p. {page}]")

    return '\n'.join(bullets) if bullets else "• Project overview information not available in extracted facts."


def _generate_baseline(env_facts: List[Dict], social_facts: List[Dict]) -> str:
    """Generate baseline as bullet points."""
    if not env_facts and not social_facts:
        return "• Baseline information not available in extracted facts."

    bullets = []
    all_facts = env_facts[:4] + social_facts[:4]

    for fact in all_facts[:6]:
        text = fact['text'].strip()
        page = fact.get('page', '?')

        # Clean up and truncate text if needed
        if len(text) > 250:
            end_pos = text.find('. ', 150)
            if end_pos > 0:
                text = text[:end_pos + 1]
            else:
                text = text[:250] + '...'

        bullets.append(f"• {text} [p. {page}]")

    return '\n'.join(bullets) if bullets else "• Baseline information not available in extracted facts."


def _generate_impacts(facts: List[Dict]) -> str:
    """Generate impacts as bullet points."""
    if not facts:
        return "• Impact assessment information not available in extracted facts."

    bullets = []

    for fact in facts[:6]:
        text = fact['text'].strip()
        page = fact.get('page', '?')

        # Clean up and truncate text if needed
        if len(text) > 250:
            end_pos = text.find('. ', 150)
            if end_pos > 0:
                text = text[:end_pos + 1]
            else:
                text = text[:250] + '...'

        bullets.append(f"• {text} [p. {page}]")

    return '\n'.join(bullets) if bullets else "• Impact assessment information not available in extracted facts."


def _generate_mitigation(facts: List[Dict]) -> str:
    """Generate mitigation as bullet points."""
    if not facts:
        return "• Mitigation measures information not available in extracted facts."

    bullets = []

    for fact in facts[:6]:
        text = fact['text'].strip()
        page = fact.get('page', '?')

        # Clean up and truncate text if needed
        if len(text) > 250:
            end_pos = text.find('. ', 150)
            if end_pos > 0:
                text = text[:end_pos + 1]
            else:
                text = text[:250] + '...'

        bullets.append(f"• {text} [p. {page}]")

    return '\n'.join(bullets) if bullets else "• Mitigation measures information not available in extracted facts."


def _generate_compliance(facts: List[Dict]) -> str:
    """Generate compliance/residual risks as bullet points."""
    if not facts:
        return "• Compliance information not available in extracted facts."

    bullets = []

    for fact in facts[:6]:
        text = fact['text'].strip()
        page = fact.get('page', '?')

        # Clean up and truncate text if needed
        if len(text) > 250:
            end_pos = text.find('. ', 150)
            if end_pos > 0:
                text = text[:end_pos + 1]
            else:
                text = text[:250] + '...'

        bullets.append(f"• {text} [p. {page}]")

    return '\n'.join(bullets) if bullets else "• Compliance information not available in extracted facts."
