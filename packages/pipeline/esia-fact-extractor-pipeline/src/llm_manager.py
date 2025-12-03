
from src.config import client as google_client, openrouter_client, xai_client, openai_client
from src.config import MAX_RETRIES, INITIAL_RETRY_DELAY, RETRY_BACKOFF_MULTIPLIER
from src.config import RATE_LIMIT_GOOGLE, RATE_LIMIT_OPENAI, RATE_LIMIT_XAI, RATE_LIMIT_OPENROUTER
from google import genai
import os
import time
from functools import wraps

# Import rate limiter
try:
    from src.rate_limiter import ProviderRateLimiters
    _rate_limiters = ProviderRateLimiters()
    # Update rate limiters with config values
    _rate_limiters.PROVIDER_LIMITS['google'] = RATE_LIMIT_GOOGLE
    _rate_limiters.PROVIDER_LIMITS['openai'] = RATE_LIMIT_OPENAI
    _rate_limiters.PROVIDER_LIMITS['xai'] = RATE_LIMIT_XAI
    _rate_limiters.PROVIDER_LIMITS['openrouter'] = RATE_LIMIT_OPENROUTER
    # Reinitialize limiters with updated limits
    _rate_limiters.__init__()
    RATE_LIMITING_ENABLED = True
except ImportError:
    print("Warning: Rate limiter not available, proceeding without rate limiting")
    _rate_limiters = None
    RATE_LIMITING_ENABLED = False


def retry_on_rate_limit(func):
    """
    Decorator to implement exponential backoff retry logic for API rate limiting.

    Specifically handles Google Gemini API 429 RESOURCE_EXHAUSTED errors with:
    - Exponential backoff: 45s, 67.5s, 101s, 151s
    - Maximum 4 retries (total ~7 minutes max wait time)
    - Detailed logging of retry attempts
    - Graceful failure after max retries

    Args:
        func: Function to wrap (should be an API call method)

    Returns:
        Wrapped function with retry logic
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        last_exception = None

        for attempt in range(MAX_RETRIES + 1):  # +1 for initial attempt
            try:
                # Attempt the API call
                return func(*args, **kwargs)

            except Exception as e:
                last_exception = e
                error_str = str(e).lower()

                # Check if it's a rate limit error (429 or RESOURCE_EXHAUSTED)
                is_rate_limit = (
                    '429' in error_str or
                    'resource_exhausted' in error_str or
                    'rate limit' in error_str or
                    'quota exceeded' in error_str
                )

                if not is_rate_limit:
                    # Not a rate limit error, raise immediately
                    raise

                # If we've exhausted all retries, raise the error
                if attempt >= MAX_RETRIES:
                    print(f"\n[ERROR] Max retries ({MAX_RETRIES}) exceeded for rate limit error.")
                    print(f"[ERROR] Last error: {e}")
                    raise

                # Calculate delay with exponential backoff
                delay = INITIAL_RETRY_DELAY * (RETRY_BACKOFF_MULTIPLIER ** attempt)

                # Log retry attempt
                print(f"\n[RATE LIMIT] API rate limit hit (attempt {attempt + 1}/{MAX_RETRIES + 1})")
                print(f"[RATE LIMIT] Error: {e}")
                print(f"[RATE LIMIT] Waiting {delay:.1f} seconds before retry...")

                # Wait before retrying
                time.sleep(delay)

                print(f"[RATE LIMIT] Retrying now (attempt {attempt + 2}/{MAX_RETRIES + 1})...")

        # Should never reach here, but just in case
        raise last_exception

    return wrapper


class LLMManager:
    def __init__(self):
        self.google_client = google_client
        self.openrouter_client = openrouter_client
        self.xai_client = xai_client
        self.openai_client = openai_client

    def generate_content(self, prompt: str, model: str = "gemini-2.5-flash", provider: str = None, system_instruction: str = None, **kwargs):
        """
        Generates content using the specified model and provider.

        Args:
            prompt: The input prompt.
            model: The model name (e.g., "gemini-2.5-flash", "gpt-4o-mini", "grok-3-mini").
            provider: "google", "openai", "openrouter", or "xai". If None, infers from model name.
            system_instruction: Optional system instruction.
            **kwargs: Additional arguments passed to the API.
        """
        if provider is None:
            # Auto-detect provider from model name
            if model.startswith("gemini"):
                provider = "google"
            elif model.startswith("gpt"):
                provider = "openai"
            elif model.startswith("grok"):
                provider = "xai"
            else:
                provider = "openrouter"

        print(f"Using provider: {provider} for model: {model}")

        # Acquire rate limit token before making API call
        if RATE_LIMITING_ENABLED and _rate_limiters:
            # This will block until we're allowed to proceed
            acquired = _rate_limiters.acquire(provider, timeout=60)
            if not acquired:
                raise RuntimeError(f"Rate limiter timeout for provider: {provider}")

        if provider == "google":
            return self._generate_google(prompt, model, system_instruction=system_instruction, **kwargs)
        elif provider == "openai":
            return self._generate_openai(prompt, model, system_instruction=system_instruction, **kwargs)
        elif provider == "openrouter":
            return self._generate_openrouter(prompt, model, system_instruction=system_instruction, **kwargs)
        elif provider == "xai":
            return self._generate_xai(prompt, model, system_instruction=system_instruction, **kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    @retry_on_rate_limit
    def _generate_google(self, prompt, model, system_instruction=None, **kwargs):
        # Adapt to Google Gen AI SDK v1
        
        # Check if 'config' is explicitly passed
        generation_config = kwargs.pop('config', None)
        
        # If not, or if we need to merge system_instruction, we handle it
        if generation_config is None:
            generation_config = {}
        
        # If generation_config is a dict, we can update it. 
        # If it's a GenerateContentConfig object, we might need to set attributes or convert.
        # The SDK accepts both.
        
        if system_instruction:
            if isinstance(generation_config, dict):
                generation_config['system_instruction'] = system_instruction
            else:
                # It's an object, try setting attribute if possible, or warn
                # For now, assume if object is passed, system_instruction is already in it or we can't easily add it without knowing the class details
                # But we can try:
                try:
                    generation_config.system_instruction = system_instruction
                except:
                    pass # Can't set it
        
        # Any remaining kwargs could be for the config or the method?
        # client.models.generate_content(model=, contents=, config=)
        # If kwargs contains things like 'temperature', they should be in config.
        # But if the caller passed 'config', they should have put them there.
        # If the caller passed them as kwargs, we should put them in config.
        
        if kwargs:
            if isinstance(generation_config, dict):
                generation_config.update(kwargs)
            # If it's an object, we can't easily update from kwargs unless we iterate
        
        response = self.google_client.models.generate_content(
            model=model,
            contents=prompt,
            config=generation_config if generation_config else None
        )
        return response

    def _generate_openrouter(self, prompt, model, system_instruction=None, **kwargs):
        if not self.openrouter_client:
             raise ValueError("OpenRouter client is not initialized. Check OPENROUTER_API_KEY in .env")

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})

        messages.append({"role": "user", "content": prompt})

        # OpenRouter is compatible with OpenAI SDK
        # Use chat.completions.create() which is the standard OpenAI method
        response = self.openrouter_client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response

    def _generate_xai(self, prompt, model, system_instruction=None, **kwargs):
        """Generate content using xAI (Grok) API."""
        if not self.xai_client:
            raise ValueError("xAI client not initialized. Check XAI_API_KEY in .env")

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})

        messages.append({"role": "user", "content": prompt})

        # xAI is OpenAI-compatible
        response = self.xai_client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response

    def _generate_openai(self, prompt, model, system_instruction=None, **kwargs):
        """Generate content using native OpenAI API."""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized. Check OPENAI_API_KEY in .env")

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})

        messages.append({"role": "user", "content": prompt})

        # Native OpenAI API
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response

if __name__ == "__main__":
    # Test the manager
    manager = LLMManager()
    
    # Test Google
    try:
        print("\nTesting Google Provider:")
        res_google = manager.generate_content("Say hello from Google!", model="gemini-2.5-flash")
        print(res_google.text)
    except Exception as e:
        print(f"Google Test Failed: {e}")

    # Test OpenRouter (will fail if no key)
    try:
        print("\nTesting OpenRouter Provider:")
        # Using a free model or cheap one for test if possible, or just a standard one
        res_or = manager.generate_content("Say hello from OpenRouter!", model="google/gemini-2.0-flash-exp:free") 
        # Note: OpenRouter model names often have vendor prefix. 
        # "google/gemini-2.0-flash-exp:free" is a valid OpenRouter model ID if available, or "meta-llama/llama-3-8b-instruct:free"
        print(res_or) 
    except Exception as e:
        print(f"OpenRouter Test Failed: {e}")
