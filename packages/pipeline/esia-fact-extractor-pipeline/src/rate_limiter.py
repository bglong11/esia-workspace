#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token Bucket Rate Limiter for LLM API Calls

Implements a thread-safe token bucket algorithm to prevent rate limit errors
by pacing requests according to provider-specific limits.

Usage:
    limiter = RateLimiter(requests_per_minute=60)
    limiter.acquire()  # Blocks until request can proceed
    # ... make API call
"""

import time
from threading import Lock, Event
from typing import Optional


class RateLimiter:
    """
    Thread-safe token bucket rate limiter.

    Ensures API calls don't exceed provider rate limits by pacing requests
    evenly throughout each minute.
    """

    def __init__(self, requests_per_minute: int = 60, burst_size: Optional[int] = None):
        """
        Initialize rate limiter.

        Args:
            requests_per_minute: Maximum requests allowed per minute
            burst_size: Maximum burst capacity (defaults to requests_per_minute)
        """
        self.requests_per_minute = requests_per_minute
        self.interval = 60.0 / requests_per_minute  # Time between requests
        self.burst_size = burst_size or requests_per_minute

        # Token bucket state
        self.tokens = float(self.burst_size)  # Start with full bucket
        self.last_refill = time.time()

        # Thread safety
        self.lock = Lock()
        self.shutdown_event = Event()

    def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire permission to make a request (blocking).

        Args:
            timeout: Maximum time to wait (None = wait forever)

        Returns:
            True if acquired, False if timed out
        """
        start_time = time.time()

        while True:
            if self.shutdown_event.is_set():
                return False

            with self.lock:
                # Refill tokens based on elapsed time
                now = time.time()
                elapsed = now - self.last_refill

                # Add tokens based on time passed
                tokens_to_add = elapsed * (self.requests_per_minute / 60.0)
                self.tokens = min(self.burst_size, self.tokens + tokens_to_add)
                self.last_refill = now

                # Check if we have a token available
                if self.tokens >= 1.0:
                    self.tokens -= 1.0
                    return True

            # Check timeout
            if timeout is not None:
                if time.time() - start_time >= timeout:
                    return False

            # Sleep briefly before retry (avoid busy waiting)
            time.sleep(0.01)  # 10ms

    def try_acquire(self) -> bool:
        """
        Try to acquire without blocking.

        Returns:
            True if acquired, False if no tokens available
        """
        return self.acquire(timeout=0)

    def reset(self):
        """Reset the rate limiter (clear all tokens and timing)."""
        with self.lock:
            self.tokens = float(self.burst_size)
            self.last_refill = time.time()

    def shutdown(self):
        """Signal shutdown to unblock any waiting threads."""
        self.shutdown_event.set()

    def get_wait_time(self) -> float:
        """
        Get estimated wait time until next token is available.

        Returns:
            Seconds to wait (0 if token available now)
        """
        with self.lock:
            if self.tokens >= 1.0:
                return 0.0

            # Calculate time until next token
            tokens_needed = 1.0 - self.tokens
            time_per_token = 60.0 / self.requests_per_minute
            return tokens_needed * time_per_token


class ProviderRateLimiters:
    """
    Manages rate limiters for different LLM providers.

    Each provider has different rate limits, so we maintain separate
    rate limiters for each.
    """

    # Provider-specific rate limits (requests per minute)
    PROVIDER_LIMITS = {
        'google': 60,      # Gemini Tier 1: 60 RPM
        'openai': 60,      # OpenAI Tier 1: 60 RPM (conservative)
        'xai': 60,         # xAI Grok: 60 RPM
        'openrouter': 50,  # OpenRouter: 50 RPM (conservative, varies by model)
    }

    def __init__(self):
        """Initialize rate limiters for all providers."""
        self.limiters = {
            provider: RateLimiter(requests_per_minute=rpm)
            for provider, rpm in self.PROVIDER_LIMITS.items()
        }

    def acquire(self, provider: str, timeout: Optional[float] = None) -> bool:
        """
        Acquire rate limit token for a provider.

        Args:
            provider: Provider name ('google', 'openai', 'xai', 'openrouter')
            timeout: Maximum wait time

        Returns:
            True if acquired, False if timed out
        """
        provider = provider.lower()
        if provider not in self.limiters:
            # Unknown provider, create default limiter
            self.limiters[provider] = RateLimiter(requests_per_minute=30)

        return self.limiters[provider].acquire(timeout=timeout)

    def try_acquire(self, provider: str) -> bool:
        """Try to acquire without blocking."""
        provider = provider.lower()
        if provider not in self.limiters:
            return True  # No limit for unknown providers

        return self.limiters[provider].try_acquire()

    def get_wait_time(self, provider: str) -> float:
        """Get estimated wait time for provider."""
        provider = provider.lower()
        if provider not in self.limiters:
            return 0.0

        return self.limiters[provider].get_wait_time()

    def reset(self, provider: Optional[str] = None):
        """
        Reset rate limiters.

        Args:
            provider: Specific provider to reset (None = reset all)
        """
        if provider:
            provider = provider.lower()
            if provider in self.limiters:
                self.limiters[provider].reset()
        else:
            for limiter in self.limiters.values():
                limiter.reset()

    def shutdown(self):
        """Shutdown all rate limiters."""
        for limiter in self.limiters.values():
            limiter.shutdown()


# Global instance for easy access
_global_rate_limiters = None

def get_rate_limiter() -> ProviderRateLimiters:
    """Get the global rate limiter instance (singleton pattern)."""
    global _global_rate_limiters
    if _global_rate_limiters is None:
        _global_rate_limiters = ProviderRateLimiters()
    return _global_rate_limiters


if __name__ == "__main__":
    # Test the rate limiter
    import threading

    print("Testing RateLimiter with 10 requests/minute (6 second intervals)...")
    limiter = RateLimiter(requests_per_minute=10)

    def make_request(request_id):
        print(f"[{request_id}] Waiting for permission...")
        start = time.time()
        limiter.acquire()
        elapsed = time.time() - start
        print(f"[{request_id}] Acquired after {elapsed:.2f}s")

    # Test with concurrent requests
    threads = []
    for i in range(5):
        t = threading.Thread(target=make_request, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nTest completed!")
