import dspy

class AluminaSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Alumina Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Bauxite_Residue_Red_Mud = dspy.OutputField(desc="Extract facts about Bauxite Residue (Red Mud), specifically: Storage Facility Design, Alkalinity Management, Leachate Control, Rehabilitation", prefix="Bauxite Residue (Red Mud): ")
    Process_Emissions = dspy.OutputField(desc="Extract facts about Process Emissions, specifically: Caustic Dust, Combustion Emissions, Calcination Off-gases", prefix="Process Emissions: ")
    Water_Management = dspy.OutputField(desc="Extract facts about Water Management, specifically: Alkaline Effluent Treatment, Water Consumption, Stormwater Management", prefix="Water Management: ")


class AvianAndBatImpactsSignature(dspy.Signature):
    """
    Extracted facts for Avian And Bat Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Collision_Risk = dspy.OutputField(desc="Extract facts about Collision Risk, specifically: Pre-construction Surveys, Post-construction Monitoring, Turbine Curtailment", prefix="Collision Risk: ")
    Habitat_Displacement = dspy.OutputField(desc="Extract facts about Habitat Displacement, specifically: Migration Routes, Roosting Sites", prefix="Habitat Displacement: ")


class BaselineConditionsSignature(dspy.Signature):
    """
    Extracted facts for Baseline Conditions.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    physical_environment_5_1_1_Climate_and_Meteorology = dspy.OutputField(desc="Extract facts about 5.1.1 Climate and Meteorology", prefix="physical_environment - 5.1.1 Climate and Meteorology: ")
    physical_environment_5_1_2_Geology_and_Soils = dspy.OutputField(desc="Extract facts about 5.1.2 Geology and Soils", prefix="physical_environment - 5.1.2 Geology and Soils: ")
    physical_environment_5_1_3_Hydrology_and_Water_Resources = dspy.OutputField(desc="Extract facts about 5.1.3 Hydrology and Water Resources", prefix="physical_environment - 5.1.3 Hydrology and Water Resources: ")
    physical_environment_5_1_4_Air_Quality = dspy.OutputField(desc="Extract facts about 5.1.4 Air Quality", prefix="physical_environment - 5.1.4 Air Quality: ")
    physical_environment_5_1_5_Noise_and_Vibration = dspy.OutputField(desc="Extract facts about 5.1.5 Noise and Vibration", prefix="physical_environment - 5.1.5 Noise and Vibration: ")
    biological_environment_5_2_1_Habitat_Classification_Habitat_Type_Natural_Modified_Critical = dspy.OutputField(desc="Extract facts about Habitat Type (Natural/Modified/Critical)", prefix="biological_environment - 5.2.1 Habitat Classification - Habitat Type (Natural/Modified/Critical): ")
    biological_environment_5_2_1_Habitat_Classification_Critical_Habitat_Designation_Yes_No = dspy.OutputField(desc="Extract facts about Critical Habitat Designation (Yes/No)", prefix="biological_environment - 5.2.1 Habitat Classification - Critical Habitat Designation (Yes/No): ")
    biological_environment_5_2_1_Habitat_Classification_Critical_Habitat_Triggers = dspy.OutputField(desc="Extract facts about Critical Habitat Triggers", prefix="biological_environment - 5.2.1 Habitat Classification - Critical Habitat Triggers: ")
    biological_environment_5_2_1_Habitat_Classification_Protected_Area_Status = dspy.OutputField(desc="Extract facts about Protected Area Status", prefix="biological_environment - 5.2.1 Habitat Classification - Protected Area Status: ")
    biological_environment_5_2_1_Habitat_Classification_Protected_Area_Category_IUCN = dspy.OutputField(desc="Extract facts about Protected Area Category (IUCN)", prefix="biological_environment - 5.2.1 Habitat Classification - Protected Area Category (IUCN): ")
    biological_environment_5_2_1_Habitat_Classification_Distance_to_Nearest_Protected_Area_km = dspy.OutputField(desc="Extract facts about Distance to Nearest Protected Area (km)", prefix="biological_environment - 5.2.1 Habitat Classification - Distance to Nearest Protected Area (km): ")
    biological_environment_5_2_1_Habitat_Classification_Ecosystem_Type = dspy.OutputField(desc="Extract facts about Ecosystem Type", prefix="biological_environment - 5.2.1 Habitat Classification - Ecosystem Type: ")
    biological_environment_5_2_1_Habitat_Classification_Habitat_Condition_Assessment = dspy.OutputField(desc="Extract facts about Habitat Condition Assessment", prefix="biological_environment - 5.2.1 Habitat Classification - Habitat Condition Assessment: ")
    biological_environment_5_2_2_Flora_and_Vegetation_Vegetation_Types_Present = dspy.OutputField(desc="Extract facts about Vegetation Types Present", prefix="biological_environment - 5.2.2 Flora and Vegetation - Vegetation Types Present: ")
    biological_environment_5_2_2_Flora_and_Vegetation_Dominant_Plant_Species = dspy.OutputField(desc="Extract facts about Dominant Plant Species", prefix="biological_environment - 5.2.2 Flora and Vegetation - Dominant Plant Species: ")
    biological_environment_5_2_2_Flora_and_Vegetation_Endemic_Plant_Species = dspy.OutputField(desc="Extract facts about Endemic Plant Species", prefix="biological_environment - 5.2.2 Flora and Vegetation - Endemic Plant Species: ")
    biological_environment_5_2_2_Flora_and_Vegetation_IUCN_Red_List_Plant_Species_Critically_Endangered = dspy.OutputField(desc="Extract facts about IUCN Red List Plant Species - Critically Endangered", prefix="biological_environment - 5.2.2 Flora and Vegetation - IUCN Red List Plant Species - Critically Endangered: ")
    biological_environment_5_2_2_Flora_and_Vegetation_IUCN_Red_List_Plant_Species_Endangered = dspy.OutputField(desc="Extract facts about IUCN Red List Plant Species - Endangered", prefix="biological_environment - 5.2.2 Flora and Vegetation - IUCN Red List Plant Species - Endangered: ")
    biological_environment_5_2_2_Flora_and_Vegetation_IUCN_Red_List_Plant_Species_Vulnerable = dspy.OutputField(desc="Extract facts about IUCN Red List Plant Species - Vulnerable", prefix="biological_environment - 5.2.2 Flora and Vegetation - IUCN Red List Plant Species - Vulnerable: ")
    biological_environment_5_2_2_Flora_and_Vegetation_Nationally_Listed_Threatened_Plant_Species = dspy.OutputField(desc="Extract facts about Nationally Listed Threatened Plant Species", prefix="biological_environment - 5.2.2 Flora and Vegetation - Nationally Listed Threatened Plant Species: ")
    biological_environment_5_2_2_Flora_and_Vegetation_Plant_Species_Richness_total_count = dspy.OutputField(desc="Extract facts about Plant Species Richness (total count)", prefix="biological_environment - 5.2.2 Flora and Vegetation - Plant Species Richness (total count): ")
    biological_environment_5_2_2_Flora_and_Vegetation_Invasive_Plant_Species = dspy.OutputField(desc="Extract facts about Invasive Plant Species", prefix="biological_environment - 5.2.2 Flora and Vegetation - Invasive Plant Species: ")
    biological_environment_5_2_2_Flora_and_Vegetation_Key_Plant_Habitats = dspy.OutputField(desc="Extract facts about Key Plant Habitats", prefix="biological_environment - 5.2.2 Flora and Vegetation - Key Plant Habitats: ")
    biological_environment_5_2_2_Flora_and_Vegetation_Forest_Cover_hectares = dspy.OutputField(desc="Extract facts about Forest Cover (hectares)", prefix="biological_environment - 5.2.2 Flora and Vegetation - Forest Cover (hectares): ")
    biological_environment_5_2_2_Flora_and_Vegetation_Wetland_Vegetation = dspy.OutputField(desc="Extract facts about Wetland Vegetation", prefix="biological_environment - 5.2.2 Flora and Vegetation - Wetland Vegetation: ")
    biological_environment_5_2_3_Fauna_Dominant_Animal_Species = dspy.OutputField(desc="Extract facts about Dominant Animal Species", prefix="biological_environment - 5.2.3 Fauna - Dominant Animal Species: ")
    biological_environment_5_2_3_Fauna_Endemic_Animal_Species = dspy.OutputField(desc="Extract facts about Endemic Animal Species", prefix="biological_environment - 5.2.3 Fauna - Endemic Animal Species: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Mammals_Critically_Endangered = dspy.OutputField(desc="Extract facts about IUCN Red List Mammals - Critically Endangered", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Mammals - Critically Endangered: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Mammals_Endangered = dspy.OutputField(desc="Extract facts about IUCN Red List Mammals - Endangered", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Mammals - Endangered: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Mammals_Vulnerable = dspy.OutputField(desc="Extract facts about IUCN Red List Mammals - Vulnerable", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Mammals - Vulnerable: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Birds_Critically_Endangered = dspy.OutputField(desc="Extract facts about IUCN Red List Birds - Critically Endangered", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Birds - Critically Endangered: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Birds_Endangered = dspy.OutputField(desc="Extract facts about IUCN Red List Birds - Endangered", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Birds - Endangered: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Birds_Vulnerable = dspy.OutputField(desc="Extract facts about IUCN Red List Birds - Vulnerable", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Birds - Vulnerable: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Reptiles_Critically_Endangered = dspy.OutputField(desc="Extract facts about IUCN Red List Reptiles - Critically Endangered", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Reptiles - Critically Endangered: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Reptiles_Endangered = dspy.OutputField(desc="Extract facts about IUCN Red List Reptiles - Endangered", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Reptiles - Endangered: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Reptiles_Vulnerable = dspy.OutputField(desc="Extract facts about IUCN Red List Reptiles - Vulnerable", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Reptiles - Vulnerable: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Amphibians_Critically_Endangered = dspy.OutputField(desc="Extract facts about IUCN Red List Amphibians - Critically Endangered", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Amphibians - Critically Endangered: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Amphibians_Endangered = dspy.OutputField(desc="Extract facts about IUCN Red List Amphibians - Endangered", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Amphibians - Endangered: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Amphibians_Vulnerable = dspy.OutputField(desc="Extract facts about IUCN Red List Amphibians - Vulnerable", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Amphibians - Vulnerable: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Fish_Critically_Endangered = dspy.OutputField(desc="Extract facts about IUCN Red List Fish - Critically Endangered", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Fish - Critically Endangered: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Fish_Endangered = dspy.OutputField(desc="Extract facts about IUCN Red List Fish - Endangered", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Fish - Endangered: ")
    biological_environment_5_2_3_Fauna_IUCN_Red_List_Fish_Vulnerable = dspy.OutputField(desc="Extract facts about IUCN Red List Fish - Vulnerable", prefix="biological_environment - 5.2.3 Fauna - IUCN Red List Fish - Vulnerable: ")
    biological_environment_5_2_3_Fauna_Nationally_Listed_Threatened_Animal_Species = dspy.OutputField(desc="Extract facts about Nationally Listed Threatened Animal Species", prefix="biological_environment - 5.2.3 Fauna - Nationally Listed Threatened Animal Species: ")
    biological_environment_5_2_3_Fauna_Migratory_Species = dspy.OutputField(desc="Extract facts about Migratory Species", prefix="biological_environment - 5.2.3 Fauna - Migratory Species: ")
    biological_environment_5_2_3_Fauna_Species_of_Economic_Importance = dspy.OutputField(desc="Extract facts about Species of Economic Importance", prefix="biological_environment - 5.2.3 Fauna - Species of Economic Importance: ")
    biological_environment_5_2_3_Fauna_Invasive_Animal_Species = dspy.OutputField(desc="Extract facts about Invasive Animal Species", prefix="biological_environment - 5.2.3 Fauna - Invasive Animal Species: ")
    biological_environment_5_2_4_Aquatic_Biodiversity_Aquatic_Habitat_Types = dspy.OutputField(desc="Extract facts about Aquatic Habitat Types", prefix="biological_environment - 5.2.4 Aquatic Biodiversity - Aquatic Habitat Types: ")
    biological_environment_5_2_4_Aquatic_Biodiversity_Dominant_Fish_Species = dspy.OutputField(desc="Extract facts about Dominant Fish Species", prefix="biological_environment - 5.2.4 Aquatic Biodiversity - Dominant Fish Species: ")
    biological_environment_5_2_4_Aquatic_Biodiversity_Endemic_Fish_Species = dspy.OutputField(desc="Extract facts about Endemic Fish Species", prefix="biological_environment - 5.2.4 Aquatic Biodiversity - Endemic Fish Species: ")
    biological_environment_5_2_4_Aquatic_Biodiversity_Fish_Species_Richness = dspy.OutputField(desc="Extract facts about Fish Species Richness", prefix="biological_environment - 5.2.4 Aquatic Biodiversity - Fish Species Richness: ")
    biological_environment_5_2_4_Aquatic_Biodiversity_Macroinvertebrate_Diversity = dspy.OutputField(desc="Extract facts about Macroinvertebrate Diversity", prefix="biological_environment - 5.2.4 Aquatic Biodiversity - Macroinvertebrate Diversity: ")
    biological_environment_5_2_4_Aquatic_Biodiversity_Aquatic_Vegetation = dspy.OutputField(desc="Extract facts about Aquatic Vegetation", prefix="biological_environment - 5.2.4 Aquatic Biodiversity - Aquatic Vegetation: ")
    biological_environment_5_2_4_Aquatic_Biodiversity_Spawning_Areas = dspy.OutputField(desc="Extract facts about Spawning Areas", prefix="biological_environment - 5.2.4 Aquatic Biodiversity - Spawning Areas: ")
    biological_environment_5_2_4_Aquatic_Biodiversity_Migration_Routes = dspy.OutputField(desc="Extract facts about Migration Routes", prefix="biological_environment - 5.2.4 Aquatic Biodiversity - Migration Routes: ")
    biological_environment_5_2_5_Ecosystems_and_Ecological_Functions_Key_Ecosystem_Services = dspy.OutputField(desc="Extract facts about Key Ecosystem Services", prefix="biological_environment - 5.2.5 Ecosystems and Ecological Functions - Key Ecosystem Services: ")
    biological_environment_5_2_5_Ecosystems_and_Ecological_Functions_Ecological_Connectivity = dspy.OutputField(desc="Extract facts about Ecological Connectivity", prefix="biological_environment - 5.2.5 Ecosystems and Ecological Functions - Ecological Connectivity: ")
    biological_environment_5_2_5_Ecosystems_and_Ecological_Functions_Wildlife_Corridors = dspy.OutputField(desc="Extract facts about Wildlife Corridors", prefix="biological_environment - 5.2.5 Ecosystems and Ecological Functions - Wildlife Corridors: ")
    biological_environment_5_2_5_Ecosystems_and_Ecological_Functions_Breeding_Sites = dspy.OutputField(desc="Extract facts about Breeding Sites", prefix="biological_environment - 5.2.5 Ecosystems and Ecological Functions - Breeding Sites: ")
    biological_environment_5_2_5_Ecosystems_and_Ecological_Functions_Feeding_Areas = dspy.OutputField(desc="Extract facts about Feeding Areas", prefix="biological_environment - 5.2.5 Ecosystems and Ecological Functions - Feeding Areas: ")
    biological_environment_5_2_5_Ecosystems_and_Ecological_Functions_Roosting_Sites = dspy.OutputField(desc="Extract facts about Roosting Sites", prefix="biological_environment - 5.2.5 Ecosystems and Ecological Functions - Roosting Sites: ")
    biological_environment_5_2_5_Ecosystems_and_Ecological_Functions_Ecosystem_Integrity_Assessment = dspy.OutputField(desc="Extract facts about Ecosystem Integrity Assessment", prefix="biological_environment - 5.2.5 Ecosystems and Ecological Functions - Ecosystem Integrity Assessment: ")
    biological_environment_5_2_6_Biodiversity_Surveys_Survey_Methods_Used = dspy.OutputField(desc="Extract facts about Survey Methods Used", prefix="biological_environment - 5.2.6 Biodiversity Surveys - Survey Methods Used: ")
    biological_environment_5_2_6_Biodiversity_Surveys_Survey_Duration_and_Seasonality = dspy.OutputField(desc="Extract facts about Survey Duration and Seasonality", prefix="biological_environment - 5.2.6 Biodiversity Surveys - Survey Duration and Seasonality: ")
    biological_environment_5_2_6_Biodiversity_Surveys_Survey_Coverage_Area_hectares = dspy.OutputField(desc="Extract facts about Survey Coverage Area (hectares)", prefix="biological_environment - 5.2.6 Biodiversity Surveys - Survey Coverage Area (hectares): ")
    biological_environment_5_2_6_Biodiversity_Surveys_Survey_Limitations = dspy.OutputField(desc="Extract facts about Survey Limitations", prefix="biological_environment - 5.2.6 Biodiversity Surveys - Survey Limitations: ")
    biological_environment_5_2_6_Biodiversity_Surveys_Baseline_Biodiversity_Indices_Shannon_Simpson = dspy.OutputField(desc="Extract facts about Baseline Biodiversity Indices (Shannon/Simpson)", prefix="biological_environment - 5.2.6 Biodiversity Surveys - Baseline Biodiversity Indices (Shannon/Simpson): ")
    socio_economic_environment_5_3_1_Demography_and_Settlements_Total_Population_in_Project_Area = dspy.OutputField(desc="Extract facts about Total Population in Project Area", prefix="socio_economic_environment - 5.3.1 Demography and Settlements - Total Population in Project Area: ")
    socio_economic_environment_5_3_1_Demography_and_Settlements_Population_Density = dspy.OutputField(desc="Extract facts about Population Density", prefix="socio_economic_environment - 5.3.1 Demography and Settlements - Population Density: ")
    socio_economic_environment_5_3_1_Demography_and_Settlements_Population_Growth_Rate = dspy.OutputField(desc="Extract facts about Population Growth Rate", prefix="socio_economic_environment - 5.3.1 Demography and Settlements - Population Growth Rate: ")
    socio_economic_environment_5_3_1_Demography_and_Settlements_Age_Structure_0_14_15_64_65 = dspy.OutputField(desc="Extract facts about Age Structure (0-14, 15-64, 65+)", prefix="socio_economic_environment - 5.3.1 Demography and Settlements - Age Structure (0-14, 15-64, 65+): ")
    socio_economic_environment_5_3_1_Demography_and_Settlements_Gender_Ratio = dspy.OutputField(desc="Extract facts about Gender Ratio", prefix="socio_economic_environment - 5.3.1 Demography and Settlements - Gender Ratio: ")
    socio_economic_environment_5_3_1_Demography_and_Settlements_Ethnic_Composition = dspy.OutputField(desc="Extract facts about Ethnic Composition", prefix="socio_economic_environment - 5.3.1 Demography and Settlements - Ethnic Composition: ")
    socio_economic_environment_5_3_1_Demography_and_Settlements_Religious_Groups = dspy.OutputField(desc="Extract facts about Religious Groups", prefix="socio_economic_environment - 5.3.1 Demography and Settlements - Religious Groups: ")
    socio_economic_environment_5_3_1_Demography_and_Settlements_Vulnerable_Groups_Women_headed_households_Elderly_Disabled = dspy.OutputField(desc="Extract facts about Vulnerable Groups (Women-headed households, Elderly, Disabled)", prefix="socio_economic_environment - 5.3.1 Demography and Settlements - Vulnerable Groups (Women-headed households, Elderly, Disabled): ")
    socio_economic_environment_5_3_1_Demography_and_Settlements_Settlement_Types_Urban_Rural_Peri_urban = dspy.OutputField(desc="Extract facts about Settlement Types (Urban/Rural/Peri-urban)", prefix="socio_economic_environment - 5.3.1 Demography and Settlements - Settlement Types (Urban/Rural/Peri-urban): ")
    socio_economic_environment_5_3_1_Demography_and_Settlements_Migration_Patterns_In_migration_Out_migration = dspy.OutputField(desc="Extract facts about Migration Patterns (In-migration/Out-migration)", prefix="socio_economic_environment - 5.3.1 Demography and Settlements - Migration Patterns (In-migration/Out-migration): ")
    socio_economic_environment_5_3_1_Demography_and_Settlements_Average_Household_Size = dspy.OutputField(desc="Extract facts about Average Household Size", prefix="socio_economic_environment - 5.3.1 Demography and Settlements - Average Household Size: ")
    socio_economic_environment_5_3_1_Demography_and_Settlements_Indigenous_Peoples_Presence_Yes_No = dspy.OutputField(desc="Extract facts about Indigenous Peoples Presence (Yes/No)", prefix="socio_economic_environment - 5.3.1 Demography and Settlements - Indigenous Peoples Presence (Yes/No): ")
    socio_economic_environment_5_3_2_Land_Use_and_Tenure_Land_Tenure_Systems_Customary_Statutory_Mixed = dspy.OutputField(desc="Extract facts about Land Tenure Systems (Customary/Statutory/Mixed)", prefix="socio_economic_environment - 5.3.2 Land Use and Tenure - Land Tenure Systems (Customary/Statutory/Mixed): ")
    socio_economic_environment_5_3_2_Land_Use_and_Tenure_Land_Ownership_Patterns = dspy.OutputField(desc="Extract facts about Land Ownership Patterns", prefix="socio_economic_environment - 5.3.2 Land Use and Tenure - Land Ownership Patterns: ")
    socio_economic_environment_5_3_2_Land_Use_and_Tenure_Major_Land_Use_Types_Agriculture_Grazing_Residential_Forestry = dspy.OutputField(desc="Extract facts about Major Land Use Types (Agriculture/Grazing/Residential/Forestry)", prefix="socio_economic_environment - 5.3.2 Land Use and Tenure - Major Land Use Types (Agriculture/Grazing/Residential/Forestry): ")
    socio_economic_environment_5_3_2_Land_Use_and_Tenure_Agricultural_Practices_Subsistence_Commercial = dspy.OutputField(desc="Extract facts about Agricultural Practices (Subsistence/Commercial)", prefix="socio_economic_environment - 5.3.2 Land Use and Tenure - Agricultural Practices (Subsistence/Commercial): ")
    socio_economic_environment_5_3_2_Land_Use_and_Tenure_Crop_Types = dspy.OutputField(desc="Extract facts about Crop Types", prefix="socio_economic_environment - 5.3.2 Land Use and Tenure - Crop Types: ")
    socio_economic_environment_5_3_2_Land_Use_and_Tenure_Livestock_Ownership = dspy.OutputField(desc="Extract facts about Livestock Ownership", prefix="socio_economic_environment - 5.3.2 Land Use and Tenure - Livestock Ownership: ")
    socio_economic_environment_5_3_2_Land_Use_and_Tenure_Natural_Resource_Usage_Hunting_Gathering_Fishing = dspy.OutputField(desc="Extract facts about Natural Resource Usage (Hunting/Gathering/Fishing)", prefix="socio_economic_environment - 5.3.2 Land Use and Tenure - Natural Resource Usage (Hunting/Gathering/Fishing): ")
    socio_economic_environment_5_3_2_Land_Use_and_Tenure_Common_Property_Resources = dspy.OutputField(desc="Extract facts about Common Property Resources", prefix="socio_economic_environment - 5.3.2 Land Use and Tenure - Common Property Resources: ")
    socio_economic_environment_5_3_2_Land_Use_and_Tenure_Land_Conflicts_or_Disputes = dspy.OutputField(desc="Extract facts about Land Conflicts or Disputes", prefix="socio_economic_environment - 5.3.2 Land Use and Tenure - Land Conflicts or Disputes: ")
    socio_economic_environment_5_3_3_Economic_Activities_and_Livelihoods_Primary_Livelihood_Activities = dspy.OutputField(desc="Extract facts about Primary Livelihood Activities", prefix="socio_economic_environment - 5.3.3 Economic Activities and Livelihoods - Primary Livelihood Activities: ")
    socio_economic_environment_5_3_3_Economic_Activities_and_Livelihoods_Secondary_Livelihood_Activities = dspy.OutputField(desc="Extract facts about Secondary Livelihood Activities", prefix="socio_economic_environment - 5.3.3 Economic Activities and Livelihoods - Secondary Livelihood Activities: ")
    socio_economic_environment_5_3_3_Economic_Activities_and_Livelihoods_Employment_Rates_Formal_Informal = dspy.OutputField(desc="Extract facts about Employment Rates (Formal/Informal)", prefix="socio_economic_environment - 5.3.3 Economic Activities and Livelihoods - Employment Rates (Formal/Informal): ")
    socio_economic_environment_5_3_3_Economic_Activities_and_Livelihoods_Unemployment_Rates = dspy.OutputField(desc="Extract facts about Unemployment Rates", prefix="socio_economic_environment - 5.3.3 Economic Activities and Livelihoods - Unemployment Rates: ")
    socio_economic_environment_5_3_3_Economic_Activities_and_Livelihoods_Average_Income_Levels = dspy.OutputField(desc="Extract facts about Average Income Levels", prefix="socio_economic_environment - 5.3.3 Economic Activities and Livelihoods - Average Income Levels: ")
    socio_economic_environment_5_3_3_Economic_Activities_and_Livelihoods_Poverty_Rates = dspy.OutputField(desc="Extract facts about Poverty Rates", prefix="socio_economic_environment - 5.3.3 Economic Activities and Livelihoods - Poverty Rates: ")
    socio_economic_environment_5_3_3_Economic_Activities_and_Livelihoods_Subsistence_Activities = dspy.OutputField(desc="Extract facts about Subsistence Activities", prefix="socio_economic_environment - 5.3.3 Economic Activities and Livelihoods - Subsistence Activities: ")
    socio_economic_environment_5_3_3_Economic_Activities_and_Livelihoods_Market_Access_and_Value_Chains = dspy.OutputField(desc="Extract facts about Market Access and Value Chains", prefix="socio_economic_environment - 5.3.3 Economic Activities and Livelihoods - Market Access and Value Chains: ")
    socio_economic_environment_5_3_3_Economic_Activities_and_Livelihoods_Economic_Vulnerability_Factors = dspy.OutputField(desc="Extract facts about Economic Vulnerability Factors", prefix="socio_economic_environment - 5.3.3 Economic Activities and Livelihoods - Economic Vulnerability Factors: ")
    socio_economic_environment_5_3_3_Economic_Activities_and_Livelihoods_Local_Business_Enterprises = dspy.OutputField(desc="Extract facts about Local Business Enterprises", prefix="socio_economic_environment - 5.3.3 Economic Activities and Livelihoods - Local Business Enterprises: ")
    socio_economic_environment_5_3_4_Public_Health_Health_Infrastructure_Hospitals_Clinics_Health_Posts = dspy.OutputField(desc="Extract facts about Health Infrastructure (Hospitals/Clinics/Health Posts)", prefix="socio_economic_environment - 5.3.4 Public Health - Health Infrastructure (Hospitals/Clinics/Health Posts): ")
    socio_economic_environment_5_3_4_Public_Health_Distance_to_Nearest_Health_Facility = dspy.OutputField(desc="Extract facts about Distance to Nearest Health Facility", prefix="socio_economic_environment - 5.3.4 Public Health - Distance to Nearest Health Facility: ")
    socio_economic_environment_5_3_4_Public_Health_Prevalent_Diseases_Malaria_HIV_AIDS_TB_Waterborne = dspy.OutputField(desc="Extract facts about Prevalent Diseases (Malaria/HIV/AIDS/TB/Waterborne)", prefix="socio_economic_environment - 5.3.4 Public Health - Prevalent Diseases (Malaria/HIV/AIDS/TB/Waterborne): ")
    socio_economic_environment_5_3_4_Public_Health_Maternal_Health_Indicators = dspy.OutputField(desc="Extract facts about Maternal Health Indicators", prefix="socio_economic_environment - 5.3.4 Public Health - Maternal Health Indicators: ")
    socio_economic_environment_5_3_4_Public_Health_Child_Mortality_Rates = dspy.OutputField(desc="Extract facts about Child Mortality Rates", prefix="socio_economic_environment - 5.3.4 Public Health - Child Mortality Rates: ")
    socio_economic_environment_5_3_4_Public_Health_Access_to_Clean_Water_Sources = dspy.OutputField(desc="Extract facts about Access to Clean Water Sources", prefix="socio_economic_environment - 5.3.4 Public Health - Access to Clean Water Sources: ")
    socio_economic_environment_5_3_4_Public_Health_Sanitation_Facilities_Coverage = dspy.OutputField(desc="Extract facts about Sanitation Facilities Coverage", prefix="socio_economic_environment - 5.3.4 Public Health - Sanitation Facilities Coverage: ")
    socio_economic_environment_5_3_4_Public_Health_Nutrition_Status_and_Food_Security = dspy.OutputField(desc="Extract facts about Nutrition Status and Food Security", prefix="socio_economic_environment - 5.3.4 Public Health - Nutrition Status and Food Security: ")
    socio_economic_environment_5_3_4_Public_Health_Health_Seeking_Behavior = dspy.OutputField(desc="Extract facts about Health Seeking Behavior", prefix="socio_economic_environment - 5.3.4 Public Health - Health Seeking Behavior: ")
    socio_economic_environment_5_3_5_Cultural_Heritage_Tangible_Heritage_Sites_Archaeological_Historical_Religious = dspy.OutputField(desc="Extract facts about Tangible Heritage Sites (Archaeological/Historical/Religious)", prefix="socio_economic_environment - 5.3.5 Cultural Heritage - Tangible Heritage Sites (Archaeological/Historical/Religious): ")
    socio_economic_environment_5_3_5_Cultural_Heritage_Intangible_Heritage_Traditions_Festivals_Language = dspy.OutputField(desc="Extract facts about Intangible Heritage (Traditions/Festivals/Language)", prefix="socio_economic_environment - 5.3.5 Cultural Heritage - Intangible Heritage (Traditions/Festivals/Language): ")
    socio_economic_environment_5_3_5_Cultural_Heritage_Sacred_Sites_Graves_Shrines_Sacred_Groves = dspy.OutputField(desc="Extract facts about Sacred Sites (Graves/Shrines/Sacred Groves)", prefix="socio_economic_environment - 5.3.5 Cultural Heritage - Sacred Sites (Graves/Shrines/Sacred Groves): ")
    socio_economic_environment_5_3_5_Cultural_Heritage_Chance_Find_Procedures_Existing_Proposed = dspy.OutputField(desc="Extract facts about Chance Find Procedures (Existing/Proposed)", prefix="socio_economic_environment - 5.3.5 Cultural Heritage - Chance Find Procedures (Existing/Proposed): ")
    socio_economic_environment_5_3_5_Cultural_Heritage_Cultural_Significance_of_Landscape = dspy.OutputField(desc="Extract facts about Cultural Significance of Landscape", prefix="socio_economic_environment - 5.3.5 Cultural Heritage - Cultural Significance of Landscape: ")
    socio_economic_environment_5_3_5_Cultural_Heritage_Archaeological_Potential_of_Area = dspy.OutputField(desc="Extract facts about Archaeological Potential of Area", prefix="socio_economic_environment - 5.3.5 Cultural Heritage - Archaeological Potential of Area: ")
    socio_economic_environment_5_3_6_Infrastructure_and_Services_Road_Network_Condition_and_Access = dspy.OutputField(desc="Extract facts about Road Network Condition and Access", prefix="socio_economic_environment - 5.3.6 Infrastructure and Services - Road Network Condition and Access: ")
    socio_economic_environment_5_3_6_Infrastructure_and_Services_Transport_Services_Availability = dspy.OutputField(desc="Extract facts about Transport Services Availability", prefix="socio_economic_environment - 5.3.6 Infrastructure and Services - Transport Services Availability: ")
    socio_economic_environment_5_3_6_Infrastructure_and_Services_Energy_Access_Electricity_Grid_Off_grid_Fuel = dspy.OutputField(desc="Extract facts about Energy Access (Electricity Grid/Off-grid/Fuel)", prefix="socio_economic_environment - 5.3.6 Infrastructure and Services - Energy Access (Electricity Grid/Off-grid/Fuel): ")
    socio_economic_environment_5_3_6_Infrastructure_and_Services_Education_Facilities_Schools_Vocational_Training = dspy.OutputField(desc="Extract facts about Education Facilities (Schools/Vocational Training)", prefix="socio_economic_environment - 5.3.6 Infrastructure and Services - Education Facilities (Schools/Vocational Training): ")
    socio_economic_environment_5_3_6_Infrastructure_and_Services_Literacy_Rates = dspy.OutputField(desc="Extract facts about Literacy Rates", prefix="socio_economic_environment - 5.3.6 Infrastructure and Services - Literacy Rates: ")
    socio_economic_environment_5_3_6_Infrastructure_and_Services_Telecommunications_Coverage = dspy.OutputField(desc="Extract facts about Telecommunications Coverage", prefix="socio_economic_environment - 5.3.6 Infrastructure and Services - Telecommunications Coverage: ")
    socio_economic_environment_5_3_6_Infrastructure_and_Services_Waste_Management_Services = dspy.OutputField(desc="Extract facts about Waste Management Services", prefix="socio_economic_environment - 5.3.6 Infrastructure and Services - Waste Management Services: ")
    socio_economic_environment_5_3_6_Infrastructure_and_Services_Social_Services_Police_Fire_Community_Centers = dspy.OutputField(desc="Extract facts about Social Services (Police/Fire/Community Centers)", prefix="socio_economic_environment - 5.3.6 Infrastructure and Services - Social Services (Police/Fire/Community Centers): ")
    socio_economic_environment_5_3_6_Infrastructure_and_Services_Housing_Conditions = dspy.OutputField(desc="Extract facts about Housing Conditions", prefix="socio_economic_environment - 5.3.6 Infrastructure and Services - Housing Conditions: ")


class BridgeAndTunnelConstructionSignature(dspy.Signature):
    """
    Extracted facts for Bridge And Tunnel Construction.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Structural_Integrity = dspy.OutputField(desc="Extract facts about Structural Integrity", prefix="Structural Integrity: ")
    Geotechnical_Stability = dspy.OutputField(desc="Extract facts about Geotechnical Stability", prefix="Geotechnical Stability: ")


class CoalPowerSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Coal Power Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Air_Emissions = dspy.OutputField(desc="Extract facts about Air Emissions, specifically: SOx Emissions, NOx Emissions, Particulate Matter (PM10, PM2.5), Mercury Emissions", prefix="Air Emissions: ")
    Ash_Management = dspy.OutputField(desc="Extract facts about Ash Management, specifically: Fly Ash Disposal, Bottom Ash Storage, Ash Pond Stability, Leachate Management", prefix="Ash Management: ")
    Thermal_Discharge = dspy.OutputField(desc="Extract facts about Thermal Discharge, specifically: Cooling Water Temperature, Mixing Zone, Impact on Aquatic Life", prefix="Thermal Discharge: ")


class ConclusionAndRecommendationsSignature(dspy.Signature):
    """
    Extracted facts for Conclusion And Recommendations.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    overall_conclusion_Summary_of_Project_Description = dspy.OutputField(desc="Extract facts about Summary of Project Description", prefix="overall_conclusion - Summary of Project Description: ")
    overall_conclusion_Summary_of_Key_Environmental_Impacts = dspy.OutputField(desc="Extract facts about Summary of Key Environmental Impacts", prefix="overall_conclusion - Summary of Key Environmental Impacts: ")
    overall_conclusion_Summary_of_Key_Social_Impacts = dspy.OutputField(desc="Extract facts about Summary of Key Social Impacts", prefix="overall_conclusion - Summary of Key Social Impacts: ")
    overall_conclusion_Summary_of_Mitigation_Measures = dspy.OutputField(desc="Extract facts about Summary of Mitigation Measures", prefix="overall_conclusion - Summary of Mitigation Measures: ")
    overall_conclusion_Residual_Impacts_after_Mitigation = dspy.OutputField(desc="Extract facts about Residual Impacts after Mitigation", prefix="overall_conclusion - Residual Impacts after Mitigation: ")
    overall_conclusion_Overall_Environmental_and_Social_Feasibility = dspy.OutputField(desc="Extract facts about Overall Environmental and Social Feasibility", prefix="overall_conclusion - Overall Environmental and Social Feasibility: ")
    recommendations_for_project_approval_Conditions_for_Environmental_Approval = dspy.OutputField(desc="Extract facts about Conditions for Environmental Approval", prefix="recommendations_for_project_approval - Conditions for Environmental Approval: ")
    recommendations_for_project_approval_Conditions_for_Social_Approval = dspy.OutputField(desc="Extract facts about Conditions for Social Approval", prefix="recommendations_for_project_approval - Conditions for Social Approval: ")
    recommendations_for_project_approval_Key_Permits_and_Licenses_Required = dspy.OutputField(desc="Extract facts about Key Permits and Licenses Required", prefix="recommendations_for_project_approval - Key Permits and Licenses Required: ")
    recommendations_for_project_approval_Monitoring_and_Reporting_Requirements = dspy.OutputField(desc="Extract facts about Monitoring and Reporting Requirements", prefix="recommendations_for_project_approval - Monitoring and Reporting Requirements: ")
    recommendations_for_esmp_implementation_Institutional_Arrangements = dspy.OutputField(desc="Extract facts about Institutional Arrangements", prefix="recommendations_for_esmp_implementation - Institutional Arrangements: ")
    recommendations_for_esmp_implementation_Capacity_Building_Needs = dspy.OutputField(desc="Extract facts about Capacity Building Needs", prefix="recommendations_for_esmp_implementation - Capacity Building Needs: ")
    recommendations_for_esmp_implementation_Budget_Allocation = dspy.OutputField(desc="Extract facts about Budget Allocation", prefix="recommendations_for_esmp_implementation - Budget Allocation: ")
    recommendations_for_esmp_implementation_Monitoring_and_Evaluation_Framework = dspy.OutputField(desc="Extract facts about Monitoring and Evaluation Framework", prefix="recommendations_for_esmp_implementation - Monitoring and Evaluation Framework: ")
    recommendations_for_future_studies_Additional_Baseline_Studies_Required = dspy.OutputField(desc="Extract facts about Additional Baseline Studies Required", prefix="recommendations_for_future_studies - Additional Baseline Studies Required: ")
    recommendations_for_future_studies_Detailed_Design_Phase_Studies = dspy.OutputField(desc="Extract facts about Detailed Design Phase Studies", prefix="recommendations_for_future_studies - Detailed Design Phase Studies: ")
    recommendations_for_future_studies_Adaptive_Management_Triggers = dspy.OutputField(desc="Extract facts about Adaptive Management Triggers", prefix="recommendations_for_future_studies - Adaptive Management Triggers: ")


class DecommissioningSignature(dspy.Signature):
    """
    Extracted facts for Decommissioning.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Decommissioning_Bonds = dspy.OutputField(desc="Extract facts about Decommissioning Bonds, specifically: Financial Provision, Site Restoration", prefix="Decommissioning Bonds: ")


class ElectromagneticFieldsEmfSignature(dspy.Signature):
    """
    Extracted facts for Electromagnetic Fields (Emf).
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    EMF_Assessment = dspy.OutputField(desc="Extract facts about EMF Assessment, specifically: Transmission Lines, Substations", prefix="EMF Assessment: ")


class EnvironmentalAndSocialImpactAssessmentSignature(dspy.Signature):
    """
    Extracted facts for Environmental And Social Impact Assessment.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    impact_identification_and_characterization_Impact_Scoping_Methods = dspy.OutputField(desc="Extract facts about Impact Scoping Methods", prefix="impact_identification_and_characterization - Impact Scoping Methods: ")
    impact_identification_and_characterization_Impact_Screening_Criteria = dspy.OutputField(desc="Extract facts about Impact Screening Criteria", prefix="impact_identification_and_characterization - Impact Screening Criteria: ")
    impact_identification_and_characterization_Direct_Impacts_Identified = dspy.OutputField(desc="Extract facts about Direct Impacts Identified", prefix="impact_identification_and_characterization - Direct Impacts Identified: ")
    impact_identification_and_characterization_Indirect_Impacts_Identified = dspy.OutputField(desc="Extract facts about Indirect Impacts Identified", prefix="impact_identification_and_characterization - Indirect Impacts Identified: ")
    impact_identification_and_characterization_Induced_Impacts_Identified = dspy.OutputField(desc="Extract facts about Induced Impacts Identified", prefix="impact_identification_and_characterization - Induced Impacts Identified: ")
    impact_identification_and_characterization_Cumulative_Impacts_Identified = dspy.OutputField(desc="Extract facts about Cumulative Impacts Identified", prefix="impact_identification_and_characterization - Cumulative Impacts Identified: ")
    impact_identification_and_characterization_Transboundary_Impacts_Identified = dspy.OutputField(desc="Extract facts about Transboundary Impacts Identified", prefix="impact_identification_and_characterization - Transboundary Impacts Identified: ")
    impact_identification_and_characterization_Residual_Impacts_Identified = dspy.OutputField(desc="Extract facts about Residual Impacts Identified", prefix="impact_identification_and_characterization - Residual Impacts Identified: ")
    impact_identification_and_characterization_Positive_Impacts_Benefits = dspy.OutputField(desc="Extract facts about Positive Impacts (Benefits)", prefix="impact_identification_and_characterization - Positive Impacts (Benefits): ")
    assessment_methodology_Impact_Significance_Criteria_Major_Moderate_Minor_Negligible = dspy.OutputField(desc="Extract facts about Impact Significance Criteria (Major/Moderate/Minor/Negligible)", prefix="assessment_methodology - Impact Significance Criteria (Major/Moderate/Minor/Negligible): ")
    assessment_methodology_Impact_Magnitude_Assessment_Intensity_Extent_Duration = dspy.OutputField(desc="Extract facts about Impact Magnitude Assessment (Intensity/Extent/Duration)", prefix="assessment_methodology - Impact Magnitude Assessment (Intensity/Extent/Duration): ")
    assessment_methodology_Receptor_Sensitivity_Assessment_High_Medium_Low = dspy.OutputField(desc="Extract facts about Receptor Sensitivity Assessment (High/Medium/Low)", prefix="assessment_methodology - Receptor Sensitivity Assessment (High/Medium/Low): ")
    assessment_methodology_Impact_Probability_Assessment = dspy.OutputField(desc="Extract facts about Impact Probability Assessment", prefix="assessment_methodology - Impact Probability Assessment: ")
    assessment_methodology_Impact_Assessment_Matrices = dspy.OutputField(desc="Extract facts about Impact Assessment Matrices", prefix="assessment_methodology - Impact Assessment Matrices: ")
    assessment_methodology_Mathematical_Modeling_Used_e_g_Air_Dispersion_Noise = dspy.OutputField(desc="Extract facts about Mathematical Modeling Used (e.g., Air Dispersion, Noise)", prefix="assessment_methodology - Mathematical Modeling Used (e.g., Air Dispersion, Noise): ")
    assessment_methodology_Expert_Judgment_Application = dspy.OutputField(desc="Extract facts about Expert Judgment Application", prefix="assessment_methodology - Expert Judgment Application: ")
    assessment_methodology_Stakeholder_Input_in_Assessment = dspy.OutputField(desc="Extract facts about Stakeholder Input in Assessment", prefix="assessment_methodology - Stakeholder Input in Assessment: ")
    potential_impacts_on_physical_environment_6_3_1_Air_Quality_and_Climate_Dust_Emissions_Construction_Operation = dspy.OutputField(desc="Extract facts about Dust Emissions (Construction/Operation)", prefix="potential_impacts_on_physical_environment - 6.3.1 Air Quality and Climate - Dust Emissions (Construction/Operation): ")
    potential_impacts_on_physical_environment_6_3_1_Air_Quality_and_Climate_Gaseous_Emissions_NOx_SOx_CO_VOCs = dspy.OutputField(desc="Extract facts about Gaseous Emissions (NOx, SOx, CO, VOCs)", prefix="potential_impacts_on_physical_environment - 6.3.1 Air Quality and Climate - Gaseous Emissions (NOx, SOx, CO, VOCs): ")
    potential_impacts_on_physical_environment_6_3_1_Air_Quality_and_Climate_Greenhouse_Gas_Emissions_CO2e = dspy.OutputField(desc="Extract facts about Greenhouse Gas Emissions (CO2e)", prefix="potential_impacts_on_physical_environment - 6.3.1 Air Quality and Climate - Greenhouse Gas Emissions (CO2e): ")
    potential_impacts_on_physical_environment_6_3_1_Air_Quality_and_Climate_Odor_Impacts = dspy.OutputField(desc="Extract facts about Odor Impacts", prefix="potential_impacts_on_physical_environment - 6.3.1 Air Quality and Climate - Odor Impacts: ")
    potential_impacts_on_physical_environment_6_3_1_Air_Quality_and_Climate_Impacts_on_Sensitive_Receptors_Schools_Hospitals = dspy.OutputField(desc="Extract facts about Impacts on Sensitive Receptors (Schools/Hospitals)", prefix="potential_impacts_on_physical_environment - 6.3.1 Air Quality and Climate - Impacts on Sensitive Receptors (Schools/Hospitals): ")
    potential_impacts_on_physical_environment_6_3_2_Noise_and_Vibration_Construction_Noise_Levels_dB = dspy.OutputField(desc="Extract facts about Construction Noise Levels (dB)", prefix="potential_impacts_on_physical_environment - 6.3.2 Noise and Vibration - Construction Noise Levels (dB): ")
    potential_impacts_on_physical_environment_6_3_2_Noise_and_Vibration_Operational_Noise_Levels_dB = dspy.OutputField(desc="Extract facts about Operational Noise Levels (dB)", prefix="potential_impacts_on_physical_environment - 6.3.2 Noise and Vibration - Operational Noise Levels (dB): ")
    potential_impacts_on_physical_environment_6_3_2_Noise_and_Vibration_Vibration_Impacts_PPV = dspy.OutputField(desc="Extract facts about Vibration Impacts (PPV)", prefix="potential_impacts_on_physical_environment - 6.3.2 Noise and Vibration - Vibration Impacts (PPV): ")
    potential_impacts_on_physical_environment_6_3_2_Noise_and_Vibration_Blasting_Impacts_if_applicable = dspy.OutputField(desc="Extract facts about Blasting Impacts (if applicable)", prefix="potential_impacts_on_physical_environment - 6.3.2 Noise and Vibration - Blasting Impacts (if applicable): ")
    potential_impacts_on_physical_environment_6_3_2_Noise_and_Vibration_Traffic_Noise_Impacts = dspy.OutputField(desc="Extract facts about Traffic Noise Impacts", prefix="potential_impacts_on_physical_environment - 6.3.2 Noise and Vibration - Traffic Noise Impacts: ")
    potential_impacts_on_physical_environment_6_3_3_Surface_Water_and_Hydrology_Changes_in_Flow_Regime = dspy.OutputField(desc="Extract facts about Changes in Flow Regime", prefix="potential_impacts_on_physical_environment - 6.3.3 Surface Water and Hydrology - Changes in Flow Regime: ")
    potential_impacts_on_physical_environment_6_3_3_Surface_Water_and_Hydrology_Water_Quality_Degradation_Sediment_Chemicals = dspy.OutputField(desc="Extract facts about Water Quality Degradation (Sediment/Chemicals)", prefix="potential_impacts_on_physical_environment - 6.3.3 Surface Water and Hydrology - Water Quality Degradation (Sediment/Chemicals): ")
    potential_impacts_on_physical_environment_6_3_3_Surface_Water_and_Hydrology_Impacts_on_Downstream_Users = dspy.OutputField(desc="Extract facts about Impacts on Downstream Users", prefix="potential_impacts_on_physical_environment - 6.3.3 Surface Water and Hydrology - Impacts on Downstream Users: ")
    potential_impacts_on_physical_environment_6_3_3_Surface_Water_and_Hydrology_Flood_Risk_Alteration = dspy.OutputField(desc="Extract facts about Flood Risk Alteration", prefix="potential_impacts_on_physical_environment - 6.3.3 Surface Water and Hydrology - Flood Risk Alteration: ")
    potential_impacts_on_physical_environment_6_3_3_Surface_Water_and_Hydrology_River_Morphology_Changes = dspy.OutputField(desc="Extract facts about River Morphology Changes", prefix="potential_impacts_on_physical_environment - 6.3.3 Surface Water and Hydrology - River Morphology Changes: ")
    potential_impacts_on_physical_environment_6_3_4_Groundwater_and_Soils_Groundwater_Level_Drawdown = dspy.OutputField(desc="Extract facts about Groundwater Level Drawdown", prefix="potential_impacts_on_physical_environment - 6.3.4 Groundwater and Soils - Groundwater Level Drawdown: ")
    potential_impacts_on_physical_environment_6_3_4_Groundwater_and_Soils_Groundwater_Contamination_Risk = dspy.OutputField(desc="Extract facts about Groundwater Contamination Risk", prefix="potential_impacts_on_physical_environment - 6.3.4 Groundwater and Soils - Groundwater Contamination Risk: ")
    potential_impacts_on_physical_environment_6_3_4_Groundwater_and_Soils_Soil_Erosion_and_Sedimentation = dspy.OutputField(desc="Extract facts about Soil Erosion and Sedimentation", prefix="potential_impacts_on_physical_environment - 6.3.4 Groundwater and Soils - Soil Erosion and Sedimentation: ")
    potential_impacts_on_physical_environment_6_3_4_Groundwater_and_Soils_Soil_Contamination_Risk = dspy.OutputField(desc="Extract facts about Soil Contamination Risk", prefix="potential_impacts_on_physical_environment - 6.3.4 Groundwater and Soils - Soil Contamination Risk: ")
    potential_impacts_on_physical_environment_6_3_4_Groundwater_and_Soils_Land_Take_and_Soil_Sealing = dspy.OutputField(desc="Extract facts about Land Take and Soil Sealing", prefix="potential_impacts_on_physical_environment - 6.3.4 Groundwater and Soils - Land Take and Soil Sealing: ")
    potential_impacts_on_physical_environment_6_3_4_Groundwater_and_Soils_Impacts_on_Soil_Fertility = dspy.OutputField(desc="Extract facts about Impacts on Soil Fertility", prefix="potential_impacts_on_physical_environment - 6.3.4 Groundwater and Soils - Impacts on Soil Fertility: ")
    potential_impacts_on_physical_environment_6_3_5_Geology_and_Geohazards_Slope_Stability_Risks = dspy.OutputField(desc="Extract facts about Slope Stability Risks", prefix="potential_impacts_on_physical_environment - 6.3.5 Geology and Geohazards - Slope Stability Risks: ")
    potential_impacts_on_physical_environment_6_3_5_Geology_and_Geohazards_Seismic_Risks_Induced_Exacerbated = dspy.OutputField(desc="Extract facts about Seismic Risks Induced/Exacerbated", prefix="potential_impacts_on_physical_environment - 6.3.5 Geology and Geohazards - Seismic Risks Induced/Exacerbated: ")
    potential_impacts_on_physical_environment_6_3_5_Geology_and_Geohazards_Subsidence_Risks = dspy.OutputField(desc="Extract facts about Subsidence Risks", prefix="potential_impacts_on_physical_environment - 6.3.5 Geology and Geohazards - Subsidence Risks: ")
    potential_impacts_on_physical_environment_6_3_5_Geology_and_Geohazards_Impacts_on_Geological_Heritage = dspy.OutputField(desc="Extract facts about Impacts on Geological Heritage", prefix="potential_impacts_on_physical_environment - 6.3.5 Geology and Geohazards - Impacts on Geological Heritage: ")
    potential_impacts_on_physical_environment_6_3_6_Landscape_and_Visual_Visual_Intrusion_Impacts = dspy.OutputField(desc="Extract facts about Visual Intrusion/Impacts", prefix="potential_impacts_on_physical_environment - 6.3.6 Landscape and Visual - Visual Intrusion/Impacts: ")
    potential_impacts_on_physical_environment_6_3_6_Landscape_and_Visual_Change_in_Landscape_Character = dspy.OutputField(desc="Extract facts about Change in Landscape Character", prefix="potential_impacts_on_physical_environment - 6.3.6 Landscape and Visual - Change in Landscape Character: ")
    potential_impacts_on_physical_environment_6_3_6_Landscape_and_Visual_Light_Pollution_Glare = dspy.OutputField(desc="Extract facts about Light Pollution/Glare", prefix="potential_impacts_on_physical_environment - 6.3.6 Landscape and Visual - Light Pollution/Glare: ")
    potential_impacts_on_physical_environment_6_3_6_Landscape_and_Visual_Impacts_on_Scenic_Views = dspy.OutputField(desc="Extract facts about Impacts on Scenic Views", prefix="potential_impacts_on_physical_environment - 6.3.6 Landscape and Visual - Impacts on Scenic Views: ")
    potential_impacts_on_biological_environment_6_4_1_Habitat_Loss_and_Fragmentation_Total_Habitat_Loss_hectares = dspy.OutputField(desc="Extract facts about Total Habitat Loss (hectares)", prefix="potential_impacts_on_biological_environment - 6.4.1 Habitat Loss and Fragmentation - Total Habitat Loss (hectares): ")
    potential_impacts_on_biological_environment_6_4_1_Habitat_Loss_and_Fragmentation_Habitat_Loss_by_Type = dspy.OutputField(desc="Extract facts about Habitat Loss by Type", prefix="potential_impacts_on_biological_environment - 6.4.1 Habitat Loss and Fragmentation - Habitat Loss by Type: ")
    potential_impacts_on_biological_environment_6_4_1_Habitat_Loss_and_Fragmentation_Critical_Habitat_Affected_hectares = dspy.OutputField(desc="Extract facts about Critical Habitat Affected (hectares)", prefix="potential_impacts_on_biological_environment - 6.4.1 Habitat Loss and Fragmentation - Critical Habitat Affected (hectares): ")
    potential_impacts_on_biological_environment_6_4_1_Habitat_Loss_and_Fragmentation_Fragmentation_Effects = dspy.OutputField(desc="Extract facts about Fragmentation Effects", prefix="potential_impacts_on_biological_environment - 6.4.1 Habitat Loss and Fragmentation - Fragmentation Effects: ")
    potential_impacts_on_biological_environment_6_4_1_Habitat_Loss_and_Fragmentation_Edge_Effects = dspy.OutputField(desc="Extract facts about Edge Effects", prefix="potential_impacts_on_biological_environment - 6.4.1 Habitat Loss and Fragmentation - Edge Effects: ")
    potential_impacts_on_biological_environment_6_4_1_Habitat_Loss_and_Fragmentation_Barrier_Effects_on_Wildlife_Movement = dspy.OutputField(desc="Extract facts about Barrier Effects on Wildlife Movement", prefix="potential_impacts_on_biological_environment - 6.4.1 Habitat Loss and Fragmentation - Barrier Effects on Wildlife Movement: ")
    potential_impacts_on_biological_environment_6_4_2_Impacts_on_Flora_Vegetation_Clearing_hectares = dspy.OutputField(desc="Extract facts about Vegetation Clearing (hectares)", prefix="potential_impacts_on_biological_environment - 6.4.2 Impacts on Flora - Vegetation Clearing (hectares): ")
    potential_impacts_on_biological_environment_6_4_2_Impacts_on_Flora_Impacts_on_Dominant_Plant_Species = dspy.OutputField(desc="Extract facts about Impacts on Dominant Plant Species", prefix="potential_impacts_on_biological_environment - 6.4.2 Impacts on Flora - Impacts on Dominant Plant Species: ")
    potential_impacts_on_biological_environment_6_4_2_Impacts_on_Flora_Impacts_on_Endemic_Plant_Species = dspy.OutputField(desc="Extract facts about Impacts on Endemic Plant Species", prefix="potential_impacts_on_biological_environment - 6.4.2 Impacts on Flora - Impacts on Endemic Plant Species: ")
    potential_impacts_on_biological_environment_6_4_2_Impacts_on_Flora_Impacts_on_IUCN_Red_List_Plant_Species = dspy.OutputField(desc="Extract facts about Impacts on IUCN Red List Plant Species", prefix="potential_impacts_on_biological_environment - 6.4.2 Impacts on Flora - Impacts on IUCN Red List Plant Species: ")
    potential_impacts_on_biological_environment_6_4_2_Impacts_on_Flora_Impacts_on_Nationally_Threatened_Plants = dspy.OutputField(desc="Extract facts about Impacts on Nationally Threatened Plants", prefix="potential_impacts_on_biological_environment - 6.4.2 Impacts on Flora - Impacts on Nationally Threatened Plants: ")
    potential_impacts_on_biological_environment_6_4_3_Impacts_on_Fauna_Impacts_on_Dominant_Animal_Species = dspy.OutputField(desc="Extract facts about Impacts on Dominant Animal Species", prefix="potential_impacts_on_biological_environment - 6.4.3 Impacts on Fauna - Impacts on Dominant Animal Species: ")
    potential_impacts_on_biological_environment_6_4_3_Impacts_on_Fauna_Impacts_on_Endemic_Animal_Species = dspy.OutputField(desc="Extract facts about Impacts on Endemic Animal Species", prefix="potential_impacts_on_biological_environment - 6.4.3 Impacts on Fauna - Impacts on Endemic Animal Species: ")
    potential_impacts_on_biological_environment_6_4_3_Impacts_on_Fauna_Impacts_on_IUCN_Red_List_Species = dspy.OutputField(desc="Extract facts about Impacts on IUCN Red List Species", prefix="potential_impacts_on_biological_environment - 6.4.3 Impacts on Fauna - Impacts on IUCN Red List Species: ")
    potential_impacts_on_biological_environment_6_4_3_Impacts_on_Fauna_Impacts_on_Nationally_Threatened_Species = dspy.OutputField(desc="Extract facts about Impacts on Nationally Threatened Species", prefix="potential_impacts_on_biological_environment - 6.4.3 Impacts on Fauna - Impacts on Nationally Threatened Species: ")
    potential_impacts_on_biological_environment_6_4_3_Impacts_on_Fauna_Impacts_on_Migratory_Species = dspy.OutputField(desc="Extract facts about Impacts on Migratory Species", prefix="potential_impacts_on_biological_environment - 6.4.3 Impacts on Fauna - Impacts on Migratory Species: ")
    potential_impacts_on_biological_environment_6_4_3_Impacts_on_Fauna_Wildlife_Mortality_Risk = dspy.OutputField(desc="Extract facts about Wildlife Mortality Risk", prefix="potential_impacts_on_biological_environment - 6.4.3 Impacts on Fauna - Wildlife Mortality Risk: ")
    potential_impacts_on_biological_environment_6_4_3_Impacts_on_Fauna_Disturbance_to_Breeding_Nesting_Sites = dspy.OutputField(desc="Extract facts about Disturbance to Breeding/Nesting Sites", prefix="potential_impacts_on_biological_environment - 6.4.3 Impacts on Fauna - Disturbance to Breeding/Nesting Sites: ")
    potential_impacts_on_biological_environment_6_4_3_Impacts_on_Fauna_Noise_and_Vibration_Impacts_on_Wildlife = dspy.OutputField(desc="Extract facts about Noise and Vibration Impacts on Wildlife", prefix="potential_impacts_on_biological_environment - 6.4.3 Impacts on Fauna - Noise and Vibration Impacts on Wildlife: ")
    potential_impacts_on_biological_environment_6_4_3_Impacts_on_Fauna_Lighting_Impacts_on_Wildlife = dspy.OutputField(desc="Extract facts about Lighting Impacts on Wildlife", prefix="potential_impacts_on_biological_environment - 6.4.3 Impacts on Fauna - Lighting Impacts on Wildlife: ")
    potential_impacts_on_biological_environment_6_4_4_Impacts_on_Aquatic_Biodiversity_Impacts_on_Fish_Populations = dspy.OutputField(desc="Extract facts about Impacts on Fish Populations", prefix="potential_impacts_on_biological_environment - 6.4.4 Impacts on Aquatic Biodiversity - Impacts on Fish Populations: ")
    potential_impacts_on_biological_environment_6_4_4_Impacts_on_Aquatic_Biodiversity_Impacts_on_Endemic_Fish_Species = dspy.OutputField(desc="Extract facts about Impacts on Endemic Fish Species", prefix="potential_impacts_on_biological_environment - 6.4.4 Impacts on Aquatic Biodiversity - Impacts on Endemic Fish Species: ")
    potential_impacts_on_biological_environment_6_4_4_Impacts_on_Aquatic_Biodiversity_Impacts_on_IUCN_Red_List_Fish = dspy.OutputField(desc="Extract facts about Impacts on IUCN Red List Fish", prefix="potential_impacts_on_biological_environment - 6.4.4 Impacts on Aquatic Biodiversity - Impacts on IUCN Red List Fish: ")
    potential_impacts_on_biological_environment_6_4_4_Impacts_on_Aquatic_Biodiversity_Impacts_on_Spawning_Grounds = dspy.OutputField(desc="Extract facts about Impacts on Spawning Grounds", prefix="potential_impacts_on_biological_environment - 6.4.4 Impacts on Aquatic Biodiversity - Impacts on Spawning Grounds: ")
    potential_impacts_on_biological_environment_6_4_4_Impacts_on_Aquatic_Biodiversity_Impacts_on_Migration_Routes = dspy.OutputField(desc="Extract facts about Impacts on Migration Routes", prefix="potential_impacts_on_biological_environment - 6.4.4 Impacts on Aquatic Biodiversity - Impacts on Migration Routes: ")
    potential_impacts_on_biological_environment_6_4_4_Impacts_on_Aquatic_Biodiversity_Water_Quality_Impacts_on_Aquatic_Life = dspy.OutputField(desc="Extract facts about Water Quality Impacts on Aquatic Life", prefix="potential_impacts_on_biological_environment - 6.4.4 Impacts on Aquatic Biodiversity - Water Quality Impacts on Aquatic Life: ")
    potential_impacts_on_biological_environment_6_4_5_Impacts_on_Ecosystem_Services_Impacts_on_Pollination_Services = dspy.OutputField(desc="Extract facts about Impacts on Pollination Services", prefix="potential_impacts_on_biological_environment - 6.4.5 Impacts on Ecosystem Services - Impacts on Pollination Services: ")
    potential_impacts_on_biological_environment_6_4_5_Impacts_on_Ecosystem_Services_Impacts_on_Water_Regulation = dspy.OutputField(desc="Extract facts about Impacts on Water Regulation", prefix="potential_impacts_on_biological_environment - 6.4.5 Impacts on Ecosystem Services - Impacts on Water Regulation: ")
    potential_impacts_on_biological_environment_6_4_5_Impacts_on_Ecosystem_Services_Impacts_on_Carbon_Sequestration = dspy.OutputField(desc="Extract facts about Impacts on Carbon Sequestration", prefix="potential_impacts_on_biological_environment - 6.4.5 Impacts on Ecosystem Services - Impacts on Carbon Sequestration: ")
    potential_impacts_on_biological_environment_6_4_5_Impacts_on_Ecosystem_Services_Impacts_on_Soil_Formation = dspy.OutputField(desc="Extract facts about Impacts on Soil Formation", prefix="potential_impacts_on_biological_environment - 6.4.5 Impacts on Ecosystem Services - Impacts on Soil Formation: ")
    potential_impacts_on_biological_environment_6_4_5_Impacts_on_Ecosystem_Services_Impacts_on_Nutrient_Cycling = dspy.OutputField(desc="Extract facts about Impacts on Nutrient Cycling", prefix="potential_impacts_on_biological_environment - 6.4.5 Impacts on Ecosystem Services - Impacts on Nutrient Cycling: ")
    potential_impacts_on_biological_environment_6_4_6_Invasive_Species_Risk_Risk_of_Introducing_Invasive_Species = dspy.OutputField(desc="Extract facts about Risk of Introducing Invasive Species", prefix="potential_impacts_on_biological_environment - 6.4.6 Invasive Species Risk - Risk of Introducing Invasive Species: ")
    potential_impacts_on_biological_environment_6_4_6_Invasive_Species_Risk_Pathways_for_Invasive_Species_Introduction = dspy.OutputField(desc="Extract facts about Pathways for Invasive Species Introduction", prefix="potential_impacts_on_biological_environment - 6.4.6 Invasive Species Risk - Pathways for Invasive Species Introduction: ")
    potential_impacts_on_biological_environment_6_4_6_Invasive_Species_Risk_Potential_Impacts_of_Invasive_Species = dspy.OutputField(desc="Extract facts about Potential Impacts of Invasive Species", prefix="potential_impacts_on_biological_environment - 6.4.6 Invasive Species Risk - Potential Impacts of Invasive Species: ")
    potential_impacts_on_socio_economic_environment_6_5_1_Displacement_and_Resettlement_Physical_Displacement_Number_of_Households = dspy.OutputField(desc="Extract facts about Physical Displacement (Number of Households)", prefix="potential_impacts_on_socio_economic_environment - 6.5.1 Displacement and Resettlement - Physical Displacement (Number of Households): ")
    potential_impacts_on_socio_economic_environment_6_5_1_Displacement_and_Resettlement_Economic_Displacement_Number_of_People = dspy.OutputField(desc="Extract facts about Economic Displacement (Number of People)", prefix="potential_impacts_on_socio_economic_environment - 6.5.1 Displacement and Resettlement - Economic Displacement (Number of People): ")
    potential_impacts_on_socio_economic_environment_6_5_1_Displacement_and_Resettlement_Loss_of_Agricultural_Land_hectares = dspy.OutputField(desc="Extract facts about Loss of Agricultural Land (hectares)", prefix="potential_impacts_on_socio_economic_environment - 6.5.1 Displacement and Resettlement - Loss of Agricultural Land (hectares): ")
    potential_impacts_on_socio_economic_environment_6_5_1_Displacement_and_Resettlement_Loss_of_Residential_Structures = dspy.OutputField(desc="Extract facts about Loss of Residential Structures", prefix="potential_impacts_on_socio_economic_environment - 6.5.1 Displacement and Resettlement - Loss of Residential Structures: ")
    potential_impacts_on_socio_economic_environment_6_5_1_Displacement_and_Resettlement_Loss_of_Commercial_Structures = dspy.OutputField(desc="Extract facts about Loss of Commercial Structures", prefix="potential_impacts_on_socio_economic_environment - 6.5.1 Displacement and Resettlement - Loss of Commercial Structures: ")
    potential_impacts_on_socio_economic_environment_6_5_1_Displacement_and_Resettlement_Impacts_on_Tenants_and_Informal_Settlers = dspy.OutputField(desc="Extract facts about Impacts on Tenants and Informal Settlers", prefix="potential_impacts_on_socio_economic_environment - 6.5.1 Displacement and Resettlement - Impacts on Tenants and Informal Settlers: ")
    potential_impacts_on_socio_economic_environment_6_5_2_Livelihoods_and_Economy_Impacts_on_Livelihoods_Agriculture_Fishing_Business = dspy.OutputField(desc="Extract facts about Impacts on Livelihoods (Agriculture/Fishing/Business)", prefix="potential_impacts_on_socio_economic_environment - 6.5.2 Livelihoods and Economy - Impacts on Livelihoods (Agriculture/Fishing/Business): ")
    potential_impacts_on_socio_economic_environment_6_5_2_Livelihoods_and_Economy_Loss_of_Income_Sources = dspy.OutputField(desc="Extract facts about Loss of Income Sources", prefix="potential_impacts_on_socio_economic_environment - 6.5.2 Livelihoods and Economy - Loss of Income Sources: ")
    potential_impacts_on_socio_economic_environment_6_5_2_Livelihoods_and_Economy_Employment_Opportunities_Direct_Indirect = dspy.OutputField(desc="Extract facts about Employment Opportunities (Direct/Indirect)", prefix="potential_impacts_on_socio_economic_environment - 6.5.2 Livelihoods and Economy - Employment Opportunities (Direct/Indirect): ")
    potential_impacts_on_socio_economic_environment_6_5_2_Livelihoods_and_Economy_Local_Procurement_Opportunities = dspy.OutputField(desc="Extract facts about Local Procurement Opportunities", prefix="potential_impacts_on_socio_economic_environment - 6.5.2 Livelihoods and Economy - Local Procurement Opportunities: ")
    potential_impacts_on_socio_economic_environment_6_5_2_Livelihoods_and_Economy_Inflationary_Effects_Local_prices = dspy.OutputField(desc="Extract facts about Inflationary Effects (Local prices)", prefix="potential_impacts_on_socio_economic_environment - 6.5.2 Livelihoods and Economy - Inflationary Effects (Local prices): ")
    potential_impacts_on_socio_economic_environment_6_5_2_Livelihoods_and_Economy_Impacts_on_Tourism = dspy.OutputField(desc="Extract facts about Impacts on Tourism", prefix="potential_impacts_on_socio_economic_environment - 6.5.2 Livelihoods and Economy - Impacts on Tourism: ")
    potential_impacts_on_socio_economic_environment_6_5_3_Community_Health_and_Safety_Influx_of_Workers_Social_conflict_Disease_transmission = dspy.OutputField(desc="Extract facts about Influx of Workers (Social conflict/Disease transmission)", prefix="potential_impacts_on_socio_economic_environment - 6.5.3 Community Health and Safety - Influx of Workers (Social conflict/Disease transmission): ")
    potential_impacts_on_socio_economic_environment_6_5_3_Community_Health_and_Safety_Communicable_Diseases_HIV_AIDS_Vector_borne = dspy.OutputField(desc="Extract facts about Communicable Diseases (HIV/AIDS/Vector-borne)", prefix="potential_impacts_on_socio_economic_environment - 6.5.3 Community Health and Safety - Communicable Diseases (HIV/AIDS/Vector-borne): ")
    potential_impacts_on_socio_economic_environment_6_5_3_Community_Health_and_Safety_Traffic_Safety_Risks = dspy.OutputField(desc="Extract facts about Traffic Safety Risks", prefix="potential_impacts_on_socio_economic_environment - 6.5.3 Community Health and Safety - Traffic Safety Risks: ")
    potential_impacts_on_socio_economic_environment_6_5_3_Community_Health_and_Safety_Hazardous_Materials_Exposure_Risks = dspy.OutputField(desc="Extract facts about Hazardous Materials Exposure Risks", prefix="potential_impacts_on_socio_economic_environment - 6.5.3 Community Health and Safety - Hazardous Materials Exposure Risks: ")
    potential_impacts_on_socio_economic_environment_6_5_3_Community_Health_and_Safety_Emergency_Response_Capabilities = dspy.OutputField(desc="Extract facts about Emergency Response Capabilities", prefix="potential_impacts_on_socio_economic_environment - 6.5.3 Community Health and Safety - Emergency Response Capabilities: ")
    potential_impacts_on_socio_economic_environment_6_5_3_Community_Health_and_Safety_Security_Personnel_Risks = dspy.OutputField(desc="Extract facts about Security Personnel Risks", prefix="potential_impacts_on_socio_economic_environment - 6.5.3 Community Health and Safety - Security Personnel Risks: ")
    potential_impacts_on_socio_economic_environment_6_5_4_Cultural_Heritage_Direct_Impacts_on_Archaeological_Sites = dspy.OutputField(desc="Extract facts about Direct Impacts on Archaeological Sites", prefix="potential_impacts_on_socio_economic_environment - 6.5.4 Cultural Heritage - Direct Impacts on Archaeological Sites: ")
    potential_impacts_on_socio_economic_environment_6_5_4_Cultural_Heritage_Impacts_on_Sacred_Sites_Graves = dspy.OutputField(desc="Extract facts about Impacts on Sacred Sites/Graves", prefix="potential_impacts_on_socio_economic_environment - 6.5.4 Cultural Heritage - Impacts on Sacred Sites/Graves: ")
    potential_impacts_on_socio_economic_environment_6_5_4_Cultural_Heritage_Impacts_on_Intangible_Heritage = dspy.OutputField(desc="Extract facts about Impacts on Intangible Heritage", prefix="potential_impacts_on_socio_economic_environment - 6.5.4 Cultural Heritage - Impacts on Intangible Heritage: ")
    potential_impacts_on_socio_economic_environment_6_5_4_Cultural_Heritage_Visual_Impacts_on_Heritage_Sites = dspy.OutputField(desc="Extract facts about Visual Impacts on Heritage Sites", prefix="potential_impacts_on_socio_economic_environment - 6.5.4 Cultural Heritage - Visual Impacts on Heritage Sites: ")
    potential_impacts_on_socio_economic_environment_6_5_5_Indigenous_Peoples_Impacts_on_Traditional_Lands_Resources = dspy.OutputField(desc="Extract facts about Impacts on Traditional Lands/Resources", prefix="potential_impacts_on_socio_economic_environment - 6.5.5 Indigenous Peoples - Impacts on Traditional Lands/Resources: ")
    potential_impacts_on_socio_economic_environment_6_5_5_Indigenous_Peoples_Impacts_on_Cultural_Practices = dspy.OutputField(desc="Extract facts about Impacts on Cultural Practices", prefix="potential_impacts_on_socio_economic_environment - 6.5.5 Indigenous Peoples - Impacts on Cultural Practices: ")
    potential_impacts_on_socio_economic_environment_6_5_5_Indigenous_Peoples_Free_Prior_and_Informed_Consent_FPIC_Status = dspy.OutputField(desc="Extract facts about Free, Prior, and Informed Consent (FPIC) Status", prefix="potential_impacts_on_socio_economic_environment - 6.5.5 Indigenous Peoples - Free, Prior, and Informed Consent (FPIC) Status: ")
    potential_impacts_on_socio_economic_environment_6_5_5_Indigenous_Peoples_Benefit_Sharing_Agreements = dspy.OutputField(desc="Extract facts about Benefit Sharing Agreements", prefix="potential_impacts_on_socio_economic_environment - 6.5.5 Indigenous Peoples - Benefit Sharing Agreements: ")
    potential_impacts_on_socio_economic_environment_6_5_6_Labor_and_Working_Conditions_Occupational_Health_and_Safety_Risks = dspy.OutputField(desc="Extract facts about Occupational Health and Safety Risks", prefix="potential_impacts_on_socio_economic_environment - 6.5.6 Labor and Working Conditions - Occupational Health and Safety Risks: ")
    potential_impacts_on_socio_economic_environment_6_5_6_Labor_and_Working_Conditions_Labor_Influx_Management = dspy.OutputField(desc="Extract facts about Labor Influx Management", prefix="potential_impacts_on_socio_economic_environment - 6.5.6 Labor and Working Conditions - Labor Influx Management: ")
    potential_impacts_on_socio_economic_environment_6_5_6_Labor_and_Working_Conditions_Child_Labor_Forced_Labor_Risks = dspy.OutputField(desc="Extract facts about Child Labor/Forced Labor Risks", prefix="potential_impacts_on_socio_economic_environment - 6.5.6 Labor and Working Conditions - Child Labor/Forced Labor Risks: ")
    potential_impacts_on_socio_economic_environment_6_5_6_Labor_and_Working_Conditions_Worker_Accommodation_Standards = dspy.OutputField(desc="Extract facts about Worker Accommodation Standards", prefix="potential_impacts_on_socio_economic_environment - 6.5.6 Labor and Working Conditions - Worker Accommodation Standards: ")
    cumulative_impacts_Valued_Environmental_and_Social_Components_VECs_Identified = dspy.OutputField(desc="Extract facts about Valued Environmental and Social Components (VECs) Identified", prefix="cumulative_impacts - Valued Environmental and Social Components (VECs) Identified: ")
    cumulative_impacts_Spatial_Boundaries_for_Cumulative_Assessment = dspy.OutputField(desc="Extract facts about Spatial Boundaries for Cumulative Assessment", prefix="cumulative_impacts - Spatial Boundaries for Cumulative Assessment: ")
    cumulative_impacts_Temporal_Boundaries_for_Cumulative_Assessment = dspy.OutputField(desc="Extract facts about Temporal Boundaries for Cumulative Assessment", prefix="cumulative_impacts - Temporal Boundaries for Cumulative Assessment: ")
    cumulative_impacts_Other_Past_Present_and_Future_Projects_Considered = dspy.OutputField(desc="Extract facts about Other Past, Present, and Future Projects Considered", prefix="cumulative_impacts - Other Past, Present, and Future Projects Considered: ")
    cumulative_impacts_Cumulative_Impacts_on_Biodiversity = dspy.OutputField(desc="Extract facts about Cumulative Impacts on Biodiversity", prefix="cumulative_impacts - Cumulative Impacts on Biodiversity: ")
    cumulative_impacts_Cumulative_Impacts_on_Water_Resources = dspy.OutputField(desc="Extract facts about Cumulative Impacts on Water Resources", prefix="cumulative_impacts - Cumulative Impacts on Water Resources: ")
    cumulative_impacts_Cumulative_Impacts_on_Air_Quality = dspy.OutputField(desc="Extract facts about Cumulative Impacts on Air Quality", prefix="cumulative_impacts - Cumulative Impacts on Air Quality: ")
    cumulative_impacts_Cumulative_Impacts_on_Social_Infrastructure = dspy.OutputField(desc="Extract facts about Cumulative Impacts on Social Infrastructure", prefix="cumulative_impacts - Cumulative Impacts on Social Infrastructure: ")
    cumulative_impacts_Significance_of_Cumulative_Impacts = dspy.OutputField(desc="Extract facts about Significance of Cumulative Impacts", prefix="cumulative_impacts - Significance of Cumulative Impacts: ")
    climate_change_impacts_6_7_1_Greenhouse_Gas_Emissions_Scope_1_Emissions_Direct = dspy.OutputField(desc="Extract facts about Scope 1 Emissions (Direct)", prefix="climate_change_impacts - 6.7.1 Greenhouse Gas Emissions - Scope 1 Emissions (Direct): ")
    climate_change_impacts_6_7_1_Greenhouse_Gas_Emissions_Scope_2_Emissions_Indirect_Energy = dspy.OutputField(desc="Extract facts about Scope 2 Emissions (Indirect Energy)", prefix="climate_change_impacts - 6.7.1 Greenhouse Gas Emissions - Scope 2 Emissions (Indirect Energy): ")
    climate_change_impacts_6_7_1_Greenhouse_Gas_Emissions_Scope_3_Emissions_Value_Chain = dspy.OutputField(desc="Extract facts about Scope 3 Emissions (Value Chain)", prefix="climate_change_impacts - 6.7.1 Greenhouse Gas Emissions - Scope 3 Emissions (Value Chain): ")
    climate_change_impacts_6_7_1_Greenhouse_Gas_Emissions_Total_Estimated_CO2e_Emissions_tons_year = dspy.OutputField(desc="Extract facts about Total Estimated CO2e Emissions (tons/year)", prefix="climate_change_impacts - 6.7.1 Greenhouse Gas Emissions - Total Estimated CO2e Emissions (tons/year): ")
    climate_change_impacts_6_7_1_Greenhouse_Gas_Emissions_Carbon_Intensity_of_Project = dspy.OutputField(desc="Extract facts about Carbon Intensity of Project", prefix="climate_change_impacts - 6.7.1 Greenhouse Gas Emissions - Carbon Intensity of Project: ")
    climate_change_impacts_6_7_2_Climate_Change_Risk_Assessment_Physical_Climate_Risks_Floods_Droughts_Storms = dspy.OutputField(desc="Extract facts about Physical Climate Risks (Floods/Droughts/Storms)", prefix="climate_change_impacts - 6.7.2 Climate Change Risk Assessment - Physical Climate Risks (Floods/Droughts/Storms): ")
    climate_change_impacts_6_7_2_Climate_Change_Risk_Assessment_Climate_Resilience_of_Infrastructure = dspy.OutputField(desc="Extract facts about Climate Resilience of Infrastructure", prefix="climate_change_impacts - 6.7.2 Climate Change Risk Assessment - Climate Resilience of Infrastructure: ")
    climate_change_impacts_6_7_2_Climate_Change_Risk_Assessment_Impact_of_Climate_Change_on_Water_Availability = dspy.OutputField(desc="Extract facts about Impact of Climate Change on Water Availability", prefix="climate_change_impacts - 6.7.2 Climate Change Risk Assessment - Impact of Climate Change on Water Availability: ")
    climate_change_impacts_6_7_2_Climate_Change_Risk_Assessment_Impact_of_Climate_Change_on_Biodiversity = dspy.OutputField(desc="Extract facts about Impact of Climate Change on Biodiversity", prefix="climate_change_impacts - 6.7.2 Climate Change Risk Assessment - Impact of Climate Change on Biodiversity: ")
    climate_change_impacts_6_7_2_Climate_Change_Risk_Assessment_Adaptation_Measures_Proposed = dspy.OutputField(desc="Extract facts about Adaptation Measures Proposed", prefix="climate_change_impacts - 6.7.2 Climate Change Risk Assessment - Adaptation Measures Proposed: ")
    climate_change_impacts_6_7_3_Transition_Risks_Policy_and_Legal_Risks_Carbon_pricing = dspy.OutputField(desc="Extract facts about Policy and Legal Risks (Carbon pricing)", prefix="climate_change_impacts - 6.7.3 Transition Risks - Policy and Legal Risks (Carbon pricing): ")
    climate_change_impacts_6_7_3_Transition_Risks_Market_Risks = dspy.OutputField(desc="Extract facts about Market Risks", prefix="climate_change_impacts - 6.7.3 Transition Risks - Market Risks: ")
    climate_change_impacts_6_7_3_Transition_Risks_Reputational_Risks = dspy.OutputField(desc="Extract facts about Reputational Risks", prefix="climate_change_impacts - 6.7.3 Transition Risks - Reputational Risks: ")


class EnvironmentalAndSocialManagementPlanEsmpSignature(dspy.Signature):
    """
    Extracted facts for Environmental And Social Management Plan Esmp.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    esmp_framework_Environmental_and_Social_Policy = dspy.OutputField(desc="Extract facts about Environmental and Social Policy", prefix="esmp_framework - Environmental and Social Policy: ")
    esmp_framework_Management_Programs_Operational_Procedures = dspy.OutputField(desc="Extract facts about Management Programs (Operational Procedures)", prefix="esmp_framework - Management Programs (Operational Procedures): ")
    esmp_framework_Roles_and_Responsibilities_Matrix = dspy.OutputField(desc="Extract facts about Roles and Responsibilities Matrix", prefix="esmp_framework - Roles and Responsibilities Matrix: ")
    esmp_framework_Implementation_Schedule = dspy.OutputField(desc="Extract facts about Implementation Schedule", prefix="esmp_framework - Implementation Schedule: ")
    esmp_framework_Reporting_and_Review_Procedures = dspy.OutputField(desc="Extract facts about Reporting and Review Procedures", prefix="esmp_framework - Reporting and Review Procedures: ")
    esmp_framework_Adaptive_Management_Mechanisms = dspy.OutputField(desc="Extract facts about Adaptive Management Mechanisms", prefix="esmp_framework - Adaptive Management Mechanisms: ")
    monitoring_plan_8_2_1_Biodiversity_Monitoring_Monitoring_Objectives = dspy.OutputField(desc="Extract facts about Monitoring Objectives", prefix="monitoring_plan - 8.2.1 Biodiversity Monitoring - Monitoring Objectives: ")
    monitoring_plan_8_2_1_Biodiversity_Monitoring_Indicator_Species_for_Monitoring = dspy.OutputField(desc="Extract facts about Indicator Species for Monitoring", prefix="monitoring_plan - 8.2.1 Biodiversity Monitoring - Indicator Species for Monitoring: ")
    monitoring_plan_8_2_1_Biodiversity_Monitoring_IUCN_Red_List_Species_Monitoring_Protocol = dspy.OutputField(desc="Extract facts about IUCN Red List Species Monitoring Protocol", prefix="monitoring_plan - 8.2.1 Biodiversity Monitoring - IUCN Red List Species Monitoring Protocol: ")
    monitoring_plan_8_2_1_Biodiversity_Monitoring_Habitat_Monitoring_Frequency = dspy.OutputField(desc="Extract facts about Habitat Monitoring Frequency", prefix="monitoring_plan - 8.2.1 Biodiversity Monitoring - Habitat Monitoring Frequency: ")
    monitoring_plan_8_2_1_Biodiversity_Monitoring_Vegetation_Monitoring_Methods = dspy.OutputField(desc="Extract facts about Vegetation Monitoring Methods", prefix="monitoring_plan - 8.2.1 Biodiversity Monitoring - Vegetation Monitoring Methods: ")
    monitoring_plan_8_2_1_Biodiversity_Monitoring_Fauna_Monitoring_Methods = dspy.OutputField(desc="Extract facts about Fauna Monitoring Methods", prefix="monitoring_plan - 8.2.1 Biodiversity Monitoring - Fauna Monitoring Methods: ")
    monitoring_plan_8_2_1_Biodiversity_Monitoring_Aquatic_Biodiversity_Monitoring = dspy.OutputField(desc="Extract facts about Aquatic Biodiversity Monitoring", prefix="monitoring_plan - 8.2.1 Biodiversity Monitoring - Aquatic Biodiversity Monitoring: ")
    monitoring_plan_8_2_1_Biodiversity_Monitoring_Invasive_Species_Monitoring = dspy.OutputField(desc="Extract facts about Invasive Species Monitoring", prefix="monitoring_plan - 8.2.1 Biodiversity Monitoring - Invasive Species Monitoring: ")
    monitoring_plan_8_2_1_Biodiversity_Monitoring_Monitoring_Duration_years = dspy.OutputField(desc="Extract facts about Monitoring Duration (years)", prefix="monitoring_plan - 8.2.1 Biodiversity Monitoring - Monitoring Duration (years): ")
    monitoring_plan_8_2_1_Biodiversity_Monitoring_Adaptive_Management_Triggers = dspy.OutputField(desc="Extract facts about Adaptive Management Triggers", prefix="monitoring_plan - 8.2.1 Biodiversity Monitoring - Adaptive Management Triggers: ")
    monitoring_plan_8_2_2_Physical_Environment_Monitoring_Air_Quality_Monitoring_Parameters = dspy.OutputField(desc="Extract facts about Air Quality Monitoring Parameters", prefix="monitoring_plan - 8.2.2 Physical Environment Monitoring - Air Quality Monitoring Parameters: ")
    monitoring_plan_8_2_2_Physical_Environment_Monitoring_Water_Quality_Monitoring_Parameters = dspy.OutputField(desc="Extract facts about Water Quality Monitoring Parameters", prefix="monitoring_plan - 8.2.2 Physical Environment Monitoring - Water Quality Monitoring Parameters: ")
    monitoring_plan_8_2_2_Physical_Environment_Monitoring_Noise_Level_Monitoring = dspy.OutputField(desc="Extract facts about Noise Level Monitoring", prefix="monitoring_plan - 8.2.2 Physical Environment Monitoring - Noise Level Monitoring: ")
    monitoring_plan_8_2_2_Physical_Environment_Monitoring_Soil_Erosion_Monitoring = dspy.OutputField(desc="Extract facts about Soil Erosion Monitoring", prefix="monitoring_plan - 8.2.2 Physical Environment Monitoring - Soil Erosion Monitoring: ")
    monitoring_plan_8_2_2_Physical_Environment_Monitoring_Hydrological_Monitoring_Flows_Levels = dspy.OutputField(desc="Extract facts about Hydrological Monitoring (Flows/Levels)", prefix="monitoring_plan - 8.2.2 Physical Environment Monitoring - Hydrological Monitoring (Flows/Levels): ")
    monitoring_plan_8_2_2_Physical_Environment_Monitoring_Monitoring_Locations_Map_Coordinates = dspy.OutputField(desc="Extract facts about Monitoring Locations (Map/Coordinates)", prefix="monitoring_plan - 8.2.2 Physical Environment Monitoring - Monitoring Locations (Map/Coordinates): ")
    monitoring_plan_8_2_2_Physical_Environment_Monitoring_Monitoring_Frequency = dspy.OutputField(desc="Extract facts about Monitoring Frequency", prefix="monitoring_plan - 8.2.2 Physical Environment Monitoring - Monitoring Frequency: ")
    monitoring_plan_8_2_2_Physical_Environment_Monitoring_Compliance_Standards_National_International = dspy.OutputField(desc="Extract facts about Compliance Standards (National/International)", prefix="monitoring_plan - 8.2.2 Physical Environment Monitoring - Compliance Standards (National/International): ")
    monitoring_plan_8_2_3_Social_Monitoring_Livelihood_Restoration_Monitoring = dspy.OutputField(desc="Extract facts about Livelihood Restoration Monitoring", prefix="monitoring_plan - 8.2.3 Social Monitoring - Livelihood Restoration Monitoring: ")
    monitoring_plan_8_2_3_Social_Monitoring_Resettlement_Monitoring_Indicators = dspy.OutputField(desc="Extract facts about Resettlement Monitoring Indicators", prefix="monitoring_plan - 8.2.3 Social Monitoring - Resettlement Monitoring Indicators: ")
    monitoring_plan_8_2_3_Social_Monitoring_Community_Health_and_Safety_Monitoring = dspy.OutputField(desc="Extract facts about Community Health and Safety Monitoring", prefix="monitoring_plan - 8.2.3 Social Monitoring - Community Health and Safety Monitoring: ")
    monitoring_plan_8_2_3_Social_Monitoring_Grievance_Redress_Mechanism_Effectiveness = dspy.OutputField(desc="Extract facts about Grievance Redress Mechanism Effectiveness", prefix="monitoring_plan - 8.2.3 Social Monitoring - Grievance Redress Mechanism Effectiveness: ")
    monitoring_plan_8_2_3_Social_Monitoring_Employment_and_Local_Content_Monitoring = dspy.OutputField(desc="Extract facts about Employment and Local Content Monitoring", prefix="monitoring_plan - 8.2.3 Social Monitoring - Employment and Local Content Monitoring: ")
    monitoring_plan_8_2_3_Social_Monitoring_Stakeholder_Engagement_Activities = dspy.OutputField(desc="Extract facts about Stakeholder Engagement Activities", prefix="monitoring_plan - 8.2.3 Social Monitoring - Stakeholder Engagement Activities: ")
    institutional_arrangements_and_responsibilities_Organizational_Structure_for_ESMP_Implementation = dspy.OutputField(desc="Extract facts about Organizational Structure for ESMP Implementation", prefix="institutional_arrangements_and_responsibilities - Organizational Structure for ESMP Implementation: ")
    institutional_arrangements_and_responsibilities_Environmental_and_Social_Unit_ESU_Staffing = dspy.OutputField(desc="Extract facts about Environmental and Social Unit (ESU) Staffing", prefix="institutional_arrangements_and_responsibilities - Environmental and Social Unit (ESU) Staffing: ")
    institutional_arrangements_and_responsibilities_Role_of_Contractor_vs_Developer = dspy.OutputField(desc="Extract facts about Role of Contractor vs. Developer", prefix="institutional_arrangements_and_responsibilities - Role of Contractor vs. Developer: ")
    institutional_arrangements_and_responsibilities_Regulatory_Oversight_Bodies = dspy.OutputField(desc="Extract facts about Regulatory Oversight Bodies", prefix="institutional_arrangements_and_responsibilities - Regulatory Oversight Bodies: ")
    institutional_arrangements_and_responsibilities_Independent_Environmental_Control_Officer_IECO = dspy.OutputField(desc="Extract facts about Independent Environmental Control Officer (IECO)", prefix="institutional_arrangements_and_responsibilities - Independent Environmental Control Officer (IECO): ")
    institutional_arrangements_and_responsibilities_Community_Liaison_Officer_CLO_Roles = dspy.OutputField(desc="Extract facts about Community Liaison Officer (CLO) Roles", prefix="institutional_arrangements_and_responsibilities - Community Liaison Officer (CLO) Roles: ")
    capacity_building_and_training_Training_Needs_Assessment = dspy.OutputField(desc="Extract facts about Training Needs Assessment", prefix="capacity_building_and_training - Training Needs Assessment: ")
    capacity_building_and_training_Environmental_Awareness_Training = dspy.OutputField(desc="Extract facts about Environmental Awareness Training", prefix="capacity_building_and_training - Environmental Awareness Training: ")
    capacity_building_and_training_Health_and_Safety_Training_Programs = dspy.OutputField(desc="Extract facts about Health and Safety Training Programs", prefix="capacity_building_and_training - Health and Safety Training Programs: ")
    capacity_building_and_training_Specialized_Training_e_g_Spill_Response_Biodiversity = dspy.OutputField(desc="Extract facts about Specialized Training (e.g., Spill Response, Biodiversity)", prefix="capacity_building_and_training - Specialized Training (e.g., Spill Response, Biodiversity): ")
    capacity_building_and_training_Training_Schedule_and_Frequency = dspy.OutputField(desc="Extract facts about Training Schedule and Frequency", prefix="capacity_building_and_training - Training Schedule and Frequency: ")
    capacity_building_and_training_Target_Audience_for_Training_Staff_Contractors_Community = dspy.OutputField(desc="Extract facts about Target Audience for Training (Staff/Contractors/Community)", prefix="capacity_building_and_training - Target Audience for Training (Staff/Contractors/Community): ")
    grievance_mechanism_Grievance_Redress_Mechanism_GRM_Structure = dspy.OutputField(desc="Extract facts about Grievance Redress Mechanism (GRM) Structure", prefix="grievance_mechanism - Grievance Redress Mechanism (GRM) Structure: ")
    grievance_mechanism_Grievance_Receipt_and_Recording_Procedures = dspy.OutputField(desc="Extract facts about Grievance Receipt and Recording Procedures", prefix="grievance_mechanism - Grievance Receipt and Recording Procedures: ")
    grievance_mechanism_Resolution_Timeframes = dspy.OutputField(desc="Extract facts about Resolution Timeframes", prefix="grievance_mechanism - Resolution Timeframes: ")
    grievance_mechanism_Appeal_Process = dspy.OutputField(desc="Extract facts about Appeal Process", prefix="grievance_mechanism - Appeal Process: ")
    grievance_mechanism_Accessibility_for_Vulnerable_Groups = dspy.OutputField(desc="Extract facts about Accessibility for Vulnerable Groups", prefix="grievance_mechanism - Accessibility for Vulnerable Groups: ")
    grievance_mechanism_Reporting_on_Grievances = dspy.OutputField(desc="Extract facts about Reporting on Grievances", prefix="grievance_mechanism - Reporting on Grievances: ")
    emergency_preparedness_and_response_plan_Emergency_Response_Procedures = dspy.OutputField(desc="Extract facts about Emergency Response Procedures", prefix="emergency_preparedness_and_response_plan - Emergency Response Procedures: ")
    emergency_preparedness_and_response_plan_Emergency_Contacts_and_Communication_Channels = dspy.OutputField(desc="Extract facts about Emergency Contacts and Communication Channels", prefix="emergency_preparedness_and_response_plan - Emergency Contacts and Communication Channels: ")
    emergency_preparedness_and_response_plan_Spill_Response_Plan = dspy.OutputField(desc="Extract facts about Spill Response Plan", prefix="emergency_preparedness_and_response_plan - Spill Response Plan: ")
    emergency_preparedness_and_response_plan_Fire_Safety_Plan = dspy.OutputField(desc="Extract facts about Fire Safety Plan", prefix="emergency_preparedness_and_response_plan - Fire Safety Plan: ")
    emergency_preparedness_and_response_plan_Medical_Emergency_Procedures = dspy.OutputField(desc="Extract facts about Medical Emergency Procedures", prefix="emergency_preparedness_and_response_plan - Medical Emergency Procedures: ")
    emergency_preparedness_and_response_plan_Drills_and_Simulation_Exercises = dspy.OutputField(desc="Extract facts about Drills and Simulation Exercises", prefix="emergency_preparedness_and_response_plan - Drills and Simulation Exercises: ")
    cost_estimates_Total_ESMP_Implementation_Budget = dspy.OutputField(desc="Extract facts about Total ESMP Implementation Budget", prefix="cost_estimates - Total ESMP Implementation Budget: ")
    cost_estimates_Mitigation_Measure_Costs = dspy.OutputField(desc="Extract facts about Mitigation Measure Costs", prefix="cost_estimates - Mitigation Measure Costs: ")
    cost_estimates_Monitoring_Costs = dspy.OutputField(desc="Extract facts about Monitoring Costs", prefix="cost_estimates - Monitoring Costs: ")
    cost_estimates_Capacity_Building_and_Training_Costs = dspy.OutputField(desc="Extract facts about Capacity Building and Training Costs", prefix="cost_estimates - Capacity Building and Training Costs: ")
    cost_estimates_Contingency_Budget = dspy.OutputField(desc="Extract facts about Contingency Budget", prefix="cost_estimates - Contingency Budget: ")
    cost_estimates_Source_of_Funding = dspy.OutputField(desc="Extract facts about Source of Funding", prefix="cost_estimates - Source of Funding: ")


class ExecutiveSummarySignature(dspy.Signature):
    """
    Extracted facts for Executive Summary.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    project_overview_Project_Name = dspy.OutputField(desc="Extract facts about Project Name", prefix="project_overview - Project Name: ")
    project_overview_Project_Proponent_Developer = dspy.OutputField(desc="Extract facts about Project Proponent / Developer", prefix="project_overview - Project Proponent / Developer: ")
    project_overview_Project_Location_Region_Country_Coordinates = dspy.OutputField(desc="Extract facts about Project Location (Region, Country, Coordinates)", prefix="project_overview - Project Location (Region, Country, Coordinates): ")
    project_overview_Project_Type_and_Sector = dspy.OutputField(desc="Extract facts about Project Type and Sector", prefix="project_overview - Project Type and Sector: ")
    project_overview_Project_Rationale_Need_for_the_Project = dspy.OutputField(desc="Extract facts about Project Rationale / Need for the Project", prefix="project_overview - Project Rationale / Need for the Project: ")
    project_overview_Key_Project_Components_e_g_Dam_Powerhouse_Transmission_Line_Access_Roads = dspy.OutputField(desc="Extract facts about Key Project Components (e.g., Dam, Powerhouse, Transmission Line, Access Roads)", prefix="project_overview - Key Project Components (e.g., Dam, Powerhouse, Transmission Line, Access Roads): ")
    project_overview_Project_Lifecycle_Phases_Construction_Operation_Decommissioning = dspy.OutputField(desc="Extract facts about Project Lifecycle Phases (Construction, Operation, Decommissioning)", prefix="project_overview - Project Lifecycle Phases (Construction, Operation, Decommissioning): ")
    project_overview_Investment_Cost = dspy.OutputField(desc="Extract facts about Investment Cost", prefix="project_overview - Investment Cost: ")
    project_overview_Implementation_Schedule = dspy.OutputField(desc="Extract facts about Implementation Schedule", prefix="project_overview - Implementation Schedule: ")
    policy_legal_and_administrative_framework_summary_Key_National_Legislation_Compliance = dspy.OutputField(desc="Extract facts about Key National Legislation Compliance", prefix="policy_legal_and_administrative_framework_summary - Key National Legislation Compliance: ")
    policy_legal_and_administrative_framework_summary_International_Standards_Compliance_e_g_IFC_PS_WB_EHS_Guidelines = dspy.OutputField(desc="Extract facts about International Standards Compliance (e.g., IFC PS, WB EHS Guidelines)", prefix="policy_legal_and_administrative_framework_summary - International Standards Compliance (e.g., IFC PS, WB EHS Guidelines): ")
    policy_legal_and_administrative_framework_summary_Key_Permits_and_Approvals_Required = dspy.OutputField(desc="Extract facts about Key Permits and Approvals Required", prefix="policy_legal_and_administrative_framework_summary - Key Permits and Approvals Required: ")
    analysis_of_alternatives_summary_No_Project_Alternative = dspy.OutputField(desc="Extract facts about No-Project Alternative", prefix="analysis_of_alternatives_summary - No-Project Alternative: ")
    analysis_of_alternatives_summary_Site_Alternatives_Considered = dspy.OutputField(desc="Extract facts about Site Alternatives Considered", prefix="analysis_of_alternatives_summary - Site Alternatives Considered: ")
    analysis_of_alternatives_summary_Technology_Design_Alternatives_Considered = dspy.OutputField(desc="Extract facts about Technology/Design Alternatives Considered", prefix="analysis_of_alternatives_summary - Technology/Design Alternatives Considered: ")
    analysis_of_alternatives_summary_Selected_Alternative_and_Justification = dspy.OutputField(desc="Extract facts about Selected Alternative and Justification", prefix="analysis_of_alternatives_summary - Selected Alternative and Justification: ")
    baseline_conditions_summary_Physical_Environment_Key_Features_e_g_Hydrology_Geology_Air_Quality = dspy.OutputField(desc="Extract facts about Physical Environment Key Features (e.g., Hydrology, Geology, Air Quality)", prefix="baseline_conditions_summary - Physical Environment Key Features (e.g., Hydrology, Geology, Air Quality): ")
    baseline_conditions_summary_Biological_Environment_Key_Features_e_g_Protected_Areas_Endangered_Species = dspy.OutputField(desc="Extract facts about Biological Environment Key Features (e.g., Protected Areas, Endangered Species)", prefix="baseline_conditions_summary - Biological Environment Key Features (e.g., Protected Areas, Endangered Species): ")
    baseline_conditions_summary_Socio_Economic_Environment_Key_Features_e_g_Affected_Communities_Land_Use_Cultural_Heritage = dspy.OutputField(desc="Extract facts about Socio-Economic Environment Key Features (e.g., Affected Communities, Land Use, Cultural Heritage)", prefix="baseline_conditions_summary - Socio-Economic Environment Key Features (e.g., Affected Communities, Land Use, Cultural Heritage): ")
    summary_of_key_environmental_and_social_impacts_Key_Positive_Impacts_Benefits = dspy.OutputField(desc="Extract facts about Key Positive Impacts (Benefits)", prefix="summary_of_key_environmental_and_social_impacts - Key Positive Impacts (Benefits): ")
    summary_of_key_environmental_and_social_impacts_Key_Negative_Impacts_Construction_Phase = dspy.OutputField(desc="Extract facts about Key Negative Impacts - Construction Phase", prefix="summary_of_key_environmental_and_social_impacts - Key Negative Impacts - Construction Phase: ")
    summary_of_key_environmental_and_social_impacts_Key_Negative_Impacts_Operation_Phase = dspy.OutputField(desc="Extract facts about Key Negative Impacts - Operation Phase", prefix="summary_of_key_environmental_and_social_impacts - Key Negative Impacts - Operation Phase: ")
    summary_of_key_environmental_and_social_impacts_Cumulative_Impacts_Summary = dspy.OutputField(desc="Extract facts about Cumulative Impacts Summary", prefix="summary_of_key_environmental_and_social_impacts - Cumulative Impacts Summary: ")
    summary_of_key_environmental_and_social_impacts_Transboundary_Impacts_Summary_if_applicable = dspy.OutputField(desc="Extract facts about Transboundary Impacts Summary (if applicable)", prefix="summary_of_key_environmental_and_social_impacts - Transboundary Impacts Summary (if applicable): ")
    summary_of_key_environmental_and_social_impacts_Climate_Change_Risks_and_GHG_Emissions_Summary = dspy.OutputField(desc="Extract facts about Climate Change Risks and GHG Emissions Summary", prefix="summary_of_key_environmental_and_social_impacts - Climate Change Risks and GHG Emissions Summary: ")
    summary_of_mitigation_and_enhancement_measures_Key_Mitigation_Measures_for_Significant_Impacts = dspy.OutputField(desc="Extract facts about Key Mitigation Measures for Significant Impacts", prefix="summary_of_mitigation_and_enhancement_measures - Key Mitigation Measures for Significant Impacts: ")
    summary_of_mitigation_and_enhancement_measures_Residual_Impacts_after_Mitigation = dspy.OutputField(desc="Extract facts about Residual Impacts after Mitigation", prefix="summary_of_mitigation_and_enhancement_measures - Residual Impacts after Mitigation: ")
    summary_of_mitigation_and_enhancement_measures_Proposed_Enhancement_Measures = dspy.OutputField(desc="Extract facts about Proposed Enhancement Measures", prefix="summary_of_mitigation_and_enhancement_measures - Proposed Enhancement Measures: ")
    environmental_and_social_management_plan_esmp_summary_ESMP_Structure_and_Responsibilities = dspy.OutputField(desc="Extract facts about ESMP Structure and Responsibilities", prefix="environmental_and_social_management_plan_esmp_summary - ESMP Structure and Responsibilities: ")
    environmental_and_social_management_plan_esmp_summary_Monitoring_Program_Overview = dspy.OutputField(desc="Extract facts about Monitoring Program Overview", prefix="environmental_and_social_management_plan_esmp_summary - Monitoring Program Overview: ")
    environmental_and_social_management_plan_esmp_summary_Estimated_ESMP_Budget = dspy.OutputField(desc="Extract facts about Estimated ESMP Budget", prefix="environmental_and_social_management_plan_esmp_summary - Estimated ESMP Budget: ")
    public_consultation_and_stakeholder_engagement_summary_Key_Stakeholders_Identified = dspy.OutputField(desc="Extract facts about Key Stakeholders Identified", prefix="public_consultation_and_stakeholder_engagement_summary - Key Stakeholders Identified: ")
    public_consultation_and_stakeholder_engagement_summary_Consultation_Activities_Undertaken = dspy.OutputField(desc="Extract facts about Consultation Activities Undertaken", prefix="public_consultation_and_stakeholder_engagement_summary - Consultation Activities Undertaken: ")
    public_consultation_and_stakeholder_engagement_summary_Key_Issues_Raised_by_Stakeholders = dspy.OutputField(desc="Extract facts about Key Issues Raised by Stakeholders", prefix="public_consultation_and_stakeholder_engagement_summary - Key Issues Raised by Stakeholders: ")
    public_consultation_and_stakeholder_engagement_summary_Grievance_Redress_Mechanism_GRM_Overview = dspy.OutputField(desc="Extract facts about Grievance Redress Mechanism (GRM) Overview", prefix="public_consultation_and_stakeholder_engagement_summary - Grievance Redress Mechanism (GRM) Overview: ")
    conclusion_and_recommendations_Overall_Conclusion_on_Project_Feasibility_E_S_perspective = dspy.OutputField(desc="Extract facts about Overall Conclusion on Project Feasibility (E&S perspective)", prefix="conclusion_and_recommendations - Overall Conclusion on Project Feasibility (E&S perspective): ")
    conclusion_and_recommendations_Key_Conditions_for_Approval = dspy.OutputField(desc="Extract facts about Key Conditions for Approval", prefix="conclusion_and_recommendations - Key Conditions for Approval: ")


class GeothermalSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Geothermal Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Air_Emissions = dspy.OutputField(desc="Extract facts about Air Emissions, specifically: Hydrogen Sulfide (H2S), Mercury, Greenhouse Gases (CO2, CH4)", prefix="Air Emissions: ")
    Geological_Hazards = dspy.OutputField(desc="Extract facts about Geological Hazards, specifically: Ground Subsidence, Induced Seismicity", prefix="Geological Hazards: ")
    Brine_Management = dspy.OutputField(desc="Extract facts about Brine Management, specifically: Reinjection Strategy, Thermal Pollution, Chemical Composition", prefix="Brine Management: ")


class HazardousMaterialsManagementSignature(dspy.Signature):
    """
    Extracted facts for Hazardous Materials Management.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Storage_and_Handling = dspy.OutputField(desc="Extract facts about Storage and Handling, specifically: Chemicals, Waste", prefix="Storage and Handling: ")
    Emergency_Response = dspy.OutputField(desc="Extract facts about Emergency Response, specifically: Spill Contingency, Fire Safety", prefix="Emergency Response: ")


class HydrocarbonManagementSignature(dspy.Signature):
    """
    Extracted facts for Hydrocarbon Management.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Spill_Prevention = dspy.OutputField(desc="Extract facts about Spill Prevention, specifically: Emergency Response Plans, Containment Measures, Pipeline Integrity", prefix="Spill Prevention: ")
    Flaring_Impacts = dspy.OutputField(desc="Extract facts about Flaring Impacts, specifically: Air Quality, Noise, Greenhouse Gas Emissions", prefix="Flaring Impacts: ")


class HydropowerSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Hydropower Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Hydrology_and_Flow = dspy.OutputField(desc="Extract facts about Hydrology and Flow, specifically: Environmental Flow, Downstream Flow Alteration, Reservoir Filling", prefix="Hydrology and Flow: ")
    Dam_Safety = dspy.OutputField(desc="Extract facts about Dam Safety, specifically: Structural Integrity, Emergency Preparedness (Dam Break), Sedimentation", prefix="Dam Safety: ")
    Aquatic_Ecology = dspy.OutputField(desc="Extract facts about Aquatic Ecology, specifically: Fish Migration, Fish Mortality (Turbines), Habitat Fragmentation", prefix="Aquatic Ecology: ")


class IntroductionSignature(dspy.Signature):
    """
    Extracted facts for Introduction.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    project_background_Project_Origin_and_History = dspy.OutputField(desc="Extract facts about Project Origin and History", prefix="project_background - Project Origin and History: ")
    project_background_Project_Proponent_Details_Name_Contact_Experience = dspy.OutputField(desc="Extract facts about Project Proponent Details (Name, Contact, Experience)", prefix="project_background - Project Proponent Details (Name, Contact, Experience): ")
    project_background_Project_Location_and_Setting = dspy.OutputField(desc="Extract facts about Project Location and Setting", prefix="project_background - Project Location and Setting: ")
    project_background_Overview_of_the_Project_Development_Cycle = dspy.OutputField(desc="Extract facts about Overview of the Project Development Cycle", prefix="project_background - Overview of the Project Development Cycle: ")
    project_rationale_and_justification_Need_for_the_Project_e_g_Energy_Demand_Transport_Gap = dspy.OutputField(desc="Extract facts about Need for the Project (e.g., Energy Demand, Transport Gap)", prefix="project_rationale_and_justification - Need for the Project (e.g., Energy Demand, Transport Gap): ")
    project_rationale_and_justification_Strategic_Importance_National_Regional = dspy.OutputField(desc="Extract facts about Strategic Importance (National/Regional)", prefix="project_rationale_and_justification - Strategic Importance (National/Regional): ")
    project_rationale_and_justification_Economic_Benefits = dspy.OutputField(desc="Extract facts about Economic Benefits", prefix="project_rationale_and_justification - Economic Benefits: ")
    project_rationale_and_justification_Social_Benefits = dspy.OutputField(desc="Extract facts about Social Benefits", prefix="project_rationale_and_justification - Social Benefits: ")
    objectives_of_the_esia_Identify_and_Assess_Impacts = dspy.OutputField(desc="Extract facts about Identify and Assess Impacts", prefix="objectives_of_the_esia - Identify and Assess Impacts: ")
    objectives_of_the_esia_Develop_Mitigation_Measures = dspy.OutputField(desc="Extract facts about Develop Mitigation Measures", prefix="objectives_of_the_esia - Develop Mitigation Measures: ")
    objectives_of_the_esia_Ensure_Compliance_with_Laws_and_Standards = dspy.OutputField(desc="Extract facts about Ensure Compliance with Laws and Standards", prefix="objectives_of_the_esia - Ensure Compliance with Laws and Standards: ")
    objectives_of_the_esia_Facilitate_Public_Participation = dspy.OutputField(desc="Extract facts about Facilitate Public Participation", prefix="objectives_of_the_esia - Facilitate Public Participation: ")
    scope_of_the_esia_Geographical_Scope_Study_Area = dspy.OutputField(desc="Extract facts about Geographical Scope (Study Area)", prefix="scope_of_the_esia - Geographical Scope (Study Area): ")
    scope_of_the_esia_Temporal_Scope_Construction_Operation_Decommissioning = dspy.OutputField(desc="Extract facts about Temporal Scope (Construction, Operation, Decommissioning)", prefix="scope_of_the_esia - Temporal Scope (Construction, Operation, Decommissioning): ")
    scope_of_the_esia_Technical_Scope_Key_Issues_Covered = dspy.OutputField(desc="Extract facts about Technical Scope (Key Issues Covered)", prefix="scope_of_the_esia - Technical Scope (Key Issues Covered): ")
    scope_of_the_esia_Limitations_and_Assumptions = dspy.OutputField(desc="Extract facts about Limitations and Assumptions", prefix="scope_of_the_esia - Limitations and Assumptions: ")
    esia_methodology_Screening_and_Scoping_Process = dspy.OutputField(desc="Extract facts about Screening and Scoping Process", prefix="esia_methodology - Screening and Scoping Process: ")
    esia_methodology_Baseline_Data_Collection_Methods_Primary_Secondary = dspy.OutputField(desc="Extract facts about Baseline Data Collection Methods (Primary/Secondary)", prefix="esia_methodology - Baseline Data Collection Methods (Primary/Secondary): ")
    esia_methodology_Impact_Assessment_Methodology_Significance_Criteria = dspy.OutputField(desc="Extract facts about Impact Assessment Methodology (Significance Criteria)", prefix="esia_methodology - Impact Assessment Methodology (Significance Criteria): ")
    esia_methodology_Stakeholder_Engagement_Methodology = dspy.OutputField(desc="Extract facts about Stakeholder Engagement Methodology", prefix="esia_methodology - Stakeholder Engagement Methodology: ")
    structure_of_the_esia_report_Overview_of_Report_Chapters = dspy.OutputField(desc="Extract facts about Overview of Report Chapters", prefix="structure_of_the_esia_report - Overview of Report Chapters: ")
    esia_team_and_competency_Lead_Consultant_Firm = dspy.OutputField(desc="Extract facts about Lead Consultant / Firm", prefix="esia_team_and_competency - Lead Consultant / Firm: ")
    esia_team_and_competency_Key_Experts_and_Specialists = dspy.OutputField(desc="Extract facts about Key Experts and Specialists", prefix="esia_team_and_competency - Key Experts and Specialists: ")
    esia_team_and_competency_Accreditation_Certification = dspy.OutputField(desc="Extract facts about Accreditation / Certification", prefix="esia_team_and_competency - Accreditation / Certification: ")


class MineralWasteManagementSignature(dspy.Signature):
    """
    Extracted facts for Mineral Waste Management.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Waste_Rock_Management = dspy.OutputField(desc="Extract facts about Waste Rock Management, specifically: Geochemical Characterization, Storage Facilities, Rehabilitation", prefix="Waste Rock Management: ")


class MineClosureAndRehabilitationSignature(dspy.Signature):
    """
    Extracted facts for Mine Closure And Rehabilitation.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Closure_Plan = dspy.OutputField(desc="Extract facts about Closure Plan, specifically: Progressive Rehabilitation, Final Landform Design, Post-Mining Land Use", prefix="Closure Plan: ")
    Post_Closure_Monitoring = dspy.OutputField(desc="Extract facts about Post-Closure Monitoring, specifically: Water Quality, Slope Stability, Revegetation Success", prefix="Post-Closure Monitoring: ")


class MineSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Mine Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Tailings_Management = dspy.OutputField(desc="Extract facts about Tailings Management, specifically: Design, Monitoring, Closure", prefix="Tailings Management: ")
    Acid_Mine_Drainage = dspy.OutputField(desc="Extract facts about Acid Mine Drainage, specifically: Prediction, Prevention, Treatment", prefix="Acid Mine Drainage: ")
    Blasting_and_Vibration = dspy.OutputField(desc="Extract facts about Blasting and Vibration, specifically: Ground Vibration, Air Overpressure, Structural Integrity", prefix="Blasting and Vibration: ")


class MitigationAndEnhancementMeasuresSignature(dspy.Signature):
    """
    Extracted facts for Mitigation And Enhancement Measures.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    general_mitigation_principles_Mitigation_Hierarchy_Application_Avoid_Minimize_Restore_Offset = dspy.OutputField(desc="Extract facts about Mitigation Hierarchy Application (Avoid/Minimize/Restore/Offset)", prefix="general_mitigation_principles - Mitigation Hierarchy Application (Avoid/Minimize/Restore/Offset): ")
    general_mitigation_principles_Precautionary_Principle_Application = dspy.OutputField(desc="Extract facts about Precautionary Principle Application", prefix="general_mitigation_principles - Precautionary Principle Application: ")
    general_mitigation_principles_Polluter_Pays_Principle = dspy.OutputField(desc="Extract facts about Polluter Pays Principle", prefix="general_mitigation_principles - Polluter Pays Principle: ")
    general_mitigation_principles_Adaptive_Management_Approach = dspy.OutputField(desc="Extract facts about Adaptive Management Approach", prefix="general_mitigation_principles - Adaptive Management Approach: ")
    general_mitigation_principles_Best_Available_Techniques_BAT = dspy.OutputField(desc="Extract facts about Best Available Techniques (BAT)", prefix="general_mitigation_principles - Best Available Techniques (BAT): ")
    general_mitigation_principles_Good_International_Industry_Practice_GIIP = dspy.OutputField(desc="Extract facts about Good International Industry Practice (GIIP)", prefix="general_mitigation_principles - Good International Industry Practice (GIIP): ")
    general_mitigation_principles_Integrated_Management_Systems_ISO_14001_45001 = dspy.OutputField(desc="Extract facts about Integrated Management Systems (ISO 14001/45001)", prefix="general_mitigation_principles - Integrated Management Systems (ISO 14001/45001): ")
    mitigation_measures_for_physical_environment_7_2_1_Air_Quality_Management_Dust_Suppression_Measures_Watering_Chemical = dspy.OutputField(desc="Extract facts about Dust Suppression Measures (Watering/Chemical)", prefix="mitigation_measures_for_physical_environment - 7.2.1 Air Quality Management - Dust Suppression Measures (Watering/Chemical): ")
    mitigation_measures_for_physical_environment_7_2_1_Air_Quality_Management_Emission_Control_Technologies_Filters_Scrubbers = dspy.OutputField(desc="Extract facts about Emission Control Technologies (Filters/Scrubbers)", prefix="mitigation_measures_for_physical_environment - 7.2.1 Air Quality Management - Emission Control Technologies (Filters/Scrubbers): ")
    mitigation_measures_for_physical_environment_7_2_1_Air_Quality_Management_Vehicle_Equipment_Maintenance_Schedules = dspy.OutputField(desc="Extract facts about Vehicle/Equipment Maintenance Schedules", prefix="mitigation_measures_for_physical_environment - 7.2.1 Air Quality Management - Vehicle/Equipment Maintenance Schedules: ")
    mitigation_measures_for_physical_environment_7_2_1_Air_Quality_Management_Speed_Limits_on_Unpaved_Roads = dspy.OutputField(desc="Extract facts about Speed Limits on Unpaved Roads", prefix="mitigation_measures_for_physical_environment - 7.2.1 Air Quality Management - Speed Limits on Unpaved Roads: ")
    mitigation_measures_for_physical_environment_7_2_1_Air_Quality_Management_Covering_of_Stockpiles_Trucks = dspy.OutputField(desc="Extract facts about Covering of Stockpiles/Trucks", prefix="mitigation_measures_for_physical_environment - 7.2.1 Air Quality Management - Covering of Stockpiles/Trucks: ")
    mitigation_measures_for_physical_environment_7_2_1_Air_Quality_Management_Greenhouse_Gas_Reduction_Strategies = dspy.OutputField(desc="Extract facts about Greenhouse Gas Reduction Strategies", prefix="mitigation_measures_for_physical_environment - 7.2.1 Air Quality Management - Greenhouse Gas Reduction Strategies: ")
    mitigation_measures_for_physical_environment_7_2_2_Noise_and_Vibration_Control_Noise_Barriers_Enclosures = dspy.OutputField(desc="Extract facts about Noise Barriers/Enclosures", prefix="mitigation_measures_for_physical_environment - 7.2.2 Noise and Vibration Control - Noise Barriers/Enclosures: ")
    mitigation_measures_for_physical_environment_7_2_2_Noise_and_Vibration_Control_Equipment_Silencers_Mufflers = dspy.OutputField(desc="Extract facts about Equipment Silencers/Mufflers", prefix="mitigation_measures_for_physical_environment - 7.2.2 Noise and Vibration Control - Equipment Silencers/Mufflers: ")
    mitigation_measures_for_physical_environment_7_2_2_Noise_and_Vibration_Control_Scheduling_of_Noisy_Activities_Daytime_only = dspy.OutputField(desc="Extract facts about Scheduling of Noisy Activities (Daytime only)", prefix="mitigation_measures_for_physical_environment - 7.2.2 Noise and Vibration Control - Scheduling of Noisy Activities (Daytime only): ")
    mitigation_measures_for_physical_environment_7_2_2_Noise_and_Vibration_Control_Vibration_Isolation_Measures = dspy.OutputField(desc="Extract facts about Vibration Isolation Measures", prefix="mitigation_measures_for_physical_environment - 7.2.2 Noise and Vibration Control - Vibration Isolation Measures: ")
    mitigation_measures_for_physical_environment_7_2_2_Noise_and_Vibration_Control_Blasting_Protocols_Warning_systems_Timing = dspy.OutputField(desc="Extract facts about Blasting Protocols (Warning systems/Timing)", prefix="mitigation_measures_for_physical_environment - 7.2.2 Noise and Vibration Control - Blasting Protocols (Warning systems/Timing): ")
    mitigation_measures_for_physical_environment_7_2_2_Noise_and_Vibration_Control_Traffic_Management_Plans = dspy.OutputField(desc="Extract facts about Traffic Management Plans", prefix="mitigation_measures_for_physical_environment - 7.2.2 Noise and Vibration Control - Traffic Management Plans: ")
    mitigation_measures_for_physical_environment_7_2_3_Water_Resources_Management_Wastewater_Treatment_Systems_Oil_water_separators_STPs = dspy.OutputField(desc="Extract facts about Wastewater Treatment Systems (Oil-water separators/STPs)", prefix="mitigation_measures_for_physical_environment - 7.2.3 Water Resources Management - Wastewater Treatment Systems (Oil-water separators/STPs): ")
    mitigation_measures_for_physical_environment_7_2_3_Water_Resources_Management_Stormwater_Management_Plans = dspy.OutputField(desc="Extract facts about Stormwater Management Plans", prefix="mitigation_measures_for_physical_environment - 7.2.3 Water Resources Management - Stormwater Management Plans: ")
    mitigation_measures_for_physical_environment_7_2_3_Water_Resources_Management_Sediment_and_Erosion_Control_Structures_Silt_fences_Sediment_ponds = dspy.OutputField(desc="Extract facts about Sediment and Erosion Control Structures (Silt fences/Sediment ponds)", prefix="mitigation_measures_for_physical_environment - 7.2.3 Water Resources Management - Sediment and Erosion Control Structures (Silt fences/Sediment ponds): ")
    mitigation_measures_for_physical_environment_7_2_3_Water_Resources_Management_Water_Recycling_and_Reuse = dspy.OutputField(desc="Extract facts about Water Recycling and Reuse", prefix="mitigation_measures_for_physical_environment - 7.2.3 Water Resources Management - Water Recycling and Reuse: ")
    mitigation_measures_for_physical_environment_7_2_3_Water_Resources_Management_Spill_Prevention_and_Control_Plans = dspy.OutputField(desc="Extract facts about Spill Prevention and Control Plans", prefix="mitigation_measures_for_physical_environment - 7.2.3 Water Resources Management - Spill Prevention and Control Plans: ")
    mitigation_measures_for_physical_environment_7_2_3_Water_Resources_Management_Ecological_Flow_Maintenance = dspy.OutputField(desc="Extract facts about Ecological Flow Maintenance", prefix="mitigation_measures_for_physical_environment - 7.2.3 Water Resources Management - Ecological Flow Maintenance: ")
    mitigation_measures_for_physical_environment_7_2_4_Soil_and_Land_Management_Topsoil_Stripping_and_Stockpiling = dspy.OutputField(desc="Extract facts about Topsoil Stripping and Stockpiling", prefix="mitigation_measures_for_physical_environment - 7.2.4 Soil and Land Management - Topsoil Stripping and Stockpiling: ")
    mitigation_measures_for_physical_environment_7_2_4_Soil_and_Land_Management_Soil_Erosion_Control_Measures_Revegetation_Mulching = dspy.OutputField(desc="Extract facts about Soil Erosion Control Measures (Revegetation/Mulching)", prefix="mitigation_measures_for_physical_environment - 7.2.4 Soil and Land Management - Soil Erosion Control Measures (Revegetation/Mulching): ")
    mitigation_measures_for_physical_environment_7_2_4_Soil_and_Land_Management_Contaminated_Land_Remediation = dspy.OutputField(desc="Extract facts about Contaminated Land Remediation", prefix="mitigation_measures_for_physical_environment - 7.2.4 Soil and Land Management - Contaminated Land Remediation: ")
    mitigation_measures_for_physical_environment_7_2_4_Soil_and_Land_Management_Waste_Management_Plans_Hazardous_Non_hazardous = dspy.OutputField(desc="Extract facts about Waste Management Plans (Hazardous/Non-hazardous)", prefix="mitigation_measures_for_physical_environment - 7.2.4 Soil and Land Management - Waste Management Plans (Hazardous/Non-hazardous): ")
    mitigation_measures_for_physical_environment_7_2_4_Soil_and_Land_Management_Land_Rehabilitation_and_Closure_Plans = dspy.OutputField(desc="Extract facts about Land Rehabilitation and Closure Plans", prefix="mitigation_measures_for_physical_environment - 7.2.4 Soil and Land Management - Land Rehabilitation and Closure Plans: ")
    mitigation_measures_for_physical_environment_7_2_5_Landscape_and_Visual_Mitigation_Screening_Planting_Landscaping = dspy.OutputField(desc="Extract facts about Screening Planting/Landscaping", prefix="mitigation_measures_for_physical_environment - 7.2.5 Landscape and Visual Mitigation - Screening Planting/Landscaping: ")
    mitigation_measures_for_physical_environment_7_2_5_Landscape_and_Visual_Mitigation_Design_Integration_with_Landscape = dspy.OutputField(desc="Extract facts about Design Integration with Landscape", prefix="mitigation_measures_for_physical_environment - 7.2.5 Landscape and Visual Mitigation - Design Integration with Landscape: ")
    mitigation_measures_for_physical_environment_7_2_5_Landscape_and_Visual_Mitigation_Light_Pollution_Control_Directional_lighting = dspy.OutputField(desc="Extract facts about Light Pollution Control (Directional lighting)", prefix="mitigation_measures_for_physical_environment - 7.2.5 Landscape and Visual Mitigation - Light Pollution Control (Directional lighting): ")
    mitigation_measures_for_physical_environment_7_2_5_Landscape_and_Visual_Mitigation_Site_Restoration_after_Decommissioning = dspy.OutputField(desc="Extract facts about Site Restoration after Decommissioning", prefix="mitigation_measures_for_physical_environment - 7.2.5 Landscape and Visual Mitigation - Site Restoration after Decommissioning: ")
    mitigation_measures_for_biological_environment_7_3_1_Mitigation_Hierarchy_Application_Avoidance_Measures = dspy.OutputField(desc="Extract facts about Avoidance Measures", prefix="mitigation_measures_for_biological_environment - 7.3.1 Mitigation Hierarchy Application - Avoidance Measures: ")
    mitigation_measures_for_biological_environment_7_3_1_Mitigation_Hierarchy_Application_Minimization_Measures = dspy.OutputField(desc="Extract facts about Minimization Measures", prefix="mitigation_measures_for_biological_environment - 7.3.1 Mitigation Hierarchy Application - Minimization Measures: ")
    mitigation_measures_for_biological_environment_7_3_1_Mitigation_Hierarchy_Application_Restoration_Measures = dspy.OutputField(desc="Extract facts about Restoration Measures", prefix="mitigation_measures_for_biological_environment - 7.3.1 Mitigation Hierarchy Application - Restoration Measures: ")
    mitigation_measures_for_biological_environment_7_3_1_Mitigation_Hierarchy_Application_Biodiversity_Offsets_if_applicable = dspy.OutputField(desc="Extract facts about Biodiversity Offsets (if applicable)", prefix="mitigation_measures_for_biological_environment - 7.3.1 Mitigation Hierarchy Application - Biodiversity Offsets (if applicable): ")
    mitigation_measures_for_biological_environment_7_3_2_Habitat_Protection_and_Restoration_Protected_Area_Establishment = dspy.OutputField(desc="Extract facts about Protected Area Establishment", prefix="mitigation_measures_for_biological_environment - 7.3.2 Habitat Protection and Restoration - Protected Area Establishment: ")
    mitigation_measures_for_biological_environment_7_3_2_Habitat_Protection_and_Restoration_Habitat_Restoration_Plan = dspy.OutputField(desc="Extract facts about Habitat Restoration Plan", prefix="mitigation_measures_for_biological_environment - 7.3.2 Habitat Protection and Restoration - Habitat Restoration Plan: ")
    mitigation_measures_for_biological_environment_7_3_2_Habitat_Protection_and_Restoration_Restoration_Area_hectares = dspy.OutputField(desc="Extract facts about Restoration Area (hectares)", prefix="mitigation_measures_for_biological_environment - 7.3.2 Habitat Protection and Restoration - Restoration Area (hectares): ")
    mitigation_measures_for_biological_environment_7_3_2_Habitat_Protection_and_Restoration_Ecological_Connectivity_Measures = dspy.OutputField(desc="Extract facts about Ecological Connectivity Measures", prefix="mitigation_measures_for_biological_environment - 7.3.2 Habitat Protection and Restoration - Ecological Connectivity Measures: ")
    mitigation_measures_for_biological_environment_7_3_2_Habitat_Protection_and_Restoration_Wildlife_Corridor_Design = dspy.OutputField(desc="Extract facts about Wildlife Corridor Design", prefix="mitigation_measures_for_biological_environment - 7.3.2 Habitat Protection and Restoration - Wildlife Corridor Design: ")
    mitigation_measures_for_biological_environment_7_3_3_Species_Specific_Mitigation_Mitigation_for_IUCN_Red_List_Species = dspy.OutputField(desc="Extract facts about Mitigation for IUCN Red List Species", prefix="mitigation_measures_for_biological_environment - 7.3.3 Species-Specific Mitigation - Mitigation for IUCN Red List Species: ")
    mitigation_measures_for_biological_environment_7_3_3_Species_Specific_Mitigation_Mitigation_for_Endemic_Species = dspy.OutputField(desc="Extract facts about Mitigation for Endemic Species", prefix="mitigation_measures_for_biological_environment - 7.3.3 Species-Specific Mitigation - Mitigation for Endemic Species: ")
    mitigation_measures_for_biological_environment_7_3_3_Species_Specific_Mitigation_Translocation_Plans_if_applicable = dspy.OutputField(desc="Extract facts about Translocation Plans (if applicable)", prefix="mitigation_measures_for_biological_environment - 7.3.3 Species-Specific Mitigation - Translocation Plans (if applicable): ")
    mitigation_measures_for_biological_environment_7_3_3_Species_Specific_Mitigation_Rescue_and_Relocation_Programs = dspy.OutputField(desc="Extract facts about Rescue and Relocation Programs", prefix="mitigation_measures_for_biological_environment - 7.3.3 Species-Specific Mitigation - Rescue and Relocation Programs: ")
    mitigation_measures_for_biological_environment_7_3_3_Species_Specific_Mitigation_Breeding_Programs_if_applicable = dspy.OutputField(desc="Extract facts about Breeding Programs (if applicable)", prefix="mitigation_measures_for_biological_environment - 7.3.3 Species-Specific Mitigation - Breeding Programs (if applicable): ")
    mitigation_measures_for_biological_environment_7_3_4_Aquatic_Biodiversity_Mitigation_Fish_Passage_Facilities = dspy.OutputField(desc="Extract facts about Fish Passage Facilities", prefix="mitigation_measures_for_biological_environment - 7.3.4 Aquatic Biodiversity Mitigation - Fish Passage Facilities: ")
    mitigation_measures_for_biological_environment_7_3_4_Aquatic_Biodiversity_Mitigation_Environmental_Flow_Requirements = dspy.OutputField(desc="Extract facts about Environmental Flow Requirements", prefix="mitigation_measures_for_biological_environment - 7.3.4 Aquatic Biodiversity Mitigation - Environmental Flow Requirements: ")
    mitigation_measures_for_biological_environment_7_3_4_Aquatic_Biodiversity_Mitigation_Spawning_Habitat_Protection = dspy.OutputField(desc="Extract facts about Spawning Habitat Protection", prefix="mitigation_measures_for_biological_environment - 7.3.4 Aquatic Biodiversity Mitigation - Spawning Habitat Protection: ")
    mitigation_measures_for_biological_environment_7_3_4_Aquatic_Biodiversity_Mitigation_Water_Quality_Management = dspy.OutputField(desc="Extract facts about Water Quality Management", prefix="mitigation_measures_for_biological_environment - 7.3.4 Aquatic Biodiversity Mitigation - Water Quality Management: ")
    mitigation_measures_for_biological_environment_7_3_5_Invasive_Species_Management_Invasive_Species_Prevention_Plan = dspy.OutputField(desc="Extract facts about Invasive Species Prevention Plan", prefix="mitigation_measures_for_biological_environment - 7.3.5 Invasive Species Management - Invasive Species Prevention Plan: ")
    mitigation_measures_for_biological_environment_7_3_5_Invasive_Species_Management_Early_Detection_and_Rapid_Response = dspy.OutputField(desc="Extract facts about Early Detection and Rapid Response", prefix="mitigation_measures_for_biological_environment - 7.3.5 Invasive Species Management - Early Detection and Rapid Response: ")
    mitigation_measures_for_biological_environment_7_3_5_Invasive_Species_Management_Control_and_Eradication_Measures = dspy.OutputField(desc="Extract facts about Control and Eradication Measures", prefix="mitigation_measures_for_biological_environment - 7.3.5 Invasive Species Management - Control and Eradication Measures: ")
    mitigation_measures_for_biological_environment_7_3_6_Net_Gain_No_Net_Loss_Strategy_Biodiversity_Net_Gain_Target = dspy.OutputField(desc="Extract facts about Biodiversity Net Gain Target", prefix="mitigation_measures_for_biological_environment - 7.3.6 Net Gain/No Net Loss Strategy - Biodiversity Net Gain Target: ")
    mitigation_measures_for_biological_environment_7_3_6_Net_Gain_No_Net_Loss_Strategy_No_Net_Loss_Commitment_for_Critical_Habitat = dspy.OutputField(desc="Extract facts about No Net Loss Commitment (for Critical Habitat)", prefix="mitigation_measures_for_biological_environment - 7.3.6 Net Gain/No Net Loss Strategy - No Net Loss Commitment (for Critical Habitat): ")
    mitigation_measures_for_biological_environment_7_3_6_Net_Gain_No_Net_Loss_Strategy_Offset_Ratio = dspy.OutputField(desc="Extract facts about Offset Ratio", prefix="mitigation_measures_for_biological_environment - 7.3.6 Net Gain/No Net Loss Strategy - Offset Ratio: ")
    mitigation_measures_for_biological_environment_7_3_6_Net_Gain_No_Net_Loss_Strategy_Offset_Location_and_Design = dspy.OutputField(desc="Extract facts about Offset Location and Design", prefix="mitigation_measures_for_biological_environment - 7.3.6 Net Gain/No Net Loss Strategy - Offset Location and Design: ")
    mitigation_measures_for_biological_environment_7_3_6_Net_Gain_No_Net_Loss_Strategy_Long_term_Offset_Management = dspy.OutputField(desc="Extract facts about Long-term Offset Management", prefix="mitigation_measures_for_biological_environment - 7.3.6 Net Gain/No Net Loss Strategy - Long-term Offset Management: ")
    mitigation_measures_for_socio_economic_environment_7_4_1_Resettlement_and_Livelihood_Restoration_Resettlement_Action_Plan_RAP_Implementation = dspy.OutputField(desc="Extract facts about Resettlement Action Plan (RAP) Implementation", prefix="mitigation_measures_for_socio_economic_environment - 7.4.1 Resettlement and Livelihood Restoration - Resettlement Action Plan (RAP) Implementation: ")
    mitigation_measures_for_socio_economic_environment_7_4_1_Resettlement_and_Livelihood_Restoration_Livelihood_Restoration_Plan_LRP_Implementation = dspy.OutputField(desc="Extract facts about Livelihood Restoration Plan (LRP) Implementation", prefix="mitigation_measures_for_socio_economic_environment - 7.4.1 Resettlement and Livelihood Restoration - Livelihood Restoration Plan (LRP) Implementation: ")
    mitigation_measures_for_socio_economic_environment_7_4_1_Resettlement_and_Livelihood_Restoration_Compensation_Framework_Replacement_Cost = dspy.OutputField(desc="Extract facts about Compensation Framework (Replacement Cost)", prefix="mitigation_measures_for_socio_economic_environment - 7.4.1 Resettlement and Livelihood Restoration - Compensation Framework (Replacement Cost): ")
    mitigation_measures_for_socio_economic_environment_7_4_1_Resettlement_and_Livelihood_Restoration_Assistance_to_Vulnerable_Groups = dspy.OutputField(desc="Extract facts about Assistance to Vulnerable Groups", prefix="mitigation_measures_for_socio_economic_environment - 7.4.1 Resettlement and Livelihood Restoration - Assistance to Vulnerable Groups: ")
    mitigation_measures_for_socio_economic_environment_7_4_1_Resettlement_and_Livelihood_Restoration_Grievance_Redress_Mechanism_Resettlement_specific = dspy.OutputField(desc="Extract facts about Grievance Redress Mechanism (Resettlement-specific)", prefix="mitigation_measures_for_socio_economic_environment - 7.4.1 Resettlement and Livelihood Restoration - Grievance Redress Mechanism (Resettlement-specific): ")
    mitigation_measures_for_socio_economic_environment_7_4_2_Community_Health_and_Safety_Community_Health_and_Safety_Plan = dspy.OutputField(desc="Extract facts about Community Health and Safety Plan", prefix="mitigation_measures_for_socio_economic_environment - 7.4.2 Community Health and Safety - Community Health and Safety Plan: ")
    mitigation_measures_for_socio_economic_environment_7_4_2_Community_Health_and_Safety_Traffic_Safety_Measures_Speed_limits_Signage = dspy.OutputField(desc="Extract facts about Traffic Safety Measures (Speed limits, Signage)", prefix="mitigation_measures_for_socio_economic_environment - 7.4.2 Community Health and Safety - Traffic Safety Measures (Speed limits, Signage): ")
    mitigation_measures_for_socio_economic_environment_7_4_2_Community_Health_and_Safety_Disease_Prevention_Programs_HIV_AIDS_Vector_borne = dspy.OutputField(desc="Extract facts about Disease Prevention Programs (HIV/AIDS, Vector-borne)", prefix="mitigation_measures_for_socio_economic_environment - 7.4.2 Community Health and Safety - Disease Prevention Programs (HIV/AIDS, Vector-borne): ")
    mitigation_measures_for_socio_economic_environment_7_4_2_Community_Health_and_Safety_Emergency_Preparedness_and_Response_Plan_Community = dspy.OutputField(desc="Extract facts about Emergency Preparedness and Response Plan (Community)", prefix="mitigation_measures_for_socio_economic_environment - 7.4.2 Community Health and Safety - Emergency Preparedness and Response Plan (Community): ")
    mitigation_measures_for_socio_economic_environment_7_4_2_Community_Health_and_Safety_Influx_Management_Plan = dspy.OutputField(desc="Extract facts about Influx Management Plan", prefix="mitigation_measures_for_socio_economic_environment - 7.4.2 Community Health and Safety - Influx Management Plan: ")
    mitigation_measures_for_socio_economic_environment_7_4_2_Community_Health_and_Safety_Security_Personnel_Management_Voluntary_Principles = dspy.OutputField(desc="Extract facts about Security Personnel Management (Voluntary Principles)", prefix="mitigation_measures_for_socio_economic_environment - 7.4.2 Community Health and Safety - Security Personnel Management (Voluntary Principles): ")
    mitigation_measures_for_socio_economic_environment_7_4_3_Cultural_Heritage_Protection_Cultural_Heritage_Management_Plan_CHMP = dspy.OutputField(desc="Extract facts about Cultural Heritage Management Plan (CHMP)", prefix="mitigation_measures_for_socio_economic_environment - 7.4.3 Cultural Heritage Protection - Cultural Heritage Management Plan (CHMP): ")
    mitigation_measures_for_socio_economic_environment_7_4_3_Cultural_Heritage_Protection_Chance_Finds_Procedure = dspy.OutputField(desc="Extract facts about Chance Finds Procedure", prefix="mitigation_measures_for_socio_economic_environment - 7.4.3 Cultural Heritage Protection - Chance Finds Procedure: ")
    mitigation_measures_for_socio_economic_environment_7_4_3_Cultural_Heritage_Protection_Protection_of_Sacred_Sites_Graves = dspy.OutputField(desc="Extract facts about Protection of Sacred Sites/Graves", prefix="mitigation_measures_for_socio_economic_environment - 7.4.3 Cultural Heritage Protection - Protection of Sacred Sites/Graves: ")
    mitigation_measures_for_socio_economic_environment_7_4_3_Cultural_Heritage_Protection_Archaeological_Salvage_Excavation = dspy.OutputField(desc="Extract facts about Archaeological Salvage/Excavation", prefix="mitigation_measures_for_socio_economic_environment - 7.4.3 Cultural Heritage Protection - Archaeological Salvage/Excavation: ")
    mitigation_measures_for_socio_economic_environment_7_4_4_Indigenous_Peoples_Development_Indigenous_Peoples_Plan_IPP = dspy.OutputField(desc="Extract facts about Indigenous Peoples Plan (IPP)", prefix="mitigation_measures_for_socio_economic_environment - 7.4.4 Indigenous Peoples Development - Indigenous Peoples Plan (IPP): ")
    mitigation_measures_for_socio_economic_environment_7_4_4_Indigenous_Peoples_Development_Free_Prior_and_Informed_Consent_FPIC_Process = dspy.OutputField(desc="Extract facts about Free, Prior, and Informed Consent (FPIC) Process", prefix="mitigation_measures_for_socio_economic_environment - 7.4.4 Indigenous Peoples Development - Free, Prior, and Informed Consent (FPIC) Process: ")
    mitigation_measures_for_socio_economic_environment_7_4_4_Indigenous_Peoples_Development_Benefit_Sharing_Mechanisms = dspy.OutputField(desc="Extract facts about Benefit Sharing Mechanisms", prefix="mitigation_measures_for_socio_economic_environment - 7.4.4 Indigenous Peoples Development - Benefit Sharing Mechanisms: ")
    mitigation_measures_for_socio_economic_environment_7_4_4_Indigenous_Peoples_Development_Protection_of_Traditional_Knowledge_Lands = dspy.OutputField(desc="Extract facts about Protection of Traditional Knowledge/Lands", prefix="mitigation_measures_for_socio_economic_environment - 7.4.4 Indigenous Peoples Development - Protection of Traditional Knowledge/Lands: ")
    mitigation_measures_for_socio_economic_environment_7_4_5_Labor_and_Working_Conditions_Human_Resources_Policy = dspy.OutputField(desc="Extract facts about Human Resources Policy", prefix="mitigation_measures_for_socio_economic_environment - 7.4.5 Labor and Working Conditions - Human Resources Policy: ")
    mitigation_measures_for_socio_economic_environment_7_4_5_Labor_and_Working_Conditions_Occupational_Health_and_Safety_OHS_Plan = dspy.OutputField(desc="Extract facts about Occupational Health and Safety (OHS) Plan", prefix="mitigation_measures_for_socio_economic_environment - 7.4.5 Labor and Working Conditions - Occupational Health and Safety (OHS) Plan: ")
    mitigation_measures_for_socio_economic_environment_7_4_5_Labor_and_Working_Conditions_Worker_Accommodation_Plan = dspy.OutputField(desc="Extract facts about Worker Accommodation Plan", prefix="mitigation_measures_for_socio_economic_environment - 7.4.5 Labor and Working Conditions - Worker Accommodation Plan: ")
    mitigation_measures_for_socio_economic_environment_7_4_5_Labor_and_Working_Conditions_Worker_Grievance_Mechanism = dspy.OutputField(desc="Extract facts about Worker Grievance Mechanism", prefix="mitigation_measures_for_socio_economic_environment - 7.4.5 Labor and Working Conditions - Worker Grievance Mechanism: ")
    mitigation_measures_for_socio_economic_environment_7_4_5_Labor_and_Working_Conditions_Child_Labor_and_Forced_Labor_Prevention = dspy.OutputField(desc="Extract facts about Child Labor and Forced Labor Prevention", prefix="mitigation_measures_for_socio_economic_environment - 7.4.5 Labor and Working Conditions - Child Labor and Forced Labor Prevention: ")
    mitigation_measures_for_socio_economic_environment_7_4_5_Labor_and_Working_Conditions_Local_Recruitment_Policy = dspy.OutputField(desc="Extract facts about Local Recruitment Policy", prefix="mitigation_measures_for_socio_economic_environment - 7.4.5 Labor and Working Conditions - Local Recruitment Policy: ")
    mitigation_measures_for_socio_economic_environment_7_4_6_Local_Content_and_Economy_Local_Procurement_Plan = dspy.OutputField(desc="Extract facts about Local Procurement Plan", prefix="mitigation_measures_for_socio_economic_environment - 7.4.6 Local Content and Economy - Local Procurement Plan: ")
    mitigation_measures_for_socio_economic_environment_7_4_6_Local_Content_and_Economy_Local_Employment_Targets = dspy.OutputField(desc="Extract facts about Local Employment Targets", prefix="mitigation_measures_for_socio_economic_environment - 7.4.6 Local Content and Economy - Local Employment Targets: ")
    mitigation_measures_for_socio_economic_environment_7_4_6_Local_Content_and_Economy_Skills_Development_and_Training_Programs = dspy.OutputField(desc="Extract facts about Skills Development and Training Programs", prefix="mitigation_measures_for_socio_economic_environment - 7.4.6 Local Content and Economy - Skills Development and Training Programs: ")
    mitigation_measures_for_socio_economic_environment_7_4_6_Local_Content_and_Economy_Community_Development_Plan_CDP = dspy.OutputField(desc="Extract facts about Community Development Plan (CDP)", prefix="mitigation_measures_for_socio_economic_environment - 7.4.6 Local Content and Economy - Community Development Plan (CDP): ")


class NickelSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Nickel Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Laterite_Management = dspy.OutputField(desc="Extract facts about Laterite Management, specifically: Soil Erosion Control, Runoff Management, Sedimentation Ponds", prefix="Laterite Management: ")
    Smelting_and_Processing = dspy.OutputField(desc="Extract facts about Smelting and Processing, specifically: Air Emissions (SO2, Particulates), Slag Management, Energy Consumption", prefix="Smelting and Processing: ")
    Tailings_Management_HPAL_RKEF = dspy.OutputField(desc="Extract facts about Tailings Management (HPAL/RKEF), specifically: Tailings Storage Facility (TSF) Stability, Acid Leaching Residue, Effluent Treatment", prefix="Tailings Management (HPAL/RKEF): ")


class NoiseAndVibrationSignature(dspy.Signature):
    """
    Extracted facts for Noise And Vibration.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Industrial_Operations = dspy.OutputField(desc="Extract facts about Industrial Operations, specifically: Machinery Noise, Process Noise", prefix="Industrial Operations: ")


class PipelineIntegrityAndSafetySignature(dspy.Signature):
    """
    Extracted facts for Pipeline Integrity And Safety.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Corrosion_Management = dspy.OutputField(desc="Extract facts about Corrosion Management", prefix="Corrosion Management: ")
    Leak_Detection = dspy.OutputField(desc="Extract facts about Leak Detection", prefix="Leak Detection: ")


class PolicyLegalAndAdministrativeFrameworkSignature(dspy.Signature):
    """
    Extracted facts for Policy Legal And Administrative Framework.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    national_policy_and_legal_framework_Constitution = dspy.OutputField(desc="Extract facts about Constitution", prefix="national_policy_and_legal_framework - Constitution: ")
    national_policy_and_legal_framework_National_Environmental_Policy = dspy.OutputField(desc="Extract facts about National Environmental Policy", prefix="national_policy_and_legal_framework - National Environmental Policy: ")
    national_policy_and_legal_framework_Environmental_Management_Act_Law = dspy.OutputField(desc="Extract facts about Environmental Management Act / Law", prefix="national_policy_and_legal_framework - Environmental Management Act / Law: ")
    national_policy_and_legal_framework_EIA_Regulations_and_Guidelines = dspy.OutputField(desc="Extract facts about EIA Regulations and Guidelines", prefix="national_policy_and_legal_framework - EIA Regulations and Guidelines: ")
    national_policy_and_legal_framework_Land_Acquisition_and_Resettlement_Legislation = dspy.OutputField(desc="Extract facts about Land Acquisition and Resettlement Legislation", prefix="national_policy_and_legal_framework - Land Acquisition and Resettlement Legislation: ")
    national_policy_and_legal_framework_Labor_and_Working_Conditions_Legislation = dspy.OutputField(desc="Extract facts about Labor and Working Conditions Legislation", prefix="national_policy_and_legal_framework - Labor and Working Conditions Legislation: ")
    national_policy_and_legal_framework_Cultural_Heritage_Legislation = dspy.OutputField(desc="Extract facts about Cultural Heritage Legislation", prefix="national_policy_and_legal_framework - Cultural Heritage Legislation: ")
    national_policy_and_legal_framework_Biodiversity_and_Protected_Areas_Legislation = dspy.OutputField(desc="Extract facts about Biodiversity and Protected Areas Legislation", prefix="national_policy_and_legal_framework - Biodiversity and Protected Areas Legislation: ")
    national_policy_and_legal_framework_Water_Resources_Legislation = dspy.OutputField(desc="Extract facts about Water Resources Legislation", prefix="national_policy_and_legal_framework - Water Resources Legislation: ")
    national_policy_and_legal_framework_Waste_Management_Legislation = dspy.OutputField(desc="Extract facts about Waste Management Legislation", prefix="national_policy_and_legal_framework - Waste Management Legislation: ")
    national_policy_and_legal_framework_Air_Quality_and_Noise_Standards = dspy.OutputField(desc="Extract facts about Air Quality and Noise Standards", prefix="national_policy_and_legal_framework - Air Quality and Noise Standards: ")
    international_conventions_and_treaties_Biodiversity_Conventions_e_g_CBD_CITES_Ramsar = dspy.OutputField(desc="Extract facts about Biodiversity Conventions (e.g., CBD, CITES, Ramsar)", prefix="international_conventions_and_treaties - Biodiversity Conventions (e.g., CBD, CITES, Ramsar): ")
    international_conventions_and_treaties_Climate_Change_Conventions_e_g_UNFCCC_Paris_Agreement = dspy.OutputField(desc="Extract facts about Climate Change Conventions (e.g., UNFCCC, Paris Agreement)", prefix="international_conventions_and_treaties - Climate Change Conventions (e.g., UNFCCC, Paris Agreement): ")
    international_conventions_and_treaties_Human_Rights_Conventions = dspy.OutputField(desc="Extract facts about Human Rights Conventions", prefix="international_conventions_and_treaties - Human Rights Conventions: ")
    international_conventions_and_treaties_Labor_Conventions_ILO_Core_Conventions = dspy.OutputField(desc="Extract facts about Labor Conventions (ILO Core Conventions)", prefix="international_conventions_and_treaties - Labor Conventions (ILO Core Conventions): ")
    international_conventions_and_treaties_Transboundary_Water_Agreements = dspy.OutputField(desc="Extract facts about Transboundary Water Agreements", prefix="international_conventions_and_treaties - Transboundary Water Agreements: ")
    international_standards_and_guidelines_IFC_Performance_Standards_PS1_PS8 = dspy.OutputField(desc="Extract facts about IFC Performance Standards (PS1-PS8)", prefix="international_standards_and_guidelines - IFC Performance Standards (PS1-PS8): ")
    international_standards_and_guidelines_World_Bank_Environmental_and_Social_Standards_ESS = dspy.OutputField(desc="Extract facts about World Bank Environmental and Social Standards (ESS)", prefix="international_standards_and_guidelines - World Bank Environmental and Social Standards (ESS): ")
    international_standards_and_guidelines_World_Bank_Group_EHS_Guidelines_General = dspy.OutputField(desc="Extract facts about World Bank Group EHS Guidelines (General)", prefix="international_standards_and_guidelines - World Bank Group EHS Guidelines (General): ")
    international_standards_and_guidelines_World_Bank_Group_EHS_Guidelines_Sector_Specific = dspy.OutputField(desc="Extract facts about World Bank Group EHS Guidelines (Sector-Specific)", prefix="international_standards_and_guidelines - World Bank Group EHS Guidelines (Sector-Specific): ")
    international_standards_and_guidelines_Equator_Principles = dspy.OutputField(desc="Extract facts about Equator Principles", prefix="international_standards_and_guidelines - Equator Principles: ")
    international_standards_and_guidelines_WHO_Guidelines_Air_Water_Noise = dspy.OutputField(desc="Extract facts about WHO Guidelines (Air, Water, Noise)", prefix="international_standards_and_guidelines - WHO Guidelines (Air, Water, Noise): ")
    institutional_framework_Ministry_of_Environment_Environmental_Protection_Agency = dspy.OutputField(desc="Extract facts about Ministry of Environment / Environmental Protection Agency", prefix="institutional_framework - Ministry of Environment / Environmental Protection Agency: ")
    institutional_framework_Sectoral_Ministries_e_g_Energy_Mining_Water = dspy.OutputField(desc="Extract facts about Sectoral Ministries (e.g., Energy, Mining, Water)", prefix="institutional_framework - Sectoral Ministries (e.g., Energy, Mining, Water): ")
    institutional_framework_Local_Government_Authorities = dspy.OutputField(desc="Extract facts about Local Government Authorities", prefix="institutional_framework - Local Government Authorities: ")
    institutional_framework_Permitting_and_Licensing_Authorities = dspy.OutputField(desc="Extract facts about Permitting and Licensing Authorities", prefix="institutional_framework - Permitting and Licensing Authorities: ")
    gap_analysis_Comparison_of_National_vs_International_Standards = dspy.OutputField(desc="Extract facts about Comparison of National vs. International Standards", prefix="gap_analysis - Comparison of National vs. International Standards: ")
    gap_analysis_Measures_to_Address_Gaps_Project_Standards = dspy.OutputField(desc="Extract facts about Measures to Address Gaps (Project Standards)", prefix="gap_analysis - Measures to Address Gaps (Project Standards): ")


class ProcessEmissionsSignature(dspy.Signature):
    """
    Extracted facts for Process Emissions.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Air_Pollutants = dspy.OutputField(desc="Extract facts about Air Pollutants, specifically: Stack Emissions, Fugitive Emissions", prefix="Air Pollutants: ")
    Wastewater_Discharge = dspy.OutputField(desc="Extract facts about Wastewater Discharge, specifically: Effluent Treatment, Receiving Water Quality", prefix="Wastewater Discharge: ")


class ProjectDescriptionSignature(dspy.Signature):
    """
    Extracted facts for Project Description.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    project_location_Administrative_Location_Region_District_Village = dspy.OutputField(desc="Extract facts about Administrative Location (Region, District, Village)", prefix="project_location - Administrative Location (Region, District, Village): ")
    project_location_Geographic_Coordinates = dspy.OutputField(desc="Extract facts about Geographic Coordinates", prefix="project_location - Geographic Coordinates: ")
    project_location_Site_Accessibility_and_Access_Roads = dspy.OutputField(desc="Extract facts about Site Accessibility and Access Roads", prefix="project_location - Site Accessibility and Access Roads: ")
    project_location_Land_Ownership_and_Tenure = dspy.OutputField(desc="Extract facts about Land Ownership and Tenure", prefix="project_location - Land Ownership and Tenure: ")
    project_location_Existing_Land_Use = dspy.OutputField(desc="Extract facts about Existing Land Use", prefix="project_location - Existing Land Use: ")
    project_location_Proximity_to_Protected_Areas_or_Sensitive_Receptors = dspy.OutputField(desc="Extract facts about Proximity to Protected Areas or Sensitive Receptors", prefix="project_location - Proximity to Protected Areas or Sensitive Receptors: ")
    project_design_and_components_Main_Project_Facilities_e_g_Plant_Mine_Pit_Dam = dspy.OutputField(desc="Extract facts about Main Project Facilities (e.g., Plant, Mine Pit, Dam)", prefix="project_design_and_components - Main Project Facilities (e.g., Plant, Mine Pit, Dam): ")
    project_design_and_components_Ancillary_Facilities_e_g_Camps_Workshops_Storage = dspy.OutputField(desc="Extract facts about Ancillary Facilities (e.g., Camps, Workshops, Storage)", prefix="project_design_and_components - Ancillary Facilities (e.g., Camps, Workshops, Storage): ")
    project_design_and_components_Associated_Facilities_e_g_Transmission_Lines_Pipelines = dspy.OutputField(desc="Extract facts about Associated Facilities (e.g., Transmission Lines, Pipelines)", prefix="project_design_and_components - Associated Facilities (e.g., Transmission Lines, Pipelines): ")
    project_design_and_components_Design_Criteria_and_Standards = dspy.OutputField(desc="Extract facts about Design Criteria and Standards", prefix="project_design_and_components - Design Criteria and Standards: ")
    project_design_and_components_Project_Life_Span = dspy.OutputField(desc="Extract facts about Project Life Span", prefix="project_design_and_components - Project Life Span: ")
    construction_phase_Site_Preparation_and_Clearance = dspy.OutputField(desc="Extract facts about Site Preparation and Clearance", prefix="construction_phase - Site Preparation and Clearance: ")
    construction_phase_Construction_Activities_and_Methods = dspy.OutputField(desc="Extract facts about Construction Activities and Methods", prefix="construction_phase - Construction Activities and Methods: ")
    construction_phase_Construction_Schedule_and_Duration = dspy.OutputField(desc="Extract facts about Construction Schedule and Duration", prefix="construction_phase - Construction Schedule and Duration: ")
    construction_phase_Construction_Workforce_Number_Origin = dspy.OutputField(desc="Extract facts about Construction Workforce (Number, Origin)", prefix="construction_phase - Construction Workforce (Number, Origin): ")
    construction_phase_Construction_Equipment_and_Machinery = dspy.OutputField(desc="Extract facts about Construction Equipment and Machinery", prefix="construction_phase - Construction Equipment and Machinery: ")
    operation_phase_Operational_Activities_and_Processes = dspy.OutputField(desc="Extract facts about Operational Activities and Processes", prefix="operation_phase - Operational Activities and Processes: ")
    operation_phase_Production_Capacity_Output = dspy.OutputField(desc="Extract facts about Production Capacity / Output", prefix="operation_phase - Production Capacity / Output: ")
    operation_phase_Operation_Schedule_Shifts_Hours = dspy.OutputField(desc="Extract facts about Operation Schedule (Shifts, Hours)", prefix="operation_phase - Operation Schedule (Shifts, Hours): ")
    operation_phase_Operational_Workforce = dspy.OutputField(desc="Extract facts about Operational Workforce", prefix="operation_phase - Operational Workforce: ")
    operation_phase_Maintenance_Activities = dspy.OutputField(desc="Extract facts about Maintenance Activities", prefix="operation_phase - Maintenance Activities: ")
    decommissioning_and_closure_phase_Decommissioning_Plan_Overview = dspy.OutputField(desc="Extract facts about Decommissioning Plan Overview", prefix="decommissioning_and_closure_phase - Decommissioning Plan Overview: ")
    decommissioning_and_closure_phase_Demolition_and_Site_Rehabilitation = dspy.OutputField(desc="Extract facts about Demolition and Site Rehabilitation", prefix="decommissioning_and_closure_phase - Demolition and Site Rehabilitation: ")
    decommissioning_and_closure_phase_Post_Closure_Monitoring = dspy.OutputField(desc="Extract facts about Post-Closure Monitoring", prefix="decommissioning_and_closure_phase - Post-Closure Monitoring: ")
    resource_use_and_efficiency_Water_Requirements_and_Sources = dspy.OutputField(desc="Extract facts about Water Requirements and Sources", prefix="resource_use_and_efficiency - Water Requirements and Sources: ")
    resource_use_and_efficiency_Energy_Requirements_and_Sources = dspy.OutputField(desc="Extract facts about Energy Requirements and Sources", prefix="resource_use_and_efficiency - Energy Requirements and Sources: ")
    resource_use_and_efficiency_Raw_Material_Requirements_e_g_Aggregates_Chemicals = dspy.OutputField(desc="Extract facts about Raw Material Requirements (e.g., Aggregates, Chemicals)", prefix="resource_use_and_efficiency - Raw Material Requirements (e.g., Aggregates, Chemicals): ")
    waste_and_emissions_management_Solid_Waste_Generation_and_Disposal = dspy.OutputField(desc="Extract facts about Solid Waste Generation and Disposal", prefix="waste_and_emissions_management - Solid Waste Generation and Disposal: ")
    waste_and_emissions_management_Liquid_Effluent_Generation_and_Treatment = dspy.OutputField(desc="Extract facts about Liquid Effluent Generation and Treatment", prefix="waste_and_emissions_management - Liquid Effluent Generation and Treatment: ")
    waste_and_emissions_management_Air_Emissions_Sources_and_Controls = dspy.OutputField(desc="Extract facts about Air Emissions Sources and Controls", prefix="waste_and_emissions_management - Air Emissions Sources and Controls: ")
    waste_and_emissions_management_Noise_and_Vibration_Sources = dspy.OutputField(desc="Extract facts about Noise and Vibration Sources", prefix="waste_and_emissions_management - Noise and Vibration Sources: ")
    waste_and_emissions_management_Hazardous_Materials_Management = dspy.OutputField(desc="Extract facts about Hazardous Materials Management", prefix="waste_and_emissions_management - Hazardous Materials Management: ")


class PublicConsultationAndDisclosureSignature(dspy.Signature):
    """
    Extracted facts for Public Consultation And Disclosure.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    stakeholder_analysis_and_engagement_plan_Stakeholder_Identification_and_Mapping = dspy.OutputField(desc="Extract facts about Stakeholder Identification and Mapping", prefix="stakeholder_analysis_and_engagement_plan - Stakeholder Identification and Mapping: ")
    stakeholder_analysis_and_engagement_plan_Vulnerable_Groups_Identification = dspy.OutputField(desc="Extract facts about Vulnerable Groups Identification", prefix="stakeholder_analysis_and_engagement_plan - Vulnerable Groups Identification: ")
    stakeholder_analysis_and_engagement_plan_Stakeholder_Engagement_Plan_SEP_Overview = dspy.OutputField(desc="Extract facts about Stakeholder Engagement Plan (SEP) Overview", prefix="stakeholder_analysis_and_engagement_plan - Stakeholder Engagement Plan (SEP) Overview: ")
    stakeholder_analysis_and_engagement_plan_Engagement_Methods_and_Tools = dspy.OutputField(desc="Extract facts about Engagement Methods and Tools", prefix="stakeholder_analysis_and_engagement_plan - Engagement Methods and Tools: ")
    consultation_activities_undertaken_Scoping_Phase_Consultations = dspy.OutputField(desc="Extract facts about Scoping Phase Consultations", prefix="consultation_activities_undertaken - Scoping Phase Consultations: ")
    consultation_activities_undertaken_Draft_ESIA_Consultations = dspy.OutputField(desc="Extract facts about Draft ESIA Consultations", prefix="consultation_activities_undertaken - Draft ESIA Consultations: ")
    consultation_activities_undertaken_Public_Meetings_and_Hearings = dspy.OutputField(desc="Extract facts about Public Meetings and Hearings", prefix="consultation_activities_undertaken - Public Meetings and Hearings: ")
    consultation_activities_undertaken_Focus_Group_Discussions_FGDs = dspy.OutputField(desc="Extract facts about Focus Group Discussions (FGDs)", prefix="consultation_activities_undertaken - Focus Group Discussions (FGDs): ")
    consultation_activities_undertaken_Key_Informant_Interviews_KIIs = dspy.OutputField(desc="Extract facts about Key Informant Interviews (KIIs)", prefix="consultation_activities_undertaken - Key Informant Interviews (KIIs): ")
    key_issues_and_concerns_raised_Summary_of_Issues_Raised_by_Local_Communities = dspy.OutputField(desc="Extract facts about Summary of Issues Raised by Local Communities", prefix="key_issues_and_concerns_raised - Summary of Issues Raised by Local Communities: ")
    key_issues_and_concerns_raised_Summary_of_Issues_Raised_by_Government_Agencies = dspy.OutputField(desc="Extract facts about Summary of Issues Raised by Government Agencies", prefix="key_issues_and_concerns_raised - Summary of Issues Raised by Government Agencies: ")
    key_issues_and_concerns_raised_Summary_of_Issues_Raised_by_NGOs_Civil_Society = dspy.OutputField(desc="Extract facts about Summary of Issues Raised by NGOs/Civil Society", prefix="key_issues_and_concerns_raised - Summary of Issues Raised by NGOs/Civil Society: ")
    key_issues_and_concerns_raised_Project_Proponent_s_Response_to_Issues = dspy.OutputField(desc="Extract facts about Project Proponent's Response to Issues", prefix="key_issues_and_concerns_raised - Project Proponent's Response to Issues: ")
    information_disclosure_Disclosure_of_Scoping_Report = dspy.OutputField(desc="Extract facts about Disclosure of Scoping Report", prefix="information_disclosure - Disclosure of Scoping Report: ")
    information_disclosure_Disclosure_of_Draft_ESIA = dspy.OutputField(desc="Extract facts about Disclosure of Draft ESIA", prefix="information_disclosure - Disclosure of Draft ESIA: ")
    information_disclosure_Disclosure_Locations_and_Languages = dspy.OutputField(desc="Extract facts about Disclosure Locations and Languages", prefix="information_disclosure - Disclosure Locations and Languages: ")
    information_disclosure_Non_Technical_Summary_NTS_Availability = dspy.OutputField(desc="Extract facts about Non-Technical Summary (NTS) Availability", prefix="information_disclosure - Non-Technical Summary (NTS) Availability: ")
    grievance_redress_mechanism_grm_GRM_Structure_and_Procedures = dspy.OutputField(desc="Extract facts about GRM Structure and Procedures", prefix="grievance_redress_mechanism_grm - GRM Structure and Procedures: ")
    grievance_redress_mechanism_grm_Grievance_Logging_and_Tracking = dspy.OutputField(desc="Extract facts about Grievance Logging and Tracking", prefix="grievance_redress_mechanism_grm - Grievance Logging and Tracking: ")
    grievance_redress_mechanism_grm_Resolution_Timeframes = dspy.OutputField(desc="Extract facts about Resolution Timeframes", prefix="grievance_redress_mechanism_grm - Resolution Timeframes: ")
    grievance_redress_mechanism_grm_Accessibility_of_GRM_to_Communities = dspy.OutputField(desc="Extract facts about Accessibility of GRM to Communities", prefix="grievance_redress_mechanism_grm - Accessibility of GRM to Communities: ")
    ongoing_engagement_Future_Consultation_Plans_Construction_Operation = dspy.OutputField(desc="Extract facts about Future Consultation Plans (Construction/Operation)", prefix="ongoing_engagement - Future Consultation Plans (Construction/Operation): ")
    ongoing_engagement_Community_Liaison_Officer_CLO_Role = dspy.OutputField(desc="Extract facts about Community Liaison Officer (CLO) Role", prefix="ongoing_engagement - Community Liaison Officer (CLO) Role: ")


class ReferencesSignature(dspy.Signature):
    """
    Extracted facts for References.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    legislative_and_regulatory_references_National_Laws_and_Regulations_Vancouver_format_Number_Country_Title_of_Act_Year = dspy.OutputField(desc="Extract facts about National Laws and Regulations (Vancouver format: [Number]. Country. Title of Act. Year.)", prefix="legislative_and_regulatory_references - National Laws and Regulations (Vancouver format: [Number]. Country. Title of Act. Year.): ")
    legislative_and_regulatory_references_Regional_Local_Regulations = dspy.OutputField(desc="Extract facts about Regional/Local Regulations", prefix="legislative_and_regulatory_references - Regional/Local Regulations: ")
    legislative_and_regulatory_references_Environmental_Permits_and_Licenses = dspy.OutputField(desc="Extract facts about Environmental Permits and Licenses", prefix="legislative_and_regulatory_references - Environmental Permits and Licenses: ")
    international_standards_and_guidelines_IFC_Performance_Standards_Vancouver_format_Number_International_Finance_Corporation_Performance_Standard_X_Title_Year = dspy.OutputField(desc="Extract facts about IFC Performance Standards (Vancouver format: [Number]. International Finance Corporation. Performance Standard [X]: Title. Year.)", prefix="international_standards_and_guidelines - IFC Performance Standards (Vancouver format: [Number]. International Finance Corporation. Performance Standard [X]: Title. Year.): ")
    international_standards_and_guidelines_World_Bank_Environmental_and_Social_Standards = dspy.OutputField(desc="Extract facts about World Bank Environmental and Social Standards", prefix="international_standards_and_guidelines - World Bank Environmental and Social Standards: ")
    international_standards_and_guidelines_World_Bank_Group_EHS_Guidelines = dspy.OutputField(desc="Extract facts about World Bank Group EHS Guidelines", prefix="international_standards_and_guidelines - World Bank Group EHS Guidelines: ")
    international_standards_and_guidelines_WHO_Guidelines = dspy.OutputField(desc="Extract facts about WHO Guidelines", prefix="international_standards_and_guidelines - WHO Guidelines: ")
    international_standards_and_guidelines_ISO_Standards = dspy.OutputField(desc="Extract facts about ISO Standards", prefix="international_standards_and_guidelines - ISO Standards: ")
    technical_reports_and_studies_Baseline_Studies_Vancouver_format_Number_Author_s_Title_Organization_Year = dspy.OutputField(desc="Extract facts about Baseline Studies (Vancouver format: [Number]. Author(s). Title. Organization; Year.)", prefix="technical_reports_and_studies - Baseline Studies (Vancouver format: [Number]. Author(s). Title. Organization; Year.): ")
    technical_reports_and_studies_Specialist_Studies_e_g_Biodiversity_Hydrology = dspy.OutputField(desc="Extract facts about Specialist Studies (e.g., Biodiversity, Hydrology)", prefix="technical_reports_and_studies - Specialist Studies (e.g., Biodiversity, Hydrology): ")
    technical_reports_and_studies_Previous_ESIAs_for_Similar_Projects = dspy.OutputField(desc="Extract facts about Previous ESIAs for Similar Projects", prefix="technical_reports_and_studies - Previous ESIAs for Similar Projects: ")
    published_literature_Journal_Articles_Vancouver_format_Number_Author_s_Title_Journal_Name_Year_Volume_Issue_Pages = dspy.OutputField(desc="Extract facts about Journal Articles (Vancouver format: [Number]. Author(s). Title. Journal Name. Year;Volume(Issue):Pages.)", prefix="published_literature - Journal Articles (Vancouver format: [Number]. Author(s). Title. Journal Name. Year;Volume(Issue):Pages.): ")
    published_literature_Books_and_Book_Chapters = dspy.OutputField(desc="Extract facts about Books and Book Chapters", prefix="published_literature - Books and Book Chapters: ")
    published_literature_Conference_Papers = dspy.OutputField(desc="Extract facts about Conference Papers", prefix="published_literature - Conference Papers: ")
    maps_and_spatial_data_Topographic_Maps = dspy.OutputField(desc="Extract facts about Topographic Maps", prefix="maps_and_spatial_data - Topographic Maps: ")
    maps_and_spatial_data_Land_Use_Maps = dspy.OutputField(desc="Extract facts about Land Use Maps", prefix="maps_and_spatial_data - Land Use Maps: ")
    maps_and_spatial_data_Protected_Areas_Maps = dspy.OutputField(desc="Extract facts about Protected Areas Maps", prefix="maps_and_spatial_data - Protected Areas Maps: ")
    maps_and_spatial_data_GIS_Data_Sources = dspy.OutputField(desc="Extract facts about GIS Data Sources", prefix="maps_and_spatial_data - GIS Data Sources: ")
    consultation_and_stakeholder_documents_Meeting_Minutes = dspy.OutputField(desc="Extract facts about Meeting Minutes", prefix="consultation_and_stakeholder_documents - Meeting Minutes: ")
    consultation_and_stakeholder_documents_Stakeholder_Submissions = dspy.OutputField(desc="Extract facts about Stakeholder Submissions", prefix="consultation_and_stakeholder_documents - Stakeholder Submissions: ")
    consultation_and_stakeholder_documents_Public_Hearing_Records = dspy.OutputField(desc="Extract facts about Public Hearing Records", prefix="consultation_and_stakeholder_documents - Public Hearing Records: ")
    online_resources_Government_Websites_Vancouver_format_Number_Organization_Title_Internet_Year_cited_YYYY_Mon_DD_Available_from_URL = dspy.OutputField(desc="Extract facts about Government Websites (Vancouver format: [Number]. Organization. Title [Internet]. Year [cited YYYY Mon DD]. Available from: URL)", prefix="online_resources - Government Websites (Vancouver format: [Number]. Organization. Title [Internet]. Year [cited YYYY Mon DD]. Available from: URL): ")
    online_resources_International_Organization_Websites = dspy.OutputField(desc="Extract facts about International Organization Websites", prefix="online_resources - International Organization Websites: ")
    online_resources_Database_References = dspy.OutputField(desc="Extract facts about Database References", prefix="online_resources - Database References: ")


class SolarSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Solar Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Land_and_Water_Use = dspy.OutputField(desc="Extract facts about Land and Water Use, specifically: Land Take, Water Surface Coverage (Floating Solar), Impact on Aquatic Habitat (Floating Solar)", prefix="Land and Water Use: ")
    Visual_and_Glare = dspy.OutputField(desc="Extract facts about Visual and Glare, specifically: Glint and Glare Analysis, Visual Impact", prefix="Visual and Glare: ")
    Waste_Management = dspy.OutputField(desc="Extract facts about Waste Management, specifically: PV Panel Disposal, Battery Storage (if applicable)", prefix="Waste Management: ")


class TrafficAndTransportationSignature(dspy.Signature):
    """
    Extracted facts for Traffic And Transportation.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Traffic_Management_Plan = dspy.OutputField(desc="Extract facts about Traffic Management Plan, specifically: Construction Phase, Operational Phase, Road Safety", prefix="Traffic Management Plan: ")
    Navigation_Impacts = dspy.OutputField(desc="Extract facts about Navigation Impacts, specifically: Waterways, Airspace", prefix="Navigation Impacts: ")


class UtilitiesRelocationSignature(dspy.Signature):
    """
    Extracted facts for Utilities Relocation.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Existing_Infrastructure = dspy.OutputField(desc="Extract facts about Existing Infrastructure, specifically: Water Lines, Power Cables, Telecommunications", prefix="Existing Infrastructure: ")


class VisualAndLandscapeImpactsSignature(dspy.Signature):
    """
    Extracted facts for Visual And Landscape Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Turbine_Visibility = dspy.OutputField(desc="Extract facts about Turbine Visibility, specifically: Visual Impact Assessment, Mitigation Measures", prefix="Turbine Visibility: ")
    Shadow_Flicker = dspy.OutputField(desc="Extract facts about Shadow Flicker, specifically: Assessment, Mitigation", prefix="Shadow Flicker: ")


class WellDrillingAndCompletionSignature(dspy.Signature):
    """
    Extracted facts for Well Drilling And Completion.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    Drilling_Waste_Management = dspy.OutputField(desc="Extract facts about Drilling Waste Management, specifically: Cuttings Disposal, Drilling Fluids", prefix="Drilling Waste Management: ")
    Fracking_Impacts = dspy.OutputField(desc="Extract facts about Fracking Impacts, specifically: Groundwater Contamination, Seismicity", prefix="Fracking Impacts: ")


class AnnexesSignature(dspy.Signature):
    """
    Extracted facts for Annexes (Appendices) section of ESIA documents.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    technical_annexes_Detailed_Technical_Studies = dspy.OutputField(desc="Extract facts about Detailed Technical Studies (geotechnical, hydrological, structural)", prefix="technical_annexes - Detailed Technical Studies: ")
    technical_annexes_Engineering_Drawings_and_Specifications = dspy.OutputField(desc="Extract facts about Engineering Drawings and Specifications", prefix="technical_annexes - Engineering Drawings and Specifications: ")
    technical_annexes_Design_Calculations = dspy.OutputField(desc="Extract facts about Design Calculations", prefix="technical_annexes - Design Calculations: ")
    environmental_annexes_Biodiversity_Survey_Reports = dspy.OutputField(desc="Extract facts about Biodiversity Survey Reports (flora/fauna inventories)", prefix="environmental_annexes - Biodiversity Survey Reports: ")
    environmental_annexes_Water_Quality_Data = dspy.OutputField(desc="Extract facts about Water Quality Data and Analysis", prefix="environmental_annexes - Water Quality Data: ")
    environmental_annexes_Air_Quality_Monitoring_Data = dspy.OutputField(desc="Extract facts about Air Quality Monitoring Data", prefix="environmental_annexes - Air Quality Monitoring Data: ")
    environmental_annexes_Noise_Monitoring_Data = dspy.OutputField(desc="Extract facts about Noise Monitoring Data", prefix="environmental_annexes - Noise Monitoring Data: ")
    social_annexes_Stakeholder_Consultation_Records = dspy.OutputField(desc="Extract facts about Stakeholder Consultation Records (meeting minutes, attendance lists)", prefix="social_annexes - Stakeholder Consultation Records: ")
    social_annexes_Socioeconomic_Survey_Data = dspy.OutputField(desc="Extract facts about Socioeconomic Survey Data and Questionnaires", prefix="social_annexes - Socioeconomic Survey Data: ")
    social_annexes_Resettlement_Documentation = dspy.OutputField(desc="Extract facts about Resettlement Documentation (asset inventories, compensation records)", prefix="social_annexes - Resettlement Documentation: ")
    legal_annexes_Permits_and_Licenses = dspy.OutputField(desc="Extract facts about Permits and Licenses obtained or required", prefix="legal_annexes - Permits and Licenses: ")
    legal_annexes_Land_Acquisition_Documents = dspy.OutputField(desc="Extract facts about Land Acquisition Documents", prefix="legal_annexes - Land Acquisition Documents: ")
    management_plan_annexes_Detailed_ESMP_Matrices = dspy.OutputField(desc="Extract facts about Detailed ESMP Matrices and Action Plans", prefix="management_plan_annexes - Detailed ESMP Matrices: ")
    management_plan_annexes_Monitoring_Protocols = dspy.OutputField(desc="Extract facts about Monitoring Protocols and Procedures", prefix="management_plan_annexes - Monitoring Protocols: ")
    management_plan_annexes_Emergency_Response_Plans = dspy.OutputField(desc="Extract facts about Emergency Response Plans", prefix="management_plan_annexes - Emergency Response Plans: ")


class PumpedStorageHydropowerSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Pumped Storage Hydropower Specific Impacts.
    Covers technical configuration, reservoirs, hydraulic systems, and operational impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    # Project Configuration
    project_configuration_System_Type = dspy.OutputField(desc="Extract facts about Pumped Storage Type (Closed-loop/Open-loop/Mixed)", prefix="project_configuration - System Type: ")
    project_configuration_Generation_Capacity = dspy.OutputField(desc="Extract facts about Installed Generation Capacity (MW)", prefix="project_configuration - Generation Capacity: ")
    project_configuration_Pumping_Capacity = dspy.OutputField(desc="Extract facts about Installed Pumping Capacity (MW)", prefix="project_configuration - Pumping Capacity: ")
    project_configuration_Unit_Configuration = dspy.OutputField(desc="Extract facts about Number and Type of Reversible Units/Turbines/Pumps", prefix="project_configuration - Unit Configuration: ")
    project_configuration_Efficiency = dspy.OutputField(desc="Extract facts about Round-Trip Efficiency (%)", prefix="project_configuration - Efficiency: ")
    project_configuration_Storage_Capacity = dspy.OutputField(desc="Extract facts about Storage Capacity (GWh) and Discharge Duration", prefix="project_configuration - Storage Capacity: ")

    # Upper Reservoir
    upper_reservoir_Dimensions = dspy.OutputField(desc="Extract facts about Upper Reservoir Area (ha), Volume (million m3), Operating Levels (masl)", prefix="upper_reservoir - Dimensions: ")
    upper_reservoir_Dam_Structure = dspy.OutputField(desc="Extract facts about Embankment/Dam Height, Length, Type, Spillway Capacity", prefix="upper_reservoir - Dam Structure: ")
    upper_reservoir_Seepage_Control = dspy.OutputField(desc="Extract facts about Seepage Control Measures", prefix="upper_reservoir - Seepage Control: ")

    # Lower Reservoir
    lower_reservoir_Dimensions = dspy.OutputField(desc="Extract facts about Lower Reservoir Area (ha), Volume, Operating Levels", prefix="lower_reservoir - Dimensions: ")
    lower_reservoir_Connection = dspy.OutputField(desc="Extract facts about Connection to River/Sea, Dam/Weir configuration", prefix="lower_reservoir - Connection: ")

    # Hydraulic System
    hydraulic_system_Head_and_Flow = dspy.OutputField(desc="Extract facts about Gross/Net Head (m), Design Flow for Generation and Pumping (m3/s)", prefix="hydraulic_system - Head and Flow: ")
    hydraulic_system_Penstocks = dspy.OutputField(desc="Extract facts about Penstock Number, Diameter, Length, Material", prefix="hydraulic_system - Penstocks: ")
    hydraulic_system_Tunnels = dspy.OutputField(desc="Extract facts about Pressure Tunnel Length, Surge Tank, Tailrace Configuration", prefix="hydraulic_system - Tunnels: ")

    # Powerhouse
    powerhouse_Type_and_Dimensions = dspy.OutputField(desc="Extract facts about Powerhouse Type (Surface/Underground), Dimensions, Cavern Volume", prefix="powerhouse - Type and Dimensions: ")
    powerhouse_Access_and_Support = dspy.OutputField(desc="Extract facts about Access Tunnel, Transformer Cavern, Ventilation, Rock Support", prefix="powerhouse - Access and Support: ")

    # Operational Regime
    operational_regime_Cycling = dspy.OutputField(desc="Extract facts about Daily Pumping/Generation Cycles, Operating Hours", prefix="operational_regime - Cycling: ")
    operational_regime_Grid_Services = dspy.OutputField(desc="Extract facts about Peak Shaving, Frequency Regulation, Black Start Capability", prefix="operational_regime - Grid Services: ")

    # Water Level Fluctuations
    water_fluctuations_Daily = dspy.OutputField(desc="Extract facts about Daily Fluctuation Range in Upper/Lower Reservoirs (m)", prefix="water_fluctuations - Daily: ")
    water_fluctuations_Drawdown_Zones = dspy.OutputField(desc="Extract facts about Drawdown Zone Areas (ha), Fluctuation Rate (m/hr)", prefix="water_fluctuations - Drawdown Zones: ")

    # Hydrological Impacts
    hydrology_Initial_Filling = dspy.OutputField(desc="Extract facts about Water Source for Filling, Volume, Duration", prefix="hydrology - Initial Filling: ")
    hydrology_Water_Losses = dspy.OutputField(desc="Extract facts about Annual Evaporation/Seepage Losses, Make-up Water Requirements", prefix="hydrology - Water Losses: ")
    hydrology_Downstream_Impacts = dspy.OutputField(desc="Extract facts about Impact on Source Water Body, Downstream Flow Impacts", prefix="hydrology - Downstream Impacts: ")

    # Water Quality
    water_quality_Upper_Reservoir = dspy.OutputField(desc="Extract facts about Thermal Stratification, Dissolved Oxygen, Algal Bloom Risk in Upper Reservoir", prefix="water_quality - Upper Reservoir: ")
    water_quality_Lower_Reservoir = dspy.OutputField(desc="Extract facts about Turbidity, Temperature Changes, Sediment Resuspension in Lower Reservoir", prefix="water_quality - Lower Reservoir: ")

    # Aquatic Ecology
    aquatic_ecology_Fish_Impacts = dspy.OutputField(desc="Extract facts about Fish Entrainment Risk, Turbine Mortality, Migration Barriers", prefix="aquatic_ecology - Fish Impacts: ")
    aquatic_ecology_Habitat = dspy.OutputField(desc="Extract facts about Spawning Habitat, Littoral Zone, Benthic Community Impacts", prefix="aquatic_ecology - Habitat: ")

    # Terrestrial Ecology
    terrestrial_ecology_Inundation = dspy.OutputField(desc="Extract facts about Upper/Lower Reservoir Inundation Areas, Habitat Types Affected", prefix="terrestrial_ecology - Inundation: ")
    terrestrial_ecology_Wildlife = dspy.OutputField(desc="Extract facts about Protected Species, Wildlife Corridors, Wetland Impacts", prefix="terrestrial_ecology - Wildlife: ")

    # GHG Emissions
    ghg_emissions_Reservoir = dspy.OutputField(desc="Extract facts about Reservoir GHG Emissions, Methane, Carbon Sequestration, Net Balance", prefix="ghg_emissions - Reservoir: ")

    # Geotechnical and Seismic
    geotechnical_Seismic = dspy.OutputField(desc="Extract facts about Seismic Design Criteria, Reservoir Induced Seismicity Risk", prefix="geotechnical - Seismic: ")
    geotechnical_Slope_Stability = dspy.OutputField(desc="Extract facts about Slope Stability Upper/Lower, Landslide Risk, Rock Mass Quality", prefix="geotechnical - Slope Stability: ")

    # Dam Safety
    dam_safety_Classification = dspy.OutputField(desc="Extract facts about Dam Safety Classification Upper/Lower", prefix="dam_safety - Classification: ")
    dam_safety_Emergency = dspy.OutputField(desc="Extract facts about Dam Break Analysis, Inundation Mapping, Population at Risk, Emergency Action Plan", prefix="dam_safety - Emergency: ")

    # Visual and Landscape
    visual_landscape_Impacts = dspy.OutputField(desc="Extract facts about Visibility from Viewpoints, Landscape Character Impact, Mitigation Measures", prefix="visual_landscape - Impacts: ")

    # Noise and Vibration
    noise_vibration_Construction = dspy.OutputField(desc="Extract facts about Construction Blasting/Tunneling Noise, Vibration from Underground Works", prefix="noise_vibration - Construction: ")
    noise_vibration_Operation = dspy.OutputField(desc="Extract facts about Powerhouse/Transformer/Ventilation Operational Noise, Nearest Receptors", prefix="noise_vibration - Operation: ")

    # Social and Resettlement
    social_Resettlement = dspy.OutputField(desc="Extract facts about Households Requiring Resettlement, Land Acquisition by Type", prefix="social - Resettlement: ")
    social_Cultural_Heritage = dspy.OutputField(desc="Extract facts about Cultural Heritage Sites, Sacred Sites, Graves Requiring Relocation", prefix="social - Cultural Heritage: ")
    social_Livelihoods = dspy.OutputField(desc="Extract facts about Economic Displacement, Livelihoods Affected", prefix="social - Livelihoods: ")

    # Recreation
    recreation_Impacts = dspy.OutputField(desc="Extract facts about Existing Recreation Uses, Water Level Fluctuation Impacts, Public Access", prefix="recreation - Impacts: ")

    # Construction
    construction_Workforce = dspy.OutputField(desc="Extract facts about Construction Duration, Peak Workforce, Camp Locations", prefix="construction - Workforce: ")
    construction_Materials = dspy.OutputField(desc="Extract facts about Excavation Volume, Concrete Volume, Aggregate Requirements, Quarry Locations", prefix="construction - Materials: ")
    construction_Access = dspy.OutputField(desc="Extract facts about Access Road Construction, Haul Roads, Construction Water/Power Demand", prefix="construction - Access: ")

    # IFC Compliance
    ifc_compliance_Biodiversity_Offsets = dspy.OutputField(desc="Extract facts about Biodiversity Action Plan, Critical Habitat Assessment, Offset Requirements per IFC PS6", prefix="ifc_compliance - Biodiversity Offsets: ")
    ifc_compliance_Resettlement_Standards = dspy.OutputField(desc="Extract facts about Resettlement Action Plan compliance with IFC PS5, Livelihood Restoration", prefix="ifc_compliance - Resettlement Standards: ")
    ifc_compliance_Dam_Safety_Standards = dspy.OutputField(desc="Extract facts about Compliance with IFC/World Bank Dam Safety Requirements", prefix="ifc_compliance - Dam Safety Standards: ")


class GridIntegrationAndTransmissionSignature(dspy.Signature):
    """
    Extracted facts for Grid Integration and Transmission infrastructure.
    Covers grid connection, energy storage benefits, and transmission line impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    # Grid Connection
    grid_connection_Voltage_and_Distance = dspy.OutputField(desc="Extract facts about Connection Voltage (kV), Transmission Line Length (km)", prefix="grid_connection - Voltage and Distance: ")
    grid_connection_Substation = dspy.OutputField(desc="Extract facts about Substation Location, Switchyard Configuration", prefix="grid_connection - Substation: ")
    grid_connection_Capacity = dspy.OutputField(desc="Extract facts about Power Evacuation Capacity (MW), Grid Synchronization Requirements", prefix="grid_connection - Capacity: ")

    # Energy Storage Benefits
    storage_benefits_Peak_Shaving = dspy.OutputField(desc="Extract facts about Peak Load Shaving Capacity, Load Following Capability", prefix="storage_benefits - Peak Shaving: ")
    storage_benefits_Grid_Services = dspy.OutputField(desc="Extract facts about Frequency Regulation, Voltage Support, Spinning Reserve", prefix="storage_benefits - Grid Services: ")
    storage_benefits_Renewables_Integration = dspy.OutputField(desc="Extract facts about Renewable Energy Integration Support, Grid Stability Enhancement", prefix="storage_benefits - Renewables Integration: ")

    # Transmission Line Impacts
    transmission_ROW = dspy.OutputField(desc="Extract facts about Right-of-Way Width (m), ROW Area (ha)", prefix="transmission - ROW: ")
    transmission_Towers = dspy.OutputField(desc="Extract facts about Tower Type, Height, Number of Towers", prefix="transmission - Towers: ")
    transmission_Land_Impacts = dspy.OutputField(desc="Extract facts about Forest Clearing (ha), Agricultural Land Affected (ha)", prefix="transmission - Land Impacts: ")
    transmission_EMF = dspy.OutputField(desc="Extract facts about Electromagnetic Field (EMF) Levels and compliance", prefix="transmission - EMF: ")
    transmission_Wildlife = dspy.OutputField(desc="Extract facts about Bird Collision Risk, Wildlife Corridor Impacts", prefix="transmission - Wildlife: ")
    transmission_Visual = dspy.OutputField(desc="Extract facts about Visual Impact Assessment, Mitigation Measures", prefix="transmission - Visual: ")

    # IFC Compliance
    ifc_compliance_Land_Acquisition = dspy.OutputField(desc="Extract facts about Transmission ROW Land Acquisition per IFC PS5", prefix="ifc_compliance - Land Acquisition: ")
    ifc_compliance_Community_Safety = dspy.OutputField(desc="Extract facts about Community Health/Safety measures per IFC PS4 (EMF exposure, access restrictions)", prefix="ifc_compliance - Community Safety: ")


class CumulativeAndRegionalImpactsSignature(dspy.Signature):
    """
    Extracted facts for Cumulative and Regional Impacts assessment.
    Covers basin-level impacts, climate change considerations, and decommissioning per IFC PS1.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    # Basin Level Impacts
    basin_Other_Projects = dspy.OutputField(desc="Extract facts about Other Hydropower/Infrastructure Projects in Basin", prefix="basin - Other Projects: ")
    basin_Water_Abstraction = dspy.OutputField(desc="Extract facts about Cumulative Water Abstraction impacts", prefix="basin - Water Abstraction: ")
    basin_Habitat_Loss = dspy.OutputField(desc="Extract facts about Cumulative Habitat Loss in region", prefix="basin - Habitat Loss: ")
    basin_Flow_Regime = dspy.OutputField(desc="Extract facts about Downstream Flow Regime Changes, Inter-Basin Transfer Impacts", prefix="basin - Flow Regime: ")

    # Climate Change Considerations
    climate_Vulnerability = dspy.OutputField(desc="Extract facts about Climate Change Vulnerability Assessment", prefix="climate - Vulnerability: ")
    climate_Projections = dspy.OutputField(desc="Extract facts about Projected Precipitation and Temperature Changes", prefix="climate - Projections: ")
    climate_Adaptation = dspy.OutputField(desc="Extract facts about Adaptation Measures, Long-term Water Availability", prefix="climate - Adaptation: ")

    # Decommissioning
    decommissioning_Design_Life = dspy.OutputField(desc="Extract facts about Design Life (years)", prefix="decommissioning - Design Life: ")
    decommissioning_Plan = dspy.OutputField(desc="Extract facts about Decommissioning Plan, Reservoir Drainage Strategy", prefix="decommissioning - Plan: ")
    decommissioning_Restoration = dspy.OutputField(desc="Extract facts about Equipment Removal Plan, Site Restoration Plan", prefix="decommissioning - Restoration: ")

    # IFC Cumulative Impact Requirements
    ifc_cia_Scope = dspy.OutputField(desc="Extract facts about CIA Geographic/Temporal Scope, Valued Environmental/Social Components (VECs)", prefix="ifc_cia - Scope: ")
    ifc_cia_Analysis = dspy.OutputField(desc="Extract facts about Impact Pathway Analysis, Project's Incremental Contribution to Cumulative Impacts", prefix="ifc_cia - Analysis: ")
    ifc_cia_Management = dspy.OutputField(desc="Extract facts about Coordinated Mitigation Measures, Institutional Arrangements for CIA Management", prefix="ifc_cia - Management: ")
    ifc_cia_Stakeholder = dspy.OutputField(desc="Extract facts about Engagement with Authorities/Other Developers for Cumulative Impact Coordination", prefix="ifc_cia - Stakeholder: ")


class TransmissionLineSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Transmission Line Specific Impacts.
    Covers transmission infrastructure, land requirements, and associated impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    # Transmission Infrastructure
    transmission_infrastructure_Voltage_and_Length = dspy.OutputField(desc="Extract facts about Transmission Line Voltage (kV), Line Length (km)", prefix="transmission_infrastructure - Voltage and Length: ")
    transmission_infrastructure_Towers = dspy.OutputField(desc="Extract facts about Number of Circuits, Tower Type (Lattice/Monopole/H-frame), Tower Height (m)", prefix="transmission_infrastructure - Towers: ")
    transmission_infrastructure_Substations = dspy.OutputField(desc="Extract facts about Substation Locations, Switchyard Area, Equipment", prefix="transmission_infrastructure - Substations: ")

    # Land Requirements
    land_requirements_ROW = dspy.OutputField(desc="Extract facts about Total Right-of-Way Area (ha), ROW Width (m)", prefix="land_requirements - ROW: ")
    land_requirements_Land_Take = dspy.OutputField(desc="Extract facts about Permanent Land Take, Temporary Construction Area", prefix="land_requirements - Land Take: ")
    land_requirements_Land_Uses = dspy.OutputField(desc="Extract facts about Land Use Types Affected, Agricultural Land (ha), Forest Land (ha)", prefix="land_requirements - Land Uses: ")

    # Ecological Impacts
    ecological_impacts_Habitat = dspy.OutputField(desc="Extract facts about Forest Clearing (ha), Habitat Fragmentation, Wildlife Corridors", prefix="ecological_impacts - Habitat: ")
    ecological_impacts_Birds = dspy.OutputField(desc="Extract facts about Bird Collision Risk, Electrocution Risk, Mitigation Measures", prefix="ecological_impacts - Birds: ")
    ecological_impacts_Vegetation = dspy.OutputField(desc="Extract facts about Vegetation Management in ROW, Restoration Plans", prefix="ecological_impacts - Vegetation: ")

    # Visual and Landscape
    visual_landscape_Assessment = dspy.OutputField(desc="Extract facts about Visual Impact Assessment, Viewshed Analysis, Landscape Character", prefix="visual_landscape - Assessment: ")
    visual_landscape_Mitigation = dspy.OutputField(desc="Extract facts about Visual Mitigation (tower design, routing, screening)", prefix="visual_landscape - Mitigation: ")

    # EMF and Noise
    emf_Levels = dspy.OutputField(desc="Extract facts about EMF Levels at ROW Edge, Exposure Standards, Residential Areas within Zone", prefix="emf - Levels: ")
    noise_Impacts = dspy.OutputField(desc="Extract facts about Corona Discharge Noise (dBA), Construction Noise, Sensitive Receptors", prefix="noise - Impacts: ")

    # Social Impacts
    social_Resettlement = dspy.OutputField(desc="Extract facts about Households Requiring Resettlement, Land Acquisition (ha)", prefix="social - Resettlement: ")
    social_Access = dspy.OutputField(desc="Extract facts about Access Restrictions, Community Severance, Economic Displacement", prefix="social - Access: ")

    # Construction
    construction_Access = dspy.OutputField(desc="Extract facts about Access Road Requirements (km), Construction Camps, Methods", prefix="construction - Access: ")
    construction_Environmental = dspy.OutputField(desc="Extract facts about Soil Erosion Risk, Water Crossing Methods, Vegetation Clearing", prefix="construction - Environmental: ")

    # Operational Safety
    operational_safety = dspy.OutputField(desc="Extract facts about Public Safety Measures, ROW Access Control, Fire Risk, Maintenance Access", prefix="operational_safety: ")


class EnergyNuclearSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Energy Nuclear Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    radiation_safety = dspy.OutputField(desc="Extract facts about Radiation Safety, specifically: Dose Control, Monitoring, Exposure Standards", prefix="Radiation Safety: ")
    nuclear_waste_management = dspy.OutputField(desc="Extract facts about Nuclear Waste Management, specifically: Spent Fuel Storage, High-Level Waste, Disposal", prefix="Nuclear Waste Management: ")
    emergency_response = dspy.OutputField(desc="Extract facts about Emergency Response, specifically: Evacuation Plans, Containment, Off-site Consequences", prefix="Emergency Response: ")


class InfrastructurePortsSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Infrastructure Ports Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    marine_ecology = dspy.OutputField(desc="Extract facts about Marine Ecology, specifically: Dredging Impacts, Habitat Loss, Sediment Transport", prefix="Marine Ecology: ")
    shipping_safety = dspy.OutputField(desc="Extract facts about Shipping Safety, specifically: Vessel Traffic, Channel Navigation, Safety Zones", prefix="Shipping Safety: ")
    coastal_impacts = dspy.OutputField(desc="Extract facts about Coastal Impacts, specifically: Erosion, Water Quality, Storm Surge", prefix="Coastal Impacts: ")


class AgricultureCropsSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Agriculture Crops Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    soil_management = dspy.OutputField(desc="Extract facts about Soil Management, specifically: Soil Preparation, Fertility, Erosion Control", prefix="Soil Management: ")
    crop_production = dspy.OutputField(desc="Extract facts about Crop Production, specifically: Yield, Crop Types, Rotation, Fertilizer Use", prefix="Crop Production: ")
    water_irrigation = dspy.OutputField(desc="Extract facts about Water Irrigation, specifically: Water Source, Application Methods, Efficiency", prefix="Water Irrigation: ")


class AgricultureAnimalProductionSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Agriculture Animal Production Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    animal_welfare = dspy.OutputField(desc="Extract facts about Animal Welfare, specifically: Housing, Feed Management, Health Care", prefix="Animal Welfare: ")
    waste_management = dspy.OutputField(desc="Extract facts about Waste Management, specifically: Manure Handling, Composting, Nutrient Management", prefix="Waste Management: ")
    disease_control = dspy.OutputField(desc="Extract facts about Disease Control, specifically: Biosecurity, Vaccination, Monitoring Programs", prefix="Disease Control: ")


class AgricultureForestrySpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Agriculture Forestry Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    forest_management = dspy.OutputField(desc="Extract facts about Forest Management, specifically: Rotation Period, Harvesting Methods, Replanting", prefix="Forest Management: ")
    biodiversity_conservation = dspy.OutputField(desc="Extract facts about Biodiversity Conservation, specifically: Protected Species, Habitat Restoration, Wildlife Corridors", prefix="Biodiversity Conservation: ")
    wood_processing = dspy.OutputField(desc="Extract facts about Wood Processing, specifically: Processing Waste, Emissions, Water Use", prefix="Wood Processing: ")


class ManufacturingGeneralSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Manufacturing General Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    production_processes = dspy.OutputField(desc="Extract facts about Production Processes, specifically: Manufacturing Techniques, Capacity, Output", prefix="Production Processes: ")
    supply_chain = dspy.OutputField(desc="Extract facts about Supply Chain, specifically: Raw Materials, Supplier Management, Logistics", prefix="Supply Chain: ")
    occupational_health = dspy.OutputField(desc="Extract facts about Occupational Health, specifically: Hazards, Safety Equipment, Worker Training", prefix="Occupational Health: ")


class RealEstateCommercialSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Real Estate Commercial Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    building_design = dspy.OutputField(desc="Extract facts about Building Design, specifically: Layout, Energy Efficiency, Accessibility", prefix="Building Design: ")
    traffic_operations = dspy.OutputField(desc="Extract facts about Traffic Operations, specifically: Parking, Access, Transportation Demand", prefix="Traffic Operations: ")
    waste_management = dspy.OutputField(desc="Extract facts about Waste Management, specifically: Waste Generation, Recycling, Disposal", prefix="Waste Management: ")


class RealEstateHospitalitySpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Real Estate Hospitality Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    guest_experience = dspy.OutputField(desc="Extract facts about Guest Experience, specifically: Amenities, Accessibility, Safety", prefix="Guest Experience: ")
    resource_consumption = dspy.OutputField(desc="Extract facts about Resource Consumption, specifically: Water, Energy, Food Supplies", prefix="Resource Consumption: ")
    community_impacts = dspy.OutputField(desc="Extract facts about Community Impacts, specifically: Employment, Local Economy, Cultural Integration", prefix="Community Impacts: ")


class RealEstateHealthcareSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Real Estate Healthcare Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    patient_care = dspy.OutputField(desc="Extract facts about Patient Care, specifically: Facility Capacity, Medical Equipment, Service Quality", prefix="Patient Care: ")
    medical_waste = dspy.OutputField(desc="Extract facts about Medical Waste, specifically: Hazardous Waste Handling, Infectious Waste, Disposal", prefix="Medical Waste: ")
    emergency_preparedness = dspy.OutputField(desc="Extract facts about Emergency Preparedness, specifically: Evacuation Plans, Backup Power, Infection Control", prefix="Emergency Preparedness: ")


class FinancialBankingSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Financial Banking Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    operational_risk = dspy.OutputField(desc="Extract facts about Operational Risk, specifically: Cybersecurity, Data Protection, Business Continuity", prefix="Operational Risk: ")
    environmental_social_risk = dspy.OutputField(desc="Extract facts about Environmental & Social Risk, specifically: Loan Portfolio Risks, Sector Exposure, Climate Risks", prefix="Environmental & Social Risk: ")
    stakeholder_engagement = dspy.OutputField(desc="Extract facts about Stakeholder Engagement, specifically: Customer Relations, Regulatory Compliance, Community Support", prefix="Stakeholder Engagement: ")


class FinancialMicrofinanceSpecificImpactsSignature(dspy.Signature):
    """
    Extracted facts for Financial Microfinance Specific Impacts.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    financial_inclusion = dspy.OutputField(desc="Extract facts about Financial Inclusion, specifically: Customer Demographics, Loan Products, Access to Services", prefix="Financial Inclusion: ")
    poverty_alleviation = dspy.OutputField(desc="Extract facts about Poverty Alleviation, specifically: Income Generation, Livelihood Support, Community Development", prefix="Poverty Alleviation: ")
    client_protection = dspy.OutputField(desc="Extract facts about Client Protection, specifically: Fair Pricing, Transparency, Complaint Resolution", prefix="Client Protection: ")


class FinancialIntermediaryESMSSignature(dspy.Signature):
    """
    Extracted facts for Financial Intermediary ESMS (ESR 9 / PS FI).
    Covers FI classification, exclusion/referral lists, screening, due diligence, ESMS procedures, disclosure, and monitoring.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    fi_classification = dspy.OutputField(desc="Extract FI type, portfolio risk profile, sub-project categories distribution, high-risk sectors, ESR 9 applicability determination", prefix="FI Classification: ")
    exclusion_referral_lists = dspy.OutputField(desc="Extract exclusion list, referral list, list implementation procedures, exceptions process, list review and update frequency", prefix="Exclusion/Referral Lists: ")
    screening_categorization = dspy.OutputField(desc="Extract sub-project screening methodology, E&S categorization criteria, screening tools and checklists, decision-making process, documentation requirements, categorization review process", prefix="Screening & Categorization: ")
    due_diligence = dspy.OutputField(desc="Extract Category A and B due diligence requirements, E&S review procedures, site visits requirements, third-party assessments, compliance verification", prefix="Due Diligence: ")
    esms_procedures = dspy.OutputField(desc="Extract FI's ESMS policy, E&S management staff and resources, training programs for FI staff, sub-project approval process, covenant and condition tracking, national law compliance verification", prefix="ESMS Procedures: ")
    category_a_disclosure = dspy.OutputField(desc="Extract Category A ESIA public disclosure requirements, disclosure timeline, website links to ESIAs, language requirements, accessibility provisions, ESRs 1-8 and 10 compliance verification", prefix="Category A Disclosure: ")
    portfolio_monitoring = dspy.OutputField(desc="Extract monitoring frequency by category, E&S performance indicators, annual portfolio review, non-compliance response procedures, corrective action plans, reporting to EBRD/IFC", prefix="Portfolio Monitoring: ")


class GenderActionPlanSignature(dspy.Signature):
    """
    Extracted facts for Gender Action Plan (GAP).
    Covers women's participation, equitable access, benefits, empowerment, and implementation.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    increased_participation = dspy.OutputField(
        desc="Extract women's employment targets, women in management targets, women in non-traditional roles, participation in decision making, women's leadership development, equal pay policies",
        prefix="Increased Participation: "
    )
    equitable_access = dspy.OutputField(
        desc="Extract access to training and skills development, credit and financial services, land and property rights, technology and equipment access, transportation access, childcare facilities",
        prefix="Equitable Access: "
    )
    practical_benefits = dspy.OutputField(
        desc="Extract income generation opportunities, livelihood enhancement programs, health services access, education and literacy programs, water and sanitation improvements, time-saving infrastructure",
        prefix="Practical Benefits: "
    )
    decision_making = dspy.OutputField(
        desc="Extract representation in consultation processes, women's committees or groups, grievance mechanism access, community leadership roles, collective bargaining rights, political participation support",
        prefix="Decision Making: "
    )
    implementation_monitoring = dspy.OutputField(
        desc="Extract responsible entity for GAP implementation, budget allocation for gender activities, timeline and milestones, gender monitoring indicators, reporting frequency, evaluation mechanisms",
        prefix="Implementation & Monitoring: "
    )


class CulturallyAppropriateGRMSignature(dspy.Signature):
    """
    Extracted facts for Culturally Appropriate Grievance Redress Mechanism (GRM).
    Covers cultural design, vulnerable group provisions, GBVH reporting, and safety mechanisms.
    """

    context = dspy.InputField(desc="The text content to extract facts from.")

    cultural_design_and_accessibility = dspy.OutputField(
        desc="Extract information about whether the mechanism is culturally appropriate with explanation, languages available in GRM, literacy considerations for illiterate people, accessibility to marginalized groups, gender-sensitive approach with special provisions for women/girls, youth accessibility features, elderly access accommodations, disabled access provisions, non-interference with customary systems, integration with customary processes, cost-free or nominal fee provisions, and awareness and promotion mechanisms",
        prefix="Cultural Design & Accessibility: "
    )
    special_provisions_vulnerable_groups = dspy.OutputField(
        desc="Extract provisions for: women's safety and confidentiality with female staff options, girls/children protection with appropriate processes, indigenous peoples' respect for customary law and customary representatives, ethnic minorities' cultural identity respect, LGBTQ+ non-discrimination and safe process provisions, persons with disabilities accessibility and reasonable accommodations, elderly patient and accessible processes, migrant workers with language support and documentation not required, temporary workers protection despite employment status, caste/discrimination-based protection, GBVH-specific safe reporting and trauma-informed approach, child labor hotline if applicable, and whistleblower protections from retaliation",
        prefix="Special Provisions for Vulnerable Groups: "
    )
    gbvh_incident_reporting_and_response = dspy.OutputField(
        desc="Extract GBVH definition and scope, GBVH reporting pathway (separate or dedicated line), trauma-informed response procedures, confidentiality protections for complainants, victim support services including counseling/medical/legal, investigation procedures and responsible parties, remediation options available to victims, offender accountability and consequences, prevention integration for future occurrence prevention, monitoring and follow-up on case outcomes, third-party involvement (NGO, health, law enforcement coordination), and distinction between GBVH and other grievances (separate or integrated process)",
        prefix="GBVH Incident Reporting & Response: "
    )
    non_retribution_and_safety_mechanisms = dspy.OutputField(
        desc="Extract explicit non-retribution guarantees, retaliation monitoring procedures, retaliation reporting processes, protective measures to ensure safety, anonymity options for complainants, confidentiality levels and protections, safe whistleblower channels for protected reporting, third-party oversight and independent review mechanisms, community awareness of protections, flexibility in perpetrator identification without requirement to name them, and post-resolution safety planning to maintain safety after resolution",
        prefix="Non-Retribution & Safety Mechanisms: "
    )


