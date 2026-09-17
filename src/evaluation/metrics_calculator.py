import math
from typing import List, Dict, Any, Set

class RAGMetricsCalculator:
    """Formal research metrics calculation engine for RAG and Retrieval evaluation."""

    @staticmethod
    def calculate_precision_at_k(retrieved_ids: List[str], relevant_ids: List[str], k: int = 3) -> float:
        """Calculate Precision@K."""
        if k <= 0 or not retrieved_ids:
            return 0.0
        
        top_k_retrieved = retrieved_ids[:k]
        relevant_set = set(relevant_ids)
        
        if not relevant_set:
            return 0.0

        hits = sum(1 for cid in top_k_retrieved if cid in relevant_set)
        return round(hits / float(k), 4)

    @staticmethod
    def calculate_recall_at_k(retrieved_ids: List[str], relevant_ids: List[str], k: int = 3) -> float:
        """Calculate Recall@K."""
        if k <= 0 or not retrieved_ids or not relevant_ids:
            return 0.0

        top_k_retrieved = retrieved_ids[:k]
        relevant_set = set(relevant_ids)
        
        hits = sum(1 for cid in top_k_retrieved if cid in relevant_set)
        return round(hits / float(len(relevant_set)), 4)

    @staticmethod
    def calculate_mrr(retrieved_ids: List[str], relevant_ids: List[str]) -> float:
        """Calculate Mean Reciprocal Rank (MRR)."""
        if not retrieved_ids or not relevant_ids:
            return 0.0

        relevant_set = set(relevant_ids)
        for rank, cid in enumerate(retrieved_ids, start=1):
            if cid in relevant_set:
                return round(1.0 / rank, 4)
        return 0.0

    @staticmethod
    def calculate_ndcg_at_k(retrieved_ids: List[str], relevant_ids: List[str], k: int = 3) -> float:
        """Calculate Normalized Discounted Cumulative Gain at K (nDCG@K)."""
        if k <= 0 or not retrieved_ids or not relevant_ids:
            return 0.0

        top_k_retrieved = retrieved_ids[:k]
        relevant_set = set(relevant_ids)

        # Discounted Cumulative Gain (DCG)
        dcg = 0.0
        for i, cid in enumerate(top_k_retrieved, start=1):
            rel = 1.0 if cid in relevant_set else 0.0
            dcg += rel / math.log2(i + 1)

        # Ideal Discounted Cumulative Gain (IDCG)
        idcg = 0.0
        ideal_rel_count = min(k, len(relevant_set))
        for i in range(1, ideal_rel_count + 1):
            idcg += 1.0 / math.log2(i + 1)

        if idcg < 1e-6:
            return 0.0

        return round(dcg / idcg, 4)

    @staticmethod
    def calculate_context_relevance(retrieved_chunks: List[Dict[str, Any]], expected_keywords: List[str]) -> float:
        """Calculate proportion of expected keywords covered in retrieved chunks."""
        if not retrieved_chunks or not expected_keywords:
            return 0.0

        full_retrieved_text = " ".join([c.get("text", "").lower() for c in retrieved_chunks])
        matched = sum(1 for kw in expected_keywords if kw.lower() in full_retrieved_text)
        return round(matched / float(len(expected_keywords)), 4)

    @classmethod
    def evaluate_retrieval_event(
        cls,
        retrieved_chunks: List[Dict[str, Any]],
        relevant_ids: List[str],
        selected_strategy: str,
        optimal_strategy: str,
        expected_keywords: List[str] = None,
        k: int = 3
    ) -> Dict[str, Any]:
        """Compute full suite of metrics for a single query execution."""
        retrieved_ids = [c["chunk_id"] for c in retrieved_chunks if "chunk_id" in c]
        
        p_k = cls.calculate_precision_at_k(retrieved_ids, relevant_ids, k=k)
        r_k = cls.calculate_recall_at_k(retrieved_ids, relevant_ids, k=k)
        mrr = cls.calculate_mrr(retrieved_ids, relevant_ids)
        ndcg_k = cls.calculate_ndcg_at_k(retrieved_ids, relevant_ids, k=k)
        ctx_rel = cls.calculate_context_relevance(retrieved_chunks, expected_keywords or [])
        strat_acc = 1.0 if selected_strategy == optimal_strategy else 0.0

        return {
            "precision_at_k": p_k,
            "recall_at_k": r_k,
            "mrr": mrr,
            "ndcg_at_k": ndcg_k,
            "context_relevance": ctx_rel,
            "strategy_accuracy": strat_acc
        }
