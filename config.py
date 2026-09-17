import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Directory paths
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
MEMORY_DIR = BASE_DIR / "data" / "memory"
CACHE_DIR = BASE_DIR / "data" / "cache"

# Ensure required directories exist
SAMPLE_DATA_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Sample file locations
SAMPLE_PDF_PATH = SAMPLE_DATA_DIR / "NovaTech_Research_Knowledge_Base.pdf"
SAMPLE_QUESTIONS_PATH = SAMPLE_DATA_DIR / "test_questions.txt"
MEMORY_FILE_PATH = MEMORY_DIR / "retrieval_strategy_memory.json"

# Ingestion settings
CHUNK_SIZE = 500  # character count per chunk
CHUNK_OVERLAP = 100
MIN_CHUNK_LEN = 30

# Model settings
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K_RETRIEVAL = 4

# Retriever defaults
DEFAULT_HYBRID_ALPHA = 0.5  # Weight for BM25
DEFAULT_HYBRID_BETA = 0.5   # Weight for Semantic

# Confidence calculation weights
CONFIDENCE_WEIGHTS = {
    "score_strength": 0.35,
    "consensus_ratio": 0.25,
    "keyword_coverage": 0.25,
    "score_spread": 0.15
}
