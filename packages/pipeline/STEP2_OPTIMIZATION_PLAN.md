# Step 2 Extraction Optimization Plan

## Executive Summary

Step 2 (Fact Extraction) is the slowest part of the ESIA pipeline, often taking 2-4 hours for large documents. This plan outlines optimizations to reduce processing time by **50-70%** through parallel processing, smarter batching, and architectural improvements.

**Key Finding:** GPU acceleration provides minimal benefit for Step 2 because:
- LLM API calls are cloud-based (network latency dominates, not computation)
- The real bottleneck is **sequential processing** of sections/domains

---

## Current Architecture Analysis

### Processing Flow (Sequential)
```
┌─────────────────────────────────────────────────────────────────┐
│  CURRENT STEP 2 FLOW (SEQUENTIAL)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  chunks.jsonl (500 chunks)                                      │
│       ↓                                                         │
│  Group by Section (50 sections)                                 │
│       ↓                                                         │
│  FOR EACH section:           ← SEQUENTIAL (major bottleneck)    │
│       ├── Map to domains (1-3 domains)                          │
│       └── FOR EACH domain:   ← SEQUENTIAL (nested bottleneck)   │
│              └── LLM API call (1-3 seconds per call)            │
│                                                                 │
│  Total: 50 sections × 2 domains avg × 2 sec = ~200 seconds      │
│  Reality: ~30-60 minutes due to rate limiting, retries          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Time Breakdown (Typical 200-page ESIA Document)

| Component | Current Time | % of Total | Parallelizable? |
|-----------|-------------|------------|-----------------|
| Load chunks | 1-2 sec | <1% | No (I/O bound) |
| Group by section | <1 sec | <1% | No (CPU bound) |
| Section → Domain mapping | 5-10 sec | 1% | Yes |
| **LLM API calls** | **25-50 min** | **95%** | **Yes** |
| Results aggregation | 1-2 sec | <1% | No |
| Save JSON output | 1 sec | <1% | No |

**Key Insight:** 95% of time is spent waiting for LLM API responses, processed sequentially.

---

## Bottleneck Analysis

### 1. Sequential Section Processing
**File:** [step3_extraction_with_archetypes.py](esia-fact-extractor-pipeline/step3_extraction_with_archetypes.py#L103-L189)

```python
# CURRENT: Sequential loop (lines 103-189)
for section_name, section_chunks in sorted(sections.items()):
    # ... process one section at a time
    for match in domain_matches:
        facts = extractor.extract(combined_text, domain)  # BLOCKING CALL
```

**Problem:** Each LLM call blocks the entire process. With 50 sections × 2 domains = 100 API calls executed one at a time.

### 2. No Async/Await Pattern
**File:** [llm_manager.py](esia-fact-extractor-pipeline/src/llm_manager.py)

The `LLMManager` uses synchronous HTTP calls. All providers (Google, OpenAI, xAI) support async APIs but we're not using them.

### 3. Rate Limiting Strategy
**File:** [config.py](esia-fact-extractor-pipeline/src/config.py#L93-L95)

```python
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 5  # seconds
RETRY_BACKOFF_MULTIPLIER = 2.0
```

Current retry is per-call. No request pacing or token bucket rate limiting.

---

## Optimization Strategies

### Strategy 1: Concurrent Section Processing (High Impact)

**Approach:** Use `concurrent.futures.ThreadPoolExecutor` to process multiple sections in parallel.

**Implementation:**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_facts_parallel(chunks, max_workers=4):
    sections = group_by_section(chunks)
    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all section extractions
        futures = {
            executor.submit(process_section, section_name, section_chunks): section_name
            for section_name, section_chunks in sections.items()
        }

        # Collect results as they complete
        for future in as_completed(futures):
            section_name = futures[future]
            results[section_name] = future.result()

    return results
```

**Expected Improvement:**
- With 4 workers: ~75% reduction (4x parallel)
- With 8 workers: ~85% reduction (limited by rate limits)

**Risk:** Rate limiting from providers. Mitigation: Implement token bucket rate limiter.

---

### Strategy 2: Async LLM Calls (High Impact)

**Approach:** Convert `LLMManager` to async using `httpx` or provider async SDKs.

**Implementation:**
```python
import asyncio
from openai import AsyncOpenAI

class AsyncLLMManager:
    def __init__(self):
        self.async_openai = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.async_xai = AsyncOpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

    async def generate_content_async(self, prompt, model, provider):
        if provider == "openai":
            response = await self.async_openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        # ... similar for other providers
```

**Expected Improvement:**
- 50-70% faster with proper concurrency management
- Can process 5-10 requests concurrently without rate limit issues

---

### Strategy 3: Batch Domain Processing (Medium Impact)

**Approach:** For sections mapped to multiple domains, batch the extractions into a single LLM call.

**Current:** 3 separate API calls for 3 domains
```
Call 1: Extract "project_description" facts
Call 2: Extract "baseline_conditions" facts
Call 3: Extract "ps1" facts
```

**Optimized:** 1 combined call
```python
prompt = f"""
Extract facts from this text for the following domains:
1. Project Description
2. Baseline Conditions
3. PS1 Assessment

Context: {combined_text}

Return facts for each domain separately.
"""
```

**Expected Improvement:**
- 40-60% fewer API calls for multi-domain sections
- Slightly larger token usage per call (cost trade-off)

---

### Strategy 4: Smart Caching (Medium Impact)

**Approach:** Cache extraction results by content hash to avoid re-processing identical or similar content.

**Implementation:**
```python
import hashlib
import json
from pathlib import Path

class ExtractionCache:
    def __init__(self, cache_dir="./data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get_cache_key(self, text: str, domain: str) -> str:
        content = f"{domain}:{text[:5000]}"  # First 5000 chars + domain
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, text: str, domain: str):
        key = self.get_cache_key(text, domain)
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())
        return None

    def set(self, text: str, domain: str, facts: dict):
        key = self.get_cache_key(text, domain)
        cache_file = self.cache_dir / f"{key}.json"
        cache_file.write_text(json.dumps(facts))
```

**Expected Improvement:**
- Near-instant for repeated content (common in ESIA annexes)
- 10-20% overall speedup due to duplicate content

---

### Strategy 5: Intelligent Chunking Pre-filter (Medium Impact)

**Approach:** Use lightweight embedding similarity to filter chunks before expensive LLM extraction.

**Current Flow:**
```
All 500 chunks → Domain Mapping → LLM Extraction (expensive)
```

**Optimized Flow:**
```
All 500 chunks → Fast Embedding → Similarity Filter → Top 200 chunks → LLM Extraction
```

**Implementation:**
```python
from sentence_transformers import SentenceTransformer

class ChunkFilter:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, 22MB
        self.domain_embeddings = self._precompute_domain_embeddings()

    def filter_relevant_chunks(self, chunks, domain, top_k=50):
        chunk_texts = [c['text'] for c in chunks]
        chunk_embeddings = self.model.encode(chunk_texts)

        # Compute similarity to domain
        domain_emb = self.domain_embeddings[domain]
        similarities = chunk_embeddings @ domain_emb.T

        # Return top_k most relevant chunks
        top_indices = similarities.argsort()[-top_k:]
        return [chunks[i] for i in top_indices]
```

**Expected Improvement:**
- 30-50% fewer chunks to process
- Potential quality improvement (more focused extraction)

**Note:** This adds ~20ms per chunk but saves ~2s of LLM time per filtered chunk.

---

### Strategy 6: Provider-Specific Rate Limit Management

**Approach:** Implement token bucket rate limiting tailored to each provider's limits.

**Provider Rate Limits:**
| Provider | Requests/min | Tokens/min | Recommended Concurrency |
|----------|-------------|------------|------------------------|
| Google Gemini (Tier 1) | 60 | 1M | 8-10 |
| OpenAI (Tier 1) | 60 | 150K | 4-6 |
| xAI Grok | 60 | 200K | 6-8 |
| OpenRouter | Varies | Varies | 4-6 |

**Implementation:**
```python
import time
from threading import Lock

class RateLimiter:
    def __init__(self, requests_per_minute=60):
        self.requests_per_minute = requests_per_minute
        self.interval = 60.0 / requests_per_minute
        self.last_request = 0
        self.lock = Lock()

    def wait(self):
        with self.lock:
            elapsed = time.time() - self.last_request
            if elapsed < self.interval:
                time.sleep(self.interval - elapsed)
            self.last_request = time.time()
```

---

## GPU Acceleration Analysis

### What CAN Use GPU

| Component | GPU Benefit | Notes |
|-----------|-------------|-------|
| Step 1 Chunking (Docling) | ✅ High | Already implemented via `--use-cuda` |
| Embedding-based filtering | ✅ Medium | If implemented (Strategy 5) |
| LLM API calls | ❌ None | Cloud-based, GPU is server-side |
| Domain classification | ⚠️ Minimal | Keyword matching is faster on CPU |

### Recommendation

**GPU is NOT the solution for Step 2 optimization.** The bottleneck is network I/O and sequential processing, not local computation.

**Where GPU helps:**
- Step 1: Already using CUDA for PDF parsing
- Optional: Local embeddings for chunk filtering (Strategy 5)

**Where GPU doesn't help:**
- LLM extraction calls (100% of Step 2 time)
- These happen on Google/OpenAI/xAI servers

---

## Implementation Priority

### Phase 1: Quick Wins (1-2 hours implementation)

1. **Concurrent Section Processing** (Strategy 1)
   - Add `ThreadPoolExecutor` with 4 workers
   - Expected: 60-70% speedup
   - Risk: Low (no architectural changes)

2. **Smarter Rate Limiting** (Strategy 6)
   - Add token bucket rate limiter
   - Prevents 429 errors, enables higher concurrency

### Phase 2: Medium Effort (4-6 hours)

3. **Batch Domain Processing** (Strategy 3)
   - Combine multi-domain extractions
   - Expected: 30-40% fewer API calls

4. **Extraction Caching** (Strategy 4)
   - Cache by content hash
   - Helps with repeated runs and similar content

### Phase 3: Higher Effort (1-2 days)

5. **Async LLM Manager** (Strategy 2)
   - Convert to async/await pattern
   - Maximum concurrency potential

6. **Embedding-based Filtering** (Strategy 5)
   - Requires sentence-transformers dependency
   - Best for very large documents (500+ pages)

---

## Configuration Options

Add to `.env.local`:

```bash
# ============================================================================
# Step 2 Optimization Settings
# ============================================================================

# Parallel Processing
EXTRACTION_MAX_WORKERS=4          # Number of parallel section processors
EXTRACTION_RATE_LIMIT=50          # Requests per minute (provider-dependent)

# Caching
EXTRACTION_CACHE_ENABLED=true     # Enable extraction result caching
EXTRACTION_CACHE_DIR=./data/cache # Cache directory

# Batching
EXTRACTION_BATCH_DOMAINS=true     # Combine multi-domain extractions
EXTRACTION_MAX_BATCH_SIZE=3       # Max domains per batch call

# Filtering
EXTRACTION_USE_EMBEDDINGS=false   # Use embedding-based chunk filtering
EXTRACTION_RELEVANCE_THRESHOLD=0.5 # Minimum similarity for processing
```

---

## Expected Results

### Before Optimization
- 200-page document: **45-60 minutes**
- 500-page document: **2-4 hours**

### After Phase 1 (Concurrent + Rate Limiting)
- 200-page document: **15-20 minutes** (60-70% faster)
- 500-page document: **40-60 minutes** (70% faster)

### After All Phases
- 200-page document: **8-12 minutes** (80% faster)
- 500-page document: **25-40 minutes** (80% faster)

---

## Files to Modify

| File | Changes | Priority |
|------|---------|----------|
| [step3_extraction_with_archetypes.py](esia-fact-extractor-pipeline/step3_extraction_with_archetypes.py) | Add ThreadPoolExecutor | High |
| [llm_manager.py](esia-fact-extractor-pipeline/src/llm_manager.py) | Add rate limiter, async option | High |
| [config.py](esia-fact-extractor-pipeline/src/config.py) | Add optimization settings | Medium |
| [esia_extractor.py](esia-fact-extractor-pipeline/src/esia_extractor.py) | Add caching, batch extraction | Medium |
| New: `cache_manager.py` | Extraction caching | Medium |
| New: `rate_limiter.py` | Token bucket rate limiting | High |

---

## Summary

| Strategy | Effort | Impact | GPU Needed |
|----------|--------|--------|------------|
| 1. Concurrent sections | Low | High (60-70%) | No |
| 2. Async LLM | Medium | High (50-70%) | No |
| 3. Batch domains | Medium | Medium (30-40%) | No |
| 4. Caching | Low | Medium (10-20%) | No |
| 5. Embedding filter | High | Medium (30-50%) | Optional |
| 6. Rate limiting | Low | Enables higher concurrency | No |

**Bottom Line:** Parallel processing (not GPU) is the key to Step 2 optimization. Implementing concurrent section processing with proper rate limiting can achieve 60-70% speedup with minimal code changes.

---

## Next Steps

1. **Approve this plan** - Confirm optimization priorities
2. **Implement Phase 1** - Add concurrent processing + rate limiting
3. **Test with sample document** - Measure actual improvement
4. **Iterate on Phase 2/3** - Based on results and needs

---

**Last Updated:** December 3, 2025
**Author:** Claude Code Analysis
**Status:** Plan Ready for Implementation
