from typing import List, Dict, Any

class BaselineComparator:
    """Compares single-retriever baselines against Proposed Multi-Agent Judge system."""

    @classmethod
    def compare_retrievers(
        cls,
        query: str,
        bm25_results: List[Dict[str, Any]],
        semantic_results: List[Dict[str, Any]],
        hybrid_results: List[Dict[str, Any]],
        proposed_judge_results: Dict[str, Any],
        total_pipeline_latency_ms: float
    ) -> Dict[str, Any]:
        """Compute comparison metrics for all 4 pipelines."""
        
        def get_avg_score(chunks: List[Dict[str, Any]], score_key: str) -> float:
            if not chunks:
                return 0.0
            scores = [c.get(score_key, 0.0) for c in chunks]
            return sum(scores) / len(scores)

        # Baseline 1: BM25-only
        bm25_lat = bm25_results[0].get("retrieval_time_ms", 0.0) if bm25_results else 0.0
        bm25_cov = get_avg_score(bm25_results[:3], "bm25_score") / 5.0  # Normalized proxy

        # Baseline 2: Semantic-only
        sem_lat = semantic_results[0].get("retrieval_time_ms", 0.0) if semantic_results else 0.0
        sem_score = get_avg_score(semantic_results[:3], "similarity_score")

        # Baseline 3: Hybrid-only
        hyb_lat = hybrid_results[0].get("retrieval_time_ms", 0.0) if hybrid_results else 0.0
        hyb_score = get_avg_score(hybrid_results[:3], "combined_score")

        # Proposed: Multi-Agent + Evidence Judge
        selected_evidence = proposed_judge_results.get("selected_evidence", [])
        proposed_score = proposed_judge_results.get("overall_evidence_score", 0.0)
        selected_strategy = proposed_judge_results.get("selected_strategy", "Hybrid Retrieval")

        comparison_data = [
            {
                "System": "Baseline 1: BM25-Only RAG",
                "Strategy Used": "Fixed Keyword (BM25)",
                "Top Evidence Score": round(bm25_results[0]["bm25_score"], 2) if bm25_results else 0.0,
                "Evidence Relevance Proxy": f"{min(1.0, bm25_cov):.2f}",
                "Latency (ms)": round(bm25_lat, 2),
                "Ground Truth Metric": "Not yet evaluated against ground truth."
            },
            {
                "System": "Baseline 2: Semantic-Only RAG",
                "Strategy Used": "Fixed Vector Similarity",
                "Top Evidence Score": round(semantic_results[0]["similarity_score"], 4) if semantic_results else 0.0,
                "Evidence Relevance Proxy": f"{sem_score:.2f}",
                "Latency (ms)": round(sem_lat, 2),
                "Ground Truth Metric": "Not yet evaluated against ground truth."
            },
            {
                "System": "Baseline 3: Simple Hybrid RAG",
                "Strategy Used": "Fixed Score Fusion (0.5/0.5)",
                "Top Evidence Score": round(hybrid_results[0]["combined_score"], 4) if hybrid_results else 0.0,
                "Evidence Relevance Proxy": f"{hyb_score:.2f}",
                "Latency (ms)": round(hyb_lat, 2),
                "Ground Truth Metric": "Not yet evaluated against ground truth."
            },
            {
                "System": "Proposed: Multi-Agent + Evidence Judge",
                "Strategy Used": f"Adaptive ({selected_strategy})",
                "Top Evidence Score": round(selected_evidence[0]["judge_evidence_score"], 4) if selected_evidence else 0.0,
                "Evidence Relevance Proxy": f"{proposed_score:.2f}",
                "Latency (ms)": round(total_pipeline_latency_ms, 2),
                "Ground Truth Metric": "Not yet evaluated against ground truth."
            }
        ]

        return {
            "comparison_table": comparison_data,
            "selected_strategy": selected_strategy,
            "pipeline_latency_ms": round(total_pipeline_latency_ms, 2)
        }
