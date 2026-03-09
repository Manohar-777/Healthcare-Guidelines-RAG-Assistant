"""
Debug script to see what's actually being retrieved
"""

import requests
import json

# Test query
question = "When should hand hygiene be performed?"

print("="*60)
print(f"Question: {question}")
print("="*60)

# Call API
response = requests.post(
    "http://localhost:9070/qa",
    json={"question": question, "top_k": 5, "use_llm": True}
)

result = response.json()

print("\n📊 RETRIEVED PASSAGES:")
print("-"*60)


from pathlib import Path

corpus = Path("corpus/guidelines")

print("\nChecking hand hygiene documents...\n")

for doc in sorted(corpus.glob("*hand_hygiene*.md"))[:3]:
    print(f"📄 {doc.name}")
    print("-"*60)
    text = doc.read_text(encoding='utf-8')
    
    # Print first 500 chars
    print(text[:500])
    print("\n" + "="*60 + "\n")