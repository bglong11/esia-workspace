# LLM Extraction Debugging Guide

This guide helps diagnose why fact extraction is not working. Use these test programs in order to isolate the problem.

## Problem Summary

**Symptom:** Docling successfully extracts text from PDFs, but no facts are extracted by the LLM.

**Possible causes:**
1. LLM not returning valid JSON
2. LLM not finding facts in the content
3. DSPy integration issue
4. Ollama connection problem
5. Model not responding correctly

## Diagnostic Tools

Three test programs are provided to diagnose the issue systematically:

### 1. test_ollama_direct.py - Test Ollama Without DSPy

**Purpose:** Verify Ollama is working independently of DSPy

**Usage:**
```bash
cd saas/backend
python test_ollama_direct.py
```

**What it tests:**
- ✅ Ollama connection and API availability
- ✅ Simple text generation (basic LLM functionality)
- ✅ JSON fact extraction (structured output)
- ✅ Chat API format (alternative endpoint)

**What to look for:**
- All tests should pass if Ollama is working correctly
- Pay attention to the JSON extraction test - this shows if the model can generate structured output
- If JSON test fails but simple generation works, the model may need a different prompt format

**Expected output:**
```
✅ PASS  Connection
✅ PASS  Simple generation
✅ PASS  JSON extraction
✅ PASS  Chat format
```

### 2. test_llm_debug.py - Debug DSPy Integration

**Purpose:** Show detailed DSPy interaction with LLM

**Usage:**
```bash
cd saas/backend
python test_llm_debug.py docling_output/your_file_docling.md
```

**What it shows:**
- 📄 Input text being sent to LLM
- ⚙️ DSPy ChainOfThought signature and fields
- 💭 LLM reasoning (if available)
- 📤 Raw LLM output (facts_json field)
- 🔬 JSON parsing attempts and repairs
- ✅ Successfully created Fact objects

**What to look for:**
- Check if `facts_json` output is empty
- Check if JSON is malformed
- Check if facts are in the JSON but not being parsed
- Check for exceptions during parsing

**Alternative: Simple LLM test**
```bash
python test_llm_debug.py --test
```

This runs basic prompts to verify DSPy can call the LLM.

### 3. test_llm_extraction.py - Full Pipeline Debug

**Purpose:** Test complete extraction pipeline with progress tracking

**Usage:**
```bash
cd saas/backend
python test_llm_extraction.py docling_output/your_file_docling.md
```

**What it shows:**
- 📄 File loading and statistics
- ⚙️ LLM configuration from environment variables
- 📦 Text chunking information
- 🔄 Extraction progress for each chunk
- 📊 Summary of all extracted facts

**What to look for:**
- Number of chunks created
- Which chunks produce facts
- Error messages for specific chunks
- Total facts extracted

## Debugging Workflow

### Step 1: Test Ollama Directly

```bash
python test_ollama_direct.py
```

**If this fails:**
- Make sure Ollama is running: `ollama serve`
- Check model is installed: `ollama list | grep qwen2.5:7b-instruct`
- Pull model if needed: `ollama pull qwen2.5:7b-instruct`
- Test manually: `ollama run qwen2.5:7b-instruct "What is 2+2?"`

**If this passes:** Ollama is working. Problem is in DSPy integration.

### Step 2: Test with Debug Script

```bash
# First, make sure you have a Docling output file
python test_full_pipeline.py --pdf your_document.pdf

# This creates: docling_output/your_document_docling.md

# Then debug the LLM extraction
python test_llm_debug.py docling_output/your_document_docling.md
```

**Look for these issues:**

#### Issue A: Empty facts_json
```
📤 Raw LLM Output (facts_json):
Type: <class 'str'>
Length: 0 characters
Content:
  ⚠️  EMPTY STRING
```

**Diagnosis:** DSPy is not getting output from LLM
**Solutions:**
- Check DSPy version: `pip show dspy-ai`
- Verify DSPy is using OllamaLocal correctly
- Try raw LLM test: `python test_llm_debug.py --test`

#### Issue B: Invalid JSON
```
📤 Raw LLM Output (facts_json):
This is some text but not JSON: [{facts about...
```

**Diagnosis:** LLM is returning text instead of JSON
**Solutions:**
- Lower temperature: `export LLM_TEMPERATURE=0.1`
- Try different model: `export OLLAMA_MODEL=llama3.1`
- Check prompt format in DSPy signature

#### Issue C: Valid JSON but No Facts
```
✅ JSON parsed successfully
Type: <class 'list'>
Found 0 fact(s) in JSON
```

**Diagnosis:** LLM returns empty array `[]`
**Solutions:**
- Check if document chunk has extractable facts
- Try simpler/more explicit prompt
- Verify chunk size is appropriate (not too small/large)

#### Issue D: JSON with Facts but Parsing Fails
```
Found 3 fact(s) in JSON
Processing fact 1:
  ❌ Error: KeyError: 'name'
```

**Diagnosis:** JSON structure doesn't match expected schema
**Solutions:**
- Check JSON field names match Fact dataclass
- Update FactExtraction signature
- Add error handling for missing fields

### Step 3: Check Environment Variables

```bash
# View current configuration
env | grep -E "(OLLAMA|LLM)"

# Try different settings
export LLM_TEMPERATURE=0.1        # More consistent JSON
export LLM_MAX_TOKENS=4096        # More space for output
export OLLAMA_MODEL=llama3.1      # Try different model
```

### Step 4: Inspect Docling Output

```bash
# Check what Docling extracted
cat docling_output/your_document_docling.md | head -100

# Check file size
ls -lh docling_output/your_document_docling.md
```

**Questions to answer:**
- Does the markdown contain extractable facts?
- Is the formatting clean and readable?
- Are there tables or structured data?
- Is the text in English (or expected language)?

## Common Issues and Solutions

### 1. DSPy API Compatibility

**Symptom:** `AttributeError: module 'dspy' has no attribute 'LM'`

**Solution:** Code has been updated to use `dspy.OllamaLocal()` instead

### 2. Empty JSON Responses

**Symptom:** LLM returns empty string for facts_json

**Possible causes:**
- DSPy not configured correctly
- Ollama endpoint incorrect
- Model not loaded
- Temperature too high (randomness causing format issues)

**Solutions:**
```bash
# Verify Ollama endpoint
curl http://localhost:11434/api/tags

# Test with lower temperature
export LLM_TEMPERATURE=0.1

# Try chat endpoint instead
# (modify configure_llm to use chat format)
```

### 3. JSON Parse Errors

**Symptom:** `JSONDecodeError: Expecting value`

**Possible causes:**
- LLM returning explanation text before/after JSON
- Malformed JSON (missing quotes, commas, brackets)
- LLM not trained for JSON output

**Solutions:**
- Extract JSON from response: Find `[` to `]`
- Use repair_json() function
- Try format="json" in Ollama options
- Use a model better trained for structured output

### 4. Model Not Finding Facts

**Symptom:** Valid empty JSON array `[]`

**Possible causes:**
- Document chunk has no quantitative facts
- Prompt not clear enough
- Model doesn't understand task
- Context window too small for chunk

**Solutions:**
```bash
# Test with known factual text
echo "The project covers 500 hectares and employs 300 workers." > test_simple.md
python test_llm_debug.py test_simple.md

# If this works, problem is document content
# If this fails, problem is prompt/model
```

### 5. Pydantic Version Conflict

**Symptom:** Warning about pydantic version mismatch

**Status:** Known issue - doesn't affect functionality

```
dspy-ai 2.4.0 requires pydantic==2.5.0, but you have pydantic 2.12.4
```

**Action:** Can be ignored if tests pass

## Getting More Information

### Enable DSPy Debug Logging

```python
import dspy
dspy.settings.configure(trace=True)  # Enable tracing
```

### Check Ollama Logs

```bash
# If running Ollama as service
journalctl -u ollama -f

# If running manually
ollama serve  # Watch console output
```

### Monitor Network Traffic

```bash
# Watch Ollama API calls
tcpdump -i lo -A port 11434

# Or use curl to test endpoint
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b-instruct",
  "prompt": "What is 2+2?",
  "stream": false
}'
```

## Next Steps After Diagnosis

Once you've identified the issue:

1. **If Ollama is the problem:** Fix Ollama installation, model, or configuration
2. **If DSPy is the problem:** Update DSPy integration or switch to direct Ollama calls
3. **If prompt is the problem:** Refine the extraction signature and examples
4. **If model is the problem:** Try different models or adjust parameters

## Files Reference

- `test_ollama_direct.py` - Direct Ollama testing (bypasses DSPy)
- `test_llm_debug.py` - Detailed DSPy debugging with intermediate results
- `test_llm_extraction.py` - Full pipeline test
- `test_full_pipeline.py` - End-to-end test including Docling
- `saas/core/extractor.py` - Core extraction logic
- `saas/.env.example` - Configuration template

## Contact

If you've completed all diagnostic steps and still have issues, provide:
1. Output from `test_ollama_direct.py`
2. Output from `test_llm_debug.py`
3. First 500 chars of your Docling markdown file
4. Environment variables: `env | grep -E "(OLLAMA|LLM)"`
5. DSPy version: `pip show dspy-ai`
6. Ollama version: `ollama --version`
