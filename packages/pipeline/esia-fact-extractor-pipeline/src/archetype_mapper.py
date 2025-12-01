#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archetype Mapper: Intelligently maps document sections to ESIA archetype domains.

This module provides advanced mapping between document section names and DSPy
signature domains using hierarchical archetype structures, fuzzy matching, and
confidence scoring.

Usage:
    mapper = ArchetypeMapper()
    matches = mapper.map_section("2.0 UPDATED PROJECT DESCRIPTION")
    # Returns: [{'domain': 'project_description', 'confidence': 0.95, ...}]
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher

sys.path.append(os.getcwd())


class ArchetypeMapper:
    """
    Maps document sections to archetype domains using hierarchical indexing
    and fuzzy matching with confidence scoring.
    """

    def __init__(self, archetype_dir: str = "./data/archetypes", router_config_path: str = "./data/router_config.json"):
        """
        Initialize the archetype mapper.

        Args:
            archetype_dir: Directory containing archetype JSON files
            router_config_path: Path to router configuration JSON file
        """
        self.archetype_dir = Path(archetype_dir)
        self.archetypes = {}
        self.subsection_index = {}
        self.domain_keywords = {}
        self.router_config = None
        self.router_entries = []
        self.router_index_by_id = {}
        self.router_index_by_keyword = {}
        self.router_index_by_domain = {}

        # Load all archetypes
        self._load_archetypes()
        self._build_subsection_index()
        self._build_keyword_index()

        # Load router configuration
        self.load_router_config(router_config_path)
        self._index_router_entries()

    def _load_archetypes(self):
        """Load all archetype JSON files from the archetype directory."""
        # Load core ESIA archetypes (original)
        core_esia_dir = self.archetype_dir / "core_esia"
        if core_esia_dir.exists():
            for json_file in core_esia_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        archetype = json.load(f)
                        # Key by the first domain in the file
                        domain_key = list(archetype.keys())[0] if archetype else None
                        if domain_key:
                            self.archetypes[domain_key] = archetype[domain_key]
                except Exception as e:
                    print(f"Warning: Could not load {json_file}: {e}")

        # Load IFC Performance Standards archetypes
        ifc_ps_dir = self.archetype_dir / "core_ifc_performance_standards"
        if ifc_ps_dir.exists():
            for json_file in ifc_ps_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        archetype = json.load(f)
                        ps_code = archetype.get("standard", json_file.stem)
                        self.archetypes[ps_code] = archetype
                except Exception as e:
                    print(f"Warning: Could not load {json_file}: {e}")

        # Load project-specific extensions
        ext_dir = self.archetype_dir / "project_specific_esia"
        if ext_dir.exists():
            for json_file in ext_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        extension = json.load(f)
                        sector = extension.get("sector", json_file.stem)
                        self.archetypes[sector] = extension
                except Exception as e:
                    print(f"Warning: Could not load {json_file}: {e}")

    def _build_subsection_index(self):
        """
        Build a searchable index of all subsections from all archetypes.

        Extracts subsections/categories and creates keyword index for each.
        """
        for domain, archetype in self.archetypes.items():
            # Handle different archetype structures
            if isinstance(archetype, dict):
                # Core ESIA structure: domain -> {subsection -> [fields]}
                for subsection_key, subsection_data in archetype.items():
                    if isinstance(subsection_data, (list, dict)):
                        # Create index entry
                        keywords = self._extract_keywords(subsection_key)
                        self.subsection_index[subsection_key] = {
                            'domain': domain,
                            'archetype': domain,
                            'keywords': keywords,
                            'fields': subsection_data if isinstance(subsection_data, list) else list(subsection_data.keys())
                        }

                # Handle specialized_fields structure (extensions)
                if 'specialized_fields' in archetype:
                    for field_category, field_list in archetype['specialized_fields'].items():
                        keywords = self._extract_keywords(field_category)
                        index_key = f"{domain}_{field_category}"
                        self.subsection_index[index_key] = {
                            'domain': domain,
                            'archetype': domain,
                            'keywords': keywords,
                            'fields': field_list if isinstance(field_list, list) else []
                        }

    def _build_keyword_index(self):
        """
        Build an index mapping keywords to domains for quick lookup.
        """
        keyword_mapping = {
            # IFC Performance Standards
            'assessment': ['ps1', 'assessment_and_management'],
            'management': ['ps1', 'ps3', 'environmental_and_social_management_plan_esmp'],
            'labor': ['ps2', 'labor_and_working_conditions'],
            'working': ['ps2', 'labor_and_working_conditions'],
            'conditions': ['ps2', 'ps4', 'baseline_conditions'],
            'resource': ['ps3', 'resource_efficiency'],
            'efficiency': ['ps3', 'resource_efficiency'],
            'pollution': ['ps3', 'resource_efficiency'],
            'prevention': ['ps3', 'resource_efficiency'],
            'community': ['ps4', 'public_consultation_and_disclosure'],
            'health': ['ps4', 'baseline_conditions'],
            'safety': ['ps4', 'baseline_conditions'],
            'security': ['ps4', 'public_consultation_and_disclosure'],
            'land': ['ps5', 'project_description', 'baseline_conditions'],
            'acquisition': ['ps5', 'project_description'],
            'resettlement': ['ps5', 'project_description'],
            'biodiversity': ['ps6', 'baseline_conditions'],
            'conservation': ['ps6', 'baseline_conditions'],
            'ecosystem': ['ps6', 'baseline_conditions'],
            'indigenous': ['ps7', 'public_consultation_and_disclosure'],
            'peoples': ['ps7', 'public_consultation_and_disclosure'],
            'cultural': ['ps8', 'baseline_conditions'],
            'heritage': ['ps8', 'baseline_conditions'],
            'archaeology': ['ps8', 'baseline_conditions'],

            # Core ESIA domains
            'executive': ['executive_summary'],
            'summary': ['executive_summary'],
            'introduction': ['introduction'],
            'project': ['project_description'],
            'description': ['project_description'],
            'baseline': ['baseline_conditions'],
            'environmental': ['environmental_and_social_impact_assessment'],
            'social': ['environmental_and_social_impact_assessment'],
            'impact': ['environmental_and_social_impact_assessment'],
            'mitigation': ['mitigation_and_enhancement_measures'],
            'enhancement': ['mitigation_and_enhancement_measures'],
            'measures': ['mitigation_and_enhancement_measures'],
            'esms': ['environmental_and_social_management_plan_esmp'],
            'stakeholder': ['public_consultation_and_disclosure'],
            'engagement': ['public_consultation_and_disclosure'],
            'consultation': ['public_consultation_and_disclosure'],
            'disclosure': ['public_consultation_and_disclosure'],
            'conclusion': ['conclusion_and_recommendations'],
            'recommendations': ['conclusion_and_recommendations'],
            'reference': ['references'],
            'annex': ['annexes'],

            # Sector-specific keywords
            'solar': ['energy_solar'],
            'photovoltaic': ['energy_solar'],
            'pv': ['energy_solar'],
            'panel': ['energy_solar'],
            'hydro': ['energy_hydro'],
            'hydropower': ['energy_hydro'],
            'dam': ['energy_hydro'],
            'reservoir': ['energy_hydro'],
            'coal': ['energy_coal'],
            'thermal': ['energy_coal'],
            'nuclear': ['energy_nuclear'],
            'radiological': ['energy_nuclear'],
            'spent': ['energy_nuclear'],
            'fuel': ['energy_nuclear'],
            'floating': ['energy_floating_solar'],
            'transmission': ['energy_transmission'],
            'distribution': ['energy_transmission'],
            'line': ['energy_transmission'],
            'grid': ['energy_transmission'],
            'wind': ['energy_wind_solar'],
            'turbine': ['energy_wind_solar'],
            'geothermal': ['energy_geothermal'],
            'oil': ['energy_oil_gas'],
            'gas': ['energy_oil_gas'],
            'road': ['infrastructure_roads'],
            'highway': ['infrastructure_roads'],
            'airport': ['infrastructure_airports'],
            'aviation': ['infrastructure_airports'],
            'port': ['infrastructure_ports'],
            'maritime': ['infrastructure_ports'],
            'water': ['infrastructure_water'],
            'treatment': ['infrastructure_water'],
            'wastewater': ['infrastructure_water'],
            'crop': ['agriculture_crops'],
            'agriculture': ['agriculture_crops', 'agriculture_animal_production', 'agriculture_forestry'],
            'animal': ['agriculture_animal_production'],
            'livestock': ['agriculture_animal_production'],
            'forestry': ['agriculture_forestry'],
            'timber': ['agriculture_forestry'],
            'forest': ['agriculture_forestry'],
            'manufacturing': ['manufacturing_general'],
            'chemical': ['manufacturing_chemicals'],
            'pharmaceutical': ['manufacturing_pharmaceuticals'],
            'pharma': ['manufacturing_pharmaceuticals'],
            'textile': ['manufacturing_textiles'],
            'apparel': ['manufacturing_textiles'],
            'commercial': ['real_estate_commercial'],
            'building': ['real_estate_commercial'],
            'hotel': ['real_estate_hospitality'],
            'hospitality': ['real_estate_hospitality'],
            'resort': ['real_estate_hospitality'],
            'healthcare': ['real_estate_healthcare'],
            'hospital': ['real_estate_healthcare'],
            'clinic': ['real_estate_healthcare'],
            'banking': ['financial_banking'],
            'bank': ['financial_banking'],
            'finance': ['financial_banking'],
            'microfinance': ['financial_microfinance'],
            'mining': ['mining_extension'],
            'mine': ['mining_extension'],
            'nickel': ['mining_nickel_extension'],
            'industrial': ['industrial_extension'],
            'alumina': ['industrial_alumina_extension'],

            # Gender-related keywords (14 new)
            'gbvh': ['environmental_and_social_impact_assessment', 'ps2', 'ps4'],
            'seah': ['environmental_and_social_impact_assessment', 'ps2', 'ps4'],
            'gender-based violence': ['environmental_and_social_impact_assessment', 'ps2', 'ps4'],
            'sexual harassment': ['environmental_and_social_impact_assessment', 'ps2', 'ps4'],
            'sexual exploitation': ['environmental_and_social_impact_assessment', 'ps2', 'ps4'],
            'sexual abuse': ['environmental_and_social_impact_assessment', 'ps2', 'ps4'],
            'violence against women': ['environmental_and_social_impact_assessment', 'ps2', 'ps4'],
            'intimate partner violence': ['environmental_and_social_impact_assessment', 'ps2', 'ps4'],
            'gap': ['mitigation_and_enhancement_measures', 'ps2'],
            'gender action plan': ['mitigation_and_enhancement_measures', 'ps2'],
            'women participation': ['baseline_conditions', 'ps2'],
            'gender equality': ['baseline_conditions', 'ps2'],
            'equitable access': ['ps2', 'ps4'],
            'women empowerment': ['mitigation_and_enhancement_measures', 'ps2'],

            # Indigenous Peoples keywords (6 new)
            'fpic': ['ps7', 'public_consultation_and_disclosure'],
            'free prior informed consent': ['ps7', 'public_consultation_and_disclosure'],
            'good faith negotiation': ['ps7', 'public_consultation_and_disclosure'],
            'gfn': ['ps7', 'public_consultation_and_disclosure'],
            'indigenous consent': ['ps7', 'public_consultation_and_disclosure'],
            'collective attachment': ['ps7', 'baseline_conditions'],

            # Financial Intermediary keywords (8 new)
            'financial intermediary': ['financial_banking', 'environmental_and_social_management_plan_esmp'],
            'esr 9': ['financial_banking', 'environmental_and_social_management_plan_esmp'],
            'ps fi': ['financial_banking', 'environmental_and_social_management_plan_esmp'],
            'sub-project': ['financial_banking', 'environmental_and_social_management_plan_esmp'],
            'exclusion list': ['financial_banking', 'environmental_and_social_management_plan_esmp'],
            'referral list': ['financial_banking', 'environmental_and_social_management_plan_esmp'],
            'category a sub-project': ['financial_banking', 'environmental_and_social_management_plan_esmp'],
            'fi esms': ['financial_banking', 'environmental_and_social_management_plan_esmp'],

            # ESMS keywords (5 new)
            'nine elements': ['environmental_and_social_management_plan_esmp', 'ps1'],
            'esms policy': ['environmental_and_social_management_plan_esmp', 'ps1'],
            'management system': ['environmental_and_social_management_plan_esmp', 'ps1'],
            'organizational capacity': ['environmental_and_social_management_plan_esmp', 'ps1'],
            'continual improvement': ['environmental_and_social_management_plan_esmp', 'ps1'],

            # Environmental Flow keywords (8 new)
            'eflow': ['energy_hydro', 'environmental_and_social_impact_assessment', 'ps6'],
            'environmental flow': ['energy_hydro', 'mitigation_and_enhancement_measures', 'ps6'],
            'downstream flow': ['energy_hydro', 'environmental_and_social_impact_assessment', 'ps6'],
            'high-resolution methods': ['energy_hydro', 'environmental_and_social_impact_assessment'],
            'transboundary basin': ['energy_hydro', 'environmental_and_social_impact_assessment'],
            'cascade': ['energy_hydro', 'project_description'],
            'rehabilitation': ['mitigation_and_enhancement_measures', 'decommissioning'],
            'expansion scope': ['project_description'],

            # Concentrated Solar Power keywords (8 new)
            'csp': ['energy_solar', 'project_description'],
            'concentrated solar power': ['energy_solar', 'project_description'],
            'heat transfer fluid': ['energy_solar', 'project_description', 'ps3'],
            'htf': ['energy_solar', 'project_description', 'ps3'],
            'thermal oil': ['energy_solar', 'project_description', 'ps3'],
            'molten salt': ['energy_solar', 'project_description', 'ps3'],
            'heliostat': ['energy_solar', 'project_description'],
            'parabolic trough': ['energy_solar', 'project_description'],
            'power tower': ['energy_solar', 'project_description'],

            # Digitalization keywords (8 new)
            'digitalization': ['environmental_and_social_impact_assessment', 'project_description'],
            'cybersecurity': ['environmental_and_social_impact_assessment', 'project_description'],
            'data protection': ['environmental_and_social_impact_assessment', 'ps1'],
            'data privacy': ['environmental_and_social_impact_assessment', 'ps1'],
            'personal data': ['environmental_and_social_impact_assessment', 'ps1'],
            'digital services': ['project_description'],
            'gdpr': ['environmental_and_social_impact_assessment', 'ps1'],
            'data breach': ['environmental_and_social_impact_assessment', 'ps1'],

            # GRM keywords (4 new)
            'culturally appropriate grm': ['public_consultation_and_disclosure', 'ps7'],
            'customary dispute resolution': ['public_consultation_and_disclosure', 'ps7'],
            'traditional processes': ['public_consultation_and_disclosure', 'ps7'],
            'grm accessibility': ['public_consultation_and_disclosure', 'ps1'],
        }

        self.domain_keywords = keyword_mapping

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text by splitting on spaces, underscores, hyphens.

        Args:
            text: Text to extract keywords from

        Returns:
            List of lowercase keywords
        """
        import re
        # Split on spaces, underscores, hyphens, and camelCase boundaries
        words = re.split(r'[\s_\-]+|(?<=[a-z])(?=[A-Z])', text.lower())
        return [w for w in words if w and len(w) > 2]

    def load_router_config(self, config_path: str = "./data/router_config.json"):
        """
        Load JSON router configuration file.

        Args:
            config_path: Path to router configuration JSON file
        """
        import logging

        router_path = Path(config_path)
        if not router_path.exists():
            print(f"Warning: Router config not found at {config_path}, router features disabled")
            return

        try:
            with open(router_path, 'r', encoding='utf-8') as f:
                self.router_config = json.load(f)

            # Parse and store router entries
            self.router_entries = self.router_config.get('router_entries', [])

            # Also add sector-specific entries
            for sector, entries in self.router_config.get('sector_specific_routing', {}).items():
                self.router_entries.extend(entries)

            # Add cross-cutting theme entries
            for theme, entries in self.router_config.get('cross_cutting_themes', {}).items():
                self.router_entries.extend(entries)

            print(f"Router config loaded: {len(self.router_entries)} routing entries")

        except Exception as e:
            print(f"Warning: Could not load router config {config_path}: {e}")
            self.router_config = None
            self.router_entries = []

    def _index_router_entries(self):
        """
        Build searchable indices from router entries for fast lookup.
        """
        if not self.router_entries:
            return

        # Index by section_id (exact match)
        for entry in self.router_entries:
            section_id = entry.get('section_id', '')
            if section_id:
                if section_id not in self.router_index_by_id:
                    self.router_index_by_id[section_id] = []
                self.router_index_by_id[section_id].append(entry)

        # Index by keywords (for keyword matching)
        for entry in self.router_entries:
            for keyword in entry.get('keywords', []):
                keyword_lower = keyword.lower()
                if keyword_lower not in self.router_index_by_keyword:
                    self.router_index_by_keyword[keyword_lower] = []
                self.router_index_by_keyword[keyword_lower].append(entry)

        # Index by target_domains (reverse lookup)
        for entry in self.router_entries:
            for domain in entry.get('target_domains', []):
                if domain not in self.router_index_by_domain:
                    self.router_index_by_domain[domain] = []
                self.router_index_by_domain[domain].append(entry)

        print(f"Router indices built: {len(self.router_index_by_id)} section IDs, "
              f"{len(self.router_index_by_keyword)} keywords, "
              f"{len(self.router_index_by_domain)} domains")

    def _extract_section_id(self, section_name: str) -> Optional[str]:
        """
        Extract section ID pattern from section name using regex.

        Args:
            section_name: Section name to parse

        Returns:
            Section ID (e.g., "1.3.4", "5.2.1", "A.2.1.5") or None if not found
        """
        import re

        # Pattern: matches X.X.X or X.X format (with optional leading/trailing text)
        patterns = [
            r'^([A-Z]\.\d+\.\d+(?:\.\d+)?)\b',  # Matches A.2.1.5 or D.5.2.7 at start
            r'\b(\d+\.\d+\.\d+(?:\.\d+)?)\b',  # Matches 1.3.4 or 1.3.4.1
            r'^(\d+\.\d+)\b',  # Matches leading 5.2 or 6.1
        ]

        for pattern in patterns:
            match = re.search(pattern, section_name)
            if match:
                return match.group(1)

        return None

    def _boost_confidence_by_priority(self, confidence: float, priority: str) -> float:
        """
        Apply priority boost to confidence score.

        Args:
            confidence: Base confidence score
            priority: Priority level ("critical", "high", "medium")

        Returns:
            Boosted confidence score
        """
        priority_boost = {
            'critical': 0.2,
            'high': 0.1,
            'medium': 0.0
        }

        boost = priority_boost.get(priority.lower(), 0.0)
        return min(1.0, confidence + boost)

    def map_section_with_router(
        self,
        section_name: str,
        project_type: Optional[str] = None,
        top_n: int = 5
    ) -> List[Dict]:
        """
        Map a document section to archetype domains using router config integration.

        Enhanced routing with:
        - Step 1: Section ID exact match
        - Step 2: Router keyword matching
        - Step 3: Sector-specific routing
        - Step 4: Cross-cutting theme boosting
        - Step 5: Fall back to fuzzy matching
        - Step 6: Deduplicate and sort by confidence

        Args:
            section_name: The document section name to map
            project_type: Optional project type (e.g., "energy_hydro", "energy_solar")
            top_n: Return top N matches (ordered by confidence)

        Returns:
            List of dicts with keys: domain, confidence, source, subsection, keywords
        """
        matches = []
        section_lower = section_name.lower()

        # Step 1: Try section ID exact match
        section_id = self._extract_section_id(section_name)
        if section_id and section_id in self.router_index_by_id:
            for entry in self.router_index_by_id[section_id]:
                for domain in entry.get('target_domains', []):
                    confidence = 0.95  # High confidence for exact ID match
                    confidence = self._boost_confidence_by_priority(
                        confidence,
                        entry.get('priority', 'medium')
                    )
                    matches.append({
                        'domain': domain,
                        'confidence': round(confidence, 3),
                        'source': 'router_id_match',
                        'subsection': entry.get('title', section_id),
                        'keywords': entry.get('keywords', []),
                        'matching_keywords': [section_id]
                    })

        # Step 2: Try router keyword matching
        section_keywords = self._extract_keywords(section_name)
        for keyword in section_keywords:
            if keyword in self.router_index_by_keyword:
                for entry in self.router_index_by_keyword[keyword]:
                    # Calculate keyword match score
                    entry_keywords = [k.lower() for k in entry.get('keywords', [])]
                    matching_count = len(set(section_keywords) & set(entry_keywords))
                    total_count = len(entry_keywords)

                    keyword_score = matching_count / total_count if total_count > 0 else 0.5
                    confidence = 0.7 + (keyword_score * 0.2)  # Base 0.7, up to 0.9

                    confidence = self._boost_confidence_by_priority(
                        confidence,
                        entry.get('priority', 'medium')
                    )

                    for domain in entry.get('target_domains', []):
                        matches.append({
                            'domain': domain,
                            'confidence': round(confidence, 3),
                            'source': 'router_keyword_match',
                            'subsection': entry.get('title', domain),
                            'keywords': entry_keywords,
                            'matching_keywords': list(set(section_keywords) & set(entry_keywords))
                        })

        # Step 3: Apply sector-specific routing (if project_type provided)
        if project_type and self.router_config:
            sector_key = project_type.replace('energy_', '')  # "energy_hydro" -> "hydropower"
            sector_mapping = {
                'hydro': 'hydropower',
                'solar': 'solar',
                'coal': 'coal',
                'wind_solar': 'wind',
                'floating_solar': 'solar',
            }
            sector = sector_mapping.get(sector_key, sector_key)

            sector_entries = self.router_config.get('sector_specific_routing', {}).get(sector, [])
            for entry in sector_entries:
                # Check if keywords match
                entry_keywords = [k.lower() for k in entry.get('keywords', [])]
                matching_keywords = list(set(section_keywords) & set(entry_keywords))

                if matching_keywords:
                    confidence = 0.75 + (len(matching_keywords) / len(entry_keywords) * 0.15)
                    confidence = self._boost_confidence_by_priority(
                        confidence,
                        entry.get('priority', 'medium')
                    )

                    for domain in entry.get('target_domains', []):
                        matches.append({
                            'domain': domain,
                            'confidence': round(confidence, 3),
                            'source': 'router_sector_specific',
                            'subsection': entry.get('title', domain),
                            'keywords': entry_keywords,
                            'matching_keywords': matching_keywords
                        })

        # Step 4: Apply cross-cutting theme boosting
        if self.router_config:
            for theme, entries in self.router_config.get('cross_cutting_themes', {}).items():
                for entry in entries:
                    entry_keywords = [k.lower() for k in entry.get('keywords', [])]
                    matching_keywords = list(set(section_keywords) & set(entry_keywords))

                    if matching_keywords:
                        confidence = 0.8 + (len(matching_keywords) / len(entry_keywords) * 0.15)
                        confidence = self._boost_confidence_by_priority(
                            confidence,
                            entry.get('priority', 'medium')
                        )

                        for domain in entry.get('target_domains', []):
                            matches.append({
                                'domain': domain,
                                'confidence': round(confidence, 3),
                                'source': f'router_theme_{theme}',
                                'subsection': entry.get('title', domain),
                                'keywords': entry_keywords,
                                'matching_keywords': matching_keywords
                            })

        # Step 5: Fall back to existing fuzzy matching if no router matches
        if not matches:
            fuzzy_matches = self.map_section(section_name, top_n=top_n * 2)
            for match in fuzzy_matches:
                match['source'] = 'fuzzy_fallback'
                matches.append(match)

        # Step 6: Deduplicate matches by domain (keep highest confidence)
        seen_domains = {}
        for match in matches:
            domain = match['domain']
            if domain not in seen_domains or match['confidence'] > seen_domains[domain]['confidence']:
                seen_domains[domain] = match

        # Step 7: Sort by confidence and return top_n
        unique_matches = list(seen_domains.values())
        unique_matches = sorted(unique_matches, key=lambda x: x['confidence'], reverse=True)

        return unique_matches[:top_n]

    def map_section(self, section_name: str, top_n: int = 5) -> List[Dict]:
        """
        Map a document section to archetype domains using fuzzy matching.

        Args:
            section_name: The document section name to map
            top_n: Return top N matches (ordered by confidence)

        Returns:
            List of dicts with keys: domain, confidence, subsection, keywords
        """
        matches = []
        section_keywords = self._extract_keywords(section_name)
        section_lower = section_name.lower()

        # Try to find matches in the subsection index
        for subsection_key, metadata in self.subsection_index.items():
            # Calculate fuzzy match score using sequence matcher
            ratio = SequenceMatcher(None, section_lower, subsection_key.lower()).ratio()

            # Calculate keyword overlap score
            keyword_score = 0.0
            if section_keywords and metadata['keywords']:
                matching_keywords = len(set(section_keywords) & set(metadata['keywords']))
                total_keywords = max(len(section_keywords), len(metadata['keywords']))
                keyword_score = matching_keywords / total_keywords if total_keywords > 0 else 0.0

            # Combined confidence score (60% fuzzy, 40% keyword)
            confidence = (ratio * 0.6) + (keyword_score * 0.4)

            if confidence > 0.3:  # Minimum threshold
                matches.append({
                    'domain': metadata['domain'],
                    'subsection': subsection_key,
                    'confidence': round(confidence, 3),
                    'keywords': metadata['keywords'],
                    'matching_keywords': list(set(section_keywords) & set(metadata['keywords']))
                })

        # Also check domain keywords directly
        for keyword, domains in self.domain_keywords.items():
            if keyword in section_lower:
                for domain in domains:
                    # Check if this domain already in matches, if so increase confidence
                    existing = [m for m in matches if m['domain'] == domain]
                    if existing:
                        existing[0]['confidence'] = min(1.0, existing[0]['confidence'] + 0.1)
                    else:
                        matches.append({
                            'domain': domain,
                            'subsection': domain,
                            'confidence': 0.65,
                            'keywords': [keyword],
                            'matching_keywords': [keyword]
                        })

        # Sort by confidence (highest first)
        matches = sorted(matches, key=lambda x: x['confidence'], reverse=True)

        # Remove duplicates (keep highest confidence for each domain)
        seen_domains = set()
        unique_matches = []
        for match in matches:
            if match['domain'] not in seen_domains:
                seen_domains.add(match['domain'])
                unique_matches.append(match)

        return unique_matches[:top_n]

    def get_domain_info(self, domain: str) -> Optional[Dict]:
        """
        Get detailed information about a domain/archetype.

        Args:
            domain: Domain identifier

        Returns:
            Dictionary with archetype information, or None if not found
        """
        return self.archetypes.get(domain, None)

    def get_all_domains(self) -> List[str]:
        """
        Get list of all available domains.

        Returns:
            List of domain identifiers
        """
        return list(self.archetypes.keys())

    def get_statistics(self) -> Dict:
        """
        Get statistics about loaded archetypes.

        Returns:
            Dictionary with statistics
        """
        return {
            'total_archetypes': len(self.archetypes),
            'total_subsections': len(self.subsection_index),
            'total_domains_keywords': len(self.domain_keywords),
            'domain_list': self.get_all_domains()
        }

    def should_process_section(self, section_name: str) -> bool:
        """
        Check if a section should be processed (skip low-value sections).

        Args:
            section_name: Section name to check

        Returns:
            True if section should be processed, False otherwise
        """
        skip_keywords = {
            "acronym",
            "glossary",
            "abbreviation",
            "table of contents",
            "references",
            "appendix",
            "step 1",
            "step 2",
            "step 3",
            "step 4",
            "step 5",
            "step 6",
        }

        section_lower = section_name.lower()

        # Skip if contains skip keywords
        for keyword in skip_keywords:
            if keyword in section_lower:
                return False

        # Skip if just a short name (usually 1-3 words, no special characters)
        if len(section_name.split()) <= 3 and not any(c.isdigit() for c in section_name):
            # But allow known sections
            if section_name not in self.archetypes:
                return False

        return True


def test_mapper():
    """Test the archetype mapper with known document sections."""
    print("=" * 70)
    print("ARCHETYPE MAPPER - TESTING (WITH ROUTER INTEGRATION)")
    print("=" * 70)
    print()

    mapper = ArchetypeMapper()

    # Print statistics
    stats = mapper.get_statistics()
    print(f"Total Archetypes Loaded: {stats['total_archetypes']}")
    print(f"Total Subsections Indexed: {stats['total_subsections']}")
    print(f"Router Entries Loaded: {len(mapper.router_entries)}")
    print()

    # Test sections from actual ESIA document
    test_sections = [
        ("5.3.4 GBVH and SEAH Risk Assessment", None),
        ("4.3.7 Gender Baseline", None),
        ("7.1.4 FPIC Process and Documentation", None),
        ("A.2.1.5 Hydropower Turbine Fish Mortality", "energy_hydro"),
        ("D.5.2.7 Solar Glint and Glare Impact Assessment", "energy_solar"),
        ("6.4.1 FI Sub-Project Screening and Categorization", None),
        ("5.2 Baseline Conditions", None),
        ("Executive Summary", None),
        ("1.3.4 ESMS Organizational Structure", None),
    ]

    print("Testing Router-Enhanced Section Mapping:")
    print("-" * 70)

    for section, project_type in test_sections:
        print(f"\nSection: {section}")
        if project_type:
            print(f"  Project Type: {project_type}")

        # Check if should process
        should_process = mapper.should_process_section(section)
        print(f"  Should Process: {should_process}")

        if should_process:
            # Get mappings with router
            matches = mapper.map_section_with_router(section, project_type=project_type, top_n=3)
            print(f"  Matches: {len(matches)}")

            for i, match in enumerate(matches, 1):
                print(f"    [{i}] {match['domain']} (confidence: {match['confidence']}, source: {match.get('source', 'unknown')})")
                if match.get('matching_keywords'):
                    print(f"        Keywords: {', '.join(match['matching_keywords'][:5])}")

    print("\n" + "=" * 70)
    print("COMPARING ROUTER VS FUZZY MATCHING")
    print("=" * 70)

    comparison_sections = [
        "5.3.4 Gender-Based Violence and Harassment",
        "7.2.4 Culturally Appropriate Grievance Mechanism",
    ]

    for section in comparison_sections:
        print(f"\nSection: {section}")
        print("  Router-based:")
        router_matches = mapper.map_section_with_router(section, top_n=2)
        for match in router_matches:
            print(f"    - {match['domain']} (conf: {match['confidence']}, source: {match.get('source')})")

        print("  Fuzzy-based:")
        fuzzy_matches = mapper.map_section(section, top_n=2)
        for match in fuzzy_matches:
            print(f"    - {match['domain']} (conf: {match['confidence']})")


if __name__ == "__main__":
    test_mapper()
