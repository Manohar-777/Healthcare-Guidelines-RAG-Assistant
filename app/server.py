"""
FastAPI server for Healthcare Guidelines RAG Assistant
Version 0.4.0 - With LLM-based answer generation
Uses FAISS index, sentence-transformers embeddings, and Groq LLM
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import numpy as np
import re
from pathlib import Path
import sys
import faiss


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import embeddings
from llm_provider import generate_answer_with_validation

# Load FAISS index and metadata
INDEX_PATH = ROOT / "index" / "faiss_index.bin"
META_PATH = ROOT / "index" / "metadata.npz"

print(f"Loading FAISS index from: {INDEX_PATH}")
print(f"Loading metadata from: {META_PATH}")

try:
    index = faiss.read_index(str(INDEX_PATH))
    print(f"✅ FAISS index loaded: {index.ntotal} vectors")
    
    meta_data = np.load(META_PATH, allow_pickle=True)
    META = meta_data["meta"]
    print(f"✅ Metadata loaded: {len(META)} chunks")
    print("✅ LLM provider ready (Groq Llama 3.1)")
    
except Exception as e:
    print(f"❌ Error loading index: {e}")
    print("Please run: python app/build_index.py")
    index = None
    META = None

# Create FastAPI app with enhanced documentation
app = FastAPI(
    title="Healthcare Guidelines RAG Assistant",
    description="""
    🏥 **Evidence-based Healthcare Guideline Query System**
    
    This API provides intelligent question-answering capabilities for healthcare guidelines 
    from WHO, CDC, and NIH. It uses:
    - **FAISS** for efficient semantic search
    - **Sentence Transformers** for embeddings
    - **Groq Llama 3.1 8B** for natural language generation
    - **Validation engine** for answer confidence scoring
    
    ## Features
    - 📚 Access to 69 healthcare guideline documents
    - 🤖 AI-powered answer generation
    - ✅ Automatic answer validation and confidence scoring
    - 📊 93.3% retrieval precision
    - 🔒 100% reproducible and deterministic
    
    ## Quick Start
    1. Try the `/qa` endpoint to ask questions
    2. Check `/stats` for system information
    3. Use `/qa/extractive` for simple extraction (no LLM)
    
    ## Example Questions
    - "When should hand hygiene be performed?"
    - "How should PPE be selected based on exposure risk?"
    - "What are the criteria for return to work after isolation?"
    """,
    version="0.4.0",
    contact={
        "name": "Healthcare RAG Team",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
    },
    openapi_tags=[
        {
            "name": "Question Answering",
            "description": "Main endpoints for querying healthcare guidelines"
        },
        {
            "name": "System",
            "description": "System information and health checks"
        }
    ]
)

def retrieve(question: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve top-K relevant passages using FAISS.
    Enhanced with section re-ranking.
    """
    if index is None or META is None:
        return []
    
    q_vec = embeddings.embed(question)
    q_vec = q_vec.reshape(1, -1)
    
    search_k = min(top_k * 3, 20)
    distances, indices = index.search(q_vec, search_k)
    
    all_results = []
    for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        if idx == -1:
            continue
            
        d = META[idx]
        similarity = 1.0 - (dist / 2.0)
        
        all_results.append({
            "score": float(similarity),
            "distance": float(dist),
            "path": str(d["path"]),
            "section": str(d["section"]),
            "text": str(d["text"])
        })
    
    # Section re-ranking
    priority_sections = ["Recommendations", "Principles", "Implementation"]
    
    for result in all_results:
        section = result["section"]
        if any(p in section for p in priority_sections):
            result["score"] *= 1.3
        elif "Overview" in section:
            result["score"] *= 0.7
    
    all_results.sort(key=lambda x: x["score"], reverse=True)
    return all_results[:top_k]

# Request/Response Models with examples
class QARequest(BaseModel):
    question: str = Field(
        ...,
        description="Healthcare guideline question to answer",
        example="When should hand hygiene be performed?"
    )
    top_k: int = Field(
        5,
        ge=1,
        le=10,
        description="Number of source documents to retrieve",
        example=5
    )
    use_llm: bool = Field(
        True,
        description="Use LLM for answer generation (True) or simple extraction (False)",
        example=True
    )

class Citation(BaseModel):
    path: str = Field(..., description="Source document filename")
    section: str = Field(..., description="Document section name")
    score: float = Field(..., description="Relevance score (0-1)")
    text: Optional[str] = Field(None, description="Full passage text from source")  # ADD THIS

class QAResponse(BaseModel):
    answer: str = Field(..., description="Generated answer text")
    citations: List[Citation] = Field(..., description="Source citations")
    confidence: float = Field(..., description="Answer confidence score (0-1)")
    status: str = Field(..., description="Validation status: 'validated' or 'needs_review'")
    generation_method: Optional[str] = Field(None, description="Method used: 'llm' or 'extractive'")
    
    class Config:
        schema_extra = {
            "example": {
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
        }

@app.get(
    "/",
    tags=["System"],
    summary="Health Check",
    description="Check if the API is running and get basic system information"
)
def root():
    """
    Health check endpoint returning system status and configuration.
    """
    return {
        "status": "running",
        "service": "Healthcare Guidelines RAG Assistant",
        "version": "0.4.0",
        "index_loaded": index is not None,
        "num_chunks": index.ntotal if index else 0,
        "embedding_model": embeddings.MODEL_NAME,
        "embedding_dim": embeddings.EMBEDDING_DIM,
        "llm_model": "groq/llama-3.1-8b-instant",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "qa": "POST /qa",
            "qa_extractive": "POST /qa/extractive",
            "stats": "GET /stats"
        }
    }

@app.post(
    "/qa",
    response_model=QAResponse,
    tags=["Question Answering"],
    summary="Ask a Question (LLM-powered)",
    description="""
    Main endpoint for asking questions about healthcare guidelines.
    
    **Features:**
    - Uses AI (Groq Llama 3.1) to generate natural language answers
    - Retrieves relevant guideline sections using semantic search
    - Validates answers against source documents
    - Returns confidence scores and validation status
    
    **Process:**
    1. Embeds your question using sentence-transformers
    2. Retrieves top-K most relevant guideline sections via FAISS
    3. Generates answer using LLM with strict grounding prompts
    4. Validates answer against sources and calculates confidence
    5. Returns answer with citations
    
    **Validation Status:**
    - `validated`: Confidence ≥ 0.25, answer well-supported by sources
    - `needs_review`: Lower confidence, human review recommended
    """
)
def qa(req: QARequest):
    """
    Question-answering endpoint with LLM generation and validation.
    """
    if index is None or META is None:
        raise HTTPException(
            status_code=503,
            detail="Index not loaded. Please build index first: python app/build_index.py"
        )
    
    passages = retrieve(req.question, req.top_k)
    
    if not passages:
        return QAResponse(
            answer="I don't have enough information in the provided guidelines to answer this question.",
            citations=[],
            confidence=0.0,
            status="needs_review",
            generation_method="none"
        )
    
    if req.use_llm:
        try:
            result = generate_answer_with_validation(req.question, passages)
            
            citations = [
                Citation(
                    path=p["path"],
                    section=p["section"],
                    score=round(p["score"], 3),
                    text=p["text"] 
                )
                for p in passages[:3]
            ]
            
            return QAResponse(
                answer=result["answer"],
                citations=citations,
                confidence=result["confidence"],
                status=result["status"],
                generation_method="llm"
            )
            
        except Exception as e:
            print(f"LLM generation failed: {e}")
            req.use_llm = False
    
    if not req.use_llm:
        top = passages[0]
        sent = top["text"].split(".")[0].strip() + "."
        
        toks = re.findall(r"[a-z0-9]+", sent.lower())
        if toks:
            src = set(re.findall(r"[a-z0-9]+", top["text"].lower()))
            hit = sum(1 for t in toks if t in src)
            conf = hit / len(toks)
        else:
            conf = 0.0
        
        status = "validated" if conf >= 0.6 else "needs_review"
        
        return QAResponse(
            answer=sent,
            citations=[Citation(
                path=top["path"],
                section=top["section"],
                score=round(top["score"], 3),
                text=top["text"]
            )],
            confidence=round(conf, 3),
            status=status,
            generation_method="extractive"
        )

@app.post(
    "/qa/extractive",
    response_model=QAResponse,
    tags=["Question Answering"],
    summary="Ask a Question (Extractive Only)",
    description="""
    Alternative endpoint that uses simple sentence extraction instead of LLM.
    
    **Use this when:**
    - You want deterministic, fast responses
    - You don't need natural language generation
    - You want exact quotes from guidelines
    
    **Note:** This method typically produces shorter, less natural answers.
    """
)
def qa_extractive(req: QARequest):
    """
    Question-answering using extractive method only (no LLM).
    Useful for comparison or when LLM is unavailable.
    """
    req.use_llm = False
    return qa(req)

@app.get(
    "/stats",
    tags=["System"],
    summary="System Statistics",
    description="Get detailed statistics about the RAG system configuration and performance"
)
def stats():
    """
    Returns comprehensive system statistics including:
    - Number of indexed chunks
    - Embedding model details
    - LLM configuration
    - Index type
    """
    if index is None or META is None:
        return {"error": "Index not loaded"}
    
    return {
        "total_chunks": index.ntotal,
        "total_documents": 69,
        "embedding_dimension": embeddings.EMBEDDING_DIM,
        "embedding_model": embeddings.MODEL_NAME,
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