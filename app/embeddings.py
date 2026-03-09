"""
Embeddings module using sentence-transformers
Provides deterministic, reproducible embeddings without external API calls
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Union
import os

# Model configuration
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384  # Dimension for all-MiniLM-L6-v2

# Cache directory to ensure reproducibility
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(CACHE_DIR, exist_ok=True)

# Load model once (singleton pattern)
_model = None

def get_model():
    """Get or initialize the sentence transformer model."""
    global _model
    if _model is None:
        print(f"Loading embedding model: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME, cache_folder=CACHE_DIR)
        print(f"✅ Model loaded. Embedding dimension: {EMBEDDING_DIM}")
    return _model

def embed(text: str) -> np.ndarray:
    """
    Generate embedding for a single text.
    
    Args:
        text: Input text string
        
    Returns:
        numpy array of shape (EMBEDDING_DIM,)
    """
    model = get_model()
    # Encode returns normalized embeddings by default
    embedding = model.encode(text, normalize_embeddings=True, show_progress_bar=False)
    return embedding.astype(np.float32)

def embed_batch(texts: List[str], batch_size: int = 32, show_progress: bool = True) -> np.ndarray:
    """
    Generate embeddings for a batch of texts.
    
    Args:
        texts: List of text strings
        batch_size: Batch size for encoding
        show_progress: Whether to show progress bar
        
    Returns:
        numpy array of shape (len(texts), EMBEDDING_DIM)
    """
    model = get_model()
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,
        show_progress_bar=show_progress,
        convert_to_numpy=True
    )
    return embeddings.astype(np.float32)

# Backward compatibility: expose dimension
DIM = EMBEDDING_DIM

if __name__ == "__main__":
    # Test the embeddings
    print("Testing embeddings module...")
    
    test_text = "When should hand hygiene be performed?"
    vec = embed(test_text)
    print(f"\nSingle embedding test:")
    print(f"  Input: '{test_text}'")
    print(f"  Shape: {vec.shape}")
    print(f"  Norm: {np.linalg.norm(vec):.4f} (should be ~1.0)")
    
    test_batch = [
        "PPE guidelines for healthcare workers",
        "Hand hygiene protocols",
        "Vaccination procedures"
    ]
    batch_vecs = embed_batch(test_batch)
    print(f"\nBatch embedding test:")
    print(f"  Inputs: {len(test_batch)} texts")
    print(f"  Shape: {batch_vecs.shape}")
    print(f"  All normalized: {np.allclose(np.linalg.norm(batch_vecs, axis=1), 1.0)}")