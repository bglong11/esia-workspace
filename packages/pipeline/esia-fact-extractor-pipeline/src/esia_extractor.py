import sys
import os
sys.path.append(os.getcwd())
import dspy
from src.generated_signatures import (
    AluminaSpecificImpactsSignature,
    AnnexesSignature,
    AvianAndBatImpactsSignature,
    BaselineConditionsSignature,
    BridgeAndTunnelConstructionSignature,
    CoalPowerSpecificImpactsSignature,
    ConclusionAndRecommendationsSignature,
    CulturallyAppropriateGRMSignature,
    CumulativeAndRegionalImpactsSignature,
    DecommissioningSignature,
    ElectromagneticFieldsEmfSignature,
    EnvironmentalAndSocialImpactAssessmentSignature,
    EnvironmentalAndSocialManagementPlanEsmpSignature,
    ExecutiveSummarySignature,
    GeothermalSpecificImpactsSignature,
    GridIntegrationAndTransmissionSignature,
    HazardousMaterialsManagementSignature,
    HydrocarbonManagementSignature,
    HydropowerSpecificImpactsSignature,
    IntroductionSignature,
    MineClosureAndRehabilitationSignature,
    MineSpecificImpactsSignature,
    MineralWasteManagementSignature,
    MitigationAndEnhancementMeasuresSignature,
    NickelSpecificImpactsSignature,
    NoiseAndVibrationSignature,
    PipelineIntegrityAndSafetySignature,
    PolicyLegalAndAdministrativeFrameworkSignature,
    ProcessEmissionsSignature,
    ProjectDescriptionSignature,
    PublicConsultationAndDisclosureSignature,
    PumpedStorageHydropowerSpecificImpactsSignature,
    ReferencesSignature,
    SolarSpecificImpactsSignature,
    TrafficAndTransportationSignature,
    TransmissionLineSpecificImpactsSignature,
    UtilitiesRelocationSignature,
    VisualAndLandscapeImpactsSignature,
    WellDrillingAndCompletionSignature,
    # Phase 2: New project-specific signatures
    EnergyNuclearSpecificImpactsSignature,
    InfrastructurePortsSpecificImpactsSignature,
    AgricultureCropsSpecificImpactsSignature,
    AgricultureAnimalProductionSpecificImpactsSignature,
    AgricultureForestrySpecificImpactsSignature,
    ManufacturingGeneralSpecificImpactsSignature,
    RealEstateCommercialSpecificImpactsSignature,
    RealEstateHospitalitySpecificImpactsSignature,
    RealEstateHealthcareSpecificImpactsSignature,
    FinancialBankingSpecificImpactsSignature,
    FinancialMicrofinanceSpecificImpactsSignature,
    FinancialIntermediaryESMSSignature,
    # Phase 3B: Culturally appropriate GRM
    GenderActionPlanSignature,
    CulturallyAppropriateGRMSignature
)
from src.llm_manager import LLMManager

class ESIAExtractor:
    """
    DSPy-based extractor for ESIA documents.
    Extracts structured facts from ESIA documents using domain-specific signatures.
    """
    
    @staticmethod
    def normalize_domain_name(domain: str) -> str:
        """
        Normalize domain names by removing numbering and mapping to known domains.
        Maps archetype domain names to their corresponding signature class names.
        """
        # Remove leading numbers and dots
        import re
        normalized = re.sub(r'^\d+\.\s*', '', domain)

        # Map archetype domain names to signature class base names
        # This handles the mismatch between archetype names and signature names
        mapping = {
            # Core ESIA mappings
            "Environmental and Social Management Plan": "Environmental And Social Management Plan Esmp",
            "ESMP": "Environmental And Social Management Plan Esmp",
            "environmental_and_social_management_plan_esmp": "Environmental And Social Management Plan Esmp",
            "Policy, Legal, and Administrative Framework": "Policy Legal And Administrative Framework",

            # Energy sector mappings
            "energy_solar": "solar_specific_impacts",
            "energy_hydro": "hydropower_specific_impacts",
            "energy_coal": "coal_power_specific_impacts",
            "energy_wind_solar_extension": "solar_specific_impacts",  # Maps to solar for now
            "energy_floating_solar": "solar_specific_impacts",
            "energy_geothermal_extension": "geothermal_specific_impacts",
            "energy_oil_gas_extension": "hydrocarbon_management",
            "energy_pumped_storage_extension": "pumped_storage_hydropower_specific_impacts",
            "energy_transmission": "transmission_line_specific_impacts",

            # Mining sector mappings
            "mining_extension": "mine_specific_impacts",
            "mining_nickel_extension": "nickel_specific_impacts",
            "industrial_alumina_extension": "alumina_specific_impacts",
            "industrial_extension": "mine_specific_impacts",  # Generic fallback

            # Infrastructure mappings
            "infrastructure_extension": "bridge_and_tunnel_construction",  # Generic fallback
            "infrastructure_airports": "traffic_and_transportation",
            "infrastructure_roads": "traffic_and_transportation",
            "infrastructure_water": "utilities_relocation",

            # Manufacturing mappings
            "manufacturing_chemicals": "manufacturing_general_specific_impacts",
            "manufacturing_pharmaceuticals": "manufacturing_general_specific_impacts",
            "manufacturing_textiles": "manufacturing_general_specific_impacts",

            # IFC Performance Standards (PS1-PS8) - these map to core ESIA sections
            "PS1": "Environmental And Social Management Plan Esmp",
            "PS2": "baseline_conditions",  # Labor and working conditions
            "PS3": "environmental_and_social_impact_assessment",  # Resource efficiency
            "PS4": "baseline_conditions",  # Community health and safety
            "PS5": "project_description",  # Land acquisition and resettlement
            "PS6": "baseline_conditions",  # Biodiversity
            "PS7": "public_consultation_and_disclosure",  # Indigenous peoples
            "PS8": "baseline_conditions",  # Cultural heritage
            "ps1_esms_structure": "Environmental And Social Management Plan Esmp",
        }

        return mapping.get(normalized, normalized)
    
    def __init__(self, model="gemini-2.5-flash", provider="google"):
        """
        Initialize the ESIA extractor.
        """
        self.model = model
        self.provider = provider
        self.llm_manager = LLMManager()
        
        # Configure DSPy to use our LLM manager
        self._configure_dspy()
        
        # Initialize extractors cache
        self.extractors = {}
    
    def _configure_dspy(self):
        """Configure DSPy to use the LLM manager."""
        # Create a custom DSPy LM that wraps our LLMManager
        class CustomLM(dspy.LM):
            def __init__(self, model, provider, llm_manager):
                super().__init__(model=model)
                self.model = model
                self.provider = provider
                self.llm_manager = llm_manager
                self.history = []
                self.kwargs = {"temperature": 0.3, "max_tokens": 2000}
            
            def __call__(self, prompt=None, messages=None, **kwargs):
                if messages:
                    # Convert messages to a single prompt
                    prompt = "\n".join([f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages])
                
                try:
                    response = self.llm_manager.generate_content(
                        prompt=prompt,
                        model=self.model,
                        provider=self.provider
                    )
                    
                    text = response.text if hasattr(response, 'text') else str(response)
                    return [text]
                except Exception as e:
                    print(f"LLM call error: {e}")
                    return [""]
            
            def basic_request(self, prompt, **kwargs):
                return self.__call__(prompt=prompt, **kwargs)
        
        # Set as default DSPy LM
        dspy.settings.configure(lm=CustomLM(self.model, self.provider, self.llm_manager))

    def _get_signature_class(self, domain: str):
        """
        Dynamically retrieve the signature class for a domain.
        """
        # Normalize domain name
        normalized = self.normalize_domain_name(domain)

        # Convert to class name: "nickel_specific_impacts" -> "NickelSpecificImpactsSignature"
        # Replace underscores and hyphens with spaces, then title case and join
        clean_name = "".join(x.title() for x in normalized.replace("_", " ").replace("-", " ").split())

        # Handle acronyms that should remain uppercase (ESMS, EMF, GRM, etc.)
        # Note: ESMP is NOT in this list because the signature uses "Esmp" (TitleCase)
        acronym_map = {
            'Esms': 'ESMS',
            'Emf': 'EMF',
            'Grm': 'GRM',
            'Gbvh': 'GBVH',
            'Seah': 'SEAH',
            'Fpic': 'FPIC',
        }
        for title_case, upper_case in acronym_map.items():
            clean_name = clean_name.replace(title_case, upper_case)

        class_name = f"{clean_name}Signature"

        # Try to get from generated_signatures
        import src.generated_signatures as gen_sigs
        signature_class = getattr(gen_sigs, class_name, None)

        if not signature_class:
            # Try with "SpecificImpacts" suffix for sector-specific signatures
            # Pattern: infrastructure_ports -> InfrastructurePortsSpecificImpactsSignature
            class_name_with_suffix = f"{clean_name}SpecificImpactsSignature"
            signature_class = getattr(gen_sigs, class_name_with_suffix, None)

            if not signature_class:
                # Try removing "specific_impacts" from domain if present and retry
                # Pattern: nickel_specific_impacts -> NickelSpecificImpactsSignature
                if '_specific_impacts' in normalized.lower():
                    alt_name = normalized.replace('_specific_impacts', '')
                    alt_clean = "".join(x.title() for x in alt_name.replace("_", " ").replace("-", " ").split())
                    # Apply acronym mapping to alt_clean too
                    for title_case, upper_case in acronym_map.items():
                        alt_clean = alt_clean.replace(title_case, upper_case)
                    alt_class_name = f"{alt_clean}SpecificImpactsSignature"
                    signature_class = getattr(gen_sigs, alt_class_name, None)

                    if signature_class:
                        return signature_class

                print(f"Warning: No signature found for domain '{domain}' (Tried: {class_name}, {class_name_with_suffix})")
                return None

        return signature_class

    def extract(self, context: str, domain: str):
        """
        Extract facts from a text chunk for a specific domain.
        """
        # Get signature dynamically
        signature_class = self._get_signature_class(domain)
        
        if not signature_class:
            raise ValueError(f"Unknown domain: {domain}. No matching signature found.")
            
        # Create predictor if not cached
        # We cache predictors by domain to reuse compiled modules if we were using DSPy optimization
        if domain not in self.extractors:
            self.extractors[domain] = dspy.Predict(signature_class)
            
        extractor = self.extractors[domain]
        signature = extractor.signature
        
        # Dynamically update docstring to request page numbers and handle contradictions
        original_doc = signature.__doc__ or ""
        if "page number" not in original_doc.lower():
            signature.__doc__ = original_doc + "\n\nIMPORTANT INSTRUCTIONS:\n1. CITATIONS: For every extracted value, you MUST append the page number where found in brackets, e.g., 'Solar Project [Page 12]'. The context contains page markers like '--- PAGE 12 ---' or 'Page | 12'. If a fact spans multiple pages, cite the first one.\n2. CONTRADICTIONS: If you find conflicting information (e.g., different values for the same field on different pages), DO NOT resolve it yourself. List ALL conflicting values with their respective page numbers, separated by ' | '. Example: '100 MW [Page 5] | 120 MW [Page 22]'.\n3. TRANSLATION: Extracted values MUST be in English. If the source text is in another language (e.g., Indonesian, Spanish), translate the value to English before outputting. Keep proper nouns (names of places, companies) in their original form."
        
        # Run extraction
        result = extractor(context=context)
        
        # Convert result to plain dictionary
        facts = {}
        
        # Get expected output fields from the signature
        # dspy signatures store fields in .fields map
        for field_name, field_obj in signature.fields.items():
            # Skip input fields (like context)
            if field_name == 'context':
                continue
                
            # Get value from result
            value = getattr(result, field_name, None)
            
            if value is not None:
                # Skip callable objects (methods, functions)
                if callable(value):
                    continue
                    
                # Unwrap single-item lists (common in DSPy outputs)
                if isinstance(value, list) and len(value) == 1:
                    value = value[0]
                
                # Check if it's a complex object (like Completions) and skip or convert
                if hasattr(value, '__dict__') and not isinstance(value, (str, int, float, bool, list, dict)):
                    continue
                
                facts[field_name] = value
        
        return facts
    
    def extract_all_domains(self, context: str):
        """
        Extract facts from a text chunk for all domains.
        
        Args:
            context: The text content to extract from
            
        Returns:
            dict: Dictionary mapping domain names to extracted facts
        """
        all_facts = {}
        for domain in self.extractors.keys():
            try:
                facts = self.extract(context, domain)
                all_facts[domain] = facts
            except Exception as e:
                print(f"Error extracting {domain}: {e}")
                all_facts[domain] = {"error": str(e)}
        
        return all_facts
    
    def extract_from_file(self, file_path: str, domain: str = None):
        """
        Extract facts from a text file.
        
        Args:
            file_path: Path to the text file (markdown, txt, etc.)
            domain: Specific domain to extract, or None for all domains
            
        Returns:
            dict: Extracted facts
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            context = f.read()
        
        if domain:
            return {domain: self.extract(context, domain)}
        else:
            return self.extract_all_domains(context)

if __name__ == "__main__":
    # Example usage
    extractor = ESIAExtractor()
    
    # Test extraction with sample text
    sample_context = """
    Project Name: Green Energy Power Plant
    Location: Northern Region
    Developer: GreenPower Inc.
    Objective: Generate 500 MW of renewable energy
    """
    
    try:
        facts = extractor.extract(sample_context, "Project Description")
        print("Extracted Facts:")
        for key, value in facts.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error during extraction: {e}")
