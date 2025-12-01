"""
Main ESIAReviewer class for orchestrating ESIA document analysis.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Optional, Dict, List

from .consistency import check_consistency, check_unit_standardization
from .thresholds import check_thresholds
from .gaps import analyze_gaps
from .exporters.html import export_html
from .exporters.excel import export_excel


class ESIAReviewer:
    """Main class for ESIA fact analysis and review."""

    def __init__(self, skill_dir: Path):
        """
        Initialize the ESIA Reviewer.

        Args:
            skill_dir: Path to skill directory containing reference data
        """
        self.skill_dir = skill_dir
        self.thresholds = self._load_json(skill_dir / "references" / "ifc_thresholds.json")
        self.taxonomy = self._load_json(skill_dir / "references" / "esia_taxonomy.json")
        self.checklists = self._load_json(skill_dir / "references" / "reviewer_checklists.json")
        self.facts = []
        self.metadata = {}
        self.document_name = "Unknown"
        self.categorized_facts = defaultdict(list)
        self.issues = []
        self.unit_issues = []
        self.threshold_checks = []
        self.gaps = []
        self.factsheet = {}
        self.factsheet_summary = None
        self.page_factsheet = {}
        self.tables = []
        self.enable_table_analysis = False

    def _load_json(self, path: Path) -> dict:
        """Load JSON file with graceful fallback."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"WARNING: Reference file not found: {path}")
            print(f"         Using empty defaults for: {path.name}")
            return {}

    def load_data(self, chunks_path: Path, meta_path: Optional[Path] = None):
        """
        Load JSONL chunks and optional metadata.

        Args:
            chunks_path: Path to JSONL file with document chunks
            meta_path: Optional path to metadata JSON file
        """
        # Extract document name from chunks filename
        chunks_name = chunks_path.name
        if chunks_name.endswith('_chunks.jsonl'):
            self.document_name = chunks_name.replace('_chunks.jsonl', '')
        elif chunks_name.endswith('.jsonl'):
            self.document_name = chunks_name.replace('.jsonl', '')
        else:
            self.document_name = chunks_name

        with open(chunks_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    self.facts.append(json.loads(line))

        if meta_path and meta_path.exists():
            self.metadata = self._load_json(meta_path)
            self.load_tables()

        print(f"Loaded {len(self.facts)} chunks from {chunks_path.name}")

    def load_tables(self):
        """Load tables from metadata (read-only, no analysis yet).

        Returns:
            List of table dictionaries from metadata. Each table contains:
            - table_id: Unique identifier
            - page: Page number where table appears
            - caption: Table caption/title
            - content: Markdown-formatted table content
            - metadata: Additional table metadata
        """
        if not self.metadata:
            return []

        try:
            tables = self.metadata.get('tables', [])
            if not tables:
                print("DEBUG: No tables found in metadata")
                return []

            # Store tables for later use
            self.tables = tables
            print(f"DEBUG: Loaded {len(tables)} tables from metadata")
            return tables
        except Exception as e:
            print(f"ERROR: Error loading tables: {e}")
            return []

    def categorize_facts(self):
        """Categorize each fact according to taxonomy."""
        categories = self.taxonomy.get("categories", {})

        if not categories:
            # Fall back to section-based categorization
            for fact in self.facts:
                section = fact.get("section") or "UNCATEGORIZED"
                fact["categories"] = [section]
                self.categorized_facts[section].append(fact)
            print(f"Categorized {len(self.facts)} facts by document section (no taxonomy)")
            return

        for fact in self.facts:
            text = fact.get("text", "").lower()
            section = (fact.get("section") or "").lower()
            headings = " ".join(fact.get("metadata", {}).get("headings", [])).lower()
            combined = f"{text} {section} {headings}"

            matched = []
            for cat_name, cat_data in categories.items():
                keywords = cat_data.get("keywords", [])
                for kw in keywords:
                    if kw.lower() in combined:
                        matched.append(cat_name)
                        break

            if not matched:
                matched = ["UNCATEGORIZED"]

            fact["categories"] = matched
            for cat in matched:
                self.categorized_facts[cat].append(fact)

    def build_factsheet(self) -> dict:
        """Build organized factsheet from facts grouped by actual sections and extracted topics."""
        facts_by_section = defaultdict(list)

        for fact in self.facts:
            section = (fact.get('section') or 'Uncategorized').strip()
            if section and section not in ['TABLE OF CONTENTS', 'LIST OF FIGURES', 'LIST OF TABLES', 'LIST OF APPENDICES', 'ABBREVIATIONS']:
                facts_by_section[section].append(fact)

        factsheet = {}

        for section_name in sorted(facts_by_section.keys()):
            section_facts = facts_by_section[section_name]

            if not section_facts:
                continue

            topics_dict = self._extract_topics_from_facts(section_facts)

            if topics_dict:
                factsheet[section_name] = topics_dict

        return factsheet

    def _extract_topics_from_facts(self, facts: list) -> dict:
        """Extract topics/keywords from a list of facts."""
        topics_dict = {}

        for fact in facts:
            text = fact.get('text', '')
            page = fact.get('page', '?')

            if not text:
                continue

            topic = self._extract_topic_keyword(text)

            if topic:
                if topic not in topics_dict:
                    topics_dict[topic] = []

                topics_dict[topic].append({
                    'text': text,
                    'page': page
                })

        return topics_dict

    def _extract_topic_keyword(self, text: str) -> str:
        """Extract a topic keyword from fact text."""
        common_topics = [
            r'(dam|reservoir|water intake)',
            r'(power station|power plant|generating station)',
            r'(mine|mining|pit|excavation)',
            r'(pipeline|transmission line|infrastructure)',
            r'(road|transport|access|bridge)',
            r'(railway|rail|train)',
            r'(port|harbor|jetty|wharf)',
            r'(settlement|village|community|population)',
            r'(agriculture|farming|land use|forest)',
            r'(species|flora|fauna|wildlife|habitat)',
            r'(river|stream|water body|wetland|marsh)',
            r'(soil|geology|bedrock|minerals)',
            r'(air quality|atmosphere|emissions)',
            r'(noise|vibration)',
            r'(waste|wastewater|effluent)',
            r'(climate|temperature|rainfall)',
            r'(cultural|heritage|archaeological)',
            r'(management|monitoring|mitigation|plan)',
            r'(ecosystem|biodiversity|conservation)',
            r'(workforce|employment|labor)',
            r'(equipment|facility|infrastructure)',
            r'(monitoring|assessment|survey)',
            r'(baseline|existing|current)',
            r'(impact|effect|outcome)',
        ]

        text_lower = text.lower()

        for pattern in common_topics:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).title()

        # Fallback: extract first capitalized phrase
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', text)
        if capitalized and len(capitalized[0].split()) >= 2:
            return capitalized[0]

        # Fallback: first significant word
        words = text.split()
        if len(words) > 2:
            skip_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'is', 'are', 'was', 'were', 'be', 'been'}
            for word in words:
                word_lower = word.lower().rstrip('.,;:')
                if word_lower not in skip_words and len(word) > 3 and word[0].isupper():
                    return word.rstrip('.,;:')

        return None

    def generate_summary(self) -> dict:
        """Generate analysis summary."""
        max_page = 0
        for fact in self.facts:
            page = fact.get("page")
            if page and isinstance(page, int) and page > max_page:
                max_page = page
        total_pages = max_page if max_page > 0 else "Unknown"

        return {
            "document": self.document_name,
            "total_chunks": len(self.facts),
            "total_pages": total_pages,
            "analysis_date": datetime.now().isoformat(),
            "categories": {cat: len(facts) for cat, facts in self.categorized_facts.items()},
            "issues": {
                "total": len(self.issues),
                "high_severity": len([i for i in self.issues if i.get("severity") == "high"]),
                "medium_severity": len([i for i in self.issues if i.get("severity") == "medium"]),
            },
            "unit_issues": {
                "total": len(self.unit_issues),
            },
            "threshold_checks": {
                "total": len(self.threshold_checks),
                "exceedances": len([t for t in self.threshold_checks if t["status"] == "EXCEEDANCE"]),
                "approaching": len([t for t in self.threshold_checks if t["status"] == "APPROACHING"]),
                "compliant": len([t for t in self.threshold_checks if t["status"] == "COMPLIANT"]),
            },
            "gaps": {
                "total_checked": len(self.gaps),
                "missing": len([g for g in self.gaps if g["status"] == "MISSING"]),
                "present": len([g for g in self.gaps if g["status"] == "PRESENT"]),
            }
        }

    def generate_factsheet_summary(self, use_llm: bool = True) -> Optional[Dict]:
        """
        Generate factsheet summary using LLM or static templates.

        Args:
            use_llm: Whether to attempt LLM generation (falls back to static if unavailable)

        Returns:
            Factsheet summary dictionary or None
        """
        try:
            from .factsheet import FactSelector, FactsheetGenerator

            # Step 1: Select facts for summary
            selector = FactSelector()
            selected_facts = selector.select_facts_for_summary(self.facts)

            # Step 2: Generate summary
            generator = FactsheetGenerator()
            self.factsheet_summary = generator.generate_summary(selected_facts, use_llm=use_llm)

            return self.factsheet_summary
        except ImportError as e:
            print(f"Warning: Could not import factsheet modules: {e}")
            return None
        except Exception as e:
            print(f"Warning: Factsheet summary generation failed: {e}")
            return None

    def generate_page_factsheet(self, use_llm: bool = True) -> Dict[int, Dict]:
        """
        Generate page-by-page factsheet with LLM distillation.

        Transforms verbose ESIA paragraphs into clear, concise bullet points
        organized by page number for easy cross-referencing.

        Args:
            use_llm: Whether to use LLM for intelligent distillation

        Returns:
            Dictionary mapping page numbers to distilled facts
        """
        try:
            from .factsheet.page_distiller import PageDistiller

            print("Distilling facts by page...")
            distiller = PageDistiller()
            self.page_factsheet = distiller.distill_document(self.facts, use_llm=use_llm)
            print(f"Distilled {len(self.page_factsheet)} pages")
            return self.page_factsheet
        except ImportError as e:
            print(f"Warning: Could not import PageDistiller: {e}")
            return self._fallback_page_factsheet()
        except Exception as e:
            print(f"Warning: Page factsheet generation failed: {e}")
            return self._fallback_page_factsheet()

    def _fallback_page_factsheet(self) -> Dict[int, Dict]:
        """Fallback: group chunks by page without LLM distillation."""
        from collections import defaultdict

        pages = defaultdict(list)
        for fact in self.facts:
            page = fact.get('page')
            if page and isinstance(page, (int, str)):
                try:
                    page_num = int(page)
                    pages[page_num].append({
                        'text': fact.get('text', '')[:200] + '...' if len(fact.get('text', '')) > 200 else fact.get('text', ''),
                        'section': fact.get('section', ''),
                        'page': page_num
                    })
                except (ValueError, TypeError):
                    continue

        result = {}
        for page, chunks in pages.items():
            result[page] = {
                'page': page,
                'section_context': chunks[0].get('section', '') if chunks else '',
                'distilled_facts': [c['text'] for c in chunks[:15]],
                'original_chunks': chunks
            }

        self.page_factsheet = result
        return result

    def run_analysis(self):
        """Run full analysis pipeline."""
        print("Categorizing facts...")
        self.categorize_facts()

        print("Building factsheet...")
        self.factsheet = self.build_factsheet()

        print("Checking internal consistency (context-aware)...")
        self.issues = check_consistency(self.facts)

        print("Checking unit standardization...")
        self.unit_issues = check_unit_standardization(self.facts)

        print("Checking IFC thresholds...")
        self.threshold_checks = check_thresholds(self.facts, self.thresholds)

        print("Analyzing gaps...")
        self.gaps = analyze_gaps(self.facts)

        print("Generating project summary...")
        self.generate_factsheet_summary(use_llm=True)

        print("Generating page factsheet...")
        self.generate_page_factsheet(use_llm=True)

        print("Generating summary...")
        return self.generate_summary()

    def export_html(self, output_path: Path):
        """Export analysis results to HTML dashboard."""
        summary = self.generate_summary()
        export_html(
            output_path=output_path,
            summary=summary,
            issues=self.issues,
            unit_issues=self.unit_issues,
            threshold_checks=self.threshold_checks,
            gaps=self.gaps,
            factsheet=self.factsheet,
            factsheet_summary=self.factsheet_summary,
            page_factsheet=self.page_factsheet
        )

    def export_excel(self, output_path: Path):
        """Export analysis results to Excel workbook."""
        summary = self.generate_summary()
        export_excel(
            output_path=output_path,
            summary=summary,
            categorized_facts=dict(self.categorized_facts),
            issues=self.issues,
            unit_issues=self.unit_issues,
            threshold_checks=self.threshold_checks,
            gaps=self.gaps,
            factsheet_summary=self.factsheet_summary
        )
