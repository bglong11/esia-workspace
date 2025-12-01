import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

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


# Constants
STORE_NAME_PREFIX = "esia_store_"

# API Rate Limiting Configuration
# For Tier 1 Gemini: Higher quota, but retry logic still needed for edge cases
MAX_RETRIES = 3  # Reduced from 4 since Tier 1 has better quotas
INITIAL_RETRY_DELAY = 30  # seconds (reduced from 45)
RETRY_BACKOFF_MULTIPLIER = 1.5  # 30s -> 45s -> 67.5s delays
