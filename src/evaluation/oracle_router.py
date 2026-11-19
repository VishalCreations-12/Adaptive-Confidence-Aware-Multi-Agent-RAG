from typing import List, Dict, Any, Tuple
from src.evaluation.metrics_calculator import RAGMetricsCalculator

class OracleRouter:
    """Theoretical upper bound: Oracle Retriever Router.
    
    For each query, determines the best-performing candidate retrieval strategy
    according to an objective metric (nDCG@3 with tie-breaking on P@3 and latency).
    """

    STRATEGY_NAMES = [
        "BM25 Retrieval",
        "Semantic Retrieval",
        "Hybrid Retrieval",
        "RRF Retrieval",
        "Tuned Hybrid Retrieval"
    ]

    @classmethod
    def evaluate_candidate_strategies(
        cls,
        candidate_results: Dict[str, List[Dict[str, Any]]],
        relevant_ids: List[str],
        expected_keywords: List[str] = None,
        k: int = 3
    ) -> Tuple[str, Dict[str, Any], Dict[str, Dict[str, Any]]]:
        """Evaluate all candidate strategies on a single query and identify the oracle strategy.
        
        Args:
            candidate_results: Dict mapping strategy_name -> retrieved_chunks list.
            relevant_ids: Ground truth relevant chunk IDs.
            expected_keywords: Keywords for context relevance.
            k: Cutoff rank (default 3).
            
        Returns:
            Tuple of:
                - oracle_strategy_name
                - oracle_metrics
                - all_strategies_metrics
        """
        all_metrics: Dict[str, Dict[str, Any]] = {}
        best_strategy = None
        best_score = -1.0
        best_latency = float('inf')

        for strat_name, chunks in candidate_results.items():
            metrics = RAGMetricsCalculator.evaluate_retrieval_event(
                retrieved_chunks=chunks,
                relevant_ids=relevant_ids,
                selected_strategy=strat_name,
                optimal_strategy=strat_name,
                expected_keywords=expected_keywords or [],
                k=k
            )
            lat = chunks[0].get("retrieval_time_ms", 10.0) if chunks else 10.0
            metrics["latency_ms"] = lat

            # Composite ranking score: nDCG@3 + minor tie-breakers
            score = metrics["ndcg_at_k"] + (0.01 * metrics["precision_at_k"])
            all_metrics[strat_name] = metrics

            if score > best_score or (abs(score - best_score) < 1e-5 and lat < best_latency):
                best_score = score
                best_latency = lat
                best_strategy = strat_name

        if best_strategy is None:
            best_strategy = "Hybrid Retrieval"

        oracle_metrics = dict(all_metrics[best_strategy])
        oracle_metrics["is_oracle"] = True
        return best_strategy, oracle_metrics, all_metrics
