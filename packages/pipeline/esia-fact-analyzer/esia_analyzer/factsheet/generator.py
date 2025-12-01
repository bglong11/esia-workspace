"""
LLM-based factsheet summary generation.

Uses OpenRouter API with Gemini 2.5 Flash for generating professional prose from selected facts.
Falls back to static templates when LLM is unavailable.
"""

import os
import re
import json
from typing import Dict, List, Optional
import urllib.request
import urllib.error

from .templates import generate_static_summary


# Default configuration
DEFAULT_CONFIG = {
    'provider': 'openrouter',
    'model': 'google/gemini-2.5-flash',
    'max_tokens': 2500,
    'temperature': 0.3,
    'api_key_env': 'OPENROUTER_API_KEY',
    'base_url': 'https://openrouter.ai/api/v1/chat/completions'
}

# LLM prompt template
FACTSHEET_PROMPT = """You are a professional ESIA (Environmental and Social Impact Assessment) document reviewer.

Given the structured facts below, write a detailed Project Summary consisting of exactly 5 sections in DOT-POINT FORMAT:

1. **Project Overview**: Project type, proponent, location, key parameters (capacity, area, workforce, timeline, investment)
2. **Environmental and Social Baseline**: Key existing environmental conditions (climate, air, water, biodiversity) and social conditions (communities, livelihoods, land use)
3. **Major Anticipated Impacts**: Most significant environmental and social impacts identified, their severity and duration
4. **Mitigation and Management Measures**: Key commitments, management plans (ESMP, monitoring), and specific mitigation actions
5. **Residual Risks and Compliance**: Remaining risks after mitigation, applicable standards (IFC, World Bank, national regulations), compliance status

FORMAT RULES:
- Each section must have 4-8 bullet points
- Each bullet point MUST be a complete, self-contained sentence that makes sense on its own
- End each bullet point with the page reference in square brackets: [p. 45] or [pp. 45-47]
- Start each bullet point with "•"
- Include specific numbers, names, locations, and quantitative data where available
- Do NOT use sentence fragments or incomplete thoughts

CONTENT RULES:
- Use ONLY information from the facts provided below
- Do NOT introduce any new facts, assumptions, or information not present in the input
- Each bullet point should convey one clear, complete piece of information
- Use professional, objective language suitable for lender/regulator review
- If a section has insufficient facts, include only what is available

EXAMPLE FORMAT:
• The project is a copper-gold mine located in West Nusa Tenggara Province, Indonesia. [p. 12]
• Peak construction workforce is estimated at 3,000 workers, with 6,000 during operations. [p. 45]

FACTS BY DOMAIN:
{structured_facts}

Write the Project Summary now, with each section clearly labeled and using bullet points:
"""


class FactsheetGenerator:
    """Generates factsheet summaries using LLM or static templates."""

    def __init__(self, config: Dict = None):
        """
        Initialize the generator.

        Args:
            config: Optional configuration dictionary with LLM settings
                - provider: 'openrouter' (default)
                - model: Model identifier (default: 'google/gemini-2.5-flash-preview')
                - max_tokens: Maximum tokens in response
                - temperature: Sampling temperature
                - api_key_env: Environment variable name for API key
        """
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.model = self.config['model']
        self.max_tokens = self.config['max_tokens']
        self.temperature = self.config['temperature']
        self.base_url = self.config['base_url']
        self.api_key_env = self.config['api_key_env']

    def generate_summary(
        self,
        selected_facts: Dict[str, List[Dict]],
        use_llm: bool = True
    ) -> Dict:
        """
        Generate factsheet summary from selected facts.

        Args:
            selected_facts: Dictionary mapping domains to lists of facts
            use_llm: Whether to attempt LLM generation

        Returns:
            Dictionary with paragraphs, fact_mapping, and validation info
        """
        # Build fact mapping for traceability
        fact_mapping = {}
        for domain, facts in selected_facts.items():
            for fact in facts:
                fact_mapping[fact['id']] = {
                    'text': fact['text'],
                    'page': fact['page'],
                    'domain': domain
                }

        # Try LLM generation if enabled
        if use_llm:
            try:
                paragraphs = self._generate_with_llm(selected_facts)
                if paragraphs:
                    return {
                        'paragraphs': paragraphs,
                        'fact_mapping': fact_mapping,
                        'method': 'llm',
                        'model': self.model,
                        'validation': self._validate_summary(paragraphs, fact_mapping)
                    }
            except Exception as e:
                print(f"LLM generation failed: {e}. Falling back to static templates.")

        # Fallback to static templates
        paragraphs = generate_static_summary(selected_facts)
        return {
            'paragraphs': paragraphs,
            'fact_mapping': fact_mapping,
            'method': 'static',
            'validation': self._validate_summary(paragraphs, fact_mapping)
        }

    def _generate_with_llm(self, selected_facts: Dict[str, List[Dict]]) -> Optional[Dict[str, str]]:
        """
        Generate summary using OpenRouter API.

        Args:
            selected_facts: Dictionary of domain -> facts

        Returns:
            Dictionary of section -> paragraph text, or None if failed
        """
        # Check for API key
        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            print(f"{self.api_key_env} not set. Skipping LLM generation.")
            return None

        # Format facts for prompt
        formatted_facts = self._format_facts_for_prompt(selected_facts)

        # Build prompt
        prompt = FACTSHEET_PROMPT.format(structured_facts=formatted_facts)

        # Build request payload
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional environmental consultant writing ESIA factsheet summaries. Be precise, factual, and include fact ID references."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }

        # Make API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/esia-fact-analyzer",
            "X-Title": "ESIA Fact Analyzer"
        }

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(self.base_url, data=data, headers=headers, method='POST')

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                content = result['choices'][0]['message']['content']
                return self._parse_llm_response(content)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            raise Exception(f"API error {e.code}: {error_body}")
        except urllib.error.URLError as e:
            raise Exception(f"Network error: {e.reason}")

    def _format_facts_for_prompt(self, selected_facts: Dict[str, List[Dict]]) -> str:
        """Format facts as structured text for LLM prompt."""
        sections = []

        domain_labels = {
            'project_overview': 'PROJECT OVERVIEW',
            'env_baseline': 'ENVIRONMENTAL BASELINE',
            'social_baseline': 'SOCIAL BASELINE',
            'major_impacts': 'MAJOR IMPACTS',
            'mitigation_commitments': 'MITIGATION & COMMITMENTS',
            'compliance': 'COMPLIANCE & RESIDUAL RISKS'
        }

        for domain, label in domain_labels.items():
            facts = selected_facts.get(domain, [])
            if facts:
                sections.append(f"\n{label}:")
                for fact in facts[:8]:  # Limit to avoid token overflow
                    text = fact['text'][:400]  # Truncate long facts
                    sections.append(f"  [{fact['id']}] {text} (p.{fact['page']})")

        return '\n'.join(sections)

    def _parse_llm_response(self, content: str) -> Dict[str, str]:
        """
        Parse LLM response into structured sections with bullet points.

        Args:
            content: Raw LLM response text

        Returns:
            Dictionary mapping section names to bullet-point text
        """
        paragraphs = {
            'project_overview': '',
            'baseline': '',
            'impacts': '',
            'mitigation': '',
            'residual_risks': ''
        }

        # Clean content first - remove markdown bold markers
        content = re.sub(r'\*\*', '', content)

        # Define section headers and their keys
        section_headers = [
            ('project_overview', ['Project Overview', '1. Project Overview', '1.Project Overview']),
            ('baseline', ['Environmental and Social Baseline', '2. Environmental and Social Baseline', '2.Environmental']),
            ('impacts', ['Major Anticipated Impacts', '3. Major Anticipated Impacts', '3.Major']),
            ('mitigation', ['Mitigation and Management', '4. Mitigation and Management', '4.Mitigation']),
            ('residual_risks', ['Residual Risks', '5. Residual Risks', '5.Residual'])
        ]

        # Find positions of each section header
        section_positions = []
        for key, headers in section_headers:
            for header in headers:
                # Search for header (case insensitive)
                match = re.search(re.escape(header), content, re.IGNORECASE)
                if match:
                    section_positions.append((match.start(), match.end(), key, header))
                    break

        # Sort by position
        section_positions.sort(key=lambda x: x[0])

        # Extract content between sections
        for i, (start, header_end, key, header) in enumerate(section_positions):
            # Find end position (start of next section or end of content)
            if i + 1 < len(section_positions):
                end_pos = section_positions[i + 1][0]
            else:
                end_pos = len(content)

            # Extract and clean section content
            section_content = content[header_end:end_pos].strip()
            # Remove the colon if present at start
            section_content = re.sub(r'^[:\s]+', '', section_content)
            # Normalize bullet characters to •
            section_content = re.sub(r'^[\-\*]\s+', '• ', section_content, flags=re.MULTILINE)
            # Remove standalone section numbers (e.g., "2." or "3." on their own line)
            section_content = re.sub(r'^\d+\.\s*$', '', section_content, flags=re.MULTILINE)
            # Clean up extra whitespace while preserving line breaks
            section_content = re.sub(r'[ \t]+', ' ', section_content)
            section_content = re.sub(r'\n{3,}', '\n\n', section_content)
            # Remove empty lines at the end
            section_content = re.sub(r'\n+$', '', section_content)

            paragraphs[key] = section_content.strip()

        # Fallback: if parsing failed, try splitting by numbered sections
        if not any(paragraphs.values()):
            parts = re.split(r'\n\s*\d+\.', content)
            keys = ['project_overview', 'baseline', 'impacts', 'mitigation', 'residual_risks']
            for i, part in enumerate(parts[1:6]):  # Skip first empty part
                if i < len(keys):
                    text = part.strip()
                    text = re.sub(r'^[\-\*]\s+', '• ', text, flags=re.MULTILINE)
                    paragraphs[keys[i]] = text

        return paragraphs

    def _validate_summary(self, paragraphs: Dict[str, str], fact_mapping: Dict) -> Dict:
        """
        Validate the generated summary.

        Args:
            paragraphs: Dictionary of section -> paragraph text
            fact_mapping: Dictionary of fact ID -> fact info

        Returns:
            Validation results dictionary
        """
        validation = {
            'all_sections_present': True,
            'sections_with_content': [],
            'sections_missing': [],
            'fact_ids_referenced': [],
            'orphan_fact_ids': []
        }

        # Check sections
        for section, content in paragraphs.items():
            if content and content.strip() and 'not available' not in content.lower():
                validation['sections_with_content'].append(section)
            else:
                validation['sections_missing'].append(section)
                validation['all_sections_present'] = False

        # Extract fact ID references
        all_content = ' '.join(paragraphs.values())
        fact_refs = re.findall(r'\[FIDs?:\s*([^\]]+)\]', all_content, re.IGNORECASE)

        referenced_ids = set()
        for ref in fact_refs:
            ids = re.findall(r'F\d+', ref)
            referenced_ids.update(ids)

        validation['fact_ids_referenced'] = list(referenced_ids)

        # Check for orphan references (IDs not in mapping)
        for fid in referenced_ids:
            if fid not in fact_mapping:
                validation['orphan_fact_ids'].append(fid)

        return validation
