# LLM Configuration Test Script

Comprehensive test script for validating all LLM provider configurations (Ollama, OpenAI, Anthropic, Gemini) with detailed debugging output.

## Overview

The `test_llm_configuration.py` script provides:

- **Multi-provider testing**: Tests all 4 supported LLM providers
- **Detailed diagnostics**: Shows configuration, environment, and DSPy state
- **Security**: Masks API keys for safe output display
- **Error handling**: Graceful detection and explanation of errors
- **Performance metrics**: Response time comparison across providers
- **Actionable recommendations**: Specific troubleshooting steps

## Test Results Summary

### Current Status: 3/4 Providers Functional

```
✅ Ollama       PASS       (Local, fast)
✅ Anthropic    PASS - 1.91s (Claude models)
✅ Gemini       PASS - 1.37s (Google AI)
⚠️  OpenAI       FAIL       (Invalid API key)
```

## Usage

### Run All Providers
```bash
python test_llm_configuration.py
```

### Run Specific Provider
```bash
python test_llm_configuration.py --provider ollama
python test_llm_configuration.py --provider anthropic
python test_llm_configuration.py --provider gemini
python test_llm_configuration.py --provider openai
```

### Verbose Output
```bash
python test_llm_configuration.py --verbose
```

Shows detailed error traces for debugging.

## Test Output Explanation

### Per-Provider Test Output

Each provider shows:

```
Testing {Provider} Configuration
═════════════════════════════════

Environment:
  Model: {model_name}
  API Key: {masked_key}
  Temperature: {value}
  Max Tokens: {value}

Validating API Key...
  ✓ API key present and not placeholder

Creating LM object...
  ✓ LM object created

Configuring DSPy...
  ✓ DSPy configured

Testing simple prompt...
  ✓ Response received in {time}s
  Response: {output}

✅ PASS: {Provider} configuration successful
```

### Summary Report

Shows overall results with:
- Pass/fail status for each provider (✅/⚠️/❌)
- Response times for performance comparison
- Actionable recommendations
- System readiness assessment

## Test Cases Covered

### 1. Ollama (Local)
- ✓ Service connectivity check
- ✓ Model availability verification
- ✓ LM object creation
- ✓ DSPy configuration
- ✓ Simple prompt execution

### 2. OpenAI (Cloud)
- ✓ API key validation (not placeholder)
- ✓ dspy.LM initialization
- ✓ DSPy configuration
- ✓ Authentication and prompt execution

### 3. Anthropic/Claude (Cloud)
- ✓ API key validation
- ✓ dspy.LM with anthropic provider
- ✓ DSPy configuration
- ✓ Simple prompt execution

### 4. Google Gemini (Cloud)
- ✓ API key validation
- ✓ dspy.LM with gemini provider
- ✓ DSPy configuration
- ✓ Simple prompt execution

## Configuration Details

### Ollama
```
Environment Variables:
  OLLAMA_MODEL=mistral:latest
  OLLAMA_BASE_URL=http://localhost:11434
  OLLAMA_TEMPERATURE=0.1
  OLLAMA_MAX_TOKENS=2048

Requirements:
  - Ollama service running locally
  - Model pulled (ollama pull mistral:latest)
  - Port 11434 accessible
```

### OpenAI
```
Environment Variables:
  OPENAI_API_KEY=sk-proj-...
  OPENAI_MODEL=gpt-4o-mini
  OPENAI_TEMPERATURE=0.1
  OPENAI_MAX_TOKENS=2048

Requirements:
  - Valid OpenAI API key
  - API key must not be placeholder
  - Network access to api.openai.com
```

### Anthropic
```
Environment Variables:
  ANTHROPIC_API_KEY=sk-ant-...
  ANTHROPIC_MODEL=claude-haiku-4-5-20251001
  ANTHROPIC_TEMPERATURE=0.1
  ANTHROPIC_MAX_TOKENS=2048

Requirements:
  - Valid Anthropic API key
  - API key must not be placeholder
  - Network access to api.anthropic.com
```

### Gemini
```
Environment Variables:
  GEMINI_API_KEY=AIzaSy...
  GEMINI_MODEL=gemini-2.5-flash
  GEMINI_TEMPERATURE=0.1
  GEMINI_MAX_TOKENS=2048

Requirements:
  - Valid Google Gemini API key
  - API key must not be placeholder
  - Network access to generativelanguage.googleapis.com
```

## Troubleshooting

### Ollama Failures

**Error: "Ollama service not accessible"**
```bash
# Start Ollama service
ollama serve

# In another terminal, pull the model
ollama pull mistral:latest
```

**Error: "Model 'mistral:latest' not found"**
```bash
# Pull the configured model
ollama pull mistral:latest

# Or configure a different model in .env
# OLLAMA_MODEL=qwen2.5:7b-instruct
ollama pull qwen2.5:7b-instruct
```

### OpenAI Failures

**Error: "Incorrect API key provided"**
- Check API key validity at https://platform.openai.com/api-keys
- Ensure key is not revoked or expired
- Copy exact key (no extra spaces or characters)

**Error: "API quota exceeded"**
- Check usage limits at https://platform.openai.com/account/billing/overview
- Upgrade account if quota exceeded

### Anthropic Failures

**Error: "ANTHROPIC_API_KEY not set"**
- Add to .env: `ANTHROPIC_API_KEY=your_key_here`
- Get key from https://console.anthropic.com/

**Error: "Invalid API key"**
- Verify key is valid at https://console.anthropic.com/account/keys
- Check for typos or extra whitespace

### Gemini Failures

**Error: "GEMINI_API_KEY not set"**
- Add to .env: `GEMINI_API_KEY=your_key_here`
- Get key from https://ai.google.dev/

**Error: "Invalid API key"**
- Verify key is valid at https://ai.google.dev/
- Check for typos or extra whitespace

## Performance Comparison

Based on test results:

| Provider   | Status | Response Time | Strengths |
|-----------|--------|---------------|-----------|
| Gemini     | ✅ PASS | 1.37s | Fastest, free tier available |
| Anthropic  | ✅ PASS | 1.91s | Reliable, good performance |
| Ollama     | ✅ PASS | Variable | Local, free, no API key needed |
| OpenAI     | ⚠️ FAIL | 4.89s | Would be good but key is invalid |

## Security Notes

### API Key Masking

API keys are displayed as: `sk-proj-P2EZ...****`
- Shows first 8 characters only
- Rest replaced with asterisks
- Safe to share output without exposing credentials

### Environment Variables

- All API keys stored in .env file (git ignored)
- Never commit .env to version control
- Use different keys for development/production
- Rotate keys regularly for security

## Integration with ESIA Extractor

The test script validates that `configure_llm()` function in `esia_extractor.py` works correctly for all providers.

### Using with Extraction

After confirming test passes, use with extraction:

```bash
# Using Anthropic (fast, reliable)
export LLM_PROVIDER=anthropic
python esia_extractor.py input.md output/

# Using Gemini (fastest)
export LLM_PROVIDER=gemini
python esia_extractor.py input.md output/

# Using Ollama (free, local)
export LLM_PROVIDER=ollama
python esia_extractor.py input.md output/

# Using OpenAI (needs valid key)
export LLM_PROVIDER=openai
python esia_extractor.py input.md output/
```

## Development Notes

### Script Structure

```
test_llm_configuration.py
├─ Imports & setup
├─ Utility functions
│  ├─ mask_api_key()
│  ├─ print_section()
│  ├─ test_simple_prompt()
│  └─ get_env_value()
├─ Provider test functions
│  ├─ test_ollama_config()
│  ├─ test_openai_config()
│  ├─ test_anthropic_config()
│  └─ test_gemini_config()
├─ Test orchestration
│  ├─ run_all_provider_tests()
│  └─ print_summary_report()
└─ Main entry point
```

### Error Handling

- **AttributeError** for dspy.OllamaLocal (older DSPy API)
  → Falls back to dspy.LM with ollama provider
- **ValueError** for missing/invalid API keys
  → Shows clear message and recommendations
- **AuthenticationError** for cloud providers
  → Indicates API key validity issue
- **Connection errors** for Ollama
  → Indicates service not running or unreachable

### Testing Approach

1. **Environment validation**: Check if required env vars exist
2. **Configuration creation**: Build LM object with validated settings
3. **DSPy integration**: Verify dspy.configure() works
4. **Functional test**: Execute simple prompt to ensure LLM is responsive

## Recommendations

### For Production Use

**Recommended Provider Rankings:**

1. **Gemini** (Fastest, free tier available)
2. **Anthropic** (Reliable, good performance)
3. **Ollama** (No API key needed, runs locally)
4. **OpenAI** (Powerful but higher cost, key currently invalid)

### For Cost Optimization

```
Free: Ollama (local) + Gemini (limited free tier)
Low Cost: Anthropic Claude Haiku
Medium Cost: OpenAI GPT-4o-mini
Premium: OpenAI GPT-4 or Anthropic Claude Opus
```

### For Speed Optimization

```
Fastest: Gemini (1.37s)
         Anthropic (1.91s)
Slowest: OpenAI (4.89s when working)
         Ollama (varies by model, local latency)
```

## Known Issues

1. **OpenAI API Key Invalid**: The configured API key in .env appears to be expired or invalid
   - Solution: Update OPENAI_API_KEY with valid key from https://platform.openai.com/api-keys

2. **DSPy API Compatibility**: dspy.OllamaLocal removed in newer versions
   - Solution: Script auto-detects and falls back to dspy.LM

## Future Improvements

- [ ] Add timeout handling for slow providers
- [ ] Test with multiple models per provider
- [ ] Measure token usage and costs
- [ ] Add streaming response tests
- [ ] Test JSON output validation
- [ ] Add benchmark mode for performance testing

## License

Part of ESIA Fact Extractor project.
