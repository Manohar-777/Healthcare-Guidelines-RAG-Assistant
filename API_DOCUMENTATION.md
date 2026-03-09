# 🔌 API Documentation - Healthcare RAG Assistant

**Version:** 0.4.0  
**Base URL:** `http://localhost:9070`

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Request/Response Models](#requestresponse-models)
5. [Error Handling](#error-handling)
6. [Rate Limits](#rate-limits)
7. [Examples](#examples)

---

## 🎯 Overview

The Healthcare RAG Assistant API provides evidence-based question-answering for healthcare guidelines using Retrieval-Augmented Generation (RAG).

**Key Features:**
- ✅ Semantic search over 69 healthcare guideline documents
- ✅ AI-powered answer generation (Groq Llama 3.1 8B)
- ✅ Automatic validation and confidence scoring
- ✅ Source citation tracking
- ✅ RESTful design with OpenAPI/Swagger documentation

**Interactive Documentation:**
- Swagger UI: http://localhost:9070/docs
- ReDoc: http://localhost:9070/redoc
- OpenAPI Spec: http://localhost:9070/openapi.json

---

## 🔑 Authentication

**Current Version:** No authentication required (local deployment)

**For production deployment, consider:**
- API key authentication
- OAuth 2.0
- JWT tokens

---

## 📡 Endpoints

### 1. Health Check

**GET** `/`

Check if the API is running and get system information.

**Response:**
```json
{
  "status": "running",
  "service": "Healthcare Guidelines RAG Assistant",
  "version": "0.4.0",
  "index_loaded": true,
  "num_chunks": 345,
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "embedding_dim": 384,
  "llm_model": "groq/llama-3.1-8b-instant",
  "endpoints": {
    "docs": "/docs",
    "redoc": "/redoc",
    "qa": "POST /qa",
    "qa_extractive": "POST /qa/extractive",
    "stats": "GET /stats"
  }
}
```

**cURL Example:**
```bash
curl http://localhost:9070/
```

---

### 2. Question Answering (LLM-Powered)

**POST** `/qa`

Main endpoint for asking questions about healthcare guidelines.

**Request Body:**
```json
{
  "question": "When should hand hygiene be performed?",
  "top_k": 5,
  "use_llm": true
}
```

**Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `question` | string | ✅ Yes | - | Healthcare guideline question |
| `top_k` | integer | ❌ No | 5 | Number of sources to retrieve (1-10) |
| `use_llm` | boolean | ❌ No | true | Use LLM generation (true) or extraction (false) |

**Response:**
```json
{
  "answer": "Hand hygiene should be performed before touching a patient, after touching a patient, before aseptic procedures, after body fluid exposure, and after touching patient surroundings.",
  "citations": [
    {
      "path": "cdc_hand_hygiene_2019_v7.md",
      "section": "Recommendations",
      "score": 0.862,
      "text": "- perform hand hygiene before touching a patient..."
    },
    {
      "path": "who_hand_hygiene_2020.md",
      "section": "Recommendations",
      "score": 0.862,
      "text": "- perform hand hygiene before touching a patient..."
    }
  ],
  "confidence": 0.725,
  "status": "validated",
  "generation_method": "llm"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `answer` | string | Generated answer text |
| `citations` | array | List of source documents used |
| `confidence` | float | Confidence score (0.0-1.0) |
| `status` | string | "validated" or "needs_review" |
| `generation_method` | string | "llm" or "extractive" |

**Status Codes:**
- `200 OK` - Success
- `503 Service Unavailable` - Index not loaded
- `422 Unprocessable Entity` - Invalid request format

**cURL Example:**
```bash
curl -X POST http://localhost:9070/qa \
  -H "Content-Type: application/json" \
  -d '{
    "question": "When should hand hygiene be performed?",
    "top_k": 5,
    "use_llm": true
  }'
```

---

### 3. Question Answering (Extractive Only)

**POST** `/qa/extractive`

Alternative endpoint using simple sentence extraction (no LLM).

**Request Body:**
```json
{
  "question": "What are the principles of hand hygiene?",
  "top_k": 5
}
```

**Note:** `use_llm` parameter is ignored (always false).

**Response:** Same format as `/qa` endpoint, but:
- `generation_method` will be "extractive"
- Answer will be first sentence from top source
- Typically faster but less comprehensive

**cURL Example:**
```bash
curl -X POST http://localhost:9070/qa/extractive \
  -H "Content-Type: application/json" \
  -d '{"question":"What are PPE principles?","top_k":3}'
```

---

### 4. System Statistics

**GET** `/stats`

Get detailed system statistics and configuration.

**Response:**
```json
{
  "total_chunks": 345,
  "total_documents": 69,
  "embedding_dimension": 384,
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "index_type": "FAISS IndexFlatL2 (exact search)",
  "llm_model": "groq/llama-3.1-8b-instant",
  "llm_temperature": 0.1,
  "llm_max_tokens": 300,
  "validation_threshold": 0.25,
  "performance": {
    "precision_at_5": 0.933,
    "validation_rate": 0.76,
    "mean_confidence": 0.432
  }
}
```

**cURL Example:**
```bash
curl http://localhost:9070/stats
```

---

## 📦 Request/Response Models

### QARequest
```python
{
  "question": str,      # Required: Question text
  "top_k": int,         # Optional: 1-10, default 5
  "use_llm": bool       # Optional: default true
}
```

### Citation
```python
{
  "path": str,          # Source document filename
  "section": str,       # Document section name
  "score": float,       # Relevance score (0.0-1.0)
  "text": str           # Full passage text
}
```

### QAResponse
```python
{
  "answer": str,                    # Generated answer
  "citations": List[Citation],      # Source citations
  "confidence": float,              # Confidence score (0.0-1.0)
  "status": str,                    # "validated" or "needs_review"
  "generation_method": str          # "llm" or "extractive"
}
```

---

## ⚠️ Error Handling

### Error Response Format
```json
{
  "detail": "Error description here"
}
```

### Common Errors

#### 503 Service Unavailable

**Cause:** Index not loaded

**Response:**
```json
{
  "detail": "Index not loaded. Please build index first: python app/build_index.py"
}
```

**Solution:** Run `python scripts/pipeline.py`

---

#### 422 Unprocessable Entity

**Cause:** Invalid request format

**Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "question"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Solution:** Check request body matches QARequest model

---

#### 500 Internal Server Error

**Cause:** LLM API failure or internal error

**Response:**
```json
{
  "detail": "Internal server error"
}
```

**Solution:** Check server logs, verify Groq API key

---

## 🚦 Rate Limits

### Current Limits (Groq Free Tier)

- **Requests:** Unlimited (local processing)
- **LLM calls:** Subject to Groq API limits
  - ~30 requests/minute (typical free tier)
  - Automatic retry on rate limit

### Best Practices

- Cache responses for repeated questions
- Use `/qa/extractive` for non-critical queries (no LLM call)
- Implement client-side rate limiting if needed

---

## 📚 Examples

### Example 1: Simple Question

**Request:**
```bash
curl -X POST http://localhost:9070/qa \
  -H "Content-Type: application/json" \
  -d '{
    "question": "When should hand hygiene be performed?",
    "top_k": 3
  }'
```

**Response:**
```json
{
  "answer": "Hand hygiene should be performed before touching a patient, after touching a patient, before aseptic procedures, after body fluid exposure, and after touching patient surroundings.",
  "citations": [
    {
      "path": "cdc_hand_hygiene_2019_v7.md",
      "section": "Recommendations",
      "score": 0.862
    }
  ],
  "confidence": 0.725,
  "status": "validated",
  "generation_method": "llm"
}
```

---

### Example 2: Complex Question

**Request:**
```bash
curl -X POST http://localhost:9070/qa \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How should PPE be selected based on exposure risk?",
    "top_k": 5,
    "use_llm": true
  }'
```

**Response:**
```json
{
  "answer": "PPE should be selected based on risk assessment. Use gloves, gowns, and eye protection when exposure risk exists. Don and doff safely per protocol.",
  "citations": [
    {
      "path": "cdc_ppe_2022_v6.md",
      "section": "Recommendations",
      "score": 0.911
    }
  ],
  "confidence": 0.703,
  "status": "validated",
  "generation_method": "llm"
}
```

---

### Example 3: Extractive Mode

**Request:**
```bash
curl -X POST http://localhost:9070/qa/extractive \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are environmental cleaning principles?",
    "top_k": 3
  }'
```

**Response:**
```json
{
  "answer": "- identify high-touch surfaces for routine cleaning.",
  "citations": [
    {
      "path": "who_environmental_cleaning_2019.md",
      "section": "Recommendations",
      "score": 0.892
    }
  ],
  "confidence": 1.0,
  "status": "validated",
  "generation_method": "extractive"
}
```

---

### Example 4: Python Client
```python
import requests

API_URL = "http://localhost:9070"

def ask_question(question, top_k=5):
    """Query the RAG API"""
    response = requests.post(
        f"{API_URL}/qa",
        json={
            "question": question,
            "top_k": top_k,
            "use_llm": True
        }
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code}")

# Usage
result = ask_question("When should hand hygiene be performed?")
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']}")
print(f"Status: {result['status']}")
```

---

### Example 5: JavaScript/Fetch
```javascript
async function askQuestion(question) {
  const response = await fetch('http://localhost:9070/qa', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question: question,
      top_k: 5,
      use_llm: true
    })
  });
  
  const data = await response.json();
  return data;
}

// Usage
askQuestion("What are PPE guidelines?")
  .then(result => {
    console.log("Answer:", result.answer);
    console.log("Confidence:", result.confidence);
  });
```

---

## 🔄 Versioning

**Current Version:** 0.4.0

Future versions may include:
- v0.5.0: Streaming responses
- v0.6.0: Authentication
- v1.0.0: Production-ready release

**Breaking changes will increment major version.**

---

## 📞 Support

For API issues:
1. Check `/docs` for interactive testing
2. Review `RUNBOOK.md` for operational guidance
3. See `TROUBLESHOOTING.md` for common issues

---

## 📄 License

[Your License Here]

---

**Last Updated:** February 2026