import requests
import json

print("="*60)
print("Testing LLM-Powered RAG System")
print("="*60)

# Test with LLM
print("\n1. Testing with LLM generation:")
response = requests.post(
    "http://localhost:9070/qa",
    json={
        "question": "When should hand hygiene be performed?",
        "top_k": 5,
        "use_llm": True
    }
)

if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Test extractive for comparison
print("\n" + "="*60)
print("\n2. Testing extractive method (for comparison):")
response = requests.post(
    "http://localhost:9070/qa/extractive",
    json={
        "question": "When should hand hygiene be performed?",
        "top_k": 5
    }
)

if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Test complex query
print("\n" + "="*60)
print("\n3. Testing complex query with LLM:")
response = requests.post(
    "http://localhost:9070/qa",
    json={
        "question": "How should PPE be selected based on exposure risk and what are the key safety considerations?",
        "top_k": 5,
        "use_llm": True
    }
)

if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)