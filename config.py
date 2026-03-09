from pathlib import Path

# Project paths
ROOT = Path(__file__).parent
CORPUS_DIR = ROOT / "corpus" / "guidelines"
INDEX_DIR = ROOT / "index"
EVAL_DIR = ROOT / "evaluation"
OUTPUT_DIR = ROOT / "outputs"
LOG_DIR = ROOT / "logs"

# Model configurations
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2" 
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 dimension

# RAG configurations
DEFAULT_TOP_K = 5
CONFIDENCE_THRESHOLD = 0.6

# API configurations
API_HOST = "0.0.0.0"
API_PORT = 9070

# LLM configurations (for Phase 4)
LLM_PROVIDER = "grok"  
LLM_MODEL = "grok-beta"
LLM_MAX_TOKENS = 500

# Evaluation configurations
MIN_TEST_QUERIES = 30
TARGET_PRECISION_AT_5 = 0.65
TARGET_PASS_RATE = 0.80