# CONFIDENCE_THRESHOLD Environment Configuration

## Quick Start

Edit `packages/pipeline/.env` to change the confidence threshold:

```bash
# File: packages/pipeline/.env
CONFIDENCE_THRESHOLD=0.5
```

Then run your pipeline - the new threshold will be applied automatically.

## How It Works

1. **File Location:** `packages/pipeline/.env`
2. **Setting:** `CONFIDENCE_THRESHOLD=0.5` (default)
3. **Automatic Loading:** Python scripts automatically load this value when they start
4. **Priority:** Environment variable → .env file → code default (0.5)

## Available Thresholds

| Value | Use Case | Speed | Quality |
|-------|----------|-------|---------|
| 0.0 | Disabled (all domains) | Baseline | High |
| 0.3 | Conservative | 11-23% faster | High |
| 0.4 | Moderate-Conservative | 29-40% faster | High |
| **0.5** | **Balanced (DEFAULT)** | **40-50% faster** | **Good** |
| 0.6 | Moderate-Aggressive | 48-60% faster | Medium |
| 0.7 | Aggressive | 57-67% faster | Medium |

## How to Change It

### Option 1: Edit .env file (Recommended)
```bash
# Edit: packages/pipeline/.env
CONFIDENCE_THRESHOLD=0.7
```

### Option 2: Set environment variable (One-time)

**Windows PowerShell:**
```powershell
$env:CONFIDENCE_THRESHOLD = "0.7"
python step3_extraction_with_archetypes.py --chunks chunks.jsonl
```

**Windows Command Prompt:**
```cmd
set CONFIDENCE_THRESHOLD=0.7
python step3_extraction_with_archetypes.py --chunks chunks.jsonl
```

**Linux/Mac:**
```bash
export CONFIDENCE_THRESHOLD=0.7
python step3_extraction_with_archetypes.py --chunks chunks.jsonl
```

## Example Workflow

1. **Edit .env:**
   ```
   CONFIDENCE_THRESHOLD=0.6
   ```

2. **Run pipeline (any method):**
   ```bash
   # Via UI: Upload PDF at http://localhost:3000
   # Via CLI: python run-esia-pipeline.py document.pdf --steps 1,2,3
   ```

3. **Pipeline automatically uses the new threshold**

## Testing Different Thresholds

Run multiple tests with different thresholds:

```bash
# Test with 0.5 (balanced)
$env:CONFIDENCE_THRESHOLD = "0.5"
python step3_extraction_with_archetypes.py --chunks chunks.jsonl -o facts_0.5.json

# Test with 0.7 (aggressive)
$env:CONFIDENCE_THRESHOLD = "0.7"
python step3_extraction_with_archetypes.py --chunks chunks.jsonl -o facts_0.7.json

# Compare results
compare_facts.py facts_0.5.json facts_0.7.json
```

## Documentation

For detailed information about how confidence filtering works, see:
- [packages/pipeline/CONFIDENCE_THRESHOLD.md](packages/pipeline/CONFIDENCE_THRESHOLD.md)

## Current Configuration

**File:** `packages/pipeline/.env`
**Current Setting:** `CONFIDENCE_THRESHOLD=0.5`
**Auto-Loaded By:** All Python pipeline scripts that use `from dotenv import load_dotenv`

