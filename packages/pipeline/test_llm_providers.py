#!/usr/bin/env python3
"""Test script to verify all LLM providers work correctly."""

import os
import sys
from pathlib import Path

# Add both paths to import correctly
extractor_root = Path(__file__).parent / "esia-fact-extractor-pipeline"
sys.path.insert(0, str(extractor_root))
sys.path.insert(0, str(extractor_root / "src"))

from src.llm_manager import LLMManager
from src.config import LLM_PROVIDER, GOOGLE_MODEL, OPENAI_MODEL, OPENROUTER_MODEL, XAI_MODEL

def test_provider(provider_name, model):
    """Test a specific LLM provider."""
    print(f"\n{'='*60}")
    print(f"Testing {provider_name.upper()} Provider")
    print(f"Model: {model}")
    print(f"{'='*60}")

    manager = LLMManager()

    try:
        response = manager.generate_content(
            prompt="Say 'Hello from [provider name]' in one sentence.",
            model=model,
            provider=provider_name
        )

        # Extract text from response
        if hasattr(response, 'text'):
            text = response.text
        elif hasattr(response, 'choices'):
            text = response.choices[0].message.content
        else:
            text = str(response)

        print(f"[SUCCESS]")
        print(f"Response: {text[:100]}...")
        return True

    except Exception as e:
        print(f"[FAILED]: {type(e).__name__}")
        print(f"Error: {str(e)[:200]}")
        return False

def main():
    """Run tests for all configured providers."""
    results = {}

    print(f"\nCurrent LLM_PROVIDER: {LLM_PROVIDER}")

    # Test Google (if API key present)
    if os.getenv("GOOGLE_API_KEY"):
        results['google'] = test_provider("google", GOOGLE_MODEL)
    else:
        print(f"\n{'='*60}")
        print("Google Provider: SKIPPED (no GOOGLE_API_KEY)")
        print(f"{'='*60}")

    # Test OpenAI (if API key present)
    if os.getenv("OPENAI_API_KEY"):
        results['openai'] = test_provider("openai", OPENAI_MODEL)
    else:
        print(f"\n{'='*60}")
        print("OpenAI Provider: SKIPPED (no OPENAI_API_KEY)")
        print(f"{'='*60}")

    # Test OpenRouter (if API key present)
    if os.getenv("OPENROUTER_API_KEY"):
        results['openrouter'] = test_provider("openrouter", OPENROUTER_MODEL)
    else:
        print(f"\n{'='*60}")
        print("OpenRouter Provider: SKIPPED (no OPENROUTER_API_KEY)")
        print(f"{'='*60}")

    # Test xAI (if API key present)
    if os.getenv("XAI_API_KEY"):
        results['xai'] = test_provider("xai", XAI_MODEL)
    else:
        print(f"\n{'='*60}")
        print("xAI Provider: SKIPPED (no XAI_API_KEY)")
        print(f"{'='*60}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for provider, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{provider:15s} [{status}]")

    if not results:
        print("No providers tested - check API keys in .env.local")
        return 1

    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
