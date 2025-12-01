"""
Gap analysis for ESIA expected content.
"""

import re
from typing import List, Dict


# Gap analysis patterns for expected ESIA content
GAP_CHECKS = {
    "Project Description": {
        "Location Coordinates": r'\d+°\s*\d+\'\s*\d+"?\s*[NS].*?\d+°\s*\d+\'\s*\d+"?\s*[EW]',
        "Project Area": r'\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:ha|hectares?|km²|km2)\b',
        "Workforce Numbers": r'(?:workforce|employees?|workers?)\s*(?:of\s*)?\d+[\d,]*',
        "Water Consumption": r'water\s+(?:consumption|use|demand|requirement)[^.]*?\d+[^.]*',
        "Power Consumption": r'(?:power|electricity|energy)\s+(?:consumption|demand|requirement)[^.]*?\d+[^.]*',
        "Project Duration": r'(?:project\s+)?(?:duration|lifetime|life\s+of\s+mine)[^.]*?\d+\s*(?:years?|months?)',
        "Capital Cost": r'(?:capital|capex|investment)[^.]*?(?:USD|\$|Rp)[^.]*?\d+',
    },
    "Physical Baseline": {
        "Ambient Air Quality": r'(?:ambient|background)\s+air\s+quality[^.]*',
        "Noise Measurements": r'noise[^.]*?(?:measurement|monitoring|survey|level)[^.]*?\d+\s*dB',
        "Water Quality Data": r'water\s+quality[^.]*?(?:data|results|measurements|sampling)',
        "Rainfall Data": r'(?:rainfall|precipitation)[^.]*?\d+\s*mm',
        "Seismic Assessment": r'(?:seismic|earthquake)[^.]*?(?:hazard|risk|assessment|zone)',
        "Climate Data": r'(?:climate|temperature|humidity)[^.]*?\d+\s*(?:°C|%|mm)',
        "Topography": r'(?:topography|elevation|slope)[^.]*?\d+\s*(?:m|%|degrees?)',
    },
    "Biological Baseline": {
        "Species Lists": r'(?:species\s+list|flora\s+and\s+fauna|biodiversity\s+survey|species\s+recorded)',
        "IUCN Status": r'IUCN[^.]*(?:status|category|listed|endangered|vulnerable|threatened)',
        "Protected Areas": r'(?:protected\s+area|conservation\s+area|national\s+park|nature\s+reserve)[^.]*',
        "Critical Habitat": r'critical\s+habitat[^.]*',
        "Endemic Species": r'endemic\s+(?:species|flora|fauna)[^.]*',
    },
    "Social Baseline": {
        "Population Data": r'population[^.]*?\d+[\d,]*\s*(?:people|persons|inhabitants)?',
        "Household Data": r'household[^.]*?\d+[\d,]*',
        "Livelihood Sources": r'livelihood[^.]*?(?:source|activity|occupation|income|farming|fishing)',
        "Vulnerable Groups": r'vulnerable\s+(?:group|people|community|population)[^.]*',
        "Land Tenure": r'(?:land\s+tenure|land\s+ownership|customary\s+land)[^.]*',
        "Indigenous Peoples": r'(?:indigenous|adat|tribal)[^.]*(?:people|community|group)',
    },
    "Impact Assessment": {
        "Significance Criteria": r'(?:significance|impact)\s+(?:criteria|rating|assessment)[^.]*',
        "Cumulative Impacts": r'cumulative\s+(?:impact|effect)[^.]*',
        "Transboundary Impacts": r'(?:transboundary|cross-border)\s+(?:impact|effect)[^.]*',
    },
    "Mitigation & Management": {
        "ESMP Reference": r'(?:ESMP|environmental\s+and\s+social\s+management\s+plan)[^.]*',
        "Monitoring Plan": r'(?:monitoring\s+plan|monitoring\s+program)[^.]*',
        "Emergency Response": r'(?:emergency\s+response|contingency\s+plan|spill\s+response)[^.]*',
    }
}


def analyze_gaps(facts: List[Dict]) -> List[Dict]:
    """
    Identify gaps in expected content with actual content extraction.

    Args:
        facts: List of fact dictionaries with text and page keys

    Returns:
        List of gap analysis result dictionaries
    """
    gaps = []

    # Search through all chunks to find matches with page references
    for section, checks in GAP_CHECKS.items():
        for item, pattern in checks.items():
            found_matches = []

            for fact in facts:
                text = fact.get("text", "")
                page = fact.get("page", "?")

                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    for match in matches[:2]:  # Limit to 2 matches per chunk
                        # Clean up the match
                        if isinstance(match, tuple):
                            match = match[0]
                        match_text = match.strip()
                        if len(match_text) > 150:
                            match_text = match_text[:150] + "..."

                        found_matches.append({
                            "content": match_text,
                            "page": page
                        })

            # Deduplicate and limit matches
            seen_content = set()
            unique_matches = []
            for m in found_matches:
                content_key = m["content"][:50].lower()
                if content_key not in seen_content:
                    seen_content.add(content_key)
                    unique_matches.append(m)
                    if len(unique_matches) >= 3:  # Max 3 examples per item
                        break

            if unique_matches:
                gaps.append({
                    "section": section,
                    "item": item,
                    "status": "PRESENT",
                    "severity": "none",
                    "matches": unique_matches
                })
            else:
                gaps.append({
                    "section": section,
                    "item": item,
                    "status": "MISSING",
                    "severity": "high" if section in ["Project Description", "Social Baseline"] else "medium",
                    "matches": []
                })

    return gaps
