import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load environment variables from project root .env.local
# Path calculation: config.py is in esia-workspace/packages/pipeline/esia-fact-extractor-pipeline/src/
# So we need to go up 5 levels to reach esia-ai project root:
# src/ -> esia-fact-extractor-pipeline/ -> pipeline/ -> packages/ -> esia-workspace/ -> esia-ai/
config_file_path = Path(__file__).resolve()  # Absolute path to config.py
project_root = config_file_path.parent.parent.parent.parent.parent.parent  # Go up 6 levels to esia-ai

# Try project root .env.local first (SINGLE SOURCE OF TRUTH)
env_local_path = project_root / ".env.local"

# Only load from file if env vars aren't already set by parent process
# This allows pipelineExecutor.js to pass env vars that take precedence
if env_local_path.exists():
    load_dotenv(env_local_path, override=False)  # override=False: don't override parent process env
else:
    load_dotenv()  # Fallback to default behavior

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Initialize the v1 Client
client = genai.Client(api_key=API_KEY)

# Initialize OpenRouter Client
# OpenRouter is compatible with OpenAI SDK, so we use that
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
openrouter_client = None
if OPENROUTER_API_KEY:
    try:
        from openai import OpenAI
        # OpenRouter uses OpenAI-compatible API
        openrouter_client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
    except ImportError:
        print("OpenAI package not installed. Install with `pip install openai`")

# Initialize xAI Client
# xAI (Grok) is also compatible with OpenAI SDK
XAI_API_KEY = os.getenv("XAI_API_KEY")
xai_client = None
if XAI_API_KEY:
    try:
        from openai import OpenAI
        # xAI uses OpenAI-compatible API
        xai_client = OpenAI(
            api_key=XAI_API_KEY,
            base_url="https://api.x.ai/v1"
        )
    except ImportError:
        print("OpenAI package not installed. Install with `pip install openai`")

# Initialize OpenAI Native Client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = None
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        # Native OpenAI API
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    except ImportError:
        print("OpenAI package not installed. Install with `pip install openai`")


# ============================================================================
# LLM Configuration from .env.local
# ============================================================================

# LLM Provider and Models (configured in .env.local)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")
XAI_MODEL = os.getenv("XAI_MODEL", "grok-3-mini")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))

# Constants
STORE_NAME_PREFIX = "esia_store_"

# API Rate Limiting Configuration
# For Tier 1 Gemini: Higher quota, but retry logic still needed for edge cases
# Phase 1 optimization: Reduced delays as Gemini API typically recovers in 3-5 seconds
MAX_RETRIES = 3  # Reduced from 4 since Tier 1 has better quotas
INITIAL_RETRY_DELAY = 5  # seconds (reduced from 30 - Gemini recovers quickly)
RETRY_BACKOFF_MULTIPLIER = 2.0  # 5s -> 10s -> 20s delays (total: 35s vs previous 142.5s)

# ============================================================================
# Step 2 Optimization Settings (Phase 1)
# ============================================================================

# Parallel Processing
EXTRACTION_MAX_WORKERS = int(os.getenv("EXTRACTION_MAX_WORKERS", "4"))
# Number of parallel workers for section processing
# Recommended: 4-8 depending on provider rate limits
# Higher values may trigger rate limiting

# Provider-Specific Rate Limits (requests per minute)
# These are used by the RateLimiter to pace API calls
RATE_LIMIT_GOOGLE = int(os.getenv("RATE_LIMIT_GOOGLE", "60"))      # Gemini Tier 1
RATE_LIMIT_OPENAI = int(os.getenv("RATE_LIMIT_OPENAI", "60"))      # OpenAI Tier 1
RATE_LIMIT_XAI = int(os.getenv("RATE_LIMIT_XAI", "60"))            # xAI Grok
RATE_LIMIT_OPENROUTER = int(os.getenv("RATE_LIMIT_OPENROUTER", "50"))  # OpenRouter (conservative)

# ============================================================================
# Step 2 Optimization Settings (Phase 2) - Batched Domain Extraction
# ============================================================================

# Batched Domain Extraction
EXTRACTION_BATCH_DOMAINS = os.getenv("EXTRACTION_BATCH_DOMAINS", "true").lower() == "true"
# Enable batching of multi-domain extractions into single API calls
# Reduces API calls by 30-40% for sections with multiple domains
# Recommended: true (disable only for debugging)

EXTRACTION_MAX_BATCH_SIZE = int(os.getenv("EXTRACTION_MAX_BATCH_SIZE", "3"))
# Maximum number of domains to batch in a single call
# Recommended: 2-4 (higher values may reduce quality or exceed token limits)
