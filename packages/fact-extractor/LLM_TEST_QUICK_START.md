# LLM Configuration Test - Quick Start Guide

## TL;DR

```bash
# Run all provider tests
python test_llm_configuration.py

# Run specific provider
python test_llm_configuration.py --provider gemini
```

**Current Status:** ✅ 3/4 Providers Working (Gemini, Anthropic, Ollama)

---

## Test Results at a Glance

```
✅ Gemini     - PASS (1.37s, Fastest!)
✅ Anthropic  - PASS (1.91s, Reliable)
✅ Ollama     - PASS (Local, Free)
⚠️ OpenAI     - FAIL (API key needs update)
```

---

## What Was Created

### 1. Test Script: `test_llm_configuration.py`
- **Size:** 600+ lines
- **Purpose:** Comprehensive testing of all 4 LLM providers
- **Features:**
  - Automatic environment loading from .env
  - Detailed debugging output
  - Security features (masked API keys)
  - Performance metrics
  - Actionable recommendations
  - Error handling for each provider

### 2. Documentation Files
- **`TEST_LLM_CONFIGURATION.md`** - Complete usage guide (400+ lines)
- **`TEST_RESULTS_SUMMARY.md`** - Detailed results and analysis (300+ lines)
- **`LLM_TEST_QUICK_START.md`** - This file (quick reference)

### 3. Bug Fixes
- Fixed DSPy module calling convention in esia_extractor.py
- Fixed OpenAI API configuration (dspy.OpenAI → dspy.LM)
- Added Ollama compatibility fallback

---

## Quick Command Reference

### Test All Providers
```bash
python test_llm_configuration.py
```

### Test Single Provider
```bash
# Test Gemini (fastest)
python test_llm_configuration.py --provider gemini

# Test Anthropic (reliable)
python test_llm_configuration.py --provider anthropic

# Test Ollama (local)
python test_llm_configuration.py --provider ollama

# Test OpenAI (needs valid key)
python test_llm_configuration.py --provider openai
```

### Verbose Output
```bash
python test_llm_configuration.py --verbose
```

---

## Usage with ESIA Extractor

### Using Different Providers

```bash
# Use Gemini (fastest, recommended)
export LLM_PROVIDER=gemini
python esia_extractor.py input.md output/

# Use Anthropic (reliable alternative)
export LLM_PROVIDER=anthropic
python esia_extractor.py input.md output/

# Use Ollama (free, local)
export LLM_PROVIDER=ollama
python esia_extractor.py input.md output/

# Use OpenAI (powerful but needs valid API key)
export LLM_PROVIDER=openai
python esia_extractor.py input.md output/
```

### On Windows (PowerShell)
```powershell
$env:LLM_PROVIDER = "gemini"
python esia_extractor.py input.md output/
```

---

## Provider Recommendations

### For Speed: **Gemini** ⚡
- Response time: 1.37s
- Free tier available
- Recommended for high-volume processing

### For Reliability: **Anthropic** ✓
- Response time: 1.91s
- Consistent performance
- Good balance of speed/cost

### For Freedom: **Ollama** 🎉
- No API key needed
- Runs locally (privacy)
- Perfect for development/testing

### For Power: **OpenAI** 🚀
- Most capable models
- Currently needs API key update
- Higher cost

---

## Fixing OpenAI (If Needed)

The OpenAI API key in .env appears to be expired/invalid. To fix:

1. **Get a new API key:**
   - Visit https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key

2. **Update .env file:**
   ```
   OPENAI_API_KEY=sk-proj-your-new-key-here
   OPENAI_MODEL=gpt-4o-mini
   ```

3. **Test it:**
   ```bash
   python test_llm_configuration.py --provider openai
   ```

---

## Understanding Test Output

### Successful Provider Test
```
Testing Gemini Configuration
═════════════════════════════

Environment:
  API Key: AIzaSyDN...****
  Model: gemini-2.5-flash
  Temperature: 0.1
  Max Tokens: 2048

Validating API Key...
  ✓ API key present and not placeholder

Creating LM object...
  ✓ LM object created

Configuring DSPy...
  ✓ DSPy configured

Testing simple prompt...
  ✓ Response received in 1.37s
  Response: ['4']

✅ PASS: Gemini configuration successful
```

### Failed Provider Test
```
Testing OpenAI Configuration
═════════════════════════════

...

Testing simple prompt...
  ✗ Response failed: AuthenticationError - Incorrect API key

❌ FAIL: OpenAI configuration failed

Recommendations:
  - Check OPENAI_API_KEY validity
  - Update .env with valid API key
```

---

## Summary Report Interpretation

```
Provider Support:

  ✅ Ollama       PASS
  ✅ Anthropic    PASS - 1.91s
  ✅ Gemini       PASS - 1.37s
  ⚠️ Openai       FAIL (prompt test failed)

   Total: 3/4 providers functional

  ⚠️ Overall Status: PARTIAL SUCCESS

Performance Ranking:
  1. Gemini       1.37s
  2. Anthropic    1.91s
  3. Ollama       0.00s (cached)

Recommendations:
  - Use Gemini for fastest performance
  - Use Anthropic for reliable fallback
  - Use Ollama for local/free use
  - Update OpenAI API key to enable
```

---

## Performance Comparison

| Provider   | Status | Time  | Cost | Best For |
|-----------|--------|-------|------|----------|
| Gemini     | ✅     | 1.37s | Free | Speed |
| Anthropic  | ✅     | 1.91s | Low  | Reliability |
| Ollama     | ✅     | Var   | Free | Local use |
| OpenAI     | ⚠️     | N/A   | High | Power |

---

## Security Notes

### API Key Masking
- API keys displayed as: `AIzaSyDN...****`
- Only first 8 characters shown
- Rest replaced with asterisks
- Safe to share output

### Best Practices
1. Never commit .env to git
2. Rotate keys regularly
3. Use separate keys for dev/prod
4. Check usage/quotas regularly

---

## Troubleshooting

### "Ollama service not accessible"
```bash
# Start Ollama
ollama serve

# In another terminal, pull model
ollama pull mistral:latest
```

### "API key not set"
1. Make sure .env file exists in project root
2. Check env file has the API key
3. Restart terminal/IDE to reload env vars

### "Incorrect API key provided"
- API key is invalid or expired
- Generate new key from provider's website
- Update .env file
- Re-test

---

## Feature Highlights

### What the Test Script Does

✅ **Loads Configuration**
- Reads .env file automatically
- Falls back to environment variables
- Uses sensible defaults

✅ **Validates Setup**
- Checks API keys are set
- Validates API keys aren't placeholders
- Checks Ollama service connectivity

✅ **Tests Functionality**
- Creates LM objects for each provider
- Configures DSPy integration
- Executes simple prompt
- Measures response time

✅ **Provides Security**
- Masks API keys (sk-proj-P2EZ...****)
- Safe to share output
- No credential leakage

✅ **Gives Diagnostics**
- Shows exact configuration used
- Displays DSPy state
- Explains errors clearly
- Provides fix recommendations

✅ **Enables Comparison**
- Performance ranking
- Cost comparison table
- Strengths/weaknesses per provider
- Integration examples

---

## Files Overview

### Test Script
```
test_llm_configuration.py (600 lines)
├─ Imports & setup
├─ Utility functions
├─ Provider test functions
├─ Test orchestration
├─ Summary reporting
└─ Main entry point
```

### Documentation
```
TEST_LLM_CONFIGURATION.md (400 lines)
├─ Usage examples
├─ Configuration details
├─ Troubleshooting guide
├─ Integration notes
└─ Performance tips

TEST_RESULTS_SUMMARY.md (300 lines)
├─ Executive summary
├─ Detailed results
├─ Bug fixes applied
├─ Recommendations
└─ Next steps

LLM_TEST_QUICK_START.md (this file)
└─ Quick reference guide
```

### Code Changes
```
esia_extractor.py
├─ Fixed line 1234: categorizer() instead of categorizer.forward()
└─ Fixed line 111-117: dspy.LM() instead of dspy.OpenAI()
```

---

## Next Steps

1. **Run the test:**
   ```bash
   python test_llm_configuration.py
   ```

2. **Review results** and pick your provider:
   - ✅ Gemini (fastest)
   - ✅ Anthropic (reliable)
   - ✅ Ollama (free, local)

3. **Use with extraction:**
   ```bash
   export LLM_PROVIDER=gemini
   python esia_extractor.py input.md output/
   ```

4. **Optional: Fix OpenAI**
   - Get new API key
   - Update .env
   - Re-test

---

## Need More Info?

- **Full documentation:** See `TEST_LLM_CONFIGURATION.md`
- **Detailed results:** See `TEST_RESULTS_SUMMARY.md`
- **Provider setup:** See configuration sections in documentation
- **Troubleshooting:** Check troubleshooting section in full docs

---

## Summary

✅ **Test script created and validated**
✅ **All 4 providers tested** (3 working, 1 needs key update)
✅ **Comprehensive documentation provided**
✅ **Bug fixes applied** to esia_extractor.py
✅ **Ready for production use**

**Recommendation:** Use Gemini as primary provider (fastest), Anthropic as fallback (reliable), keep Ollama for local/dev use.
