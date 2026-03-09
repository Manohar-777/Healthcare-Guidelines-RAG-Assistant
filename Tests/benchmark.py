"""
Performance benchmark for Healthcare RAG Assistant
Measures response times and throughput
"""

import requests
import time
import statistics
from pathlib import Path

API_URL = "http://localhost:9070"

TEST_QUERIES = [
    "When should hand hygiene be performed?",
    "What are PPE selection guidelines?",
    "How should environmental cleaning be done?",
    "What are respiratory etiquette recommendations?",
    "When can staff return to work after isolation?"
]

def benchmark_query(question, iterations=3):
    """Benchmark a single query"""
    times = []
    
    for _ in range(iterations):
        start = time.time()
        
        response = requests.post(
            f"{API_URL}/qa",
            json={"question": question, "top_k": 5}
        )
        
        elapsed = time.time() - start
        times.append(elapsed)
        
        if response.status_code != 200:
            print(f"❌ Query failed: {response.status_code}")
            return None
    
    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "min": min(times),
        "max": max(times)
    }

def run_benchmark():
    """Run performance benchmark"""
    
    print("="*60)
    print("PERFORMANCE BENCHMARK")
    print("="*60)
    print()
    
    results = []
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"[{i}/{len(TEST_QUERIES)}] Testing: {query[:50]}...")
        
        result = benchmark_query(query)
        
        if result:
            results.append(result)
            print(f"   Mean: {result['mean']:.2f}s | " +
                  f"Median: {result['median']:.2f}s | " +
                  f"Range: {result['min']:.2f}-{result['max']:.2f}s")
        else:
            print("   ❌ Failed")
    
    # Overall statistics
    if results:
        all_means = [r["mean"] for r in results]
        
        print("\n" + "="*60)
        print("OVERALL PERFORMANCE")
        print("="*60)
        print(f"Average response time: {statistics.mean(all_means):.2f}s")
        print(f"Fastest query: {min(all_means):.2f}s")
        print(f"Slowest query: {max(all_means):.2f}s")
        print(f"Std deviation: {statistics.stdev(all_means):.2f}s")
        
        # Performance targets
        print("\n" + "="*60)
        print("PERFORMANCE TARGETS")
        print("="*60)
        
        avg_time = statistics.mean(all_means)
        
        if avg_time < 5:
            print("✅ EXCELLENT: Average < 5s")
        elif avg_time < 10:
            print("✅ GOOD: Average < 10s")
        elif avg_time < 20:
            print("⚠️  ACCEPTABLE: Average < 20s")
        else:
            print("❌ SLOW: Average > 20s")

if __name__ == "__main__":
    try:
        # Warmup query
        print("Warming up...")
        requests.post(
            f"{API_URL}/qa",
            json={"question": "test"}
        )
        
        time.sleep(2)
        
        # Run benchmark
        run_benchmark()
        
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")