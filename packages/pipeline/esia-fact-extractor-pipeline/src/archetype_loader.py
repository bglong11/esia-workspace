#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archetype Loader: Dynamically loads and composes archetypes based on project type.

This module provides functionality to load appropriate archetypes based on detected
project type and project-specific parameters. It supports composition of core ESIA
archetypes, IFC Performance Standards, and project-specific extensions.

Usage:
    loader = ArchetypeLoader()
    archetypes = loader.load_for_project("energy_solar")
    # Returns combined archetype with all relevant fields
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from src.archetype_mapper import ArchetypeMapper
from src.project_type_classifier import ProjectTypeClassifier


class ArchetypeLoader:
    """
    Loads and composes archetypes based on project type classification.

    Supports composition of:
    1. Core ESIA archetypes (12 fundamental sections)
    2. IFC Performance Standards (8 standards covering E&S risks)
    3. Project-specific extensions (31 sector-specific archetypes)
    """

    def __init__(self, archetype_dir: str = "./data/archetypes"):
        """
        Initialize the archetype loader.

        Args:
            archetype_dir: Directory containing archetype JSON files
        """
        self.archetype_dir = Path(archetype_dir)
        self.mapper = ArchetypeMapper(archetype_dir)
        self.classifier = ProjectTypeClassifier()
        self._loaded_archetypes = {}

    def load_for_project(
        self,
        project_type: str,
        include_ifc_standards: bool = True,
        include_core_esia: bool = True
    ) -> Dict[str, Any]:
        """
        Load appropriate archetypes for a given project type.

        Composes:
        - Core ESIA archetypes (always included if requested)
        - IFC Performance Standards (always included if requested)
        - Project-specific extension for the detected type

        Args:
            project_type: Project type from ProjectTypeClassifier (e.g., "energy_solar")
            include_ifc_standards: Include all 8 IFC PS archetypes
            include_core_esia: Include all 12 core ESIA archetypes

        Returns:
            Dict with composed archetype structure containing all relevant domains
        """
        composed = {
            "project_type": project_type,
            "domains": {}
        }

        # Load core ESIA archetypes
        if include_core_esia:
            core_esia = self._load_core_esia()
            composed["domains"].update(core_esia)

        # Load IFC Performance Standards
        if include_ifc_standards:
            ifc_standards = self._load_ifc_standards()
            composed["domains"].update(ifc_standards)

        # Load project-specific extension
        project_specific = self._load_project_specific(project_type)
        if project_specific:
            composed["domains"].update(project_specific)

        return composed

    def load_from_chunks(
        self,
        chunks: List[Dict],
        include_ifc_standards: bool = True,
        include_core_esia: bool = True
    ) -> Dict[str, Any]:
        """
        Load archetypes by first classifying the document from chunks.

        Args:
            chunks: List of document chunks with 'text' and 'section' fields
            include_ifc_standards: Include all 8 IFC PS archetypes
            include_core_esia: Include all 12 core ESIA archetypes

        Returns:
            Dict with composed archetype structure
        """
        # Classify the document
        classification = self.classifier.classify(chunks)

        # Load appropriate archetypes
        return self.load_for_project(
            classification.project_type,
            include_ifc_standards=include_ifc_standards,
            include_core_esia=include_core_esia
        )

    def _load_core_esia(self) -> Dict[str, Any]:
        """
        Load all 12 core ESIA archetypes.

        Returns:
            Dict mapping domain names to their fields
        """
        core_dir = self.archetype_dir / "core_esia"
        domains = {}

        if core_dir.exists():
            for json_file in sorted(core_dir.glob("*.json")):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        archetype = json.load(f)
                        # Merge domain into composed structure
                        domains.update(archetype)
                except Exception as e:
                    print(f"Warning: Failed to load {json_file}: {e}")

        return domains

    def _load_ifc_standards(self) -> Dict[str, Any]:
        """
        Load all 8 IFC Performance Standards archetypes.

        Returns:
            Dict mapping standard names to their fields
        """
        ifc_dir = self.archetype_dir / "core_ifc_performance_standards"
        domains = {}

        if ifc_dir.exists():
            for json_file in sorted(ifc_dir.glob("*.json")):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        archetype = json.load(f)
                        # Merge domain into composed structure
                        domains.update(archetype)
                except Exception as e:
                    print(f"Warning: Failed to load {json_file}: {e}")

        return domains

    def _load_project_specific(self, project_type: str) -> Optional[Dict[str, Any]]:
        """
        Load project-specific extension archetype for given project type.

        Args:
            project_type: Project type identifier (e.g., "energy_solar")

        Returns:
            Dict with project-specific domains, or None if not found
        """
        project_specific_dir = self.archetype_dir / "project_specific_esia"

        # Build expected filename from project type
        # Format: "{sector}_{subtype}.json" from archetype files
        filename_pattern = f"{project_type.lower()}.json"

        if project_specific_dir.exists():
            # Try exact match first
            filepath = project_specific_dir / filename_pattern
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as e:
                    print(f"Warning: Failed to load {filepath}: {e}")

            # Try to find file containing the project type
            for json_file in project_specific_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        archetype = json.load(f)
                        # Check if this archetype matches the project type
                        if archetype.get("project_type") == project_type or \
                           project_type in str(json_file).lower():
                            return archetype
                except Exception as e:
                    pass

        # Return None if project-specific archetype not found
        return None

    def get_available_project_types(self) -> List[str]:
        """
        Get list of all available project types.

        Returns:
            List of project type identifiers
        """
        project_types = []
        project_specific_dir = self.archetype_dir / "project_specific_esia"

        if project_specific_dir.exists():
            for json_file in project_specific_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        archetype = json.load(f)
                        if "project_type" in archetype:
                            project_types.append(archetype["project_type"])
                except Exception:
                    pass

        return sorted(project_types)

    def get_loaded_archetypes(self, project_type: str) -> Dict[str, int]:
        """
        Get statistics about loaded archetypes for a project type.

        Returns:
            Dict with counts of loaded domains and subsections
        """
        archetypes = self.load_for_project(project_type)
        domains = archetypes.get("domains", {})

        return {
            "project_type": project_type,
            "total_domains": len(domains),
            "core_esia_count": len(self._load_core_esia()),
            "ifc_standards_count": len(self._load_ifc_standards()),
            "project_specific_count": len(self._load_project_specific(project_type) or {}),
            "all_domains": list(domains.keys())
        }


if __name__ == "__main__":
    # Test the loader
    loader = ArchetypeLoader()

    # Load for solar project
    print("=" * 60)
    print("ARCHETYPE LOADER TEST")
    print("=" * 60)

    project_type = "energy_solar"
    stats = loader.get_loaded_archetypes(project_type)

    print(f"\nProject Type: {stats['project_type']}")
    print(f"Total Domains: {stats['total_domains']}")
    print(f"Core ESIA: {stats['core_esia_count']}")
    print(f"IFC Standards: {stats['ifc_standards_count']}")
    print(f"Project-Specific: {stats['project_specific_count']}")

    print(f"\nAvailable Domains:")
    for domain in stats['all_domains'][:10]:
        print(f"  - {domain}")
    if len(stats['all_domains']) > 10:
        print(f"  ... and {len(stats['all_domains']) - 10} more")
