import time
from typing import List, Dict, Any
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import config

class SemanticRetriever:
    """Semantic vector-based retrieval agent using SentenceTransformers & FAISS."""

    def __init__(self, model_name: str = config.EMBEDDING_MODEL_NAME):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks: List[Dict[str, Any]] = []
        self.is_indexed = False

    def fit(self, chunks: List[Dict[str, Any]]):
        """Encode text chunks and populate FAISS index."""
        if not chunks:
            self.is_indexed = False
            return

        self.chunks = chunks
        texts = [chunk["text"] for chunk in chunks]
        
        # Generate embeddings and normalize for Cosine Similarity (Inner Product)
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        self.is_indexed = True

    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """Perform semantic search using FAISS index."""
        if not self.is_indexed or self.index is None:
            return []

        start_time = time.time()
        
        query_embedding = self.model.encode([query], convert_to_numpy=True, show_progress_bar=False)
        faiss.normalize_L2(query_embedding)

        k = min(top_k, len(self.chunks))
        scores, indices = self.index.search(query_embedding, k)
        elapsed_time_ms = (time.time() - start_time) * 1000.0

        results = []
        for rank, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.chunks):
                continue
            chunk_copy = dict(self.chunks[idx])
            raw_sim = float(scores[0][rank])
            # Clamp cosine similarity to [0.0, 1.0] for display
            chunk_copy["similarity_score"] = round(max(0.0, min(1.0, raw_sim)), 4)
            chunk_copy["retriever"] = "semantic"
            chunk_copy["retrieval_time_ms"] = round(elapsed_time_ms, 2)
            results.append(chunk_copy)

        return results
