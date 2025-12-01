"""
Section Mapper: Maps document section names to DSPy signature domains.

This module provides intelligent mapping between actual document section names
(which vary by document) and the standardized domain names used by DSPy signatures.
"""

import re
from typing import Optional, Dict


class SectionMapper:
    """Maps document sections to DSPy signature domains."""

    # Mapping from actual section names to DSPy signature domains
    SECTION_MAPPING = {
        # Executive & Introduction
        "Executive Summary": "ExecutiveSummary",
        "ENVIRONMENTAL AND SOCIAL IMPACT ASSESSMENT FOR THE PROJECT": "EnvironmentalAndSocialImpactAssessment",
        "1.0 INTRODUCTION AND BACKGROUND": "Introduction",
        "1.1 Project Overview and Purpose of Supplementary ESIA": "ProjectDescription",
        "1.2 Project Proponent": "ProjectDescription",
        "Introduction": "Introduction",

        # Project Description
        "2.0 UPDATED PROJECT DESCRIPTION AND AREA OF INFLUENCE": "ProjectDescription",
        "2.1 Project Components": "ProjectDescription",
        "2.2 Delineation of Area of Influence": "ProjectDescription",
        "Project Components": "ProjectDescription",
        "ASSOCIATED FACILITIES": "ProjectDescription",
        "Table 2.1 Project Components and Associated Facilities": "ProjectDescription",
        "Primary Project Site": "ProjectDescription",
        "Area of Direct Influence": "ProjectDescription",
        "Road Corridor (Dili-Laleia)": "ProjectDescription",

        # Alternatives & Site Selection
        "3.0 ENHANCED ALTERNATIVES ANALYSIS AND SITE SELECTION JUSTIFICATION": "ProjectDescription",
        "3.1'No Project' Scenario": "ProjectDescription",
        "3.2 Expanded Rationale for Site Selection": "ProjectDescription",
        "TABLE 3.1 UPDATED SITE COMPARISON": "ProjectDescription",

        # Baseline Conditions & Socioeconomic
        "4.0 SOCIOECONOMIC BASELINE AND COMMUNITY PROFILING FOR LALEIA ADMINISTRATIVE POST": "BaselineConditions",
        "4.1 Administrative Boundaries": "BaselineConditions",
        "4.2 Population and Demographics": "BaselineConditions",
        "4.3 Livelihoods and Employment": "BaselineConditions",
        "4.4 Settlement Patterns and Housing": "BaselineConditions",
        "4.5 Education": "BaselineConditions",
        "4.6 Health and Healthcare Access": "BaselineConditions",
        "4.7 Water, Sanitation, and Hygiene (WASH)": "BaselineConditions",
        "4.9 Vulnerable Groups": "BaselineConditions",
        "4.10 Land Tenure and Use": "BaselineConditions",
        "4.11 Social Organization and Governance": "BaselineConditions",
        "4.12 Religion and Cultural Practices": "BaselineConditions",
        "4.13 Community Safety and Security": "BaselineConditions",
        "4.14 Gender Roles and Social Inclusion": "BaselineConditions",
        "4.15 Natural Resource Use and Ecosystem Services": "BaselineConditions",
        "4.16 Previous and Ongoing Development Initiatives": "BaselineConditions",
        "4.17 Migration and Mobility": "BaselineConditions",
        "Data Source: 2022 census data": "BaselineConditions",

        # Environmental Baseline
        "Land Cover and Use": "BaselineConditions",
        "Hydrology": "BaselineConditions",
        "Coastal Area": "BaselineConditions",
        "Ecosystems": "BaselineConditions",
        "Wildfire Risks": "BaselineConditions",

        # Indigenous Peoples
        "5.0 INDIGENOUS PEOPLES ASSESSMENT": "BaselineConditions",

        # Risk Assessment
        "7.0 PROJECT RISK ASSESSMENT": "EnvironmentalAndSocialImpactAssessment",
        "7.1 Technical Risks": "EnvironmentalAndSocialImpactAssessment",
        "7.2 Environmental Risks": "EnvironmentalAndSocialImpactAssessment",
        "7.3 Human Rights Risks": "EnvironmentalAndSocialImpactAssessment",
        "7.5 Cultural Heritage": "EnvironmentalAndSocialImpactAssessment",

        # Impacts & Benefits
        "Economic Benefits": "EnvironmentalAndSocialImpactAssessment",
        "Environmental and Social Benefits": "EnvironmentalAndSocialImpactAssessment",
        "Energy Security and Reliability": "EnvironmentalAndSocialImpactAssessment",
        "Construction Phase Impacts (Duration: approximately 24 Months)": "EnvironmentalAndSocialImpactAssessment",
        "Operational Phase Impacts and Benefits (Duration: 25 Years)": "EnvironmentalAndSocialImpactAssessment",
        "Decommissioning Phase": "EnvironmentalAndSocialImpactAssessment",
        "Improved Energy": "EnvironmentalAndSocialImpactAssessment",

        # Management Plans & Mitigation
        "8.0 SUPPLEMENTARY IMPACT ASSESSMENT AND MANAGEMENT PLANS": "MitigationAndEnhancementMeasures",
        "8.1 Access to Natural Resources and Livelihood Impacts": "MitigationAndEnhancementMeasures",
        "8.2 Surface Water Management Plan": "MitigationAndEnhancementMeasures",
        "8.3 Dust Management Plan": "MitigationAndEnhancementMeasures",
        "8.4 Traffic Management Plan": "MitigationAndEnhancementMeasures",
        "8.5 Solid Waste Management Framework": "MitigationAndEnhancementMeasures",
        "8.7Archaeological 'Chance Find' Procedure": "MitigationAndEnhancementMeasures",
        "8.8 Security Management Plan": "MitigationAndEnhancementMeasures",

        # Environmental & Social Management System
        "9.0 ENVIRONMENTAL AND SOCIAL MANAGEMENT SYSTEM": "EnvironmentalAndSocialManagementPlanEsmp",
        "9.2 Labor and Working Conditions": "EnvironmentalAndSocialManagementPlanEsmp",
        "9.3 Contractor Oversight and Compliance Plan": "EnvironmentalAndSocialManagementPlanEsmp",
        "9.4 Institutional Arrangements": "EnvironmentalAndSocialManagementPlanEsmp",
        "Capacity Building and Continuous Improvement": "EnvironmentalAndSocialManagementPlanEsmp",
        "Organizational Structure and Responsibilities": "EnvironmentalAndSocialManagementPlanEsmp",
        "Scope of the Operational ESMS": "EnvironmentalAndSocialManagementPlanEsmp",
        "Stakeholder Engagement and Reporting": "EnvironmentalAndSocialManagementPlanEsmp",
        "Construction Phase (EPC Contractor Responsibility)": "EnvironmentalAndSocialManagementPlanEsmp",
        "Operation Phase (Owner Responsibility)": "EnvironmentalAndSocialManagementPlanEsmp",
        "Supply Chain and Ethical Sourcing": "EnvironmentalAndSocialManagementPlanEsmp",
        "Diversity and Inclusion": "EnvironmentalAndSocialManagementPlanEsmp",

        # Stakeholder Engagement
        "10.0 STAKEHOLDER ENGAGEMENT": "PublicConsultationAndDisclosure",
        "Stakeholder Identification and Analysis": "PublicConsultationAndDisclosure",
        "Vulnerable Groups": "PublicConsultationAndDisclosure",
        "Past Engagement Activities": "PublicConsultationAndDisclosure",
        "Community Engagement During Construction Phase": "PublicConsultationAndDisclosure",
        "Prior to Construction Start": "PublicConsultationAndDisclosure",
        "During Construction": "PublicConsultationAndDisclosure",
        "Community Engagement During Operation Phase": "PublicConsultationAndDisclosure",
        "Opening and Symbolic Events": "PublicConsultationAndDisclosure",
        "Ongoing Communication and Grievance Redress Mechanism": "PublicConsultationAndDisclosure",
        "Local Employment Opportunities": "PublicConsultationAndDisclosure",
        "Community Awareness": "PublicConsultationAndDisclosure",
        "Local Employment and Business Opportunities during Construction": "PublicConsultationAndDisclosure",
        "Shallow Well Feasibility and Livestock Watering Initiative": "PublicConsultationAndDisclosure",
        "Tamarind Tree Compensation and Sustainable Wood Utilization": "PublicConsultationAndDisclosure",
        "Enhanced Beach Access for Fishing and Community Activities": "PublicConsultationAndDisclosure",
        "Renewable Energy Education Center and Local Tourism Promotion": "PublicConsultationAndDisclosure",
        "Targeted Support for Women's Needs and Economic Empowerment": "PublicConsultationAndDisclosure",

        # Other sections with descriptive content
        "Social Infrastructure": "BaselineConditions",
        "Fire-Fighting and Emergency Services": "BaselineConditions",
        "Roads and Transportation": "BaselineConditions",
        "Electricity": "BaselineConditions",
        "Communication Networks": "BaselineConditions",
        "Markets and Trade": "BaselineConditions",
        "Other Services": "BaselineConditions",

        # Objectives & Scope
        "Objectives": "ProjectDescription",
        "Scope": "ProjectDescription",

        # Steps (usually procedural, map to relevant domain)
        "Step 1:": "PublicConsultationAndDisclosure",
        "Step 2:": "PublicConsultationAndDisclosure",
        "Step 3:": "PublicConsultationAndDisclosure",
        "Step 4:": "PublicConsultationAndDisclosure",
        "Step 5:": "PublicConsultationAndDisclosure",
        "Step 6:": "PublicConsultationAndDisclosure",

        # Appendices & References (low-value for extraction)
        "APPENDIX 1: 2022 STAKEHOLDER ENGAGEMENT SUMMARY (ALL HELD IN ADMIN POST LALEIA, MANATUTO)": "References",
        "1.4 Cross-Referencing to 2024 EIS and EMP": "References",
        "1.5 Supplementary ESIA Consultant": "References",
        "1.5 Project Categorization": "ProjectDescription",
        "Acronyms, Abbreviations, and Glossary": "References",

        # People (names - usually metadata)
        "Adelina do Rego Soares": "ProjectDescription",
        "Bakhtiar S Aji S.Hut, M.Si": "ProjectDescription",
        "Zakirman": "ProjectDescription",

        # Low-value sections (metadata)
        "Local Communities": "BaselineConditions",
    }

    # Fallback mapping by keywords
    KEYWORD_MAPPING = {
        "impact": "EnvironmentalAndSocialImpactAssessment",
        "management": "MitigationAndEnhancementMeasures",
        "mitigation": "MitigationAndEnhancementMeasures",
        "enhancement": "MitigationAndEnhancementMeasures",
        "baseline": "BaselineConditions",
        "environmental": "EnvironmentalAndSocialImpactAssessment",
        "social": "EnvironmentalAndSocialImpactAssessment",
        "project": "ProjectDescription",
        "stakeholder": "PublicConsultationAndDisclosure",
        "engagement": "PublicConsultationAndDisclosure",
        "consultation": "PublicConsultationAndDisclosure",
        "risk": "EnvironmentalAndSocialImpactAssessment",
        "alternative": "ProjectDescription",
        "site selection": "ProjectDescription",
    }

    @classmethod
    def map_section(cls, section_name: str) -> Optional[str]:
        """
        Map a document section name to a DSPy signature domain.

        Args:
            section_name: The actual section name from the document

        Returns:
            The mapped DSPy signature domain, or None if no suitable mapping found
        """
        # First, try exact match
        if section_name in cls.SECTION_MAPPING:
            return cls.SECTION_MAPPING[section_name]

        # Second, try keyword matching
        section_lower = section_name.lower()
        for keyword, domain in cls.KEYWORD_MAPPING.items():
            if keyword in section_lower:
                return domain

        # If no match found, return None
        return None

    @classmethod
    def should_process_section(cls, section_name: str) -> bool:
        """
        Check if a section should be processed for fact extraction.

        Skip low-value sections like acronyms, names, etc.

        Args:
            section_name: The section name to check

        Returns:
            True if the section should be processed, False otherwise
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

        # Skip if just a name (usually 1-3 words, no special characters)
        if len(section_name.split()) <= 3 and not any(c.isdigit() for c in section_name):
            # But allow known sections
            if section_name not in cls.SECTION_MAPPING:
                if section_name not in [
                    "Introduction",
                    "Objectives",
                    "Scope",
                    "Vulnerable Groups",
                ]:
                    return False

        return True

    @classmethod
    def get_statistics(cls) -> Dict[str, int]:
        """Get statistics about the mapping."""
        return {
            "total_mappings": len(cls.SECTION_MAPPING),
            "total_keywords": len(cls.KEYWORD_MAPPING),
        }


# Test the mapper
if __name__ == "__main__":
    test_sections = [
        "2.0 UPDATED PROJECT DESCRIPTION AND AREA OF INFLUENCE",
        "8.0 SUPPLEMENTARY IMPACT ASSESSMENT AND MANAGEMENT PLANS",
        "Acronyms, Abbreviations, and Glossary",
        "4.3 Livelihoods and Employment",
        "10.0 STAKEHOLDER ENGAGEMENT",
    ]

    print("Testing Section Mapper")
    print("=" * 70)

    for section in test_sections:
        mapped = SectionMapper.map_section(section)
        should_process = SectionMapper.should_process_section(section)
        status = "PROCESS" if should_process else "SKIP"

        print(f"Section: {section}")
        print(f"  Mapped to: {mapped}")
        print(f"  Status: {status}")
        print()
