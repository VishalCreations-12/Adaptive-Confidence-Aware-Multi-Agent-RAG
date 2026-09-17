import re
import time
from typing import List, Dict, Any
from rank_bm25 import BM25Okapi

class BM25Retriever:
    """BM25 keyword-based retrieval agent."""

    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.bm25: BM25Okapi = None
        self.is_indexed = False

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Tokenize text into lowercase alphanumeric tokens."""
        return re.findall(r'\w+', text.lower())

    def fit(self, chunks: List[Dict[str, Any]]):
        """Build BM25 index from text chunks."""
        if not chunks:
            self.is_indexed = False
            return

        self.chunks = chunks
        corpus_tokens = [self._tokenize(chunk["text"]) for chunk in chunks]
        self.bm25 = BM25Okapi(corpus_tokens)
        self.is_indexed = True

    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """Search chunks using BM25 and measure latency."""
        if not self.is_indexed or not self.bm25:
            return []

        start_time = time.time()
        query_tokens = self._tokenize(query)
        
        if not query_tokens:
            return []

        scores = self.bm25.get_scores(query_tokens)
        elapsed_time_ms = (time.time() - start_time) * 1000.0

        # Zip scores with chunks
        scored_chunks = []
        for idx, score in enumerate(scores):
            chunk_copy = dict(self.chunks[idx])
            chunk_copy["bm25_score"] = float(score)
            chunk_copy["retriever"] = "bm25"
            chunk_copy["retrieval_time_ms"] = round(elapsed_time_ms, 2)
            scored_chunks.append(chunk_copy)

        # Sort descending by score
        scored_chunks.sort(key=lambda x: x["bm25_score"], reverse=True)
        return scored_chunks[:top_k]
