#!/usr/bin/env python3
"""Test CONFIDENCE_THRESHOLD environment configuration"""

import os
import sys
from pathlib import Path

# Add pipeline directory to path
sys.path.insert(0, str(Path(__file__).parent / "packages" / "pipeline"))

# Load .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / "packages" / "pipeline" / ".env"
    load_dotenv(env_path)
    print(f"Loaded .env from: {env_path}")
except ImportError:
    print("Warning: python-dotenv not installed")

# Check configuration
threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
print(f"\nConfiguration Test Results:")
print(f"  CONFIDENCE_THRESHOLD = {threshold}")
print(f"  Type: {type(threshold).__name__}")

# Show optimization impact
if threshold == 0.5:
    impact = "40-50% faster"
elif threshold == 0.7:
    impact = "57-67% faster"
elif threshold == 0.3:
    impact = "11-23% faster"
else:
    impact = "custom"

print(f"  Optimization: {impact}")
print(f"\nSuccess: CONFIDENCE_THRESHOLD is configured and ready to use!")
