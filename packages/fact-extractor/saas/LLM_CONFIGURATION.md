# LLM Configuration Guide

How to configure the LLM (Ollama) settings for ESIA Fact Extractor.

---

## 📍 Configuration File Location

Create a `.env` file in `saas/backend/`:

```bash
cd saas/backend
copy ..\. env.example .env    # Windows
# or
cp ../.env.example .env        # Linux/Mac
```

---

## ⚙️ Available Settings

### 1. **OLLAMA_MODEL** - Which LLM to Use

```bash
# Default (recommended):
OLLAMA_MODEL=qwen2.5:7b-instruct

# Other options (must be installed in Ollama):
OLLAMA_MODEL=llama3.2
OLLAMA_MODEL=mistral
OLLAMA_MODEL=gemma2
OLLAMA_MODEL=llama3.1:8b
```

**Check available models:**
```powershell
ollama list
```

**Install a new model:**
```powershell
ollama pull llama3.2
```

---

### 2. **OLLAMA_BASE_URL** - Ollama Server Location

```bash
# Default (local):
OLLAMA_BASE_URL=http://localhost:11434

# Different port:
OLLAMA_BASE_URL=http://localhost:11435

# Different machine:
OLLAMA_BASE_URL=http://192.168.1.100:11434

# Remote server:
OLLAMA_BASE_URL=http://ollama.yourcompany.com:11434
```

---

### 3. **LLM_TEMPERATURE** - Creativity vs Consistency

Controls randomness in responses:

```bash
# Very consistent (recommended for fact extraction):
LLM_TEMPERATURE=0.0
LLM_TEMPERATURE=0.1
LLM_TEMPERATURE=0.2   # Default

# Balanced:
LLM_TEMPERATURE=0.5

# More creative (may produce inconsistent JSON):
LLM_TEMPERATURE=0.7
LLM_TEMPERATURE=1.0
```

**For fact extraction, keep it low (0.1-0.3)** to ensure consistent JSON output.

---

### 4. **LLM_MAX_TOKENS** - Response Length

Maximum tokens the LLM can generate:

```bash
# Short responses (faster):
LLM_MAX_TOKENS=1024

# Default (balanced):
LLM_MAX_TOKENS=2048

# Long responses (slower):
LLM_MAX_TOKENS=4096
LLM_MAX_TOKENS=8192
```

**Note:** Higher values = slower processing and more memory usage.

---

## 🔧 How to Use

### Method 1: Environment File (Recommended)

**Create `saas/backend/.env`:**
```bash
OLLAMA_MODEL=qwen2.5:7b-instruct
OLLAMA_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=2048
```

Then just run normally:
```powershell
python test_full_pipeline.py --pdf test.pdf
```

---

### Method 2: Command Line (Temporary)

**Windows:**
```powershell
# Set for current session
$env:OLLAMA_MODEL="llama3.2"
$env:LLM_TEMPERATURE="0.1"

# Then run
python test_full_pipeline.py --pdf test.pdf
```

**Linux/Mac:**
```bash
export OLLAMA_MODEL="llama3.2"
export LLM_TEMPERATURE="0.1"

python test_full_pipeline.py --pdf test.pdf
```

---

### Method 3: Inline (One Command)

**Windows:**
```powershell
$env:OLLAMA_MODEL="llama3.2"; python test_full_pipeline.py --pdf test.pdf
```

**Linux/Mac:**
```bash
OLLAMA_MODEL=llama3.2 python test_full_pipeline.py --pdf test.pdf
```

---

## 🧪 Testing Different Configurations

### Test 1: Try Different Model

```powershell
# Use llama3.2 instead of qwen2.5
$env:OLLAMA_MODEL="llama3.2"
python test_full_pipeline.py --pdf test.pdf
```

### Test 2: Adjust Temperature

```powershell
# Lower temperature for more consistent JSON
$env:LLM_TEMPERATURE="0.1"
python test_full_pipeline.py --pdf test.pdf
```

### Test 3: Increase Max Tokens

```powershell
# Allow longer responses
$env:LLM_MAX_TOKENS="4096"
python test_full_pipeline.py --pdf test.pdf
```

---

## 🎯 Recommended Settings

### For JSON Fact Extraction (Production)

```bash
OLLAMA_MODEL=qwen2.5:7b-instruct
OLLAMA_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.1              # Very consistent
LLM_MAX_TOKENS=2048              # Sufficient for facts
```

### For Testing/Development

```bash
OLLAMA_MODEL=qwen2.5:7b-instruct
OLLAMA_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.2              # Slightly more flexible
LLM_MAX_TOKENS=2048
```

### For Creative Extraction (Experimental)

```bash
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.5              # More creative
LLM_MAX_TOKENS=4096              # Longer responses
```

---

## 🐛 Troubleshooting

### Issue: Empty JSON Responses

**Cause:** Temperature too high or model not responding

**Fix:**
```bash
LLM_TEMPERATURE=0.1    # Lower temperature
LLM_MAX_TOKENS=1024    # Shorter responses
```

### Issue: Slow Processing

**Cause:** Max tokens too high or large model

**Fix:**
```bash
LLM_MAX_TOKENS=1024           # Reduce max tokens
OLLAMA_MODEL=qwen2.5:3b       # Use smaller model
```

### Issue: Connection Refused

**Cause:** Wrong Ollama URL or Ollama not running

**Fix:**
```bash
# Check Ollama is running
ollama serve

# Verify URL
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 📊 Comparing Models

Test with different models to find the best for your use case:

```powershell
# Test Qwen2.5 (default)
$env:OLLAMA_MODEL="qwen2.5:7b-instruct"
python test_full_pipeline.py --pdf test.pdf

# Test Llama3.2
$env:OLLAMA_MODEL="llama3.2"
python test_full_pipeline.py --pdf test.pdf

# Test Mistral
$env:OLLAMA_MODEL="mistral"
python test_full_pipeline.py --pdf test.pdf
```

Compare:
- Number of facts extracted
- JSON parsing errors
- Processing time
- Accuracy

---

## 🔄 Switching Models Mid-Session

You can change models without restarting:

```powershell
# Run with qwen2.5
$env:OLLAMA_MODEL="qwen2.5:7b-instruct"
python test_full_pipeline.py --pdf doc1.pdf

# Switch to llama3.2
$env:OLLAMA_MODEL="llama3.2"
python test_full_pipeline.py --pdf doc2.pdf
```

Each run will use the current environment variable.

---

## ✅ Verify Configuration

Create a test script to see current settings:

```powershell
python -c "
import os
print(f'Model: {os.getenv(\"OLLAMA_MODEL\", \"qwen2.5:7b-instruct\")}')
print(f'URL: {os.getenv(\"OLLAMA_BASE_URL\", \"http://localhost:11434\")}')
print(f'Temp: {os.getenv(\"LLM_TEMPERATURE\", \"0.2\")}')
print(f'Tokens: {os.getenv(\"LLM_MAX_TOKENS\", \"2048\")}')
"
```

---

## 📝 Example .env File

```bash
# Database
DATABASE_URL=sqlite:///./esia_saas.db

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b-instruct

# LLM Parameters
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=2048

# Server
HOST=0.0.0.0
PORT=8000

# Processing
CHUNK_SIZE=4000
CONFLICT_TOLERANCE=0.02
```

---

**Need help?** The defaults are well-tuned for fact extraction. Only change if you're experiencing issues!
