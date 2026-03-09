"""
Quick smoke test - verify basic functionality
Run this as a quick check before submission
"""

import requests
import sys

API_URL = "http://localhost:9070"

def smoke_test():
    """Run basic smoke tests"""
    
    print("🔥 Running Smoke Tests...")
    print("="*60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Server Running
    print("\n1. Testing server health...")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Server is running")
            tests_passed += 1
        else:
            print(f"   ❌ Server returned {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Cannot connect to server: {e}")
        tests_failed += 1
        return False
    
    # Test 2: Index Loaded
    print("\n2. Testing index loaded...")
    try:
        data = response.json()
        if data.get("index_loaded"):
            print(f"   ✅ Index loaded ({data.get('num_chunks')} chunks)")
            tests_passed += 1
        else:
            print("   ❌ Index not loaded")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Test 3: Simple Query
    print("\n3. Testing simple query...")
    try:
        response = requests.post(
            f"{API_URL}/qa",
            json={"question": "When should hand hygiene be performed?"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("answer") and len(data["answer"]) > 10:
                print(f"   ✅ Query successful")
                print(f"      Answer: {data['answer'][:100]}...")
                print(f"      Confidence: {data['confidence']:.2f}")
                tests_passed += 1
            else:
                print("   ❌ Empty or invalid answer")
                tests_failed += 1
        else:
            print(f"   ❌ Query failed: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Test 4: LLM vs Extractive
    print("\n4. Testing LLM and extractive modes...")
    try:
        llm_resp = requests.post(
            f"{API_URL}/qa",
            json={"question": "What are PPE guidelines?", "use_llm": True}
        ).json()
        
        ext_resp = requests.post(
            f"{API_URL}/qa/extractive",
            json={"question": "What are PPE guidelines?"}
        ).json()
        
        if llm_resp.get("generation_method") == "llm" and \
           ext_resp.get("generation_method") == "extractive":
            print("   ✅ Both modes working")
            tests_passed += 1
        else:
            print("   ❌ Mode mismatch")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Test 5: Stats Endpoint
    print("\n5. Testing stats endpoint...")
    try:
        response = requests.get(f"{API_URL}/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Stats available")
            print(f"      Model: {data.get('llm_model')}")
            print(f"      Precision@5: {data.get('performance', {}).get('precision_at_5', 'N/A')}")
            tests_passed += 1
        else:
            print("   ❌ Stats endpoint failed")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "="*60)
    print("SMOKE TEST RESULTS")
    print("="*60)
    print(f"✅ Passed: {tests_passed}/5")
    print(f"❌ Failed: {tests_failed}/5")
    
    if tests_failed == 0:
        print("\n🎉 All smoke tests passed! System is ready.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please review before submission.")
        return False


if __name__ == "__main__":
    success = smoke_test()
    sys.exit(0 if success else 1)