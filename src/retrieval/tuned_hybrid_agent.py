import time
from typing import List, Dict, Any, Tuple
from src.retrieval.bm25_agent import BM25Retriever
from src.retrieval.semantic_agent import SemanticRetriever
from src.retrieval.hybrid_agent import HybridRetriever
from src.evaluation.metrics_calculator import RAGMetricsCalculator

class TunedHybridRetriever:
    """Tuned Hybrid Retriever with validation-optimized fusion weights.
    
    Weights alpha (BM25) and beta (Semantic) are optimized via grid search on
    training/validation queries, then frozen before test evaluation.
    """

    def __init__(
        self,
        bm25_agent: BM25Retriever,
        semantic_agent: SemanticRetriever,
        best_alpha: float = 0.5,
        best_beta: float = 0.5
    ):
        self.bm25_agent = bm25_agent
        self.semantic_agent = semantic_agent
        self.hybrid_agent = HybridRetriever(bm25_agent, semantic_agent)
        self.best_alpha = best_alpha
        self.best_beta = best_beta
        self.is_tuned = False
        self.tuning_history: List[Dict[str, Any]] = []

    def fit_weights(
        self,
        val_queries: List[Dict[str, Any]],
        alpha_candidates: List[float] = None,
        target_metric: str = "ndcg_at_k"
    ) -> Tuple[float, float]:
        """Perform grid search over (alpha, 1 - alpha) on validation queries.
        
        Args:
            val_queries: List of validation query dicts with 'query' and 'relevant_chunk_ids'.
            alpha_candidates: List of alpha weights to test (default: [0.1, 0.2, ..., 0.9]).
            target_metric: Metric to optimize ('ndcg_at_k' or 'precision_at_k').
            
        Returns:
            Tuple of (optimal_alpha, optimal_beta).
        """
        if not val_queries:
            self.is_tuned = False
            return self.best_alpha, self.best_beta

        candidates = alpha_candidates or [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        best_score = -1.0
        best_a = 0.5
        best_b = 0.5
        self.tuning_history = []

        for alpha in candidates:
            beta = round(1.0 - alpha, 2)
            scores = []

            for q_item in val_queries:
                query = q_item["query"]
                rel_ids = q_item["relevant_chunk_ids"]
                res = self.hybrid_agent.search(query, top_k=3, alpha=alpha, beta=beta)
                retrieved_ids = [c["chunk_id"] for c in res]

                if target_metric == "precision_at_k":
                    score = RAGMetricsCalculator.calculate_precision_at_k(retrieved_ids, rel_ids, k=3)
                else:
                    score = RAGMetricsCalculator.calculate_ndcg_at_k(retrieved_ids, rel_ids, k=3)
                scores.append(score)

            mean_score = sum(scores) / len(scores) if scores else 0.0
            self.tuning_history.append({
                "alpha": alpha,
                "beta": beta,
                f"mean_{target_metric}": round(mean_score, 4)
            })

            if mean_score > best_score:
                best_score = mean_score
                best_a = alpha
                best_b = beta

        self.best_alpha = best_a
        self.best_beta = best_b
        self.is_tuned = True
        return self.best_alpha, self.best_beta

    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """Search using the frozen, validation-tuned weights."""
        results = self.hybrid_agent.search(query, top_k=top_k, alpha=self.best_alpha, beta=self.best_beta)
        for r in results:
            r["retriever"] = "tuned_hybrid"
            r["tuned_alpha"] = self.best_alpha
            r["tuned_beta"] = self.best_beta
        return results
