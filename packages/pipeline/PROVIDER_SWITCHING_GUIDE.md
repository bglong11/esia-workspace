# LLM Provider Switching Guide

## Overview

The ESIA pipeline supports **4 LLM providers** with easy switching via `.env.local` configuration:

1. **Google Gemini** - Fast, generous free tier, good quality
2. **OpenAI Native** - Direct OpenAI API access (GPT-4o, GPT-4o-mini)
3. **OpenRouter** - Access to multiple models through one API
4. **xAI Grok** - Fast inference, 2M context window

## ✅ All Providers Tested and Working

**Test Results** (as of latest test):
- ✅ Google Gemini: **PASS**
- ✅ OpenAI Native: **PASS**
- ✅ OpenRouter: **PASS**
- ✅ xAI Grok: **PASS**

---

## How to Switch Providers

### Single Configuration Point

**File:** `.env.local` (workspace root)

Change **ONE LINE** to switch providers globally:

```bash
LLM_PROVIDER=xai  # Change this to: google, openai, openrouter, or xai
```

That's it! The entire pipeline (Steps 2 & 3) will use the selected provider.

---

## Provider Configuration

### 1. Google Gemini (Free Tier)

```bash
# .env.local
LLM_PROVIDER=google
GOOGLE_MODEL=gemini-2.5-flash
GOOGLE_API_KEY=your_google_api_key
```

**Get API Key:** https://aistudio.google.com

**Available Models:**
- `gemini-2.5-flash` - Latest, fastest (recommended)
- `gemini-2.0-flash` - Previous version
- `gemini-1.5-flash` - Stable

**Pros:**
- ✅ Generous free tier (1500 requests/day)
- ✅ Fast inference
- ✅ Good quality for ESIA extraction

**Cons:**
- ⚠️ Rate limits on free tier (429 errors if exceeded)

---

### 2. OpenAI Native (Direct API)

```bash
# .env.local
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_KEY=your_openai_api_key
```

**Get API Key:** https://platform.openai.com/api-keys

**Available Models:**
- `gpt-4o-mini` - Best cost/performance (recommended for ESIA)
- `gpt-4o` - Highest quality (expensive)
- `gpt-4-turbo` - Previous generation

**Pros:**
- ✅ Reliable, well-tested
- ✅ 128K context window (gpt-4o-mini)
- ✅ Excellent reasoning quality

**Cons:**
- 💰 Pay-per-use (no free tier)
- 💰 Can be expensive for large documents

---

### 3. OpenRouter (Multi-Model Access)

```bash
# .env.local
LLM_PROVIDER=openrouter
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_API_KEY=your_openrouter_api_key
```

**Get API Key:** https://openrouter.ai

**Available Models:**
- `openai/gpt-4o-mini` - OpenAI via OpenRouter (tested ✅)
- `google/gemini-2.5-flash` - Google via OpenRouter
- `anthropic/claude-3.5-sonnet` - Anthropic models (requires provider key)
- `meta-llama/llama-3.1-8b-instruct:free` - Free models (if available)

**Pros:**
- ✅ Access multiple providers through one API
- ✅ Competitive pricing
- ✅ Fallback options if one provider fails

**Cons:**
- ⚠️ Some models require additional provider API keys
- ⚠️ 404 errors for unavailable providers

---

### 4. xAI Grok (2M Context)

```bash
# .env.local
LLM_PROVIDER=xai
XAI_MODEL=grok-3-mini
XAI_API_KEY=your_xai_api_key
```

**Get API Key:** https://console.x.ai

**Available Models:**
- `grok-3-mini` - Fastest, cost-effective (recommended)
- `grok-3` - Good quality, 131K context
- `grok-4-fast` - Fast inference, 2M context
- `grok-4` - Highest quality, 256K context

**Pros:**
- ✅ Very fast inference
- ✅ Massive context window (up to 2M tokens)
- ✅ Good cost/performance

**Cons:**
- ⚠️ Newer provider (less battle-tested)

---

## Testing Your Configuration

Run the test script to verify all providers work:

```bash
cd packages/pipeline
venv312/Scripts/python.exe test_llm_providers.py
```

**Expected Output:**
```
============================================================
SUMMARY
============================================================
google          [PASS]
openai          [PASS]
openrouter      [PASS]
xai             [PASS]
```

---

## Switching Example

### Scenario: Google Gemini Rate Limited

**Problem:** Getting 429 errors from Google Gemini

**Solution 1 - Switch to xAI:**
```bash
# .env.local
LLM_PROVIDER=xai  # Changed from "google"
```

**Solution 2 - Switch to OpenAI:**
```bash
# .env.local
LLM_PROVIDER=openai  # Changed from "google"
```

**No code changes needed!** Just restart the pipeline.

---

## Cost Optimization

### For Development/Testing:
1. **Google Gemini** (free tier) - Best for testing
2. **xAI Grok-3-mini** - Fast, cheap for quick iterations

### For Production:
1. **OpenAI gpt-4o-mini** - Best quality/cost balance
2. **xAI Grok-4-fast** - Best for large documents (2M context)

### For Budget-Conscious:
1. **Google Gemini** (stay within free tier)
2. **OpenRouter free models** (if available)

---

## Architecture Details

### Single Source of Truth

All LLM calls go through `LLMManager` class:

```python
# Automatic provider selection based on .env.local
from src.esia_extractor import ESIAExtractor

extractor = ESIAExtractor()  # Uses LLM_PROVIDER from .env.local
```

### Components Using LLMManager

1. **Step 2: Fact Extraction** (`esia_extractor.py`)
   - Uses DSPy with LLMManager backend
   - Respects LLM_PROVIDER setting

2. **Step 3: Factsheet Generation** (`generator.py`)
   - Generates summary paragraphs
   - Respects LLM_PROVIDER setting

3. **Step 3: Page Distillation** (`page_distiller.py`)
   - Distills verbose facts per page
   - Respects LLM_PROVIDER setting

---

## Troubleshooting

### Provider Not Working

**Symptom:** Test fails for a provider

**Checks:**
1. ✅ API key set in `.env.local`
2. ✅ API key valid (not expired)
3. ✅ Model name correct for provider
4. ✅ Network connectivity

**Example Error:**
```
[FAILED]: ValueError
Error: OpenAI client not initialized. Check OPENAI_API_KEY in .env
```

**Solution:** Verify API key exists in `.env.local`:
```bash
OPENAI_API_KEY=sk-proj-...  # Must be set
```

---

### Rate Limit Errors

**Symptom:** 429 errors or "RESOURCE_EXHAUSTED"

**Solution:**
1. Switch to different provider in `.env.local`
2. Wait for rate limit to reset (Google: 1 minute)
3. Reduce batch size if processing large documents

---

### Context Length Exceeded

**Symptom:** "maximum context length is 16385 tokens"

**Solution:**
- ✅ Use models with larger context:
  - `gpt-4o-mini`: 128K tokens
  - `grok-3-mini`: 131K tokens
  - `grok-4-fast`: 2M tokens

---

## API Key Security

**IMPORTANT:** Never commit `.env.local` to version control!

**Verify `.gitignore`:**
```bash
# Should contain:
.env
.env.local
.env.*.local
```

**Check if ignored:**
```bash
git status  # Should NOT show .env.local
```

---

## Quick Reference

| Provider | API Key Variable | Model Variable | Free Tier? |
|----------|-----------------|----------------|------------|
| Google Gemini | `GOOGLE_API_KEY` | `GOOGLE_MODEL` | ✅ Yes (1500 req/day) |
| OpenAI Native | `OPENAI_API_KEY` | `OPENAI_MODEL` | ❌ Pay-per-use |
| OpenRouter | `OPENROUTER_API_KEY` | `OPENROUTER_MODEL` | ⚠️ Depends on model |
| xAI Grok | `XAI_API_KEY` | `XAI_MODEL` | ❌ Pay-per-use |

---

## Next Steps

1. ✅ **Test all providers** - Run `test_llm_providers.py`
2. ✅ **Choose provider** - Update `LLM_PROVIDER` in `.env.local`
3. ✅ **Run pipeline** - Test with sample PDF
4. ✅ **Monitor costs** - Track API usage

**For issues, see:**
- `packages/pipeline/claude.md` - Pipeline guide
- `packages/pipeline/REQUIREMENTS_GUIDE.md` - Installation
- `CLAUDE.md` - Workspace overview

---

**Last Updated:** December 3, 2025
**Status:** All 4 providers tested and working ✅
