"""
Build FAISS index from corpus documents
Uses sentence-transformers for embeddings and FAISS for efficient retrieval
"""

import re
import numpy as np
from pathlib import Path
import sys
import os
import faiss


ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT / "app"))

import embeddings

CORPUS = ROOT / "corpus" / "guidelines"
INDEX_DIR = ROOT / "index"
INDEX_PATH = INDEX_DIR / "faiss_index.bin"
META_PATH = INDEX_DIR / "metadata.npz"

def load_chunks():
    """
    Load and chunk all guideline documents.
    
    Returns:
        List of dicts with keys: path, title, section, text
    """
    docs = []
    
    for p in sorted(CORPUS.glob("*.md")):
        try:
            text = p.read_text(encoding='utf-8')
        except:
            text = p.read_text(encoding='latin-1')
        
        # Split by section headers
        parts = re.split("\n(?=## )", text)
        title = parts[0].splitlines()[0].strip("# ").strip()
        section = "Preamble"
        buf = []
        
        for part in parts:
            if part.startswith("## "):
                # Save previous section
                if buf:
                    docs.append({
                        "path": p.name,
                        "title": title,
                        "section": section,
                        "text": "\n".join(buf).strip()
                    })
                
                # Start new section
                lines = part.splitlines()
                section = lines[0].replace("## ", "").strip()
                buf = lines[1:]
            else:
                buf = part.splitlines()[1:]
        
        # Save last section
        if buf:
            docs.append({
                "path": p.name,
                "title": title,
                "section": section,
                "text": "\n".join(buf).strip()
            })
    
    return docs

def build_faiss_index(embeddings_matrix: np.ndarray) -> faiss.Index:
    """
    Build FAISS index from embeddings.
    
    Args:
        embeddings_matrix: numpy array of shape (n_docs, embedding_dim)
        
    Returns:
        FAISS index
    """
    dimension = embeddings_matrix.shape[1]
    
    # Use IndexFlatL2 for exact search (deterministic, reproducible)
    # L2 distance is used, but since embeddings are normalized,
    # this is equivalent to cosine similarity
    index = faiss.IndexFlatL2(dimension)
    
    # Add vectors to index
    index.add(embeddings_matrix)
    
    return index

def main():
    """Main function to build and save index."""
    
    # Create index directory
    os.makedirs(INDEX_DIR, exist_ok=True)
    
    print("="*60)
    print("Building FAISS Index with Sentence Transformers")
    print("="*60)
    
    # Load documents
    print("\n1. Loading and chunking documents...")
    docs = load_chunks()
    print(f"   ✅ Loaded {len(docs)} chunks from {len(list(CORPUS.glob('*.md')))} documents")
    
    # Generate embeddings
    print(f"\n2. Generating embeddings (dimension: {embeddings.EMBEDDING_DIM})...")
    texts = [d["text"] for d in docs]
    X = embeddings.embed_batch(texts, batch_size=32, show_progress=True)
    print(f"   ✅ Generated embeddings: {X.shape}")
    
    # Build FAISS index
    print("\n3. Building FAISS index...")
    index = build_faiss_index(X)
    print(f"   ✅ Index built: {index.ntotal} vectors")
    
    # Save FAISS index
    print(f"\n4. Saving index to {INDEX_PATH}...")
    faiss.write_index(index, str(INDEX_PATH))
    print(f"   ✅ FAISS index saved")
    
    # Save metadata
    print(f"\n5. Saving metadata to {META_PATH}...")
    np.savez_compressed(META_PATH, meta=np.array(docs, dtype=object))
    print(f"   ✅ Metadata saved")
    
    print("\n" + "="*60)
    print("✅ Index building complete!")
    print("="*60)
    print(f"\nIndex statistics:")
    print(f"  - Documents: {len(list(CORPUS.glob('*.md')))}")
    print(f"  - Chunks: {len(docs)}")
    print(f"  - Embedding dimension: {embeddings.EMBEDDING_DIM}")
    print(f"  - Index type: FAISS IndexFlatL2 (exact search)")
    print(f"  - Index size: {index.ntotal} vectors")
    print(f"\nFiles created:")
    print(f"  - {INDEX_PATH}")
    print(f"  - {META_PATH}")

if __name__ == "__main__":
    main()