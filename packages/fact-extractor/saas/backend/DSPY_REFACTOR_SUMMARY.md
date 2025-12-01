# DSPy Refactor Summary - Pydantic Models + JSONAdapter

## Overview

Major refactoring based on DSPy community best practices to improve structured output reliability. Replaced manual JSON parsing with Pydantic models and DSPy's JSONAdapter.

---

## Problems with Previous Approach

### 1. **Manual JSON Enforcement via Prompts**
```python
# OLD: Trying to force JSON through signature docstrings
class FactExtraction(dspy.Signature):
    """Extract facts and return as JSON array ONLY...
    CRITICAL: Output MUST start with [ and end with ]."""

    facts_json = dspy.OutputField(desc="Valid JSON array starting with [...")
```

**Issues:**
- LLM ignores instructions and returns summaries
- LLM invents wrong field names (`{"text": "...", "type": "fact"}`)
- Requires extensive JSON repair logic
- Fragile and error-prone

### 2. **Complex JSON Parsing Logic**
- 70+ lines of JSON parsing and repair code
- Manual field extraction with .get() everywhere
- Type conversion for every field
- Error-prone dictionaries

### 3. **Wrong DSPy Module**
- Using `ChainOfThought` which adds reasoning text
- Reasoning interferes with JSON output
- LLM outputs explanations instead of pure JSON

---

## New Approach (DSPy Best Practices)

### 1. **Pydantic Models for Schema Definition**

```python
from pydantic import BaseModel, Field

class ExtractedFact(BaseModel):
    """Pydantic model representing a single fact"""
    name: str = Field(description="Descriptive name of the fact")
    type: str = Field(description="Type: 'quantity' or 'categorical'")
    value: str = Field(description="Value as text string")
    value_num: float = Field(description="Numeric value")
    unit: str = Field(description="Unit of measurement")
    aliases: List[str] = Field(default_factory=list)
    evidence: str = Field(description="Direct quote from text")
```

**Benefits:**
- Type safety and automatic validation
- Clean, self-documenting schema
- Automatic serialization/deserialization
- Works natively with DSPy

### 2. **Clean Signature Focused on WHAT, Not HOW**

```python
class FactExtractionSignature(dspy.Signature):
    """Extract quantitative and categorical facts from ESIA document text.

    Focus on extracting measurable quantities (numbers with units) and important
    categorical information (names, classifications, assessors, etc.)
    """

    text: str = dspy.InputField(desc="Text chunk from document to analyze")
    facts: List[ExtractedFact] = dspy.OutputField(
        desc="List of extracted facts"
    )
```

**Key improvements:**
- Removed all JSON format instructions (adapter handles this)
- Focuses on task description, not output format
- Uses Pydantic model directly in output field
- Much cleaner and more maintainable

### 3. **JSONAdapter for Format Enforcement**

```python
def configure_llm():
    """Configure DSPy with JSONAdapter"""
    lm = dspy.OllamaLocal(model="qwen2.5:7b-instruct", ...)

    # JSONAdapter enforces JSON at LLM API level
    adapter = dspy.JSONAdapter()

    dspy.configure(lm=lm, adapter=adapter)
```

**How it works:**
- Uses LLM's native JSON mode (`response_format` parameter)
- Enforces format at API level, not prompt level
- Much more reliable than prompt-based requests
- Automatic fallback if parsing fails

### 4. **Simplified Extraction Logic**

```python
# OLD: 70+ lines of JSON parsing
result = self.extractor(text=text)
json_str = result.facts_json
facts_data = json.loads(json_str)  # Can fail
# Manual extraction of every field...
for fact_dict in facts_data:
    value_num = fact_dict.get('value_num')  # Can be missing
    if value_num is None:
        value_num = 0.0
    # ... repeat for every field

# NEW: Direct Pydantic model conversion
result = self.extractor(text=text)
extracted_facts = result.facts  # Already validated!

for extracted_fact in extracted_facts:
    fact = Fact(
        name=extracted_fact.name,  # Type-safe access
        value_num=extracted_fact.value_num,  # Already correct type
        # ... all fields guaranteed to exist
    )
```

**Lines of code reduction:**
- Before: ~150 lines in FactExtractor
- After: ~80 lines
- **46% code reduction**
- Removed: JSON parsing, repair logic, manual validation

### 5. **Pydantic-Based Few-Shot Examples**

```python
# OLD: Manual JSON dumps
example = dspy.Example(
    text="...",
    facts_json=json.dumps([{"name": "...", ...}])
).with_inputs("text")

# NEW: Type-safe Pydantic models
example = dspy.Example(
    text="...",
    facts=[
        ExtractedFact(
            name="Project area",
            type="quantity",
            value="500",
            value_num=500,
            unit="hectares",
            aliases=["site area"],
            evidence="will cover an area of 500 hectares"
        )
    ]
).with_inputs("text")
```

**Benefits:**
- Type checking at example creation time
- IDE autocomplete for field names
- Catches errors before runtime
- Self-documenting examples

---

## Architecture Changes

### Before: Manual JSON Parsing Flow

```
Text → DSPy Predict → String (JSON-like) → json.loads() → Dict
                          ↓ (often fails)
                    JSON Repair Regex
                          ↓
                    Try parse again
                          ↓
                 Manual field extraction
                          ↓
                    Type conversion
                          ↓
                   Fact objects
```

### After: Pydantic + JSONAdapter Flow

```
Text → DSPy Predict → List[ExtractedFact] (validated)
          ↑                     ↓
    JSONAdapter          Direct conversion
    (enforces JSON)            ↓
                         Fact objects
```

**Key difference:** Validation happens automatically via Pydantic before we see the data.

---

## Code Comparison

### OLD: extract_from_chunk (Complex)

```python
def extract_from_chunk(self, text: str, page: int, chunk_id: int) -> List[Fact]:
    try:
        result = self.extractor(text=text)
        json_str = result.facts_json

        # Check empty
        if not json_str or json_str.strip() == "":
            print(f"Warning: Empty response")
            return []

        # Parse JSON
        try:
            facts_data = json.loads(json_str)
        except json.JSONDecodeError:
            # Repair attempt
            json_str = self.repair_json(json_str)
            facts_data = json.loads(json_str)  # Can still fail

        # Handle format variations
        if isinstance(facts_data, dict) and 'facts' in facts_data:
            facts_data = facts_data['facts']

        facts = []
        for fact_dict in facts_data:
            # Extract with defaults
            value_num_raw = fact_dict.get('value_num')
            if value_num_raw is None or value_num_raw == '':
                value_num = 0.0
            else:
                try:
                    value_num = float(value_num_raw)
                except (ValueError, TypeError):
                    value_num = 0.0

            # Create fact
            fact = Fact(
                name=fact_dict.get('name', ''),
                type=fact_dict.get('type', 'quantity'),
                value=fact_dict.get('value', ''),
                value_num=value_num,
                unit=fact_dict.get('unit', ''),
                aliases=fact_dict.get('aliases', []) if fact_dict.get('aliases') else [],
                evidence=fact_dict.get('evidence', ''),
                page=page,
                chunk_id=chunk_id
            )

            # ... normalize
            facts.append(fact)

        return facts

    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []
```

**Problems:**
- Multiple try/except blocks
- Manual type conversion everywhere
- Fragile JSON parsing
- Defensive .get() calls with defaults
- ~60 lines

### NEW: extract_from_chunk (Simple)

```python
def extract_from_chunk(self, text: str, page: int, chunk_id: int) -> List[Fact]:
    try:
        # Call DSPy - returns validated Pydantic models
        result = self.extractor(text=text)
        extracted_facts = result.facts

        # Check empty
        if not extracted_facts:
            return []

        # Convert Pydantic models to Fact dataclass
        facts = []
        for extracted_fact in extracted_facts:
            fact = Fact(
                name=extracted_fact.name,
                type=extracted_fact.type,
                value=extracted_fact.value,
                value_num=extracted_fact.value_num,
                unit=extracted_fact.unit,
                aliases=extracted_fact.aliases,
                evidence=extracted_fact.evidence,
                page=page,
                chunk_id=chunk_id
            )

            # Normalize and add
            fact.signature = slugify(fact.name)
            fact.normalized_value, fact.normalized_unit = normalize_unit(
                fact.value_num, fact.unit
            )
            facts.append(fact)

        return facts

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return []
```

**Improvements:**
- Single try/except
- No JSON parsing needed
- No type conversion (Pydantic handles it)
- Direct field access (guaranteed to exist)
- ~25 lines
- **58% fewer lines**

---

## Testing Changes

### Debug Script Updates

The debug script (`test_llm_debug.py`) now shows:

**Before:**
```
📤 Raw LLM Output (facts_json):
Type: <class 'str'>
Content: [{"text": "...", "type": "fact"}]
```

**After:**
```
📤 Extracted Facts (Pydantic models):
Type: <class 'list'>
Count: 3

Processing fact 1:
  Type: <class 'ExtractedFact'>
  Name: Project area
  Value: 500 hectares
  Value (numeric): 500.0
  Aliases: ['site area']
```

**Benefits:**
- See actual Pydantic objects
- Field-level debugging
- Type information visible
- No JSON string parsing needed

---

## Benefits Summary

### 1. **Reliability**
- ✅ LLM's native JSON mode enforces format
- ✅ Pydantic validates all fields automatically
- ✅ Type safety prevents runtime errors
- ✅ No manual JSON parsing failures

### 2. **Maintainability**
- ✅ 46% less code (~70 lines removed)
- ✅ Cleaner, more readable
- ✅ Self-documenting Pydantic models
- ✅ Easier to extend (just add Pydantic fields)

### 3. **Developer Experience**
- ✅ IDE autocomplete for all fields
- ✅ Type checking catches errors early
- ✅ No defensive .get() calls needed
- ✅ Clear error messages from Pydantic

### 4. **Performance**
- ✅ Less string manipulation
- ✅ No regex-based JSON repair
- ✅ Faster validation (Pydantic is in Rust)
- ✅ Native LLM JSON mode is more efficient

---

## Migration Guide

### For New Signatures

1. **Define Pydantic Model:**
```python
class YourOutput(BaseModel):
    field1: str = Field(description="...")
    field2: int = Field(description="...")
```

2. **Create Signature:**
```python
class YourSignature(dspy.Signature):
    """Task description"""
    input: str = dspy.InputField(desc="...")
    output: YourOutput = dspy.OutputField(desc="...")
```

3. **Configure JSONAdapter:**
```python
dspy.configure(lm=your_lm, adapter=dspy.JSONAdapter())
```

4. **Use it:**
```python
predictor = dspy.Predict(YourSignature)
result = predictor(input="...")
output_obj = result.output  # Already validated!
```

### For Existing Code

1. Convert output field to Pydantic model
2. Remove manual JSON parsing
3. Remove JSON repair logic
4. Add JSONAdapter to dspy.configure()
5. Update few-shot examples to use Pydantic models

---

## Files Changed

### Core Changes
- **saas/core/extractor.py** - Main refactor
  - Added `ExtractedFact` Pydantic model
  - Simplified `FactExtractionSignature`
  - Added `JSONAdapter` to `configure_llm()`
  - Rewrote `FactExtractor` class
  - Removed `repair_json()` method
  - ~70 lines removed

### Test Updates
- **saas/backend/test_llm_debug.py** - Debug script
  - Uses new Pydantic models
  - Shows structured output details
  - Removed JSON parsing debug code
  - ~90 lines simplified

---

## Testing

Run the updated test to see Pydantic + JSONAdapter in action:

```bash
cd saas/backend
python test_llm_debug.py docling_output/your_document_docling.md
```

**Look for:**
- `Loaded 2 few-shot examples for fact extraction`
- `Adapter: JSONAdapter (enforces JSON at API level)`
- `Type: <class 'list'>` (not string!)
- Field values directly accessible
- No JSON parsing errors

---

## References

- [DSPy Adapters Documentation](https://dspy.ai/learn/programming/adapters/)
- [DSPy JSONAdapter API](https://dspy.ai/api/adapters/JSONAdapter/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- DSPy Community Best Practices (2025)

---

## Next Steps

1. **Test with real documents** to verify reliability improvement
2. **Add more Pydantic validation** (e.g., value ranges, enum for type field)
3. **Optimize few-shot examples** using DSPy optimizers
4. **Consider DSPy Signatures v2** for even cleaner syntax

---

## Conclusion

This refactor brings the ESIA Fact Extractor in line with DSPy community best practices:

- **Separation of concerns:** Schema (Pydantic) vs Format (Adapter) vs Logic (Signature)
- **Type safety:** Pydantic ensures correctness at every level
- **Simplicity:** Less code, fewer bugs, easier maintenance
- **Reliability:** Native LLM JSON mode + validation = robust output

The code is now **cleaner, safer, and more maintainable** while following established DSPy patterns used by the community.
