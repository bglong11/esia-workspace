"""
Project Type Classifier

Automatically classifies ESIA documents into project types by analyzing
the first few pages using LLM.
"""
import os
import json
from google.genai import types
from src.config import client

class ProjectTypeClassifier:
    """
    Classifies ESIA documents into project types using a hierarchical taxonomy.
    """
    
    # Full Project Taxonomy
    PROJECT_TAXONOMY = {
      "Mining": [
        "Gold mines", "Copper mines", "Coal mines", "Quarries", "Other metallic mines", "Industrial minerals", "Nickel mines"
      ],
      "Energy_Renewable": [
        "Wind farms", "Solar parks", "Hydropower plants", "Pumped-storage facilities", "Biomass energy plants", "Geothermal plants"
      ],
      "Energy_Oil_Gas": [
        "Oil extraction", "Gas extraction", "LNG facilities", "Pipelines", "Refineries"
      ],
      "Energy_Coal": [
        "Coal Fired Power Plants"
      ],
      "Infrastructure": [
        "Roads", "Highways", "Dams", "Ports", "Railways", "Bridges", "Tunnels"
      ],
      "Industrial_Manufacturing": [
        "Factories", "Processing plants", "Chemical production", "Pharmaceutical plants", "Metallurgical plants", "Alumina Refineries"
      ],
      "Agriculture_Forestry": [
        "Commercial plantations", "Irrigation schemes", "Agro-processing zones", "Livestock farms", "Forestry operations"
      ],
      "Water_Wastewater": [
        "Water supply systems", "Wastewater treatment plants", "Desalination plants"
      ],
      "Waste_Management": [
        "Landfills", "Incinerators", "Recycling facilities", "Hazardous-waste treatment plants"
      ],
      "Real_Estate_Urban": [
        "Residential developments", "Commercial complexes", "Urban expansion projects", "Smart-city infrastructure"
      ],
      "Tourism_Recreation": [
        "Resorts", "Ecotourism facilities", "Marinas"
      ],
      "Transport_Aviation": [
        "Airports", "Airstrips", "Aviation logistics"
      ],
      "Transport_Maritime": [
        "Harbours", "Shipyards", "Coastal terminals"
      ],
      "Telecommunications": [
        "Data centres", "Telecom towers", "Fibre-optic networks"
      ],
      "Extractive_Other": [
        "Sand mining", "Peat extraction", "Salt works"
      ],
      "Logistics_Distribution": [
        "Warehouses", "Distribution centres", "Logistics hubs"
      ],
      "Public_Services": [
        "Hospitals", "Schools", "Public buildings", "Government complexes"
      ],
      "Special_Projects": [
        "Carbon-capture facilities", "Hydrogen production plants", "Battery storage installations"
      ]
    }

    # Mapping from Subtypes/Categories to Archetype Extension Filenames
    # Key: Subtype (preferred) or Category
    # Value: Filename prefix (e.g., "mining_nickel" for "mining_nickel_extension.json")
    ARCHETYPE_MAPPING = {
        # Specific Subtype Mappings
        "Nickel mines": "mining_nickel",
        "Alumina Refineries": "industrial_alumina",
        "Coal Fired Power Plants": "energy_coal",
        "Wind farms": "energy_wind_solar",
        "Solar parks": "energy_solar",
        "Hydropower plants": "energy_hydro",
        "Pumped-storage facilities": "energy_pumped_storage",
        "Geothermal plants": "energy_geothermal",
        "LNG facilities": "energy_oil_gas",
        "Oil extraction": "energy_oil_gas",
        "Gas extraction": "energy_oil_gas",
        "Pipelines": "energy_oil_gas",
        "Refineries": "energy_oil_gas",
        "Factories": "industrial",
        "Processing plants": "industrial",
        
        # Category Fallbacks
        "Mining": "mining",
        "Energy_Renewable": "energy_wind_solar",
        "Energy_Oil_Gas": "energy_oil_gas",
        "Energy_Coal": "energy_coal",
        "Infrastructure": "infrastructure",
        "Industrial_Manufacturing": "industrial",
        "Agriculture_Forestry": "core_esia", # No extension yet
        "Water_Wastewater": "infrastructure",
        "Waste_Management": "infrastructure",
        "Real_Estate_Urban": "infrastructure",
        "Tourism_Recreation": "infrastructure",
        "Transport_Aviation": "infrastructure",
        "Transport_Maritime": "infrastructure",
        "Telecommunications": "infrastructure",
        "Extractive_Other": "mining",
        "Logistics_Distribution": "industrial",
        "Public_Services": "infrastructure",
        "Special_Projects": "industrial"
    }
    
    def __init__(self):
        self.client = client
    
    def classify(self, pdf_path: str, store_name: str = None) -> tuple[str, float]:
        """
        Classify ESIA project type from PDF.
        
        Returns:
            (archetype_name, confidence)
            archetype_name: The mapped filename prefix for the archetype extension.
            confidence: 0.0-1.0
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        print(f"Classifying project type for: {os.path.basename(pdf_path)}")
        
        if not store_name:
            raise ValueError("store_name required for classification")
        
        # Create classification prompt
        prompt = self._create_classification_prompt(os.path.basename(pdf_path))
        
        # Query LLM with File Search
        tool = {
            "file_search": {
                "file_search_store_names": [store_name]
            }
        }
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[tool],
                    temperature=0.1,
                    response_mime_type="application/json"
                )
            )
            
            # Parse response
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(text)
            category = result.get('category')
            subtype = result.get('subtype')
            confidence = result.get('confidence', 0.0)
            reasoning = result.get('reasoning', '')
            
            print(f"  Classified as: {category} / {subtype}")
            print(f"  Confidence: {confidence:.0%}")
            print(f"  Reasoning: {reasoning}")

            # Map to archetype
            archetype = self._map_to_archetype(category, subtype)
            print(f"  Mapped to Archetype: {archetype}")
            
            return archetype, confidence
            
        except Exception as e:
            print(f"Error during classification: {e}")
            return None, 0.0
    
    def classify_from_file(self, file_ref, filename: str = None) -> tuple[str, float]:
        """
        Classify project type using Direct File API (no File Search store required).

        This method works with uploaded file references from client.files.upload(),
        allowing classification without creating a File Search store first.

        Args:
            file_ref: Uploaded file reference from client.files.upload()
            filename: Optional filename hint for classification

        Returns:
            (archetype_name, confidence)
            archetype_name: The mapped filename prefix for the archetype extension.
            confidence: 0.0-1.0
        """
        display_name = filename or getattr(file_ref, 'display_name', 'document.pdf')
        print(f"[CLASSIFY] Classifying project type for: {display_name}")

        # Create classification prompt
        prompt = self._create_classification_prompt(display_name)

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(file_data=types.FileData(file_uri=file_ref.uri)),
                            types.Part(text=prompt)
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json"
                )
            )

            # Parse response
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            result = json.loads(text)
            category = result.get('category')
            subtype = result.get('subtype')
            confidence = result.get('confidence', 0.0)
            reasoning = result.get('reasoning', '')

            print(f"  Classified as: {category} / {subtype}")
            print(f"  Confidence: {confidence:.0%}")
            print(f"  Reasoning: {reasoning}")

            # Map to archetype
            archetype = self._map_to_archetype(category, subtype)
            print(f"  Mapped to Archetype: {archetype}")

            return archetype, confidence

        except Exception as e:
            print(f"Error during classification: {e}")
            return None, 0.0

    def _map_to_archetype(self, category: str, subtype: str) -> str:
        """Map the classification to a specific archetype extension."""
        # 1. Try specific subtype mapping
        if subtype in self.ARCHETYPE_MAPPING:
            return self.ARCHETYPE_MAPPING[subtype]

        # 2. Try category mapping
        if category in self.ARCHETYPE_MAPPING:
            return self.ARCHETYPE_MAPPING[category]

        # 3. Fallback based on category string matching (e.g. "Energy_Renewable" -> "energy")
        return None

    def _create_classification_prompt(self, filename: str) -> str:
        """Create the classification prompt."""
        return f"""
Analyze the first 10 pages of this ESIA document to determine the PRIMARY project type.
Filename: "{filename}" (Use this as a hint, but verify with content).

Instructions:
1. Identify the MAIN facility or activity being assessed.
2. Select the most SPECIFIC Category and Subtype from the list below.
3. **CRITICAL**: Distinguish between the PRIMARY activity and SUPPORTING facilities. 
   - Example: A mine with a captive power plant is a MINE.
   - Example: A factory with a captive power plant is a FACTORY.
   - Example: A standalone power plant is ENERGY.
4. If the project involves multiple components, choose the one that is the primary subject of the ESIA.

Taxonomy:
{json.dumps(self.PROJECT_TAXONOMY, indent=2)}

Output ONLY valid JSON:
{{
  "category": "Energy_Renewable",
  "subtype": "Solar parks",
  "confidence": 0.95,
  "reasoning": "Document describes a 50MW PV installation..."
}}
"""

if __name__ == "__main__":
    # Test the classifier
    import sys
    if len(sys.argv) < 3:
        print("Usage: python -m src.project_type_classifier <pdf_path> <store_name>")
        sys.exit(1)
    
    classifier = ProjectTypeClassifier()
    pdf_path = sys.argv[1]
    store_name = sys.argv[2]
    
    project_type, confidence = classifier.classify(pdf_path, store_name)
    
    if project_type:
        print(f"\n✓ Classification: {project_type} ({confidence:.0%})")
    else:
        print("\n✗ Classification failed (or mapped to Core only)")
