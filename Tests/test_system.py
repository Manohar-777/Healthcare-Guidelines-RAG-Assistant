"""
Comprehensive test suite for Healthcare RAG Assistant
Tests all major components and integration
"""

import pytest
import requests
import json
import time
from pathlib import Path
import sys

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

API_URL = "http://localhost:9070"

class TestSystemHealth:
    """Test basic system health and availability"""
    
    def test_server_running(self):
        """Test if server is running"""
        response = requests.get(f"{API_URL}/")
        assert response.status_code == 200
        
    def test_health_check_response(self):
        """Test health check returns correct data"""
        response = requests.get(f"{API_URL}/")
        data = response.json()
        
        assert data["status"] == "running"
        assert data["service"] == "Healthcare Guidelines RAG Assistant"
        assert data["version"] == "0.4.0"
        assert data["index_loaded"] is True
        assert data["num_chunks"] > 0
        
    def test_stats_endpoint(self):
        """Test stats endpoint"""
        response = requests.get(f"{API_URL}/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_chunks" in data
        assert "embedding_model" in data
        assert data["total_chunks"] == 345


class TestQAEndpoint:
    """Test question-answering functionality"""
    
    def test_simple_query(self):
        """Test basic query"""
        response = requests.post(
            f"{API_URL}/qa",
            json={
                "question": "When should hand hygiene be performed?",
                "top_k": 5,
                "use_llm": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert "citations" in data
        assert "confidence" in data
        assert "status" in data
        assert len(data["answer"]) > 0
        assert len(data["citations"]) > 0
        
    def test_response_structure(self):
        """Test response has correct structure"""
        response = requests.post(
            f"{API_URL}/qa",
            json={
                "question": "What are PPE guidelines?",
                "top_k": 3
            }
        )
        
        data = response.json()
        
        # Check required fields
        assert "answer" in data
        assert "citations" in data
        assert "confidence" in data
        assert "status" in data
        assert "generation_method" in data
        
        # Check citations structure
        if len(data["citations"]) > 0:
            citation = data["citations"][0]
            assert "path" in citation
            assert "section" in citation
            assert "score" in citation
            
    def test_top_k_parameter(self):
        """Test top_k parameter works"""
        for k in [1, 3, 5]:
            response = requests.post(
                f"{API_URL}/qa",
                json={
                    "question": "What are hand hygiene principles?",
                    "top_k": k
                }
            )
            
            data = response.json()
            assert len(data["citations"]) <= k
            
    def test_llm_vs_extractive(self):
        """Test LLM and extractive modes"""
        question = "What are PPE selection criteria?"
        
        # LLM mode
        llm_response = requests.post(
            f"{API_URL}/qa",
            json={"question": question, "use_llm": True}
        ).json()
        
        # Extractive mode
        ext_response = requests.post(
            f"{API_URL}/qa/extractive",
            json={"question": question}
        ).json()
        
        assert llm_response["generation_method"] == "llm"
        assert ext_response["generation_method"] == "extractive"
        
        # LLM answer should generally be longer
        # (though not always - just check they're different)
        assert llm_response["answer"] != ext_response["answer"] or \
               abs(len(llm_response["answer"]) - len(ext_response["answer"])) > 10


class TestValidation:
    """Test validation and confidence scoring"""
    
    def test_confidence_range(self):
        """Test confidence is in valid range"""
        response = requests.post(
            f"{API_URL}/qa",
            json={"question": "When should hand hygiene be performed?"}
        )
        
        data = response.json()
        confidence = data["confidence"]
        
        assert 0.0 <= confidence <= 1.0
        
    def test_status_values(self):
        """Test status is valid"""
        response = requests.post(
            f"{API_URL}/qa",
            json={"question": "What are environmental cleaning guidelines?"}
        )
        
        data = response.json()
        status = data["status"]
        
        assert status in ["validated", "needs_review"]
        
    def test_off_topic_query(self):
        """Test off-topic query handling"""
        response = requests.post(
            f"{API_URL}/qa",
            json={"question": "What is the weather today?"}
        )
        
        data = response.json()
        
        # Should have low confidence or error message
        assert data["confidence"] < 0.5 or \
               "not appear to be related" in data["answer"].lower() or \
               "don't have enough information" in data["answer"].lower()


class TestPerformance:
    """Test performance and response times"""
    
    def test_response_time(self):
        """Test query responds within reasonable time"""
        start = time.time()
        
        response = requests.post(
            f"{API_URL}/qa",
            json={"question": "What are hand hygiene recommendations?"},
            timeout=30
        )
        
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 30  # Should respond within 30 seconds
        
    def test_multiple_concurrent_queries(self):
        """Test handling multiple queries"""
        questions = [
            "When should hand hygiene be performed?",
            "What are PPE guidelines?",
            "How should environmental cleaning be done?"
        ]
        
        for question in questions:
            response = requests.post(
                f"{API_URL}/qa",
                json={"question": question}
            )
            assert response.status_code == 200


class TestErrorHandling:
    """Test error handling"""
    
    def test_missing_question(self):
        """Test missing question parameter"""
        response = requests.post(
            f"{API_URL}/qa",
            json={"top_k": 5}
        )
        
        assert response.status_code == 422  # Validation error
        
    def test_invalid_top_k(self):
        """Test invalid top_k values"""
        # Too large
        response = requests.post(
            f"{API_URL}/qa",
            json={"question": "test", "top_k": 100}
        )
        # Should either accept and cap it, or return error
        assert response.status_code in [200, 422]
        
    def test_empty_question(self):
        """Test empty question"""
        response = requests.post(
            f"{API_URL}/qa",
            json={"question": ""}
        )
        
        # Should handle gracefully
        assert response.status_code in [200, 422]



def run_all_tests():
    """Run all tests and generate report"""
    print("="*60)
    print("RUNNING COMPREHENSIVE TEST SUITE")
    print("="*60)
    print()
    
    # Run pytest
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])
    
    return exit_code


if __name__ == "__main__":
    # Make sure server is running
    try:
        requests.get(f"{API_URL}/", timeout=5)
    except:
        print("❌ ERROR: Server not running!")
        print(f"Please start server: uvicorn app.server:app --port 9070")
        sys.exit(1)
    
    # Run tests
    exit_code = run_all_tests()
    sys.exit(exit_code)