"""
Static fact selection and organization for factsheet summary generation.

Implements domain-based filtering, importance scoring, and de-duplication
to select the most relevant facts for summary generation.
"""

import re
from typing import List, Dict, Tuple


# Domain buckets for organizing facts
DOMAIN_BUCKETS = {
    'project_overview': {
        'patterns': [
            r'project\s+description', r'project\s+overview', r'executive\s+summary',
            r'project\s+location', r'project\s+components', r'project\s+schedule',
            r'capacity', r'production', r'investment', r'workforce', r'capital',
            r'operational\s+life', r'mine\s+life', r'project\s+area', r'study\s+area',
            r'coordinates', r'latitude', r'longitude'
        ],
        'section_patterns': [
            r'executive', r'summary', r'introduction', r'project\s+description',
            r'overview', r'background'
        ],
        'priority_keywords': ['total', 'main', 'primary', 'key', 'overall', 'approximately'],
        'max_facts': 10
    },
    'env_baseline': {
        'patterns': [
            r'physical\s+environment', r'climate', r'air\s+quality', r'water\s+quality',
            r'geology', r'topography', r'hydrology', r'meteorology', r'rainfall',
            r'temperature', r'humidity', r'wind', r'soil', r'groundwater',
            r'surface\s+water', r'ambient', r'baseline\s+conditions'
        ],
        'section_patterns': [
            r'physical', r'environment', r'baseline', r'climate', r'geology',
            r'hydrology', r'air\s+quality', r'water\s+quality'
        ],
        'priority_keywords': ['baseline', 'existing', 'ambient', 'background', 'measured'],
        'max_facts': 8
    },
    'social_baseline': {
        'patterns': [
            r'social\s+environment', r'socio-economic', r'population', r'livelihood',
            r'community', r'land\s+use', r'cultural\s+heritage', r'indigenous',
            r'household', r'village', r'settlement', r'affected\s+people',
            r'stakeholder', r'employment', r'income', r'education', r'health'
        ],
        'section_patterns': [
            r'social', r'socio', r'community', r'stakeholder', r'livelihood',
            r'cultural', r'heritage'
        ],
        'priority_keywords': ['affected', 'local', 'community', 'village', 'household'],
        'max_facts': 8
    },
    'major_impacts': {
        'patterns': [
            r'impact\s+assessment', r'significant\s+impact', r'major\s+impact',
            r'environmental\s+impact', r'social\s+impact', r'cumulative',
            r'adverse', r'beneficial', r'residual', r'magnitude', r'severity',
            r'duration', r'reversibility', r'likelihood'
        ],
        'section_patterns': [
            r'impact', r'assessment', r'effect', r'consequence'
        ],
        'priority_keywords': ['significant', 'major', 'high', 'adverse', 'permanent', 'irreversible'],
        'max_facts': 10
    },
    'mitigation_commitments': {
        'patterns': [
            r'mitigation', r'management\s+plan', r'ESMP', r'monitoring',
            r'commitment', r'measure', r'control', r'prevention', r'reduction',
            r'avoidance', r'compensation', r'offset', r'restoration'
        ],
        'section_patterns': [
            r'mitigation', r'management', r'ESMP', r'monitoring', r'plan'
        ],
        'priority_keywords': ['will', 'shall', 'must', 'commit', 'implement', 'ensure'],
        'max_facts': 8
    },
    'compliance': {
        'patterns': [
            r'compliance', r'regulatory', r'permit', r'license', r'standard',
            r'IFC', r'World\s+Bank', r'ADB', r'residual', r'performance\s+standard',
            r'EHS\s+guideline', r'national\s+regulation', r'legal\s+requirement'
        ],
        'section_patterns': [
            r'compliance', r'regulatory', r'legal', r'requirement', r'standard'
        ],
        'priority_keywords': ['comply', 'meet', 'exceed', 'residual', 'remaining', 'accordance'],
        'max_facts': 6
    }
}


class FactSelector:
    """Selects and organizes facts for factsheet summary generation."""

    def __init__(self, config: Dict = None):
        """
        Initialize the fact selector.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.similarity_threshold = self.config.get('similarity_threshold', 0.8)

    def select_facts_for_summary(self, facts: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Select and organize facts into domain buckets.

        Args:
            facts: List of fact dictionaries from JSONL

        Returns:
            Dictionary mapping domain names to lists of selected facts
        """
        # Step 1: Classify facts into domains
        domain_facts = {domain: [] for domain in DOMAIN_BUCKETS.keys()}

        for idx, fact in enumerate(facts):
            text = fact.get('text', '')
            section = fact.get('section', '') or ''
            page = fact.get('page', '?')

            # Skip very short facts
            if len(text.split()) < 5:
                continue

            # Find matching domains
            matched_domains = self._classify_fact(text, section)

            for domain in matched_domains:
                # Calculate importance score
                score = self._calculate_importance_score(fact, domain)

                domain_facts[domain].append({
                    'id': f'F{idx}',
                    'text': text,
                    'page': page,
                    'section': section,
                    'score': score,
                    'original_index': idx
                })

        # Step 2: De-duplicate and select top facts per domain
        selected = {}
        for domain, facts_list in domain_facts.items():
            if not facts_list:
                continue

            # De-duplicate
            unique_facts = self._deduplicate_facts(facts_list)

            # Sort by score and select top N
            max_facts = DOMAIN_BUCKETS[domain]['max_facts']
            sorted_facts = sorted(unique_facts, key=lambda x: x['score'], reverse=True)
            selected[domain] = sorted_facts[:max_facts]

        return selected

    def _classify_fact(self, text: str, section: str) -> List[str]:
        """
        Classify a fact into one or more domains.

        Args:
            text: Fact text
            section: Section name

        Returns:
            List of matching domain names
        """
        text_lower = text.lower()
        section_lower = section.lower()
        matched = []

        for domain, config in DOMAIN_BUCKETS.items():
            # Check text patterns
            text_match = False
            for pattern in config['patterns']:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    text_match = True
                    break

            # Check section patterns
            section_match = False
            for pattern in config.get('section_patterns', []):
                if re.search(pattern, section_lower, re.IGNORECASE):
                    section_match = True
                    break

            if text_match or section_match:
                matched.append(domain)

        return matched

    def _calculate_importance_score(self, fact: Dict, domain: str) -> float:
        """
        Calculate importance score for a fact.

        Args:
            fact: Fact dictionary
            domain: Domain name

        Returns:
            Importance score between 0.0 and 1.0
        """
        score = 0.0
        text = fact.get('text', '').lower()
        section = (fact.get('section') or '').lower()

        # 1. Section weight (Executive Summary > detailed sections)
        if 'executive' in section or 'summary' in section:
            score += 0.3
        elif 'introduction' in section or 'overview' in section:
            score += 0.2
        elif 'conclusion' in section:
            score += 0.15

        # 2. Numeric content (facts with numbers are often key)
        numbers = re.findall(r'\d+(?:,\d{3})*(?:\.\d+)?', text)
        if numbers:
            score += 0.15
            # Bonus for multiple numbers
            if len(numbers) >= 3:
                score += 0.05

        # 3. Priority keywords for this domain
        priority_kws = DOMAIN_BUCKETS[domain].get('priority_keywords', [])
        keyword_matches = sum(1 for kw in priority_kws if kw in text)
        score += min(0.15, keyword_matches * 0.05)

        # 4. Length optimization (prefer medium-length facts)
        word_count = len(text.split())
        if 30 <= word_count <= 100:
            score += 0.1
        elif 20 <= word_count < 30 or 100 < word_count <= 150:
            score += 0.05
        elif word_count < 15 or word_count > 200:
            score -= 0.1

        # 5. Uniqueness boost (facts with proper nouns/specific terms)
        proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', fact.get('text', ''))
        if proper_nouns:
            score += 0.1

        # 6. Has units (scientific/technical content)
        if re.search(r'\b(?:km|ha|m²|MW|tonnes?|dB|°C|mg/L|µg/m³)\b', text, re.IGNORECASE):
            score += 0.1

        return max(0.0, min(1.0, score))

    def _deduplicate_facts(self, facts: List[Dict]) -> List[Dict]:
        """
        Remove near-duplicate facts.

        Args:
            facts: List of fact dictionaries

        Returns:
            De-duplicated list of facts
        """
        unique = []
        seen_signatures = set()

        for fact in facts:
            text = fact.get('text', '').lower()

            # Create signature: normalized first 60 chars + key numbers
            signature_text = re.sub(r'\s+', ' ', text[:60])
            numbers = tuple(sorted(set(re.findall(r'\d+', text))))

            # Include page to allow same content from different pages
            key = (signature_text, numbers)

            if key not in seen_signatures:
                seen_signatures.add(key)
                unique.append(fact)

        return unique

    def format_for_llm(self, selected_facts: Dict[str, List[Dict]]) -> str:
        """
        Format selected facts as JSON for LLM input.

        Args:
            selected_facts: Dictionary of domain -> facts

        Returns:
            JSON string for LLM prompt
        """
        import json

        formatted = {}
        for domain, facts in selected_facts.items():
            formatted[domain] = [
                {
                    'id': f['id'],
                    'text': f['text'][:500],  # Truncate for token efficiency
                    'page': f['page']
                }
                for f in facts
            ]

        return json.dumps(formatted, indent=2)
