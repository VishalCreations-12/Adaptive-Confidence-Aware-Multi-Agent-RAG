import time
from typing import List, Dict, Any
from src.retrieval.bm25_agent import BM25Retriever
from src.retrieval.semantic_agent import SemanticRetriever
import config

class HybridRetriever:
    """Hybrid retrieval agent combining BM25 keyword and Semantic vector search."""

    def __init__(self, bm25_agent: BM25Retriever, semantic_agent: SemanticRetriever):
        self.bm25_agent = bm25_agent
        self.semantic_agent = semantic_agent

    @staticmethod
    def _normalize_scores(scores: List[float]) -> List[float]:
        """MinMax normalization to scale scores to [0, 1]."""
        if not scores:
            return []
        min_s = min(scores)
        max_s = max(scores)
        if max_s - min_s < 1e-6:
            return [1.0 if max_s > 0 else 0.0 for _ in scores]
        return [(s - min_s) / (max_s - min_s) for s in scores]

    def search(
        self,
        query: str,
        top_k: int = 4,
        alpha: float = config.DEFAULT_HYBRID_ALPHA,
        beta: float = config.DEFAULT_HYBRID_BETA
    ) -> List[Dict[str, Any]]:
        """Combine BM25 and Semantic search results using MinMax score fusion."""
        start_time = time.time()

        # Retrieve larger pool from both agents for effective fusion
        candidate_k = max(top_k * 2, len(self.bm25_agent.chunks))
        bm25_results = self.bm25_agent.search(query, top_k=candidate_k)
        semantic_results = self.semantic_agent.search(query, top_k=candidate_k)

        # Build lookup maps by chunk_id
        chunk_map: Dict[str, Dict[str, Any]] = {}
        bm25_scores_map: Dict[str, float] = {}
        semantic_scores_map: Dict[str, float] = {}

        for item in bm25_results:
            cid = item["chunk_id"]
            chunk_map[cid] = item
            bm25_scores_map[cid] = item["bm25_score"]

        for item in semantic_results:
            cid = item["chunk_id"]
            if cid not in chunk_map:
                chunk_map[cid] = item
            semantic_scores_map[cid] = item["similarity_score"]

        all_chunk_ids = list(chunk_map.keys())
        if not all_chunk_ids:
            return []

        # Get raw score lists for active chunks
        raw_bm25 = [bm25_scores_map.get(cid, 0.0) for cid in all_chunk_ids]
        raw_sem = [semantic_scores_map.get(cid, 0.0) for cid in all_chunk_ids]

        # MinMax normalize scores
        norm_bm25 = self._normalize_scores(raw_bm25)
        norm_sem = self._normalize_scores(raw_sem)

        elapsed_time_ms = (time.time() - start_time) * 1000.0

        hybrid_results = []
        for idx, cid in enumerate(all_chunk_ids):
            chunk = dict(chunk_map[cid])
            b_norm = norm_bm25[idx]
            s_norm = norm_sem[idx]
            combined_score = (alpha * b_norm) + (beta * s_norm)

            chunk["bm25_component"] = round(float(raw_bm25[idx]), 3)
            chunk["bm25_norm"] = round(float(b_norm), 3)
            chunk["semantic_component"] = round(float(raw_sem[idx]), 3)
            chunk["semantic_norm"] = round(float(s_norm), 3)
            chunk["combined_score"] = round(float(combined_score), 4)
            chunk["retriever"] = "hybrid"
            chunk["retrieval_time_ms"] = round(elapsed_time_ms, 2)
            hybrid_results.append(chunk)

        # Sort descending by combined score
        hybrid_results.sort(key=lambda x: x["combined_score"], reverse=True)
        return hybrid_results[:top_k]
