import time
from typing import List, Dict, Any
from src.retrieval.bm25_agent import BM25Retriever
from src.retrieval.semantic_agent import SemanticRetriever

class RRFRetriever:
    """Reciprocal Rank Fusion (RRF) retrieval baseline combining BM25 and Dense rankings."""

    def __init__(self, bm25_agent: BM25Retriever, semantic_agent: SemanticRetriever, rrf_k: int = 60):
        self.bm25_agent = bm25_agent
        self.semantic_agent = semantic_agent
        self.rrf_k = rrf_k  # Standard smoothing constant (Cormack et al., 2009)

    def search(self, query: str, top_k: int = 4, candidate_pool_size: int = 20) -> List[Dict[str, Any]]:
        """Perform Reciprocal Rank Fusion over candidate rankings.
        
        Formula:
            RRF_score(d) = sum_{m in {BM25, Dense}} 1.0 / (rrf_k + rank_m(d))
        where rank_m(d) is 1-based.
        """
        start_time = time.time()

        # Retrieve candidate pools from both retrievers
        k_pool = max(top_k * 2, candidate_pool_size)
        bm25_results = self.bm25_agent.search(query, top_k=k_pool)
        semantic_results = self.semantic_agent.search(query, top_k=k_pool)

        # Store chunk data and rank dictionaries
        chunk_map: Dict[str, Dict[str, Any]] = {}
        rrf_scores: Dict[str, float] = {}
        bm25_ranks: Dict[str, int] = {}
        semantic_ranks: Dict[str, int] = {}

        # Process BM25 rankings
        for rank, item in enumerate(bm25_results, start=1):
            cid = item["chunk_id"]
            chunk_map[cid] = item
            bm25_ranks[cid] = rank
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (self.rrf_k + rank))

        # Process Semantic rankings
        for rank, item in enumerate(semantic_results, start=1):
            cid = item["chunk_id"]
            if cid not in chunk_map:
                chunk_map[cid] = item
            semantic_ranks[cid] = rank
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (self.rrf_k + rank))

        elapsed_time_ms = (time.time() - start_time) * 1000.0

        # Construct fused results
        results = []
        for cid, score in rrf_scores.items():
            chunk_copy = dict(chunk_map[cid])
            chunk_copy["rrf_score"] = round(float(score), 6)
            chunk_copy["bm25_rank"] = bm25_ranks.get(cid, None)
            chunk_copy["semantic_rank"] = semantic_ranks.get(cid, None)
            chunk_copy["retriever"] = "rrf"
            chunk_copy["retrieval_time_ms"] = round(elapsed_time_ms, 2)
            results.append(chunk_copy)

        # Sort descending by RRF score
        results.sort(key=lambda x: x["rrf_score"], reverse=True)
        return results[:top_k]
