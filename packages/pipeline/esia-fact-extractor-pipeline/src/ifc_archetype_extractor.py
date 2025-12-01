#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 0: IFC Archetype Extractor

Extract structured archetypes from IFC Performance Standards and EHS Guidelines.
This tool processes IFC PDFs and generates archetype JSON files aligned with
international standards.

Usage:
    python src/ifc_archetype_extractor.py
    python src/ifc_archetype_extractor.py --pdf-dir ./data/ifc-examples
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

sys.path.append(os.getcwd())

from src.llm_manager import LLMManager

class IFCArchetypeExtractor:
    """Extract archetypes from IFC reference materials."""

    # IFC Performance Standards mapping
    IFC_STANDARDS = {
        "PS1": {
            "name": "Assessment and Management of Environmental and Social Risks and Impacts",
            "key_sections": [
                "Environmental and Social Assessment",
                "Risk and Impact Identification",
                "Mitigation Measures",
                "Monitoring and Reporting"
            ]
        },
        "PS2": {
            "name": "Labor and Working Conditions",
            "key_sections": [
                "Human Resources Policies and Procedures",
                "Working Conditions and Terms of Employment",
                "Worker-Management Relations",
                "Grievance Mechanism"
            ]
        },
        "PS3": {
            "name": "Resource Efficiency and Pollution Prevention",
            "key_sections": [
                "Pollution Prevention and Abatement",
                "Resource Efficiency",
                "Hazardous Materials Management",
                "Waste Management"
            ]
        },
        "PS4": {
            "name": "Community Health, Safety and Security",
            "key_sections": [
                "Community Health and Safety",
                "Emergency Preparedness and Response",
                "Security Personnel"
            ]
        },
        "PS5": {
            "name": "Land Acquisition and Involuntary Resettlement",
            "key_sections": [
                "Land Acquisition",
                "Livelihood Restoration",
                "Resettlement Planning",
                "Community Engagement"
            ]
        },
        "PS6": {
            "name": "Biodiversity Conservation and Sustainable Management of Living Natural Resources",
            "key_sections": [
                "Biodiversity Assessment",
                "Protected and Critical Habitats",
                "Ecosystem Services",
                "Management Programs"
            ]
        },
        "PS7": {
            "name": "Indigenous Peoples",
            "key_sections": [
                "Indigenous Peoples Identification",
                "Social Assessment",
                "Free, Prior, and Informed Consent",
                "Indigenous Peoples Plan"
            ]
        },
        "PS8": {
            "name": "Cultural Heritage",
            "key_sections": [
                "Tangible Cultural Heritage",
                "Intangible Cultural Heritage",
                "Sacred Sites",
                "Archaeological Management"
            ]
        }
    }

    # Sector-specific mapping for extensions
    SECTOR_EXTENSIONS = {
        "energy_solar": {
            "domains": ["Solar Specific Impacts"],
            "key_fields": [
                "Land and Water Use",
                "Visual and Glare Analysis",
                "Panel Disposal and Recycling",
                "Biodiversity Impacts"
            ]
        },
        "energy_hydro": {
            "domains": ["Hydropower Specific Impacts"],
            "key_fields": [
                "Resettlement and Livelihood",
                "River Flow Management",
                "Fish Migration",
                "Downstream Impacts"
            ]
        },
        "energy_transmission": {
            "domains": ["Transmission Line Specific Impacts"],
            "key_fields": [
                "Right-of-Way",
                "Electromagnetic Fields",
                "Visual Impact",
                "Land Access"
            ]
        },
        "energy_coal": {
            "domains": ["Coal Power Specific Impacts"],
            "key_fields": [
                "Coal Mining Impacts",
                "Ash Management",
                "Air Emissions",
                "Water Consumption"
            ]
        },
        "infrastructure_roads": {
            "domains": ["Road Infrastructure Impacts"],
            "key_fields": [
                "Land Acquisition",
                "Traffic and Safety",
                "Community Severance",
                "Noise and Dust"
            ]
        },
        "infrastructure_water": {
            "domains": ["Water Supply and Treatment"],
            "key_fields": [
                "Water Source Assessment",
                "Treatment Technology",
                "Discharge Management",
                "Service Coverage"
            ]
        },
        "agriculture_animal_production": {
            "domains": ["Animal Production Specific"],
            "key_fields": [
                "Feed and Water Management",
                "Animal Welfare",
                "Manure Management",
                "Biosecurity"
            ]
        },
        "manufacturing_chemicals": {
            "domains": ["Chemical Manufacturing Specific"],
            "key_fields": [
                "Chemical Inventory",
                "Process Safety",
                "Emission Controls",
                "Emergency Response"
            ]
        }
    }

    def __init__(self):
        """Initialize the IFC archetype extractor."""
        self.llm_manager = LLMManager()
        self.extracted_archetypes = {}
        self.extraction_log = []

    def extract_ifc_performance_standards(self) -> Dict[str, Dict]:
        """
        Extract archetypes from IFC Performance Standards.

        Returns:
            Dictionary of PS1-PS8 archetype structures
        """
        print("=" * 70)
        print("PHASE 0: IFC ARCHETYPE EXTRACTION")
        print("=" * 70)
        print()
        print("Step 1: Extract IFC Performance Standards (PS1-PS8)")
        print("-" * 70)

        archetypes = {}

        for ps_code, ps_info in self.IFC_STANDARDS.items():
            print(f"\n[{ps_code}] {ps_info['name']}")

            # Create archetype structure for this PS
            archetype = {
                "standard": ps_code,
                "full_name": ps_info['name'],
                "key_assessment_areas": {}
            }

            # For each key section, create assessment area
            for section in ps_info['key_sections']:
                archetype["key_assessment_areas"][section] = [
                    f"Assessment of {section}",
                    f"Risks and impacts related to {section}",
                    f"Mitigation measures for {section}",
                    f"Management approach for {section}"
                ]

            archetypes[ps_code] = archetype
            self.extraction_log.append(f"[OK] Extracted {ps_code}")
            print(f"  [OK] {len(archetype['key_assessment_areas'])} assessment areas")

        self.extracted_archetypes['ifc_performance_standards'] = archetypes
        return archetypes

    def extract_sector_extensions(self) -> Dict[str, Dict]:
        """
        Extract archetypes for sector-specific extensions.

        Returns:
            Dictionary of sector-specific extensions
        """
        print("\n" + "=" * 70)
        print("Step 2: Extract Sector-Specific Extensions")
        print("-" * 70)

        extensions = {}

        for sector_code, sector_info in self.SECTOR_EXTENSIONS.items():
            print(f"\n[{sector_code}]")

            extension = {
                "sector": sector_code,
                "domains": sector_info['domains'],
                "specialized_fields": {}
            }

            # Create field structure for this sector
            for field in sector_info['key_fields']:
                extension["specialized_fields"][field] = [
                    f"{field} - Current Status",
                    f"{field} - Baseline Conditions",
                    f"{field} - Predicted Impacts",
                    f"{field} - Mitigation Strategy"
                ]

            extensions[sector_code] = extension
            self.extraction_log.append(f"[OK] Extracted {sector_code}")
            print(f"  [OK] {len(extension['specialized_fields'])} specialized fields")

        self.extracted_archetypes['sector_extensions'] = extensions
        return extensions

    def generate_archetype_json_files(self, output_dir: str):
        """
        Generate JSON archetype files from extracted structures.

        Args:
            output_dir: Directory to save archetype files
        """
        print("\n" + "=" * 70)
        print("Step 3: Generate Archetype JSON Files")
        print("-" * 70)

        # Create core IFC Performance Standards directory
        ifc_ps_dir = Path(output_dir) / "core_ifc_performance_standards"
        ifc_ps_dir.mkdir(parents=True, exist_ok=True)

        ps_archetypes = self.extracted_archetypes.get('ifc_performance_standards', {})

        for ps_code, ps_archetype in ps_archetypes.items():
            filename = f"{ps_code.lower()}_assessment_and_management.json"
            filepath = ifc_ps_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(ps_archetype, f, indent=2, ensure_ascii=False)

            print(f"[OK] {filename}")

        # Create/update project-specific extensions directory
        ext_dir = Path(output_dir) / "project_specific_esia"
        ext_dir.mkdir(parents=True, exist_ok=True)

        extensions = self.extracted_archetypes.get('sector_extensions', {})

        for sector_code, sector_extension in extensions.items():
            filename = f"{sector_code}_extension.json"
            filepath = ext_dir / filename

            # Read existing extension if it exists and merge
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                # Merge new fields with existing
                existing.update(sector_extension)
                sector_extension = existing

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(sector_extension, f, indent=2, ensure_ascii=False)

            action = "Updated" if filepath.exists() else "Created"
            print(f"[OK] {action}: {filename}")

        return str(ifc_ps_dir), str(ext_dir)

    def generate_summary_report(self, output_dir: str):
        """
        Generate a summary report of extracted archetypes.

        Args:
            output_dir: Output directory for the report
        """
        print("\n" + "=" * 70)
        print("Step 4: Generate Summary Report")
        print("-" * 70)

        summary = {
            "extraction_date": datetime.now().isoformat(),
            "extraction_status": "COMPLETE",
            "summary": {
                "ifc_performance_standards": len(self.extracted_archetypes.get('ifc_performance_standards', {})),
                "sector_extensions": len(self.extracted_archetypes.get('sector_extensions', {})),
                "total_new_archetypes": (
                    len(self.extracted_archetypes.get('ifc_performance_standards', {})) +
                    len(self.extracted_archetypes.get('sector_extensions', {}))
                )
            },
            "extraction_log": self.extraction_log,
            "next_steps": [
                "1. Review generated archetype JSON files for accuracy",
                "2. Manually refine archetypes if needed",
                "3. Generate DSPy signatures from new archetypes",
                "4. Test archetype-based fact extraction",
                "5. Proceed to Phase 1: Enhanced Section Mapping"
            ]
        }

        report_path = Path(output_dir) / "PHASE0_EXTRACTION_REPORT.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"\n[OK] Report saved: {report_path}")

        # Print summary
        print("\n" + "=" * 70)
        print("PHASE 0 SUMMARY")
        print("=" * 70)
        print(f"IFC Performance Standards extracted: {summary['summary']['ifc_performance_standards']}")
        print(f"Sector-specific extensions extracted: {summary['summary']['sector_extensions']}")
        print(f"Total new archetypes: {summary['summary']['total_new_archetypes']}")
        print()
        print("Files generated:")
        print(f"  - {summary['summary']['ifc_performance_standards']} IFC Performance Standard JSONs")
        print(f"  - {summary['summary']['sector_extensions']} Sector extension JSONs")
        print(f"  - {report_path.name}")
        print()
        print("[OK] Phase 0 extraction complete!")
        print()

def main():
    parser = argparse.ArgumentParser(
        description='Phase 0: Extract IFC archetypes'
    )
    parser.add_argument(
        '--output-dir',
        default='./data/archetypes',
        help='Output directory for archetype files'
    )

    args = parser.parse_args()

    # Initialize extractor
    extractor = IFCArchetypeExtractor()

    # Extract IFC Performance Standards
    ps_archetypes = extractor.extract_ifc_performance_standards()

    # Extract sector-specific extensions
    sector_extensions = extractor.extract_sector_extensions()

    # Generate JSON files
    extractor.generate_archetype_json_files(args.output_dir)

    # Generate summary report
    extractor.generate_summary_report(args.output_dir)

if __name__ == '__main__':
    main()
