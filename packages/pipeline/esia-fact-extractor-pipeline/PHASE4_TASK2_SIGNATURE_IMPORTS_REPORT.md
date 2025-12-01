# Phase 4 Production Hardening - Task 2: Signature Import Fix

## Summary

Successfully resolved missing DSPy signature imports and fixed dynamic domain-to-signature mapping issues. All 52 signatures are now properly imported and accessible, including all 12 Phase 2 sector-specific signatures.

## Problem Identified

### Initial Issues
1. **Missing Import**: `FinancialIntermediaryESMSSignature` was not imported in `esia_extractor.py`
2. **Domain Mapping Failures**: Dynamic signature retrieval failed for Phase 2 domains:
   - `infrastructure_ports` → InfrastructurePortsSignature (NOT FOUND)
   - `manufacturing_general` → ManufacturingGeneralSignature (NOT FOUND)
   - `agriculture_crops` → AgricultureCropsSignature (NOT FOUND)
   - `financial_intermediary_esms` → FinancialIntermediaryEsmsSignature (NOT FOUND - case issue)
   - And others...

3. **Archetype-to-Signature Mismatch**: Archetype domains used different naming conventions than signatures:
   - Archetype: `energy_solar` → Signature: `SolarSpecificImpactsSignature`
   - Archetype: `energy_hydro` → Signature: `HydropowerSpecificImpactsSignature`
   - Archetype: `PS1` → Signature: `EnvironmentalAndSocialManagementPlanEsmpSignature`

## Solutions Implemented

### 1. Added Missing Import (Line 57 in `esia_extractor.py`)

```python
# Before (51 imports)
FinancialBankingSpecificImpactsSignature,
FinancialMicrofinanceSpecificImpactsSignature,
# Phase 3B: Culturally appropriate GRM
GenderActionPlanSignature,

# After (52 imports)
FinancialBankingSpecificImpactsSignature,
FinancialMicrofinanceSpecificImpactsSignature,
FinancialIntermediaryESMSSignature,  # <-- ADDED
# Phase 3B: Culturally appropriate GRM
GenderActionPlanSignature,
```

### 2. Enhanced `_get_signature_class()` Method

Added three-tier fallback strategy:

```python
def _get_signature_class(self, domain: str):
    # Tier 1: Try base signature name
    class_name = f"{clean_name}Signature"
    signature_class = getattr(gen_sigs, class_name, None)

    if not signature_class:
        # Tier 2: Try with "SpecificImpacts" suffix
        class_name_with_suffix = f"{clean_name}SpecificImpactsSignature"
        signature_class = getattr(gen_sigs, class_name_with_suffix, None)

        if not signature_class:
            # Tier 3: Remove "specific_impacts" from domain and retry
            if '_specific_impacts' in normalized.lower():
                alt_name = normalized.replace('_specific_impacts', '')
                # ... retry logic
```

**Key Feature**: Handles both patterns:
- Core ESIA: `ProjectDescriptionSignature`
- Sector-specific: `SolarSpecificImpactsSignature`

### 3. Added Acronym Handling

```python
acronym_map = {
    'Esms': 'ESMS',
    # NOTE: 'Esmp' NOT included - signature uses "Esmp" (TitleCase)
    'Emf': 'EMF',
    'Grm': 'GRM',
    'Gbvh': 'GBVH',
    'Seah': 'SEAH',
    'Fpic': 'FPIC',
}
```

**Important**: Different signatures use different casing:
- `FinancialIntermediaryESMSSignature` (uppercase ESMS)
- `EnvironmentalAndSocialManagementPlanEsmpSignature` (TitleCase Esmp)

### 4. Expanded Domain Normalization Mapping

Added comprehensive archetype-to-signature mappings in `normalize_domain_name()`:

```python
mapping = {
    # Core ESIA mappings
    "environmental_and_social_management_plan_esmp": "Environmental And Social Management Plan Esmp",

    # Energy sector (10 mappings)
    "energy_solar": "solar_specific_impacts",
    "energy_hydro": "hydropower_specific_impacts",
    "energy_coal": "coal_power_specific_impacts",
    "energy_nuclear": "energy_nuclear",  # Already correct
    # ... 6 more

    # Mining sector (4 mappings)
    "mining_extension": "mine_specific_impacts",
    "mining_nickel_extension": "nickel_specific_impacts",
    # ... 2 more

    # Infrastructure sector (5 mappings)
    "infrastructure_ports": "infrastructure_ports",  # Already correct
    "infrastructure_airports": "traffic_and_transportation",
    # ... 3 more

    # Manufacturing sector (3 mappings)
    "manufacturing_chemicals": "manufacturing_general_specific_impacts",
    "manufacturing_pharmaceuticals": "manufacturing_general_specific_impacts",
    "manufacturing_textiles": "manufacturing_general_specific_impacts",

    # IFC Performance Standards (8 mappings)
    "PS1": "Environmental And Social Management Plan Esmp",
    "PS2": "baseline_conditions",
    # ... 6 more
}
```

**Total Mappings**: 44 domain name variations → 52 unique signatures

## Verification Results

### Test 1: Import Completeness (`test_signature_imports.py`)

```
Total signatures in generated_signatures.py: 52
Total signatures imported in esia_extractor.py: 52
Missing imports: 0
Extra imports: 0

✓ STATUS: PASSED
```

### Test 2: Dynamic Signature Retrieval

All Phase 2 domains successfully map to signatures:

| Domain | Signature | Status |
|--------|-----------|--------|
| infrastructure_ports | InfrastructurePortsSpecificImpactsSignature | ✓ |
| manufacturing_general | ManufacturingGeneralSpecificImpactsSignature | ✓ |
| agriculture_crops | AgricultureCropsSpecificImpactsSignature | ✓ |
| financial_intermediary_esms | FinancialIntermediaryESMSSignature | ✓ |
| energy_nuclear | EnergyNuclearSpecificImpactsSignature | ✓ |
| real_estate_commercial | RealEstateCommercialSpecificImpactsSignature | ✓ |

### Test 3: Complete Domain Mapping (`verify_complete_signature_mapping.py`)

```
Total domains tested: 52
Successfully mapped: 52
Failed: 0

Phase 2 domains verified: 12/12

✓ VERIFICATION PASSED: All domains successfully mapped to signatures
```

## Signature Categories (52 Total)

### Core ESIA (14 signatures)
- ExecutiveSummarySignature
- IntroductionSignature
- ProjectDescriptionSignature
- BaselineConditionsSignature
- EnvironmentalAndSocialImpactAssessmentSignature
- MitigationAndEnhancementMeasuresSignature
- EnvironmentalAndSocialManagementPlanEsmpSignature
- PublicConsultationAndDisclosureSignature
- ConclusionAndRecommendationsSignature
- ReferencesSignature
- AnnexesSignature
- PolicyLegalAndAdministrativeFrameworkSignature
- CumulativeAndRegionalImpactsSignature
- DecommissioningSignature

### Energy Sector (9 signatures)
- SolarSpecificImpactsSignature
- HydropowerSpecificImpactsSignature
- CoalPowerSpecificImpactsSignature
- GeothermalSpecificImpactsSignature
- EnergyNuclearSpecificImpactsSignature ← **Phase 2**
- PumpedStorageHydropowerSpecificImpactsSignature
- TransmissionLineSpecificImpactsSignature
- GridIntegrationAndTransmissionSignature
- HydrocarbonManagementSignature

### Infrastructure Sector (3 signatures)
- InfrastructurePortsSpecificImpactsSignature ← **Phase 2**
- BridgeAndTunnelConstructionSignature
- PipelineIntegrityAndSafetySignature

### Agriculture Sector (3 signatures) ← **All Phase 2**
- AgricultureCropsSpecificImpactsSignature
- AgricultureAnimalProductionSpecificImpactsSignature
- AgricultureForestrySpecificImpactsSignature

### Manufacturing Sector (1 signature) ← **Phase 2**
- ManufacturingGeneralSpecificImpactsSignature

### Real Estate Sector (3 signatures) ← **All Phase 2**
- RealEstateCommercialSpecificImpactsSignature
- RealEstateHospitalitySpecificImpactsSignature
- RealEstateHealthcareSpecificImpactsSignature

### Financial Sector (3 signatures) ← **All Phase 2**
- FinancialBankingSpecificImpactsSignature
- FinancialMicrofinanceSpecificImpactsSignature
- FinancialIntermediaryESMSSignature

### Mining Sector (5 signatures)
- MineSpecificImpactsSignature
- NickelSpecificImpactsSignature
- AluminaSpecificImpactsSignature
- MineralWasteManagementSignature
- MineClosureAndRehabilitationSignature

### Technical/Environmental (7 signatures)
- NoiseAndVibrationSignature
- VisualAndLandscapeImpactsSignature
- AvianAndBatImpactsSignature
- ElectromagneticFieldsEmfSignature
- HazardousMaterialsManagementSignature
- ProcessEmissionsSignature
- WellDrillingAndCompletionSignature

### Cross-Cutting Themes (4 signatures)
- GenderActionPlanSignature
- CulturallyAppropriateGRMSignature
- TrafficAndTransportationSignature
- UtilitiesRelocationSignature

## Impact on Pipeline Performance

### Before Fix
- Only ~5 domains actively extracting
- Errors: "InfrastructurePortsSignature not found"
- Errors: "ManufacturingTextilesSignature not found"
- Unknown domain errors for Phase 2 sectors

### After Fix
- All 52 signatures available
- All 52 archetype domains map correctly
- 12 Phase 2 sector signatures fully functional
- Dynamic mapping handles:
  - Archetype naming variations (energy_solar → SolarSpecificImpactsSignature)
  - IFC Performance Standards (PS1-PS8 → appropriate signatures)
  - Sector extensions (mining_nickel_extension → NickelSpecificImpactsSignature)

## Files Modified

1. **src/esia_extractor.py** (3 changes)
   - Added `FinancialIntermediaryESMSSignature` import (line 57)
   - Enhanced `_get_signature_class()` with 3-tier fallback (lines 180-233)
   - Expanded `normalize_domain_name()` with 44 mappings (lines 70-129)

## Test Files Created

1. **test_signature_imports.py**
   - Verifies all signatures imported
   - Tests dynamic retrieval for key domains
   - Categorizes signatures by sector

2. **verify_complete_signature_mapping.py**
   - Tests all 52 archetype domains
   - Validates Phase 2 domains specifically
   - Provides detailed mapping diagnostics

## Next Steps

### Recommended
1. ✓ Run Phase 3 extraction again to verify no "Unknown domain" errors
2. ✓ Monitor extraction logs for signature retrieval warnings
3. Add integration test in Step 2 pipeline to catch future import issues
4. Document signature naming conventions for future Phase additions

### Future Considerations
- Consider consolidating archetype naming to match signature naming
- Add automatic signature discovery from `generated_signatures.py`
- Create signature generator that validates naming consistency

## Conclusion

All 52 DSPy signatures are now properly imported and dynamically accessible. The enhanced domain mapping system handles:
- Legacy ESIA domains
- Phase 2 sector-specific domains
- IFC Performance Standards
- Archetype naming variations

**Status**: ✓ COMPLETE - All Phase 2 signatures operational, 100% domain coverage achieved.
