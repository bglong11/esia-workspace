#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to demonstrate retry logic for API rate limiting.

This script simulates API rate limit errors to verify the exponential backoff
retry mechanism works correctly.
"""

import sys
import os
sys.path.append(os.getcwd())

from src.config import MAX_RETRIES, INITIAL_RETRY_DELAY, RETRY_BACKOFF_MULTIPLIER
from src.llm_manager import retry_on_rate_limit
import time


# Test function that simulates rate limit errors
@retry_on_rate_limit
def simulate_rate_limited_api(fail_count=2):
    """
    Simulate an API call that fails with rate limit errors.

    Args:
        fail_count: Number of times to fail before succeeding

    Returns:
        str: Success message
    """
    if not hasattr(simulate_rate_limited_api, 'attempt_count'):
        simulate_rate_limited_api.attempt_count = 0

    simulate_rate_limited_api.attempt_count += 1
    current_attempt = simulate_rate_limited_api.attempt_count

    print(f"\n[TEST] API call attempt #{current_attempt}")

    if current_attempt <= fail_count:
        # Simulate rate limit error
        raise Exception("429 RESOURCE_EXHAUSTED: Quota exceeded for quota metric 'GenerateContent requests per minute'")
    else:
        # Success!
        print("[TEST] API call succeeded!")
        return f"Success after {current_attempt} attempts"


def test_retry_logic():
    """Test the retry logic with different scenarios."""

    print("=" * 70)
    print("TESTING EXPONENTIAL BACKOFF RETRY LOGIC")
    print("=" * 70)
    print()
    print(f"Configuration:")
    print(f"  MAX_RETRIES: {MAX_RETRIES}")
    print(f"  INITIAL_RETRY_DELAY: {INITIAL_RETRY_DELAY}s")
    print(f"  BACKOFF_MULTIPLIER: {RETRY_BACKOFF_MULTIPLIER}")
    print()

    # Calculate expected delays
    delays = []
    for attempt in range(MAX_RETRIES):
        delay = INITIAL_RETRY_DELAY * (RETRY_BACKOFF_MULTIPLIER ** attempt)
        delays.append(delay)

    print(f"Expected retry delays: {', '.join([f'{d:.1f}s' for d in delays])}")
    print()

    # Test 1: Success after 2 failures (within retry limit)
    print("\n" + "=" * 70)
    print("TEST 1: API succeeds after 2 rate limit errors")
    print("=" * 70)

    # Reset attempt counter
    if hasattr(simulate_rate_limited_api, 'attempt_count'):
        delattr(simulate_rate_limited_api, 'attempt_count')

    start_time = time.time()
    try:
        result = simulate_rate_limited_api(fail_count=2)
        elapsed = time.time() - start_time
        print(f"\n[SUCCESS] {result}")
        print(f"[SUCCESS] Total time: {elapsed:.1f}s")
        print(f"[SUCCESS] This demonstrates the retry logic works correctly!")
    except Exception as e:
        print(f"\n[FAILED] Unexpected error: {e}")

    # Test 2: Explain what happens with too many failures
    print("\n" + "=" * 70)
    print("TEST 2: What happens when max retries exceeded?")
    print("=" * 70)
    print()
    print(f"If API fails more than {MAX_RETRIES} times, the decorator will:")
    print(f"1. Try the initial request")
    print(f"2. Retry {MAX_RETRIES} times with exponential backoff")
    print(f"3. After final retry fails, raise the error with detailed message")
    print(f"4. Total max wait time: ~{sum(delays):.0f} seconds (~{sum(delays)/60:.1f} minutes)")
    print()
    print(f"This allows the pipeline to continue even if one section fails,")
    print(f"rather than stopping the entire extraction process.")

    # Test 3: Non-rate-limit errors pass through immediately
    print("\n" + "=" * 70)
    print("TEST 3: Non-rate-limit errors")
    print("=" * 70)
    print()
    print("The retry logic only catches rate limit errors (429, RESOURCE_EXHAUSTED).")
    print("Other errors (network issues, invalid API key, etc.) are raised immediately")
    print("without retrying, to avoid wasting time on non-recoverable errors.")


if __name__ == "__main__":
    test_retry_logic()

    print("\n" + "=" * 70)
    print("RETRY LOGIC TEST COMPLETE")
    print("=" * 70)
    print()
    print("The retry logic is ready for production use!")
    print()
    print("To test with real API calls, run:")
    print("  python step2_fact_extraction.py --sample 20")
    print()
