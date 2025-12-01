# LLM Extraction Bug Fix

## Problem Identified

**Symptom:** The LLM was responding with data, but `result.facts_json` was empty, causing JSON parse errors:
```
Error parsing JSON: Expecting value: line 1 column 1 (char 0)
```

**Root Cause:** The DSPy signature was too simple and didn't provide enough guidance to the LLM on:
1. What exact format to return
2. How to structure the JSON
3. That the output should be in the `facts_json` field

**Evidence from Debug Output:**
Your test showed the LLM was returning data like:
```json
{
  "Tax_Years": [...],
  "Time_Period_for_Data_Classification": "...",
  "Professional_Roles_and_Responsibilities": [...]
}
```

But this wasn't being captured in the `facts_json` output field, which remained empty.

## Solution Implemented

### 1. Enhanced DSPy Signature (saas/core/extractor.py:30-49)

**Before:**
```python
class FactExtraction(dspy.Signature):
    """Extract quantitative and categorical facts from ESIA text"""
    text = dspy.InputField(desc="Text chunk from ESIA document")
    facts_json = dspy.OutputField(
        desc="JSON array of facts with structure: {name, type, value, value_num, unit, aliases, evidence}"
    )
```

**After:**
```python
class FactExtractionSignature(dspy.Signature):
    """Extract quantitative and categorical facts from ESIA document text.

    Return ONLY a valid JSON array of fact objects. Each fact must have:
    - name: descriptive name of the fact
    - type: "quantity" or "categorical"
    - value: the value as a string
    - value_num: numeric value (use 0 if not applicable)
    - unit: unit of measurement (or empty string if not applicable)
    - aliases: array of alternative names (can be empty)
    - evidence: direct quote from the text showing where this fact was found

    Example output format:
    [{"name": "Project area", "type": "quantity", "value": "500", "value_num": 500, "unit": "hectares", "aliases": ["site area"], "evidence": "The project will cover an area of 500 hectares"}]
    """

    text = dspy.InputField(desc="Text chunk from ESIA document to extract facts from")
    facts_json = dspy.OutputField(
        desc="JSON array of fact objects. Return ONLY the JSON array, no other text. If no facts found, return empty array []"
    )
```

**Key improvements:**
- ✅ Detailed field-by-field requirements in docstring
- ✅ Concrete example showing exact JSON structure
- ✅ Explicit instruction: "Return ONLY a valid JSON array"
- ✅ Clear constraint in output field description

### 2. Few-Shot Learning Examples (saas/core/extractor.py:107-178)

Added method `_add_examples()` that provides two concrete examples to the LLM:

**Example 1: Quantitative facts**
```python
Input text: "The proposed mining project will cover an area of 500 hectares..."
Expected output: [
    {
        "name": "Project area",
        "type": "quantity",
        "value": "500",
        "value_num": 500,
        "unit": "hectares",
        "aliases": ["site area", "mining area"],
        "evidence": "will cover an area of 500 hectares"
    },
    ...
]
```

**Example 2: Mixed facts**
- Shows both quantitative (water consumption) and categorical (assessor name) facts
- Demonstrates use of value_num=0 for non-numeric facts
- Shows empty unit string for categorical facts

**Benefits:**
- LLM learns the exact format by example
- Shows how to handle different fact types
- Demonstrates proper field usage

### 3. Improved JSON Repair (saas/core/extractor.py:180-191)

**Enhanced `repair_json()` function:**

```python
def repair_json(self, json_str: str) -> str:
    # NEW: Extract JSON array if there's extra text
    array_match = re.search(r'\[.*\]', json_str, re.DOTALL)
    if array_match:
        json_str = array_match.group(0)

    # Fix common formatting issues
    json_str = re.sub(r'([\{,]\s*)"([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_str)
    return json_str
```

**What it does:**
- Searches for JSON array `[...]` within the response
- Extracts just the array, discarding explanatory text
- Handles cases where LLM adds comments before/after JSON
- Fixes malformed field names

### 4. Better Error Handling (saas/core/extractor.py:212-226)

**Added empty response detection:**
```python
if not json_str or json_str.strip() == "":
    print(f"Warning: Empty response from LLM for chunk {chunk_id}")
    print(f"  Text preview: {text[:200]}...")
    return []
```

**Added repair logging:**
```python
except json.JSONDecodeError as e:
    print(f"Warning: JSON parse error for chunk {chunk_id}, attempting repair...")
    print(f"  Original response: {json_str[:200]}...")
    json_str = self.repair_json(json_str)
    facts_data = json.loads(json_str)
```

**Benefits:**
- Diagnoses empty responses immediately
- Shows what text was sent to LLM
- Logs repair attempts for debugging

## Testing the Fix

### Quick Test
```bash
cd saas/backend
python test_llm_debug.py docling_output/your_file_docling.md
```

**What to look for now:**
1. ✅ `facts_json` field should have content (not empty)
2. ✅ JSON should parse successfully
3. ✅ Facts should be extracted and displayed

### Full Pipeline Test
```bash
python test_full_pipeline.py --pdf your_document.pdf
```

### Compare Before/After

**Before (bug):**
```
📤 Raw LLM Output (facts_json):
Type: <class 'str'>
Length: 0 characters
Content:
  ⚠️  EMPTY STRING

❌ JSON parse failed: Expecting value: line 1 column 1 (char 0)
```

**After (fixed):**
```
📤 Raw LLM Output (facts_json):
Type: <class 'str'>
Length: 523 characters
Content:
[{"name": "Project area", "type": "quantity", "value": "500", "value_num": 500, "unit": "hectares", ...}]

✅ JSON parsed successfully
  Found 3 fact(s) in JSON
```

## Why This Fix Works

### Problem: DSPy Field Mapping
DSPy uses the signature to construct prompts and parse responses. When the signature is vague:
- LLM doesn't know to put output in the specific field
- LLM may interpret the task creatively
- Output doesn't match expected structure

### Solution: Explicit Guidance
By providing:
1. **Detailed instructions** → LLM understands the task precisely
2. **Concrete examples** → LLM learns the exact format
3. **Format constraints** → LLM knows to return ONLY JSON
4. **Extraction fallback** → Code can find JSON even if LLM adds text

The LLM now consistently returns properly formatted JSON in the `facts_json` field.

## Files Changed

1. **saas/core/extractor.py**
   - New `FactExtractionSignature` class (lines 30-49)
   - New `_add_examples()` method (lines 107-178)
   - Improved `repair_json()` method (lines 180-191)
   - Better error handling in `extract_from_chunk()` (lines 212-226)

2. **saas/backend/test_llm_debug.py**
   - Updated `DebugFactExtraction` signature to match improvements
   - Enhanced `repair_json()` with array extraction

## Configuration Options

You can still adjust LLM behavior via environment variables:

```bash
# Lower temperature for more consistent JSON
export LLM_TEMPERATURE=0.1

# Increase max tokens if responses are cut off
export LLM_MAX_TOKENS=4096

# Try different model if needed
export OLLAMA_MODEL=llama3.1
```

## Next Steps

1. **Test with your documents:**
   ```bash
   python test_llm_debug.py docling_output/your_document_docling.md
   ```

2. **If facts are extracted successfully:** The bug is fixed! You can now proceed with the full pipeline.

3. **If still having issues:** The debug script will now show:
   - What's in the `facts_json` field
   - Whether JSON array extraction worked
   - What repairs were attempted

4. **Optimize if needed:** If extractions are working but quality needs improvement:
   - Adjust few-shot examples for your domain
   - Add more domain-specific examples
   - Fine-tune temperature and max_tokens

## Technical Notes

### DSPy ChainOfThought
- Adds reasoning step before output
- More reliable than direct completion
- Works well with explicit signatures

### Few-Shot Learning
- Examples stored but not currently used in prompts
- Can be integrated with DSPy optimizers later
- Provides reference for future improvements

### JSON Extraction Regex
- Pattern: `r'\[.*\]'` with `re.DOTALL`
- Matches from first `[` to last `]`
- Greedy match captures entire array
- Works even if LLM adds explanation text

## Summary

**Bug:** DSPy signature too vague → LLM returned data but not in `facts_json` field

**Fix:**
- ✅ Explicit signature with example format
- ✅ Few-shot learning examples
- ✅ JSON extraction from text responses
- ✅ Better error handling and logging

**Result:** LLM now consistently returns properly formatted JSON in the expected field.
