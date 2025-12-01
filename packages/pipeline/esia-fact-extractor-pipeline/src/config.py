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

env_local_path = workspace_root / ".env.local"
if env_local_path.exists():
    load_dotenv(env_local_path, override=True)  # override=True to update existing vars
else:
    load_dotenv()  # Fallback to default behavior

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Initialize the v1 Client
client = genai.Client(api_key=API_KEY)

# Initialize OpenRouter Client
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
openrouter_client = None
if OPENROUTER_API_KEY:
    try:
        from openrouter import OpenRouter
        openrouter_client = OpenRouter(api_key=OPENROUTER_API_KEY)
    except ImportError:
        print("OpenRouter package not installed. Install with `pip install openrouter`")


# ============================================================================
# LLM Configuration from .env.local
# ============================================================================

# LLM Provider and Models (configured in .env.local)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))

# Constants
STORE_NAME_PREFIX = "esia_store_"

# API Rate Limiting Configuration
# For Tier 1 Gemini: Higher quota, but retry logic still needed for edge cases
MAX_RETRIES = 3  # Reduced from 4 since Tier 1 has better quotas
INITIAL_RETRY_DELAY = 30  # seconds (reduced from 45)
RETRY_BACKOFF_MULTIPLIER = 1.5  # 30s -> 45s -> 67.5s delays
