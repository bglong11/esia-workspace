"""
ESIA Fact Extraction System - SaaS Adapted Version
Supports PDF, DOCX, and Markdown input with Docling extraction
Database integration for web application
"""

import dspy
import json
import re
from typing import List, Dict, Any, Optional, Callable, Literal, Union
from pathlib import Path
from dataclasses import dataclass, asdict
from collections import defaultdict
import unicodedata
from datetime import datetime
from pydantic import BaseModel, Field


# Import unit conversions and utilities from original
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from esia_extractor import (
    UNIT_CONVERSIONS,
    normalize_unit,
    slugify,
    chunk_markdown
)


# Pydantic model for structured fact extraction
class ExtractedFact(BaseModel):
    """Pydantic model representing a single fact extracted from text"""
    name: str = Field(description="Descriptive name of the fact")
    type: str = Field(description="Type: 'quantity' or 'categorical'")
    value: str = Field(description="Value as text string")
    value_num: float = Field(default=0, description="Numeric value (0 if not applicable)")
    unit: str = Field(default="", description="Unit of measurement (empty string if none)")
    aliases: List[str] = Field(default_factory=list, description="Alternative names for this fact")
    evidence: str = Field(default="", description="Direct quote from text showing where fact was found")


# DSPy Signature using structured text output (easier for LLM than JSON)
class FactExtractionSignature(dspy.Signature):
    """Extract facts from ESIA text and output in structured text format.

    Think step by step:
    1. Read the text carefully
    2. Identify quantitative facts (numbers with units) and categorical facts (classifications)
    3. For each fact, output in this EXACT format (one fact per block, separated by ---)

    FORMAT FOR EACH FACT:
    FACT: [Short descriptive name]
    TYPE: [quantity or categorical]
    VALUE: [The value as text]
    VALUE_NUM: [Numeric value, 0 for categorical]
    UNIT: [Unit of measurement, empty for categorical]
    EVIDENCE: [Direct quote from text]
    ---

    Example output:
    FACT: Project area
    TYPE: quantity
    VALUE: 500
    VALUE_NUM: 500
    UNIT: hectares
    EVIDENCE: The project will cover an area of 500 hectares
    ---
    FACT: Location
    TYPE: categorical
    VALUE: Northern region
    VALUE_NUM: 0
    UNIT:
    EVIDENCE: located in the northern region
    ---
    """

    text: str = dspy.InputField(desc="Text chunk from ESIA document")
    output: str = dspy.OutputField(
        desc="Facts in structured text format. One fact per block. Separate blocks with ---"
    )


# DSPy Signature for fact categorization
class FactCategorizationSignature(dspy.Signature):
    """Intelligently categorize an ESIA fact into logical project section.

    Use domain knowledge to assign facts to appropriate categories and subcategories.
    For ambiguous facts, choose the most relevant category based on context."""

    fact_name: str = dspy.InputField(
        desc="Name/title of the extracted fact (e.g., 'Project area', 'Annual CO2 emissions')"
    )
    fact_value: str = dspy.InputField(
        desc="The value of the fact (e.g., '500', 'yes', 'coal-fired')"
    )
    fact_unit: str = dspy.InputField(
        desc="Unit of measurement if numeric (e.g., 'ha', 'MW', 'tonnes/yr'). Empty string for categorical."
    )

    category: Literal[
        "Project Overview",
        "Project Description",
        "Environmental Impacts",
        "Social Impacts",
        "Economic Impacts",
        "Health & Safety",
        "Governance & Management",
        "Risks & Issues"
    ] = dspy.OutputField(
        desc="Primary category for this fact"
    )

    subcategory: Literal[
        # Project Overview (2)
        "Basic Info", "Timeline",
        # Project Description (5)
        "Financing", "Capacity/Scale", "Technology", "Infrastructure", "Location",
        # Environmental Impacts (6)
        "Water", "Air", "Land", "Biodiversity", "Waste", "Emissions",
        # Social Impacts (4)
        "Employment", "Resettlement", "Community", "Cultural",
        # Economic Impacts (3)
        "Investment", "Revenue", "Local Procurement",
        # Health & Safety (3)
        "Occupational", "Public Health", "Emergency",
        # Governance & Management (3)
        "Institutional", "Monitoring", "Engagement",
        # Risks & Issues (3)
        "Identified Risks", "Uncertainties", "Conflicts"
    ] = dspy.OutputField(
        desc="Specific subcategory within the primary category"
    )

    confidence: Literal["high", "medium", "low"] = dspy.OutputField(
        desc="Confidence level in the categorization (high=clear fit, medium=reasonable fit, low=ambiguous)"
    )

    rationale: str = dspy.OutputField(
        desc="Brief explanation for the categorization decision (1 sentence)"
    )


@dataclass
class Fact:
    """Represents a single extracted fact"""
    name: str
    type: str  # 'quantity' or 'categorical'
    value: str
    value_num: float
    unit: str
    aliases: List[str]
    evidence: str
    page: int
    chunk_id: int
    signature: str = ""
    normalized_value: float = 0.0
    normalized_unit: str = ""
    # Conflict tracking
    occurrence_count: int = 1
    has_conflict: bool = False
    conflict_description: str = ""
    min_value: float = 0.0
    max_value: float = 0.0
    # Factsheet categorization
    category: Optional[str] = None
    subcategory: Optional[str] = None
    categorization_confidence: Optional[str] = None
    categorization_rationale: Optional[str] = None


class DocumentProcessor:
    """Handles PDF and DOCX to text conversion using Docling"""

    @staticmethod
    def extract_text_from_document(file_path: str) -> str:
        """
        Extract text from PDF or DOCX using Docling

        Args:
            file_path: Path to PDF or DOCX file

        Returns:
            Extracted text as markdown string
        """
        from docling.document_converter import DocumentConverter

        # Create converter
        converter = DocumentConverter()

        # Convert document
        result = converter.convert(file_path)

        # Export to markdown format
        markdown_text = result.document.export_to_markdown()

        return markdown_text


class FactExtractor(dspy.Module):
    """
    DSPy Module for extracting facts from documents.

    This module uses ChainOfThought reasoning to extract quantitative and categorical
    facts from ESIA document text. Output is in structured text format for reliable parsing.
    """

    def __init__(self):
        super().__init__()

        # Create the predictor with ChainOfThought reasoning
        self.extract = dspy.ChainOfThought(FactExtractionSignature)

        # Add few-shot examples
        self._add_examples()

    def _add_examples(self):
        """Add few-shot examples for in-context learning"""
        try:
            # Example 1: Quantitative facts
            example1_text = "The proposed mining project will cover an area of 500 hectares in the northern region. The total investment is estimated at $50 million. Annual coal production is expected to reach 2 million tonnes per year. The project manager is John Smith."

            example1_output = """FACT: Project area
TYPE: quantity
VALUE: 500
VALUE_NUM: 500
UNIT: hectares
EVIDENCE: The proposed mining project will cover an area of 500 hectares
---
FACT: Annual coal production
TYPE: quantity
VALUE: 2 million
VALUE_NUM: 2000000
UNIT: tonnes/year
EVIDENCE: Annual coal production is expected to reach 2 million tonnes per year
---
FACT: Total investment
TYPE: quantity
VALUE: 50 million
VALUE_NUM: 50000000
UNIT: $
EVIDENCE: The total investment is estimated at $50 million
---"""

            example1 = dspy.Example(
                text=example1_text,
                output=example1_output
            ).with_inputs("text")

            # Example 2: Mixed quantitative and categorical facts
            example2_text = "Water consumption is estimated at 150 cubic meters per day. The project will generate approximately 1000 jobs during construction and 300 permanent positions during operation. The proposed mining project is located in the northern region."

            example2_output = """FACT: Water consumption
TYPE: quantity
VALUE: 150
VALUE_NUM: 150
UNIT: m3/day
EVIDENCE: Water consumption is estimated at 150 cubic meters per day
---
FACT: Construction employment
TYPE: quantity
VALUE: 1000
VALUE_NUM: 1000
UNIT: jobs
EVIDENCE: The project will generate approximately 1000 jobs during construction
---
FACT: Permanent employment
TYPE: quantity
VALUE: 300
VALUE_NUM: 300
UNIT: jobs
EVIDENCE: 300 permanent positions during operation
---
FACT: Project location
TYPE: categorical
VALUE: Northern region
VALUE_NUM: 0
UNIT:
EVIDENCE: proposed mining project in the northern region
---"""

            example2 = dspy.Example(
                text=example2_text,
                output=example2_output
            ).with_inputs("text")

            # Add examples to the predictor for few-shot learning
            self.extract.demos = [example1, example2]
            print(f"Loaded 2 few-shot examples for fact extraction")

        except Exception as e:
            print(f"Warning: Could not add few-shot examples: {e}")

    def forward(self, text: str) -> dspy.Prediction:
        """
        Extract facts from a text chunk using ChainOfThought reasoning.

        Args:
            text: The text chunk to extract facts from

        Returns:
            A DSPy Prediction object with the output field containing structured text facts
        """
        prediction = self.extract(text=text)
        return prediction

    def _parse_structured_output(self, text_output: str) -> List[Dict[str, str]]:
        """
        Parse structured text format into fact dictionaries.

        Expected format:
        FACT: [name]
        TYPE: [type]
        VALUE: [value]
        VALUE_NUM: [number]
        UNIT: [unit]
        EVIDENCE: [quote]
        ---

        Returns:
            List of fact dictionaries
        """
        facts_list = []
        # Split by --- to separate fact blocks
        blocks = text_output.split('---')

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            fact_dict = {}
            lines = block.split('\n')

            for line in lines:
                line = line.strip()
                if ':' not in line:
                    continue

                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()

                if key == 'fact':
                    fact_dict['name'] = value
                elif key == 'type':
                    fact_dict['type'] = value.lower()
                elif key == 'value':
                    fact_dict['value'] = value
                elif key == 'value_num':
                    try:
                        fact_dict['value_num'] = float(value) if value else 0
                    except ValueError:
                        fact_dict['value_num'] = 0
                elif key == 'unit':
                    fact_dict['unit'] = value
                elif key == 'evidence':
                    fact_dict['evidence'] = value

            # Only add if we have minimum required fields
            if 'name' in fact_dict and 'type' in fact_dict:
                # Set defaults for optional fields
                fact_dict.setdefault('value', '')
                fact_dict.setdefault('value_num', 0)
                fact_dict.setdefault('unit', '')
                fact_dict.setdefault('evidence', '')
                fact_dict.setdefault('aliases', [])
                facts_list.append(fact_dict)

        return facts_list

    def extract_from_chunk(self, text: str, page: int, chunk_id: int) -> List[Fact]:
        """
        Extract facts from a single text chunk using structured text output

        Args:
            text: Text chunk
            page: Page number
            chunk_id: Chunk identifier

        Returns:
            List of extracted Fact objects
        """
        try:
            # Call DSPy - returns structured text
            result = self.forward(text=text)
            text_output = result.output

            # Check if empty or None
            if not text_output or text_output.strip() == "":
                return []

            # Parse structured text output
            facts_list = self._parse_structured_output(text_output)

            if not facts_list:
                return []

            # Convert to Fact objects
            facts = []
            for fact_dict in facts_list:
                try:
                    # Validate against Pydantic model
                    extracted_fact = ExtractedFact(**fact_dict)

                    # Create Fact object
                    fact = Fact(
                        name=extracted_fact.name,
                        type=extracted_fact.type,
                        value=extracted_fact.value,
                        value_num=extracted_fact.value_num,
                        unit=extracted_fact.unit,
                        aliases=extracted_fact.aliases,
                        evidence=extracted_fact.evidence,
                        page=page,
                        chunk_id=chunk_id
                    )

                    # Canonicalize
                    fact.signature = slugify(fact.name)

                    # Normalize units
                    fact.normalized_value, fact.normalized_unit = normalize_unit(
                        fact.value_num, fact.unit
                    )

                    facts.append(fact)
                except Exception as e:
                    print(f"Warning: Could not parse fact {fact_dict} in chunk {chunk_id}: {e}")
                    continue

            return facts

        except Exception as e:
            print(f"Error extracting facts from chunk {chunk_id}: {e}")
            import traceback
            traceback.print_exc()
            return []


class FactCategorizer(dspy.Module):
    """Uses LLM to categorize extracted facts into logical project sections.

    Implements few-shot learning with diverse examples to guide categorization
    across different ESIA fact types and project scenarios.

    Uses dspy.Predict for straightforward mapping task (not ChainOfThought).
    """

    def __init__(self):
        super().__init__()
        self.categorizer = dspy.Predict(FactCategorizationSignature)
        self._cache = {}  # Cache for previously categorized facts
        self._cache_hits = 0  # Track cache hit rate
        self._cache_misses = 0  # Track cache misses
        self._add_examples()

    def _add_examples(self):
        """Add diverse few-shot examples for better categorization.

        Examples span different project types and demonstrate confidence scoring.
        """
        examples = [
            # Example 1: Solar - Capacity (high confidence)
            dspy.Example(
                fact_name="Installed solar capacity",
                fact_value="500",
                fact_unit="MW",
                category="Project Description",
                subcategory="Capacity/Scale",
                confidence="high",
                rationale="Solar capacity is a core project descriptor."
            ),

            # Example 2: Mining - Direct employment (clear category)
            dspy.Example(
                fact_name="Direct permanent employment",
                fact_value="450",
                fact_unit="people",
                category="Social Impacts",
                subcategory="Employment",
                confidence="high",
                rationale="Employment figures are social impact indicators."
            ),

            # Example 3: Emissions (environmental impact)
            dspy.Example(
                fact_name="Annual CO2 emissions",
                fact_value="250000",
                fact_unit="tonnes/yr",
                category="Environmental Impacts",
                subcategory="Emissions",
                confidence="high",
                rationale="CO2 emissions directly measure environmental impact."
            ),

            # Example 4: Construction timeline (project description)
            dspy.Example(
                fact_name="Construction duration",
                fact_value="36",
                fact_unit="months",
                category="Project Description",
                subcategory="Timeline",
                confidence="high",
                rationale="Timeline is part of project description."
            ),

            # Example 5: Categorical fact (technology type)
            dspy.Example(
                fact_name="Technology type",
                fact_value="open-pit mining",
                fact_unit="",
                category="Project Description",
                subcategory="Technology",
                confidence="high",
                rationale="Mining method is core project technology descriptor."
            ),

            # Example 6: Ambiguous fact (medium confidence)
            dspy.Example(
                fact_name="Land affected",
                fact_value="1200",
                fact_unit="ha",
                category="Environmental Impacts",
                subcategory="Land",
                confidence="medium",
                rationale="Could be environmental or social; treating as environmental footprint."
            ),

            # Example 7: Cost/Economic (Investment category)
            dspy.Example(
                fact_name="Project capital cost",
                fact_value="1500",
                fact_unit="million USD",
                category="Economic Impacts",
                subcategory="Investment",
                confidence="high",
                rationale="Capital expenditure is primary economic indicator."
            ),

            # Example 8: Low confidence example (genuinely ambiguous)
            dspy.Example(
                fact_name="Community interaction meetings held",
                fact_value="25",
                fact_unit="events",
                category="Governance & Management",
                subcategory="Engagement",
                confidence="low",
                rationale="Could be social impacts or governance; unclear without more context."
            ),
        ]

        self.categorizer.demos = examples

    def forward(self, fact_name: str, fact_value: str, fact_unit: str = "") -> Dict[str, str]:
        """Categorize a single fact with caching support.

        Cache key uses fact name and unit (ignores value to allow value variations).
        This avoids redundant LLM calls for the same fact type across multiple occurrences.

        Args:
            fact_name: Name of the fact (e.g., "Annual CO2 emissions")
            fact_value: Value of the fact (e.g., "250000")
            fact_unit: Unit if applicable (e.g., "tonnes/yr"), empty string if categorical

        Returns:
            Dictionary with keys: category, subcategory, confidence, rationale
        """
        # Create cache key from fact name and unit (ignores value)
        cache_key = (fact_name.lower().strip(), fact_unit.lower().strip())

        # Check cache
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]

        # Cache miss - call LLM
        self._cache_misses += 1
        result = self.categorizer(
            fact_name=fact_name,
            fact_value=fact_value,
            fact_unit=fact_unit
        )

        categorization = {
            "category": result.category,
            "subcategory": result.subcategory,
            "confidence": result.confidence,
            "rationale": result.rationale
        }

        # Store in cache
        self._cache[cache_key] = categorization

        return categorization

    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache hit/miss statistics.

        Returns:
            Dictionary with hits, misses, and hit_rate
        """
        total = self._cache_hits + self._cache_misses
        hit_rate = self._cache_hits / total if total > 0 else 0.0

        return {
            "hits": self._cache_hits,
            "misses": self._cache_misses,
            "total": total,
            "hit_rate": hit_rate,
            "cache_size": len(self._cache)
        }


def cluster_facts(facts: List[Fact]) -> Dict[str, List[Fact]]:
    """Group facts by signature"""
    clusters = defaultdict(list)
    for fact in facts:
        clusters[fact.signature].append(fact)
    return dict(clusters)


def detect_conflicts(cluster: List[Fact], tolerance: float = 0.02) -> tuple[bool, str]:
    """
    Detect conflicts within a cluster of facts

    Args:
        cluster: List of facts with same signature
        tolerance: Relative difference threshold (default 2%)

    Returns:
        Tuple of (has_conflict, conflict_description)
    """
    if len(cluster) <= 1:
        return False, ""

    # Get normalized values
    values = [f.normalized_value for f in cluster if f.normalized_value > 0]

    if len(values) <= 1:
        return False, ""

    min_val = min(values)
    max_val = max(values)

    # Check for significant difference
    if min_val > 0:
        rel_diff = (max_val - min_val) / min_val
        if rel_diff > tolerance:
            # Check for order-of-magnitude errors
            ratio = max_val / min_val
            if 9 < ratio < 11 or 0.09 < ratio < 0.11:
                return True, f"Potential ×10 error: {min_val} vs {max_val}"
            else:
                return True, f"Conflicting values: {min_val} to {max_val} ({rel_diff*100:.1f}% diff)"

    return False, ""


def configure_llm():
    """
    Configure DSPy to use any supported LLM provider.

    Supports multiple providers:
    - ollama (local, free): Mistral, Qwen, etc.
    - openai (cloud): GPT-4, GPT-3.5-turbo
    - anthropic (cloud): Claude 3 variants
    - gemini (cloud): Google Gemini

    Configuration via .env file or environment variables.
    Default: ollama with mistral:latest
    """
    import os
    from pathlib import Path

    # Try to load .env file if it exists
    env_file = Path(__file__).parent.parent.parent / ".env"
    if env_file.exists():
        from dotenv import load_dotenv
        try:
            load_dotenv(env_file, verbose=False)
        except ImportError:
            # dotenv not installed, continue with os.getenv
            pass

    # Determine which provider to use
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    print(f"🤖 Configuring LLM:")
    print(f"   Provider: {provider}")

    # ========================================================================
    # OLLAMA (Local)
    # ========================================================================
    if provider == "ollama":
        model = os.getenv("OLLAMA_MODEL", "mistral:latest")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        temperature = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))
        max_tokens = int(os.getenv("OLLAMA_MAX_TOKENS", "2048"))

        print(f"   Model: {model}")
        print(f"   Base URL: {base_url}")
        print(f"   Temperature: {temperature}")
        print(f"   Max tokens: {max_tokens}")

        lm = dspy.OllamaLocal(
            model=model,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens
        )

    # ========================================================================
    # OPENAI (Cloud)
    # ========================================================================
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your-api-key-here":
            raise ValueError(
                "OPENAI_API_KEY not set in .env file. "
                "Get it from https://platform.openai.com/"
            )

        model = os.getenv("OPENAI_MODEL", "gpt-4")
        temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
        max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "2048"))

        print(f"   Model: {model}")
        print(f"   Temperature: {temperature}")
        print(f"   Max tokens: {max_tokens}")

        lm = dspy.OpenAI(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

    # ========================================================================
    # ANTHROPIC/CLAUDE (Cloud)
    # ========================================================================
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "your-api-key-here":
            raise ValueError(
                "ANTHROPIC_API_KEY not set in .env file. "
                "Get it from https://console.anthropic.com/"
            )

        model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
        temperature = float(os.getenv("ANTHROPIC_TEMPERATURE", "0.1"))
        max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", "2048"))

        print(f"   Model: {model}")
        print(f"   Temperature: {temperature}")
        print(f"   Max tokens: {max_tokens}")

        lm = dspy.Anthropic(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

    # ========================================================================
    # GOOGLE GEMINI (Cloud)
    # ========================================================================
    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your-api-key-here":
            raise ValueError(
                "GEMINI_API_KEY not set in .env file. "
                "Get it from https://ai.google.dev/"
            )

        model = os.getenv("GEMINI_MODEL", "gemini-pro")
        temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.1"))
        max_tokens = int(os.getenv("GEMINI_MAX_TOKENS", "2048"))

        print(f"   Model: {model}")
        print(f"   Temperature: {temperature}")
        print(f"   Max tokens: {max_tokens}")

        lm = dspy.Google(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

    # ========================================================================
    # UNKNOWN PROVIDER
    # ========================================================================
    else:
        raise ValueError(
            f"Unknown LLM provider: {provider}. "
            "Supported: ollama, openai, anthropic, gemini"
        )

    # Configure DSPy with the selected model
    dspy.configure(lm=lm)
    return lm


def process_document(
    file_path: str,
    progress_callback: Optional[Callable[[int, int, str], None]] = None
) -> Dict[str, Any]:
    """
    Process PDF or Markdown document and extract facts

    Args:
        file_path: Path to PDF or MD file
        progress_callback: Optional callback(current, total, status)

    Returns:
        Dictionary with extraction results
    """
    file_path = Path(file_path)

    # Configure LLM
    if progress_callback:
        progress_callback(0, 100, "Configuring LLM...")
    configure_llm()

    # Load document
    if progress_callback:
        progress_callback(5, 100, "Loading document...")

    if file_path.suffix.lower() in ['.pdf', '.docx']:
        # Use Docling for PDF and DOCX files
        text = DocumentProcessor.extract_text_from_document(str(file_path))

        # Save Docling output for inspection
        import os
        docling_output_dir = Path(__file__).parent.parent / 'backend' / 'docling_output'
        docling_output_dir.mkdir(parents=True, exist_ok=True)

        output_filename = f"{file_path.stem}_docling.md"
        output_path = docling_output_dir / output_filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"\n📄 Docling output saved to: {output_path}")
        print(f"   Characters extracted: {len(text):,}\n")
    else:
        # Fallback for markdown files
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

    # Chunk text
    if progress_callback:
        progress_callback(10, 100, "Chunking text...")
    chunks = chunk_markdown(text, max_chars=4000)
    total_chunks = len(chunks)

    # Extract facts
    if progress_callback:
        progress_callback(15, 100, f"Extracting facts from {total_chunks} chunks...")

    extractor = FactExtractor()
    all_facts = []

    for i, chunk in enumerate(chunks):
        try:
            facts = extractor.extract_from_chunk(chunk, page=i+1, chunk_id=i)
            all_facts.extend(facts)

            # Update progress (15% to 85% during extraction)
            progress = 15 + int((i + 1) / total_chunks * 70)
            if progress_callback:
                progress_callback(
                    progress,
                    100,
                    f"Processing chunk {i+1}/{total_chunks}..."
                )
        except Exception as e:
            print(f"Error processing chunk {i}: {e}")
            continue

    # Cluster facts
    if progress_callback:
        progress_callback(90, 100, "Clustering and detecting conflicts...")
    clusters = cluster_facts(all_facts)

    # Detect conflicts and add metadata
    consolidated_facts = []
    for signature, cluster in clusters.items():
        has_conflict, conflict_desc = detect_conflicts(cluster)
        normalized_values = [f.normalized_value for f in cluster if f.normalized_value > 0]

        # Take first fact as representative
        representative = cluster[0]
        representative.occurrence_count = len(cluster)
        representative.has_conflict = has_conflict
        representative.conflict_description = conflict_desc
        representative.min_value = min(normalized_values) if normalized_values else 0
        representative.max_value = max(normalized_values) if normalized_values else 0

        consolidated_facts.append(representative)

    # Categorize facts using LLM
    if progress_callback:
        progress_callback(95, 100, "Categorizing facts...")

    try:
        categorizer = FactCategorizer()
        categorized_facts = []
        failed_facts = []

        for fact in consolidated_facts:
            try:
                # Categorize using LLM (uses cache for similar facts)
                categorization = categorizer(
                    fact_name=fact.name,
                    fact_value=fact.value,
                    fact_unit=fact.unit
                )

                # Add categorization to fact object
                fact.category = categorization["category"]
                fact.subcategory = categorization["subcategory"]
                fact.categorization_confidence = categorization["confidence"]
                fact.categorization_rationale = categorization["rationale"]

                categorized_facts.append(fact)

            except Exception as fact_error:
                # Log failed fact but continue with others
                failed_facts.append({
                    "name": fact.name,
                    "error": str(fact_error)
                })
                # Add the fact without categorization
                categorized_facts.append(fact)

        # Print categorization summary
        cache_stats = categorizer.get_cache_stats()
        if cache_stats['total'] > 0:
            print(f"  Categorized {len(consolidated_facts)} facts")
            print(f"  Cache: {cache_stats['hits']}/{cache_stats['total']} hits ({cache_stats['hit_rate']*100:.1f}%)")

        if failed_facts:
            print(f"  Failed to categorize {len(failed_facts)} facts")

        consolidated_facts = categorized_facts

    except Exception as e:
        print(f"  Warning: Categorization failed: {e}")
        print(f"  Proceeding without categorization...")

    if progress_callback:
        progress_callback(100, 100, "Complete!")

    return {
        'all_facts': all_facts,
        'consolidated_facts': consolidated_facts,
        'clusters': clusters,
        'total_chunks': total_chunks,
        'stats': {
            'total_facts': len(all_facts),
            'unique_facts': len(clusters),
            'conflicts': sum(1 for f in consolidated_facts if f.has_conflict),
            'categorized': sum(1 for f in consolidated_facts if hasattr(f, 'category') and f.category)
        }
    }
