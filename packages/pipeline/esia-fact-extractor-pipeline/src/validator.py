import dspy
from src.llm_manager import LLMManager
import json

class FactValidationSignature(dspy.Signature):
    """
    Analyze the provided extracted facts for anomalies, physical impossibilities, and unit inconsistencies.
    
    You are an expert ESIA (Environmental and Social Impact Assessment) auditor.
    Your job is to review the extracted data for quality control.
    
    For each field in the JSON:
    1. Identify the unit of measurement (if applicable).
    2. Assess the probability that the value and unit are physically possible and correct.
    3. Check for contradictions.
    
    Output a JSON object mapping field names to a validation object with these fields:
    - "original_value": The raw string extracted.
    - "extracted_unit": The unit identified (e.g., "mm", "MW", "ha"). If no unit, use null.
    - "probability_score": One of ["High", "Medium", "Low"].
        - High: Value is physically plausible and unit is standard.
        - Medium: Value is unusual but possible, or unit is ambiguous.
        - Low: Value is physically impossible (e.g., 10m rainfall/day) or unit is clearly wrong (kg/m2 vs kg/cm2).
    - "reasoning": Brief explanation for the score.
    
    Example Output:
    {
        "project_site_area_hectares": {
            "original_value": "350000",
            "extracted_unit": "ha",
            "probability_score": "Medium",
            "reasoning": "Value seems very large for a single site, possibly sq meters?"
        },
        "annual_rainfall": {
            "original_value": "100m",
            "extracted_unit": "m",
            "probability_score": "Low",
            "reasoning": "100m is physically impossible for daily rainfall, likely mm."
        }
    }
    """
    domain = dspy.InputField(desc="The domain of the facts (e.g., Project Description)")
    facts_json = dspy.InputField(desc="The extracted facts in JSON format")
    validation_report = dspy.OutputField(desc="JSON string mapping field names to validation details")

class FactValidator:
    def __init__(self, model="gemini-2.5-flash", provider="google"):
        # Use ChainOfThought to encourage reasoning about physical plausibility
        self.validator = dspy.ChainOfThought(FactValidationSignature)

    def validate(self, domain: str, facts: dict) -> dict:
        """
        Validate extracted facts for a specific domain.
        
        Args:
            domain: The domain name
            facts: The dictionary of extracted facts
            
        Returns:
            dict: A dictionary of validation details (field -> {unit, score, reasoning})
        """
        # Filter out empty facts and non-serializable objects
        def is_serializable(v):
            """Check if value is JSON serializable"""
            if callable(v):  # Filter out methods/functions
                return False
            try:
                json.dumps(v)
                return True
            except (TypeError, ValueError):
                return False
        
        active_facts = {
            k: v for k, v in facts.items() 
            if v and str(v).strip() and v != "None" and is_serializable(v)
        }
        
        if not active_facts:
            return {}
            
        try:
            facts_str = json.dumps(active_facts, ensure_ascii=False)
            response = self.validator(domain=domain, facts_json=facts_str)
            
            # Parse the output
            raw_report = response.validation_report
            
            # Clean up markdown code blocks if present
            if "```json" in raw_report:
                raw_report = raw_report.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_report:
                raw_report = raw_report.split("```")[1].split("```")[0].strip()
                
            validation_dict = json.loads(raw_report)
            return validation_dict
            
        except Exception as e:
            print(f"Validation error for {domain}: {e}")
            return {"error": f"Validation failed: {str(e)}"}

if __name__ == "__main__":
    # Test
    validator = FactValidator()
    test_facts = {
        "project_name": "Test Project",
        "rainfall": "100 meters per day",
        "capacity": "50 MW [Page 1] | 60 MW [Page 2]"
    }
    # Note: This requires dspy.settings.lm to be configured globally, 
    # which usually happens in the main script or ESIAExtractor.
    # So running this directly might fail without LM setup.
    print("Validator module loaded.")
