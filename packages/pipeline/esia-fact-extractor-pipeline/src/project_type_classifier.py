"""
Project Type Classifier for ESIA Document Pipeline

Automatically detects project types from ESIA document chunks using keyword-based classification.
Supports 32 project types across energy, infrastructure, agriculture, manufacturing, mining, and more.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import re
from collections import defaultdict


@dataclass
class ClassificationResult:
    """Result of project type classification"""
    project_type: str
    confidence: float
    keywords_matched: List[str]
    sector: str
    evidence: str
    alternatives: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "project_type": self.project_type,
            "confidence": self.confidence,
            "keywords_matched": self.keywords_matched,
            "sector": self.sector,
            "evidence": self.evidence,
            "alternatives": self.alternatives
        }


class ProjectTypeClassifier:
    """
    Classifies ESIA documents by project type using keyword matching.

    Supports 32 project types across 8 major sectors:
    - Energy (solar, hydro, wind, coal, nuclear, geothermal, oil/gas, transmission, floating solar, pumped storage)
    - Infrastructure (roads, airports, ports, water, general)
    - Agriculture (crops, animal production, forestry)
    - Manufacturing (general, chemicals, pharmaceuticals, textiles)
    - Real Estate (commercial, hospitality, healthcare)
    - Financial (banking, microfinance)
    - Mining (general, nickel)
    - Industrial (general, alumina)
    """

    def __init__(self):
        """Initialize classifier with comprehensive keyword database"""
        self.project_types = self._build_keyword_database()
        self.sector_mapping = self._build_sector_mapping()

    def _build_keyword_database(self) -> Dict[str, Dict]:
        """
        Build comprehensive keyword database for all 32+ project types.
        Returns dict mapping project_type -> {keywords: [...], sector: str}
        """
        return {
            # Energy Sector
            "energy_solar": {
                "keywords": ["solar", "photovoltaic", "pv", "panel", "pvs", "solar farm", "solar plant", "solar ipp"],
                "sector": "Energy"
            },
            "energy_hydro": {
                "keywords": ["hydro", "hydropower", "dam", "reservoir", "water power", "run-of-river"],
                "sector": "Energy"
            },
            "energy_wind": {
                "keywords": ["wind", "turbine", "windmill", "anemometer", "wind farm"],
                "sector": "Energy"
            },
            "energy_coal": {
                "keywords": ["coal", "thermal", "coal power", "coal plant", "coal-fired"],
                "sector": "Energy"
            },
            "energy_nuclear": {
                "keywords": ["nuclear", "radiological", "spent fuel", "reactor", "nuclear power"],
                "sector": "Energy"
            },
            "energy_geothermal": {
                "keywords": ["geothermal", "thermal energy", "hot spring", "heat pump"],
                "sector": "Energy"
            },
            "energy_oil_gas": {
                "keywords": ["oil", "gas", "petroleum", "refinery", "pipeline", "lng", "natural gas"],
                "sector": "Energy"
            },
            "energy_transmission": {
                "keywords": ["transmission", "distribution", "power line", "grid", "substation", "transformer"],
                "sector": "Energy"
            },
            "energy_floating_solar": {
                "keywords": ["floating", "floating solar", "floating pv", "water-based", "pond", "reservoir solar"],
                "sector": "Energy"
            },
            "energy_pumped_storage": {
                "keywords": ["pumped storage", "pumped hydro", "energy storage", "pump-back", "pspp"],
                "sector": "Energy"
            },

            # Infrastructure Sector
            "infrastructure_roads": {
                "keywords": ["road", "highway", "motorway", "expressway", "bridge", "tunnel", "pavement"],
                "sector": "Infrastructure"
            },
            "infrastructure_airports": {
                "keywords": ["airport", "airfield", "runway", "aviation", "flight", "terminal", "hangar"],
                "sector": "Infrastructure"
            },
            "infrastructure_ports": {
                "keywords": ["port", "harbor", "marina", "terminal", "dock", "maritime", "shipping"],
                "sector": "Infrastructure"
            },
            "infrastructure_water": {
                "keywords": ["water supply", "treatment plant", "wastewater", "sewage", "drinking water"],
                "sector": "Infrastructure"
            },
            "infrastructure_general": {
                "keywords": ["infrastructure", "public works", "utility"],
                "sector": "Infrastructure"
            },

            # Agriculture Sector
            "agriculture_crops": {
                "keywords": ["crop", "agriculture", "plantation", "farm", "cultivated", "farming"],
                "sector": "Agriculture"
            },
            "agriculture_animal_production": {
                "keywords": ["animal", "livestock", "cattle", "poultry", "dairy", "meat"],
                "sector": "Agriculture"
            },
            "agriculture_forestry": {
                "keywords": ["forestry", "timber", "forest", "logging", "tree", "wood"],
                "sector": "Agriculture"
            },

            # Manufacturing Sector
            "manufacturing_general": {
                "keywords": ["manufacturing", "factory", "production facility", "plant"],
                "sector": "Manufacturing"
            },
            "manufacturing_chemicals": {
                "keywords": ["chemical", "chemistry", "petrochemical", "refining"],
                "sector": "Manufacturing"
            },
            "manufacturing_pharmaceuticals": {
                "keywords": ["pharmaceutical", "pharma", "drug", "medicine", "medicinal"],
                "sector": "Manufacturing"
            },
            "manufacturing_textiles": {
                "keywords": ["textile", "apparel", "clothing", "fabric", "weaving"],
                "sector": "Manufacturing"
            },

            # Real Estate Sector
            "real_estate_commercial": {
                "keywords": ["commercial", "office", "retail", "shopping", "mall"],
                "sector": "Real Estate"
            },
            "real_estate_hospitality": {
                "keywords": ["hotel", "hospitality", "resort", "tourism", "accommodation"],
                "sector": "Real Estate"
            },
            "real_estate_healthcare": {
                "keywords": ["healthcare", "hospital", "clinic", "medical", "health facility"],
                "sector": "Real Estate"
            },

            # Financial Sector
            "financial_banking": {
                "keywords": ["banking", "bank", "finance", "financial institution"],
                "sector": "Financial"
            },
            "financial_microfinance": {
                "keywords": ["microfinance", "microcredit", "financial services"],
                "sector": "Financial"
            },

            # Mining Sector
            "mining_general": {
                "keywords": ["mining", "mine", "mineral", "extraction", "quarry"],
                "sector": "Mining"
            },
            "mining_nickel": {
                "keywords": ["nickel", "nickel mine", "nickel extraction"],
                "sector": "Mining"
            },

            # Industrial Sector
            "industrial_general": {
                "keywords": ["industrial", "industry", "heavy industry"],
                "sector": "Industrial"
            },
            "industrial_alumina": {
                "keywords": ["alumina", "aluminum", "bauxite", "smelter"],
                "sector": "Industrial"
            }
        }

    def _build_sector_mapping(self) -> Dict[str, str]:
        """Map project types to sectors"""
        mapping = {}
        for project_type, info in self.project_types.items():
            mapping[project_type] = info["sector"]
        return mapping

    def classify(self, chunks: List[Dict]) -> ClassificationResult:
        """
        Classify document by scanning chunks for project type keywords.

        Args:
            chunks: List of document chunks with 'text' and 'section' fields

        Returns:
            ClassificationResult with project type, confidence, and evidence
        """
        # Combine title and introduction sections for better classification
        priority_sections = ["title", "executive", "introduction", "project description"]
        combined_text = ""

        for chunk in chunks[:10]:  # Scan first 10 chunks (usually intro/title)
            section = chunk.get("section", "").lower()
            text = chunk.get("text", "")

            # Weight early sections more heavily
            if any(p in section for p in priority_sections):
                combined_text = text + " " + combined_text
            else:
                combined_text += " " + text

        # Count keyword matches for each project type
        scores = self._calculate_scores(combined_text)

        if not scores:
            return ClassificationResult(
                project_type="unknown",
                confidence=0.0,
                keywords_matched=[],
                sector="Unknown",
                evidence="No project type keywords found in document",
                alternatives=[]
            )

        # Sort by confidence
        sorted_scores = sorted(scores.items(), key=lambda x: x[1]["confidence"], reverse=True)
        top_result = sorted_scores[0]

        return ClassificationResult(
            project_type=top_result[0],
            confidence=top_result[1]["confidence"],
            keywords_matched=top_result[1]["keywords_matched"],
            sector=self.sector_mapping[top_result[0]],
            evidence=top_result[1]["evidence"],
            alternatives=[{
                "project_type": result[0],
                "confidence": result[1]["confidence"],
                "evidence": result[1]["evidence"]
            } for result in sorted_scores[1:4]]  # Top 3 alternatives
        )

    def _calculate_scores(self, text: str) -> Dict[str, Dict]:
        """
        Calculate confidence scores for each project type based on keyword matches.

        Args:
            text: Combined document text to analyze

        Returns:
            Dict mapping project_type -> {confidence, keywords_matched, evidence}
        """
        text_lower = text.lower()
        scores = {}

        for project_type, info in self.project_types.items():
            matched_keywords = []

            for keyword in info["keywords"]:
                # Case-insensitive search
                if keyword.lower() in text_lower:
                    matched_keywords.append(keyword)

            if matched_keywords:
                # Calculate confidence based on keyword matches
                # More keywords = higher confidence, max 1.0
                confidence = min(len(matched_keywords) / 3.0, 1.0)

                scores[project_type] = {
                    "confidence": confidence,
                    "keywords_matched": matched_keywords,
                    "evidence": f"Found {len(matched_keywords)} keywords: {', '.join(matched_keywords[:3])}"
                    + (f" (+{len(matched_keywords)-3} more)" if len(matched_keywords) > 3 else "")
                }

        return scores

    def classify_from_file(self, jsonl_path: str) -> ClassificationResult:
        """
        Classify document from chunks JSONL file.

        Args:
            jsonl_path: Path to chunks JSONL file

        Returns:
            ClassificationResult with project type and confidence
        """
        import json

        chunks = []
        with open(jsonl_path, 'r') as f:
            for line in f:
                chunks.append(json.loads(line))

        return self.classify(chunks)
