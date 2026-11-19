import time
from typing import List, Dict, Any, Tuple, Optional
from src.retrieval.bm25_agent import BM25Retriever
from src.retrieval.semantic_agent import SemanticRetriever
from src.retrieval.hybrid_agent import HybridRetriever
from src.judge.evidence_judge import EvidenceJudge
from src.confidence.confidence_scorer import ConfidenceScorer
from src.query_analysis.analyzer import QueryAnalyzer
from src.memory.adaptive_selector import AdaptiveStrategySelector
from src.evaluation.metrics_calculator import RAGMetricsCalculator

class AblationStudyRunner:
    """Independent modular execution engine for ablation variants A0 - A5.
    
    CRITICAL INTEGRITY RULE: Every variant actually executes its specific pipeline.
    Zero synthetic subtraction, copying, or scaling.
    """

    VARIANTS = [
        "A0: Full V2 System",
        "A1: V2 w/o Query Traits",
        "A2: V2 w/o Evidence Judge",
        "A3: V2 w/o Confidence Mechanism",
        "A4: V2 w/o Historical Memory",
        "A5: Fixed Hybrid Baseline"
    ]

    @classmethod
    def execute_query_ablation(
        cls,
        query: str,
        rel_ids: List[str],
        expected_kws: List[str],
        bm25_agent: BM25Retriever,
        semantic_agent: SemanticRetriever,
        hybrid_agent: HybridRetriever,
        trained_selector: AdaptiveStrategySelector,
        cold_selector: AdaptiveStrategySelector,
        rrf_agent: Optional[Any] = None,
        k: int = 3
    ) -> Dict[str, Dict[str, Any]]:
        """Execute all 6 ablation variants independently for a single query."""
        
        # 1. Base Retrieval Pools
        t0 = time.time()
        res_bm25 = bm25_agent.search(query, top_k=max(k * 2, 6))
        lat_bm25 = (time.time() - t0) * 1000.0

        t0 = time.time()
        res_sem = semantic_agent.search(query, top_k=max(k * 2, 6))
        lat_sem = (time.time() - t0) * 1000.0

        t0 = time.time()
        res_hyb = hybrid_agent.search(query, top_k=max(k * 2, 6))
        lat_hyb = (time.time() - t0) * 1000.0

        res_rrf = rrf_agent.search(query, top_k=max(k * 2, 6)) if rrf_agent else None

        stats = {
            "top_bm25_score": res_bm25[0]["bm25_score"] if res_bm25 else 0.0,
            "top_semantic_sim": res_sem[0]["similarity_score"] if res_sem else 0.0
        }

        # Query Trait Analysis
        q_analysis = QueryAnalyzer.analyze(query)

        # Blank Query Trait Analysis (for A1)
        blank_analysis = {
            "query": query,
            "word_count": len(query.split()),
            "characteristics": [],
            "is_keyword_heavy": False,
            "is_semantic": False,
            "is_numerical": False,
            "is_comparison": False,
            "is_multi_part": False
        }

        # Dictionary of variant results
        results = {}

        # -------------------------------------------------------------
        # A0: Full V2 System (All components active)
        # -------------------------------------------------------------
        t0 = time.time()
        strat_a0, _ = trained_selector.predict_strategy(q_analysis, stats, heuristic_fallback="Hybrid Retrieval")
        judge_a0 = EvidenceJudge.evaluate(
            query, q_analysis, res_bm25, res_sem, res_hyb,
            target_evidence_count=k,
            strategy_override=strat_a0,
            rrf_results=res_rrf
        )
        conf_a0 = ConfidenceScorer.calculate_confidence(judge_a0, q_analysis)
        lat_a0 = (time.time() - t0) * 1000.0 + lat_hyb
        m_a0 = RAGMetricsCalculator.evaluate_retrieval_event(
            judge_a0["selected_evidence"], rel_ids, strat_a0, strat_a0, expected_kws, k=k
        )
        results["A0: Full V2 System"] = {
            "variant": "A0: Full V2 System",
            "selected_strategy": strat_a0,
            "metrics": m_a0,
            "confidence": conf_a0["confidence_score"],
            "latency_ms": round(lat_a0, 2)
        }

        # -------------------------------------------------------------
        # A1: V2 w/o Query Traits (Traits masked out)
        # -------------------------------------------------------------
        t0 = time.time()
        strat_a1, _ = trained_selector.predict_strategy(blank_analysis, stats, heuristic_fallback="Hybrid Retrieval")
        judge_a1 = EvidenceJudge.evaluate(
            query, blank_analysis, res_bm25, res_sem, res_hyb,
            target_evidence_count=k,
            strategy_override=strat_a1,
            rrf_results=res_rrf
        )
        conf_a1 = ConfidenceScorer.calculate_confidence(judge_a1, blank_analysis)
        lat_a1 = (time.time() - t0) * 1000.0 + lat_hyb
        m_a1 = RAGMetricsCalculator.evaluate_retrieval_event(
            judge_a1["selected_evidence"], rel_ids, strat_a1, strat_a0, expected_kws, k=k
        )
        results["A1: V2 w/o Query Traits"] = {
            "variant": "A1: V2 w/o Query Traits",
            "selected_strategy": strat_a1,
            "metrics": m_a1,
            "confidence": conf_a1["confidence_score"],
            "latency_ms": round(lat_a1, 2)
        }

        # -------------------------------------------------------------
        # A2: V2 w/o Evidence Judge (Pass raw retriever pool through)
        # -------------------------------------------------------------
        t0 = time.time()
        strat_a2, _ = trained_selector.predict_strategy(q_analysis, stats, heuristic_fallback="Hybrid Retrieval")
        # Direct raw pool bypass without judge filtering or consensus scoring
        if strat_a2 == "BM25 Retrieval":
            raw_evidence = res_bm25[:k]
        elif strat_a2 == "Semantic Retrieval":
            raw_evidence = res_sem[:k]
        elif strat_a2 == "RRF Retrieval":
            raw_evidence = (res_rrf if res_rrf else res_hyb)[:k]
        else:
            raw_evidence = res_hyb[:k]
        lat_a2 = (time.time() - t0) * 1000.0 + (lat_bm25 if strat_a2 == "BM25 Retrieval" else (lat_sem if strat_a2 == "Semantic Retrieval" else lat_hyb))
        m_a2 = RAGMetricsCalculator.evaluate_retrieval_event(
            raw_evidence, rel_ids, strat_a2, strat_a0, expected_kws, k=k
        )
        results["A2: V2 w/o Evidence Judge"] = {
            "variant": "A2: V2 w/o Evidence Judge",
            "selected_strategy": strat_a2,
            "metrics": m_a2,
            "confidence": 0.50, # Uniform fallback
            "latency_ms": round(lat_a2, 2)
        }

        # -------------------------------------------------------------
        # A3: V2 w/o Confidence Mechanism (Confidence disabled)
        # -------------------------------------------------------------
        t0 = time.time()
        strat_a3, _ = trained_selector.predict_strategy(q_analysis, stats, heuristic_fallback="Hybrid Retrieval")
        judge_a3 = EvidenceJudge.evaluate(
            query, q_analysis, res_bm25, res_sem, res_hyb,
            target_evidence_count=k,
            strategy_override=strat_a3,
            rrf_results=res_rrf
        )
        lat_a3 = (time.time() - t0) * 1000.0 + lat_hyb
        m_a3 = RAGMetricsCalculator.evaluate_retrieval_event(
            judge_a3["selected_evidence"], rel_ids, strat_a3, strat_a0, expected_kws, k=k
        )
        results["A3: V2 w/o Confidence Mechanism"] = {
            "variant": "A3: V2 w/o Confidence Mechanism",
            "selected_strategy": strat_a3,
            "metrics": m_a3,
            "confidence": 0.50, # Fixed uninformative constant
            "latency_ms": round(lat_a3, 2)
        }

        # -------------------------------------------------------------
        # A4: V2 w/o Historical Memory (Cold start heuristic mode)
        # -------------------------------------------------------------
        t0 = time.time()
        strat_a4, _ = cold_selector.predict_strategy(q_analysis, stats, heuristic_fallback="Hybrid Retrieval")
        judge_a4 = EvidenceJudge.evaluate(
            query, q_analysis, res_bm25, res_sem, res_hyb,
            target_evidence_count=k,
            strategy_override=strat_a4,
            rrf_results=res_rrf
        )
        conf_a4 = ConfidenceScorer.calculate_confidence(judge_a4, q_analysis)
        lat_a4 = (time.time() - t0) * 1000.0 + lat_hyb
        m_a4 = RAGMetricsCalculator.evaluate_retrieval_event(
            judge_a4["selected_evidence"], rel_ids, strat_a4, strat_a0, expected_kws, k=k
        )
        results["A4: V2 w/o Historical Memory"] = {
            "variant": "A4: V2 w/o Historical Memory",
            "selected_strategy": strat_a4,
            "metrics": m_a4,
            "confidence": conf_a4["confidence_score"],
            "latency_ms": round(lat_a4, 2)
        }

        # -------------------------------------------------------------
        # A5: Fixed Hybrid Baseline (Fixed weights, no router)
        # -------------------------------------------------------------
        m_a5 = RAGMetricsCalculator.evaluate_retrieval_event(
            res_hyb[:k], rel_ids, "Hybrid Retrieval", strat_a0, expected_kws, k=k
        )
        results["A5: Fixed Hybrid Baseline"] = {
            "variant": "A5: Fixed Hybrid Baseline",
            "selected_strategy": "Hybrid Retrieval",
            "metrics": m_a5,
            "confidence": 0.65,
            "latency_ms": round(lat_hyb, 2)
        }

        return results

    @classmethod
    def aggregate_ablation_results(cls, query_ablation_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate independent ablation query executions into summary statistics."""
        summary = {}

        for var_name in cls.VARIANTS:
            records = [r for r in query_ablation_records if r.get("variant") == var_name]
            if not records:
                continue

            p_list = [r["precision_at_k"] for r in records]
            r_list = [r["recall_at_k"] for r in records]
            mrr_list = [r["mrr"] for r in records]
            ndcg_list = [r["ndcg_at_k"] for r in records]
            ctx_list = [r.get("context_relevance", 0.0) for r in records]
            conf_list = [r.get("confidence", 0.0) for r in records]
            lat_list = [r.get("latency_ms", 0.0) for r in records]

            summary[var_name] = {
                "variant": var_name,
                "n_queries": len(records),
                "mean_precision_at_k": round(float(sum(p_list) / len(p_list)), 4),
                "mean_recall_at_k": round(float(sum(r_list) / len(r_list)), 4),
                "mean_mrr": round(float(sum(mrr_list) / len(mrr_list)), 4),
                "mean_ndcg_at_k": round(float(sum(ndcg_list) / len(ndcg_list)), 4),
                "mean_context_relevance": round(float(sum(ctx_list) / len(ctx_list)), 4),
                "mean_confidence": round(float(sum(conf_list) / len(conf_list)), 4),
                "mean_latency_ms": round(float(sum(lat_list) / len(lat_list)), 2)
            }

        return {
            "variants_evaluated": len(summary),
            "summary_table": list(summary.values())
        }
