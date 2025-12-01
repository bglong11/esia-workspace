"""
Constants for ESIA analysis including unit conversions and parameter contexts.
"""

# Unit conversion factors to base units
UNIT_CONVERSIONS = {
    # Area units -> sq m
    'ha': {'base': 'sq m', 'factor': 10000},
    'hectare': {'base': 'sq m', 'factor': 10000},
    'hectares': {'base': 'sq m', 'factor': 10000},
    'km²': {'base': 'sq m', 'factor': 1000000},
    'km2': {'base': 'sq m', 'factor': 1000000},
    'square kilometers': {'base': 'sq m', 'factor': 1000000},
    'square kilometer': {'base': 'sq m', 'factor': 1000000},
    'm²': {'base': 'sq m', 'factor': 1},
    'm2': {'base': 'sq m', 'factor': 1},
    'sq m': {'base': 'sq m', 'factor': 1},
    'sqm': {'base': 'sq m', 'factor': 1},
    'square meters': {'base': 'sq m', 'factor': 1},
    'square metres': {'base': 'sq m', 'factor': 1},
    'acres': {'base': 'sq m', 'factor': 4046.86},
    'acre': {'base': 'sq m', 'factor': 4046.86},

    # Length units -> meters
    'km': {'base': 'm', 'factor': 1000},
    'kilometers': {'base': 'm', 'factor': 1000},
    'm': {'base': 'm', 'factor': 1},
    'meters': {'base': 'm', 'factor': 1},
    'metres': {'base': 'm', 'factor': 1},

    # Volume units -> liters
    'ML': {'base': 'L', 'factor': 1000000},
    'kL': {'base': 'L', 'factor': 1000},
    'L': {'base': 'L', 'factor': 1},
    'm³': {'base': 'L', 'factor': 1000},
    'm3': {'base': 'L', 'factor': 1000},

    # Mass/emissions -> tonnes
    'tCO2e': {'base': 't', 'factor': 1},
    'tCO2': {'base': 't', 'factor': 1},
    't': {'base': 't', 'factor': 1},
    'tonnes': {'base': 't', 'factor': 1},
    'tons': {'base': 't', 'factor': 1},
    'kt': {'base': 't', 'factor': 1000},
    'Mt': {'base': 't', 'factor': 1000000},

    # Concentration units (keep separate)
    'mg/L': {'base': 'mg/L', 'factor': 1},
    'µg/m³': {'base': 'µg/m³', 'factor': 1},
    'ug/m3': {'base': 'µg/m³', 'factor': 1},
    'mg/m³': {'base': 'µg/m³', 'factor': 1000},
    'mg/m3': {'base': 'µg/m³', 'factor': 1000},

    # Power
    'MW': {'base': 'MW', 'factor': 1},
    'GW': {'base': 'MW', 'factor': 1000},
    'kW': {'base': 'MW', 'factor': 0.001},

    # People
    'people': {'base': 'people', 'factor': 1},
    'persons': {'base': 'people', 'factor': 1},
    'households': {'base': 'households', 'factor': 1},
}

# Parameter context patterns for like-for-like comparison
# Each context has patterns AND valid unit types
PARAMETER_CONTEXTS = {
    'study_area': {
        'patterns': [
            r'study\s+area',
            r'project\s+area',
            r'assessment\s+area',
            r'survey\s+area',
            r'investigation\s+area',
        ],
        'valid_units': ['sq m', 'ha', 'km²', 'km2', 'm²', 'm2', 'hectares', 'hectare', 'acres', 'acre'],
    },
    'concession_area': {
        'patterns': [
            r'concession\s+area',
            r'mining\s+area',
            r'license\s+area',
            r'permit\s+area',
            r'lease\s+area',
        ],
        'valid_units': ['sq m', 'ha', 'km²', 'km2', 'm²', 'm2', 'hectares', 'hectare', 'acres', 'acre'],
    },
    'disturbance_area': {
        'patterns': [
            r'disturbance\s+area',
            r'clearing\s+area',
            r'footprint',
            r'impact\s+area',
            r'affected\s+area',
        ],
        'valid_units': ['sq m', 'ha', 'km²', 'km2', 'm²', 'm2', 'hectares', 'hectare', 'acres', 'acre'],
    },
    'buffer_zone': {
        'patterns': [
            r'buffer\s+zone',
            r'buffer\s+area',
            r'exclusion\s+zone',
            r'setback',
        ],
        'valid_units': ['sq m', 'ha', 'km²', 'km2', 'm²', 'm2', 'hectares', 'hectare', 'm', 'km', 'meters'],
    },
    'population': {
        'patterns': [
            r'population',
            r'residents',
            r'inhabitants',
        ],
        'valid_units': ['people', 'persons', ''],  # Often just numbers
    },
    'affected_households': {
        'patterns': [
            r'affected\s+households',
            r'displaced\s+households',
            r'impacted\s+households',
            r'households\s+affected',
        ],
        'valid_units': ['households', ''],
    },
    'workforce': {
        'patterns': [
            r'workforce',
            r'employees',
            r'workers',
            r'staff',
            r'personnel',
        ],
        'valid_units': ['people', 'persons', ''],
    },
    'water_consumption': {
        'patterns': [
            r'water\s+consumption',
            r'water\s+demand',
            r'water\s+use',
            r'water\s+requirement',
        ],
        'valid_units': ['L', 'ML', 'kL', 'm³', 'm3', 'L/s', 'm³/s'],
    },
    'power_capacity': {
        'patterns': [
            r'power\s+capacity',
            r'installed\s+capacity',
            r'generation\s+capacity',
            r'rated\s+capacity',
            r'power\s+demand',
        ],
        'valid_units': ['MW', 'GW', 'kW', 'GWh'],
    },
    'emissions_ghg': {
        'patterns': [
            r'ghg\s+emissions?',
            r'greenhouse\s+gas',
            r'carbon\s+emissions?',
            r'co2\s+emissions?',
            r'tco2e?',
        ],
        'valid_units': ['t', 'tCO2e', 'tCO2', 'tonnes', 'kt', 'Mt', 't/y'],
    },
    'noise_level': {
        'patterns': [
            r'noise\s+level',
            r'sound\s+level',
            r'ambient\s+noise',
            r'background\s+noise',
        ],
        'valid_units': ['dB', 'dB(A)', 'dBA', 'decibels'],
    },
    'air_quality_pm': {
        'patterns': [
            r'pm\s*10',
            r'pm\s*2\.?5',
            r'particulate',
        ],
        'valid_units': ['µg/m³', 'ug/m3', 'mg/m³', 'mg/m3'],
    },
    'rainfall': {
        'patterns': [
            r'rainfall',
            r'precipitation',
            r'annual\s+rain',
        ],
        'valid_units': ['mm', 'mm/year', 'mm/yr'],
    },
    'temperature': {
        'patterns': [
            r'temperature',
            r'ambient\s+temp',
        ],
        'valid_units': ['°C', 'C', '°F', 'F'],
    },
}
