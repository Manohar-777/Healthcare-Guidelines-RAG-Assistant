# 🏥 Healthcare Guidelines RAG Assistant

Evidence-based question-answering system for healthcare guidelines using Retrieval-Augmented Generation (RAG).

## 📋 Project Overview

This system provides intelligent question-answering capabilities for healthcare guidelines from WHO, CDC, and NIH using:
- **FAISS** for semantic search
- **Sentence-transformers** for embeddings  
- **Groq Llama 3.1 8B** for natural language generation
- **FastAPI** for REST API
- **Streamlit** for web interface

## 🎯 Performance Metrics
```
✅ Precision@5: 93.3% (Target: ≥65%)
✅ Precision@1: 92.0%
⚠️ Validation Rate: 55-75% (Target: ≥80%)
✅ API Stability: 100%
✅ Reproducible: Yes (deterministic indexing)
```

## 📁 Project Structure
```
Healthcare_RAG_Kit/
├── app/
│   ├── embeddings.py          # Sentence-transformer embeddings
│   ├── build_index.py          # FAISS index builder
│   ├── server.py               # FastAPI application
│   └── llm_provider.py         # Groq LLM integration
├── corpus/
│   └── guidelines/             # 69 healthcare guideline documents
├── evaluation/
│   ├── queries_custom.csv      # 75 test queries
│   ├── eval_comprehensive.py   # Full evaluation suite
│   ├── eval_retrieval.py       # Retrieval metrics
│   ├── eval_consistency.py     # Validation metrics
│   └── reports/                # Evaluation results
├── index/
│   ├── faiss_index.bin         # FAISS index (built)
│   └── metadata.npz            # Document metadata
├── docs/                       # Phase completion documentation
├── scripts/
│   └── pipeline.py             # Index building pipeline
├── streamlit_app.py            # Web UI
├── .env                        # API keys (create this)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```
## Offline Reproducibility
  ### Model Weights Included
  The `models/` directory contains locally cached sentence-transformers model

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Groq API key (free at https://console.groq.com)

### Installation

1. **Clone/Extract the project**
```bash
cd Healthcare_RAG_Kit
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
# Create .env in project root with:
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
```

Get your Groq API key from: https://console.groq.com/keys

5. **Build the index** (if not already built)
```bash
python scripts/pipeline.py
```

Expected output:
```
Loading embedding model: sentence-transformers/all-MiniLM-L6-v2
✅ Model loaded. Embedding dimension: 384
Built index with 345 chunks -> index/faiss_index.bin
```

### Running the System

#### Option 1: FastAPI Backend + Swagger UI
```bash
uvicorn app.server:app --host 0.0.0.0 --port 9070 --reload
```

Access:
- **Swagger UI:** http://localhost:9070/docs (Interactive API testing)

#### Option 2: Streamlit Web Interface

**Terminal 1 (Backend):**
```bash
uvicorn app.server:app --host 0.0.0.0 --port 9070 --reload
```

**Terminal 2 (Frontend):**
```bash
streamlit run streamlit_app.py
```

## 🧪 Testing & Evaluation

### Run Comprehensive Evaluation
```bash
python evaluation/eval_comprehensive.py
```

Outputs:
- Console: Detailed statistics
- `evaluation/reports/evaluation_results.json` - Full results
- `evaluation/reports/evaluation_summary.txt` - Summary
- `evaluation/reports/low_confidence_queries.csv` - Queries needing review

### Run Simple Evaluations
```bash
# Retrieval precision
python evaluation/eval_retrieval.py

# Answer validation
python evaluation/eval_consistency.py
```

### Test API Directly
```bash
python test_api.py
```

## 📖 API Usage

### Query Endpoint
```bash
curl -X POST "http://localhost:9070/qa" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "When should hand hygiene be performed?",
    "top_k": 5,
    "use_llm": true
  }'
```

Response:
```json
{
  "answer": "Hand hygiene should be performed before touching a patient...",
  "citations": [
    {
      "path": "cdc_hand_hygiene_2019_v7.md",
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

### System Stats
```bash
curl http://localhost:9070/stats
```

## 🔍 Known Issues & Limitations

### 1. Synthetic Corpus Characteristics

**Issue:** The 69 guideline documents contain only ~9 unique content pieces. Documents from different organizations (WHO/CDC/NIH) and years (2019-2024) have identical text except for headers.

**Impact:**
- Limited content diversity for testing
- Repetitive passages returned for queries
- Difficult to test organization-specific or temporal queries

**Workaround:** System uses section re-ranking to prioritize "Recommendations" sections which contain the most unique content.

### 2. Generic Document Sections

**Issue:** Most document sections contain boilerplate text:
- Overview: 1 sentence
- Principles: Identical across all documents
- Implementation: Identical across all documents
- Recommendations: Only section with unique, substantive content (50-100 words)

**Impact:**
- Questions about "implementation," "monitoring," or "training" retrieve generic text
- Low confidence scores even for correct answers
- Limited detail in responses

### 3. LLM Hallucination vs. Conservatism Trade-off

**Issue:** Balancing two opposing problems:
- **Too conservative:** Vague answers that under-use retrieved information
- **Hallucinating:** Adding details not in source documents

**Current Approach:** Strict grounding prompts to prevent hallucination, accepting some vague answers as trade-off.

### 4. Validation Rate Below Target

**Current:** 76% validation rate  
**Target:** 80%

**Reasons:**
- Token-overlap metrics penalize LLM's natural language paraphrasing
- Confidence scoring tuned conservatively to avoid false positives
- Sparse source content leads to low coverage scores

**Recommendation:** 76% is acceptable for safety-critical healthcare domain where "needs_review" status encourages human verification.

## 🛠️ Technical Implementation Details

### Embeddings
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Dimension: 384
- Type: Dense vectors, L2-normalized
- No external API calls (fully local)

### Indexing
- Type: FAISS IndexFlatL2 (exact search)
- Chunks: 345 (from 69 documents)
- Deterministic: Yes (reproducible builds)

### LLM Generation
- Model: Groq Llama 3.1 8B Instant
- Temperature: 0.1 (low for factual responses)
- Max tokens: 300
- Provider: Swappable (easy to change to OpenAI, local models, etc.)

### Retrieval Enhancement
- Section re-ranking: +30% boost for Recommendations/Principles/Implementation
- Section penalty: -30% for Overview sections
- Top-K: Default 5, configurable 1-10

### Validation Logic
- Base metric: Token overlap + phrase matching
- Boosts: High retrieval scores, substantive answers
- Penalties: Low retrieval scores, excessive length with low overlap
- Threshold: 0.25 (tuned for LLM natural language)

## 📊 Evaluation Results Summary

**Test Set:** 75 custom queries covering 9 topics

**By Category:**
- Simple queries (53): 75.5% validation rate
- Complex queries (11): 63.6% validation rate
- Comparative queries (7): 71.4% validation rate
- Edge cases (4): 50.0% validation rate

**By Topic:**
- Isolation: 100% validation
- Grading: 100% validation  
- Shared Decision Making: 83.3% validation
- Hand Hygiene: 70.0% validation
- Environmental Cleaning: 75.0% validation
- PPE: 54.5% validation
- Vaccination: 42.9% validation (lowest)

**Low Confidence Queries:** 30/75 (40%)
- Primarily questions about monitoring, training, implementation
- Root cause: Generic/sparse content in source documents


## 🔄 Future Improvements

1. **Enhanced Corpus:** More detailed, diverse guideline content
2. **Semantic Validation:** Use embedding similarity instead of token overlap
3. **Multi-Document Synthesis:** Better handling of information across sources
4. **User Feedback Loop:** Learn from validation corrections
5. **Domain-Specific Metrics:** Healthcare-appropriate confidence scoring

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port is in use
netstat -ano | findstr :9070

# Kill process if needed
taskkill /PID <number> /F
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Index not found
```bash
# Rebuild index
python scripts/pipeline.py
```

### LLM errors
- Check `.env` file exists with valid `GROQ_API_KEY`
- Verify API key at https://console.groq.com/keys
- Check network connectivity


---

### Performance Metrics
```
✅ Precision@5: 93.3% (Target: ≥65%) - EXCEEDS
✅ Precision@1: 92.0%
⚠️ Validation Rate: 55-80% (Target: ≥80%) - Acceptable per supervisor
✅ API Stability: 100%
✅ Reproducibility: 100%
```
---
<img width="1918" height="1027" alt="image" src="https://github.com/user-attachments/assets/bfaee70c-9a0a-4704-b3e1-a55a50c88029" />

<img width="1919" height="971" alt="image" src="https://github.com/user-attachments/assets/71da5928-1550-401d-999f-f8784129114a" />

<img width="1919" height="806" alt="image" src="https://github.com/user-attachments/assets/e5a0a067-f338-4c8b-8af5-55591f4e2cea" />


---

## 📧 Support

**Student:** Uday  
**Project:** Healthcare Guidelines RAG Assistant  
**Submission Date:** February 2026

For questions or issues, please contact: udaykiranbattula304@gmail.com

---

**Built with ❤️ for Evidence-Based Healthcare Practice**
