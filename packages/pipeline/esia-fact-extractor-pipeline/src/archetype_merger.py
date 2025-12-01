import json
import os
from typing import Dict, List

def merge_archetypes(project_type: str = None) -> Dict:
    """
    Merges core ESIA archetype with project-type-specific extensions.
    
    Args:
        project_type: One of 'mining', 'energy_wind_solar', 'energy_oil_gas', 'infrastructure', 'industrial'
                     If None, returns only core archetype.
    
    Returns:
        Merged archetype dictionary with 3-level hierarchy
    """
    # Load core archetype from directory
    core_dir = "data/archetypes/core_esia"
    core_file = "data/archetypes/core_esia.json"
    
    merged = {}
    
    if os.path.exists(core_dir):
        # New modular loading
        # Sort files to ensure correct order (01_, 02_, etc.)
        for filename in sorted(os.listdir(core_dir)):
            if filename.endswith(".json"):
                file_path = os.path.join(core_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        chapter_data = json.load(f)
                        
                        # Check for key collisions
                        for key in chapter_data:
                            if key in merged:
                                raise ValueError(f"Duplicate key found: '{key}' in file '{filename}'. This key is already defined in a previous chapter.")
                                
                        merged.update(chapter_data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in {filename}: {e}")
                    raise
    elif os.path.exists(core_file):
        # Fallback to legacy monolithic file
        with open(core_file, 'r', encoding='utf-8') as f:
            merged = json.load(f)
    else:
        raise FileNotFoundError(f"Core archetype not found in {core_dir} or {core_file}")
    
    # If no project type specified, return core only
    if not project_type:
        return merged
    
    # Load extension
    extension_path = f"data/archetypes/project_specific_esia/{project_type}_extension.json"
    if not os.path.exists(extension_path):
        print(f"Warning: Extension not found for project type '{project_type}', using core only")
        return merged
    
    with open(extension_path, 'r', encoding='utf-8') as f:
        extension = json.load(f)
    
    # Merge extension into core
    # Extension domains are added as new top-level domains
    for domain, sub_domains in extension.items():
        if domain in merged:
            # If domain exists, merge sub-domains
            for sub_domain, sub_sub_domains in sub_domains.items():
                if sub_domain in merged[domain]:
                    # Merge sub-sub-domains
                    if isinstance(merged[domain][sub_domain], list) and isinstance(sub_sub_domains, list):
                        merged[domain][sub_domain].extend(sub_sub_domains)
                else:
                    merged[domain][sub_domain] = sub_sub_domains
        else:
            # Add new domain
            merged[domain] = sub_domains
    
    return merged

def list_available_project_types() -> List[str]:
    """
    Lists all available project-type extensions.
    
    Returns:
        List of project type identifiers
    """
    archetype_dir = "data/archetypes/project_specific_esia"
    if not os.path.exists(archetype_dir):
        return []
    
    extensions = []
    for filename in os.listdir(archetype_dir):
        if filename.endswith("_extension.json"):
            project_type = filename.replace("_extension.json", "")
            extensions.append(project_type)
    
    return extensions

if __name__ == "__main__":
    # Test merging
    print("Available project types:", list_available_project_types())
    
    print("\n--- Core Only ---")
    try:
        core = merge_archetypes()
        print(f"Domains: {len(core)}")
        # Print top-level keys to verify order
        print("Top-level keys:", list(core.keys()))
    except Exception as e:
        print(f"Error loading core archetype: {e}")
    
    print("\n--- Core + Mining ---")
    try:
        mining = merge_archetypes("mining")
        print(f"Domains: {len(mining)}")
        print(f"New domains: {set(mining.keys()) - set(core.keys())}")
    except Exception as e:
        print(f"Error loading mining archetype: {e}")
