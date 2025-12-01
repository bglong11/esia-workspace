#!/usr/bin/env python3
"""
Direct Ollama Test - Bypass DSPy

Tests Ollama directly without DSPy to isolate where the problem is.

Usage:
    python test_ollama_direct.py
"""

import requests
import json


def test_ollama_connection():
    """Test if Ollama is running and responding"""
    print("="*80)
    print("TEST 1: OLLAMA CONNECTION")
    print("="*80 + "\n")

    base_url = "http://localhost:11434"

    try:
        # Test API availability
        response = requests.get(f"{base_url}/api/tags")
        print(f"✅ Ollama is running at {base_url}")
        print(f"   Status code: {response.status_code}")

        if response.status_code == 200:
            models = response.json()
            print(f"\n   Available models:")
            for model in models.get('models', []):
                print(f"     - {model.get('name')}")
        return True

    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Ollama at {base_url}")
        print("   Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_simple_generation():
    """Test simple text generation"""
    print("\n" + "="*80)
    print("TEST 2: SIMPLE TEXT GENERATION")
    print("="*80 + "\n")

    base_url = "http://localhost:11434"
    model = "qwen2.5:7b-instruct"

    prompt = "What is 2+2? Answer with just the number."

    print(f"Model: {model}")
    print(f"Prompt: {prompt}")
    print(f"\nSending request to Ollama...")

    try:
        response = requests.post(
            f"{base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 100
                }
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            answer = result.get('response', '')

            print(f"\n✅ Response received:")
            print(f"   Answer: {answer}")
            print(f"   Total duration: {result.get('total_duration', 0) / 1e9:.2f}s")
            return True
        else:
            print(f"❌ Error: Status code {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_json_generation():
    """Test JSON fact extraction"""
    print("\n" + "="*80)
    print("TEST 3: JSON FACT EXTRACTION")
    print("="*80 + "\n")

    base_url = "http://localhost:11434"
    model = "qwen2.5:7b-instruct"

    # Simple ESIA-like text
    document_text = """
    Project Overview:
    The proposed mining project will cover an area of 500 hectares.
    Annual coal production is expected to reach 2 million tonnes per year.
    The project will employ approximately 300 workers.
    Water consumption is estimated at 150 cubic meters per day.
    """

    prompt = f"""Extract quantitative facts from this ESIA document excerpt.

Document text:
{document_text}

Return ONLY a valid JSON array. Each fact should have these fields:
- name: descriptive name of the fact
- type: "quantity" or "category"
- value: the value as a string
- value_num: numeric value (number, not string)
- unit: unit of measurement
- evidence: quote from document

Example format:
[{{"name": "Project area", "type": "quantity", "value": "500", "value_num": 500, "unit": "hectares", "evidence": "will cover an area of 500 hectares"}}]

Return ONLY the JSON array, no other text."""

    print(f"Model: {model}")
    print(f"\nDocument text:")
    print(document_text)
    print(f"\nSending extraction request...")

    try:
        response = requests.post(
            f"{base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 2048
                }
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            answer = result.get('response', '').strip()

            print(f"\n📤 Raw LLM Response:")
            print("-" * 80)
            print(answer)
            print("-" * 80)

            print(f"\nDuration: {result.get('total_duration', 0) / 1e9:.2f}s")

            # Try to parse JSON
            print(f"\n🔬 Attempting to parse JSON...")

            if not answer:
                print("❌ Response is empty!")
                return False

            try:
                # Try to find JSON in the response
                json_start = answer.find('[')
                json_end = answer.rfind(']') + 1

                if json_start == -1 or json_end == 0:
                    print("❌ No JSON array found in response")
                    return False

                json_str = answer[json_start:json_end]
                print(f"\nExtracted JSON substring:")
                print(json_str)

                facts = json.loads(json_str)
                print(f"\n✅ Valid JSON parsed!")
                print(f"   Number of facts: {len(facts)}")

                for i, fact in enumerate(facts):
                    print(f"\n   Fact {i+1}:")
                    print(f"     Name: {fact.get('name')}")
                    print(f"     Value: {fact.get('value')} {fact.get('unit')}")
                    print(f"     Value (numeric): {fact.get('value_num')}")
                    print(f"     Evidence: {fact.get('evidence', '')[:60]}...")

                return True

            except json.JSONDecodeError as e:
                print(f"❌ JSON parse error: {e}")
                print(f"   Position: line {e.lineno}, col {e.colno}")
                return False

        else:
            print(f"❌ Error: Status code {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_chat_format():
    """Test using chat format instead of generate"""
    print("\n" + "="*80)
    print("TEST 4: CHAT FORMAT (Alternative API)")
    print("="*80 + "\n")

    base_url = "http://localhost:11434"
    model = "qwen2.5:7b-instruct"

    document_text = """
    The proposed mining project will cover an area of 500 hectares.
    Annual coal production is expected to reach 2 million tonnes per year.
    """

    system_message = """You are a fact extraction system. Extract quantitative facts from ESIA documents and return them as JSON arrays."""

    user_message = f"""Extract facts from this text:

{document_text}

Return ONLY a JSON array with this format:
[{{"name": "fact name", "type": "quantity", "value": "500", "value_num": 500, "unit": "hectares", "evidence": "quote from text"}}]"""

    print(f"Model: {model}")
    print(f"Testing chat API endpoint...")

    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 2048
                }
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            message = result.get('message', {})
            answer = message.get('content', '').strip()

            print(f"\n📤 Raw Response:")
            print("-" * 80)
            print(answer)
            print("-" * 80)

            # Try to parse JSON
            if answer:
                try:
                    json_start = answer.find('[')
                    json_end = answer.rfind(']') + 1

                    if json_start != -1 and json_end > 0:
                        json_str = answer[json_start:json_end]
                        facts = json.loads(json_str)
                        print(f"\n✅ Valid JSON! Extracted {len(facts)} facts")
                        return True
                except:
                    print(f"\n❌ Could not parse JSON from chat response")
            else:
                print(f"\n❌ Empty response from chat API")

            return False

        else:
            print(f"❌ Error: Status code {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("OLLAMA DIRECT TEST")
    print("Testing Ollama without DSPy to isolate the problem\n")

    results = []

    # Test 1: Connection
    results.append(("Connection", test_ollama_connection()))

    if not results[0][1]:
        print("\n" + "="*80)
        print("STOPPED: Ollama is not running")
        print("="*80)
        print("\nStart Ollama with: ollama serve")
        return

    # Test 2: Simple generation
    results.append(("Simple generation", test_simple_generation()))

    # Test 3: JSON extraction
    results.append(("JSON extraction", test_json_generation()))

    # Test 4: Chat format
    results.append(("Chat format", test_chat_format()))

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80 + "\n")

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}  {test_name}")

    print("\n" + "="*80)
    print("DIAGNOSIS")
    print("="*80 + "\n")

    if all(result[1] for result in results):
        print("✅ All tests passed!")
        print("   Ollama is working correctly.")
        print("   The problem is likely in DSPy integration.")
        print("\nNext steps:")
        print("   1. Run: python test_llm_debug.py docling_output/your_file_docling.md")
        print("   2. Check DSPy version compatibility")
        print("   3. Verify DSPy is using the correct Ollama API endpoint")

    elif results[0][1] and results[1][1] and not results[2][1]:
        print("⚠️  Ollama works but JSON extraction is failing")
        print("   The model can generate text but not structured JSON.")
        print("\nPossible solutions:")
        print("   1. Try a different prompt format")
        print("   2. Increase temperature slightly (0.3-0.4)")
        print("   3. Try a different model (e.g., llama3.1)")
        print("   4. Use JSON mode if available: format='json'")

    else:
        print("❌ Ollama has issues")
        print("   Check Ollama installation and model availability")
        print("\nTroubleshooting:")
        print("   1. Check status: ollama list")
        print("   2. Pull model: ollama pull qwen2.5:7b-instruct")
        print("   3. Test manually: ollama run qwen2.5:7b-instruct")


if __name__ == "__main__":
    main()
