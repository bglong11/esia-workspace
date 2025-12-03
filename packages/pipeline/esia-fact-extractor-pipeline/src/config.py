import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load environment variables from workspace root .env.local
# Path calculation: config.py is in packages/pipeline/esia-fact-extractor-pipeline/src/
# So we need to go up 4 levels to reach workspace root:
# src/ -> esia-fact-extractor-pipeline/ -> pipeline/ -> packages/ -> workspace root
config_file_path = Path(__file__).resolve()  # Absolute path to config.py
workspace_root = config_file_path.parent.parent.parent.parent.parent  # Go up 5 levels

# Try .env.local first, then .env
env_local_path = workspace_root / ".env.local"
env_path = workspace_root / ".env"

if env_local_path.exists():
    load_dotenv(env_local_path, override=True)  # override=True to update existing vars
elif env_path.exists():
    load_dotenv(env_path, override=True)  # Use .env if .env.local doesn't exist
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
