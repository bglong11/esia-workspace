"""
LLM-based page-by-page fact distillation for Document Factsheet.

Transforms verbose ESIA paragraphs into clear, concise bullet points
organized by page number for easy cross-referencing.
"""

import os
import re
import json
from typing import Dict, List, Optional
from collections import defaultdict
import urllib.request
import urllib.error


# Default configuration
DEFAULT_CONFIG = {
    'provider': 'openrouter',
    'model': 'google/gemini-2.5-flash',
    'max_tokens': 3000,
    'temperature': 0.3,
    'api_key_env': 'OPENROUTER_API_KEY',
    'base_url': 'https://openrouter.ai/api/v1/chat/completions',
    'batch_size': 5,  # Pages per LLM call
    'max_facts_per_page': 15
}

# Sections to skip (low-value content)
SKIP_SECTIONS = {
    'table of contents', 'list of figures', 'list of tables',
    'list of appendices', 'abbreviations', 'acronyms',
    'glossary', 'references', 'bibliography', 'index'
}

# LLM prompt for fact distillation
DISTILLATION_PROMPT = """You are an ESIA (Environmental and Social Impact Assessment) document reviewer extracting key facts for compliance review.

For each page, extract UP TO {max_facts} bullet points capturing the most important facts.
Each bullet should be a complete, self-contained sentence.

PRIORITIZE:
- Quantitative data (areas, populations, thresholds, timelines, costs)
- Environmental baseline conditions (air quality, water, biodiversity)
- Social baseline data (communities, livelihoods, land use)
- Identified impacts and significance ratings
- Mitigation commitments and management plans
- Regulatory requirements and permits
- IFC Performance Standards compliance

SKIP:
- Procedural text (table of contents, document structure)
- Boilerplate/generic language
- Figure/table references without substantive content
- Repeated information already captured

OUTPUT FORMAT - Return valid JSON only:
{{
  "pages": [
    {{
      "page": 48,
      "section_context": "Brief section name",
      "facts": [
        "Clear, complete factual sentence.",
        "Another factual sentence with specific details.",
        ...
      ]
    }}
  ]
}}

INPUT - Pages {start_page} to {end_page}:
{formatted_chunks}"""


class PageDistiller:
    """Distills verbose ESIA chunks into concise per-page facts."""

    def __init__(self, config: Dict = None):
        """
        Initialize the page distiller.

        Args:
            config: Optional configuration dictionary
        """
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.model = self.config['model']
        self.max_tokens = self.config['max_tokens']
        self.temperature = self.config['temperature']
        self.base_url = self.config['base_url']
        self.api_key_env = self.config['api_key_env']
        self.batch_size = self.config['batch_size']
        self.max_facts_per_page = self.config['max_facts_per_page']
        self.cache = {}

    def distill_document(
        self,
        facts: List[Dict],
        use_llm: bool = True
    ) -> Dict[int, Dict]:
        """
        Distill all facts organized by page.

        Args:
            facts: List of fact dictionaries from JSONL
            use_llm: Whether to use LLM for distillation

        Returns:
            Dictionary mapping page number to distilled page data
        """
        # Step 1: Group facts by page
        pages_data = self._group_by_page(facts)

        # Step 2: Filter out low-value pages
        filtered_pages = self._filter_pages(pages_data)

        if not filtered_pages:
            return {}

        # Step 3: Distill via LLM or fallback
        if use_llm:
            try:
                return self._distill_with_llm(filtered_pages)
            except Exception as e:
                print(f"LLM distillation failed: {e}. Using fallback.")
                return self._fallback_distill(filtered_pages)
        else:
            return self._fallback_distill(filtered_pages)

    def _group_by_page(self, facts: List[Dict]) -> Dict[int, List[Dict]]:
        """Group facts by page number."""
        pages = defaultdict(list)
        for idx, fact in enumerate(facts):
            page = fact.get('page')
            if page and isinstance(page, (int, str)):
                try:
                    page_num = int(page)
                    pages[page_num].append({
                        'index': idx,
                        'text': fact.get('text', ''),
                        'section': fact.get('section', ''),
                        'page': page_num
                    })
                except (ValueError, TypeError):
                    continue
        return dict(pages)

    def _filter_pages(self, pages_data: Dict[int, List[Dict]]) -> Dict[int, List[Dict]]:
        """Filter out low-value pages (TOC, figures, etc.)."""
        filtered = {}

        for page, chunks in pages_data.items():
            if not chunks:
                continue

            # Filter out chunks from skip sections
            valid_chunks = []
            for chunk in chunks:
                section = (chunk.get('section') or '').lower()
                text = chunk.get('text', '')

                # Skip if section is in skip list
                if any(skip in section for skip in SKIP_SECTIONS):
                    continue

                # Skip if text is too short (likely just a heading)
                if len(text.strip()) < 50:
                    continue

                valid_chunks.append(chunk)

            # Keep page if it has valid chunks
            if valid_chunks:
                filtered[page] = valid_chunks

        return filtered

    def _distill_with_llm(self, pages_data: Dict[int, List[Dict]]) -> Dict[int, Dict]:
        """Distill pages using LLM in batches."""
        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            print(f"{self.api_key_env} not set. Using fallback distillation.")
            return self._fallback_distill(pages_data)

        result = {}
        page_numbers = sorted(pages_data.keys())

        # Process in batches
        for i in range(0, len(page_numbers), self.batch_size):
            batch_pages = page_numbers[i:i + self.batch_size]
            batch_data = {p: pages_data[p] for p in batch_pages}

            try:
                batch_result = self._process_batch(batch_data, api_key)
                result.update(batch_result)
            except Exception as e:
                print(f"Batch {i//self.batch_size + 1} failed: {e}. Using fallback for these pages.")
                for page in batch_pages:
                    result[page] = self._fallback_page(page, pages_data[page])

        return result

    def _process_batch(self, batch_data: Dict[int, List[Dict]], api_key: str) -> Dict[int, Dict]:
        """Process a batch of pages through LLM."""
        # Format input for prompt
        formatted_chunks = self._format_chunks_for_prompt(batch_data)
        page_nums = sorted(batch_data.keys())

        # Build prompt
        prompt = DISTILLATION_PROMPT.format(
            max_facts=self.max_facts_per_page,
            start_page=page_nums[0],
            end_page=page_nums[-1],
            formatted_chunks=formatted_chunks
        )

        # Build request payload
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an ESIA document analyst. Extract key facts concisely. Return valid JSON only."
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
            with urllib.request.urlopen(req, timeout=90) as response:
                result = json.loads(response.read().decode('utf-8'))
                content = result['choices'][0]['message']['content']
                return self._parse_llm_response(content, batch_data)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            raise Exception(f"API error {e.code}: {error_body}")
        except urllib.error.URLError as e:
            raise Exception(f"Network error: {e.reason}")

    def _format_chunks_for_prompt(self, batch_data: Dict[int, List[Dict]]) -> str:
        """Format page chunks for LLM prompt."""
        lines = []

        for page in sorted(batch_data.keys()):
            chunks = batch_data[page]
            section_name = chunks[0].get('section', 'Unknown') if chunks else 'Unknown'
            lines.append(f"\n=== PAGE {page} ({section_name}) ===")

            for chunk in chunks:
                text = chunk.get('text', '')[:600]  # Truncate long chunks
                lines.append(f"• {text}")

        return '\n'.join(lines)

    def _parse_llm_response(self, content: str, batch_data: Dict[int, List[Dict]]) -> Dict[int, Dict]:
        """Parse LLM JSON response into structured data."""
        # Clean up response - extract JSON
        content = content.strip()

        # Handle markdown code blocks
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # Try to find JSON object in response
            match = re.search(r'\{[\s\S]*\}', content)
            if match:
                try:
                    data = json.loads(match.group())
                except json.JSONDecodeError:
                    return {p: self._fallback_page(p, batch_data[p]) for p in batch_data}
            else:
                return {p: self._fallback_page(p, batch_data[p]) for p in batch_data}

        result = {}
        pages_in_response = {p['page']: p for p in data.get('pages', [])}

        for page in batch_data:
            if page in pages_in_response:
                page_data = pages_in_response[page]
                result[page] = {
                    'page': page,
                    'section_context': page_data.get('section_context', ''),
                    'distilled_facts': page_data.get('facts', []),
                    'original_chunks': batch_data[page]
                }
            else:
                # Page not in response, use fallback
                result[page] = self._fallback_page(page, batch_data[page])

        return result

    def _fallback_distill(self, pages_data: Dict[int, List[Dict]]) -> Dict[int, Dict]:
        """Fallback distillation without LLM - just clean up text."""
        result = {}
        for page, chunks in pages_data.items():
            result[page] = self._fallback_page(page, chunks)
        return result

    def _fallback_page(self, page: int, chunks: List[Dict]) -> Dict:
        """Create fallback page data without LLM."""
        section_context = chunks[0].get('section', '') if chunks else ''

        # Extract first sentence from each chunk as a "fact"
        facts = []
        for chunk in chunks[:self.max_facts_per_page]:
            text = chunk.get('text', '').strip()
            if text:
                # Get first sentence or first 150 chars
                first_sentence = re.split(r'(?<=[.!?])\s+', text)[0]
                if len(first_sentence) > 200:
                    first_sentence = first_sentence[:200] + '...'
                facts.append(first_sentence)

        return {
            'page': page,
            'section_context': section_context,
            'distilled_facts': facts,
            'original_chunks': chunks
        }
