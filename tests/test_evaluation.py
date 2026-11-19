import os
import sys
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.evaluation.ablation_study import AblationStudyRunner
from src.evaluation.statistical_test import StatisticalValidator
from src.evaluation.oracle_router import OracleRouter

def test_ablation_study_aggregation():
    dummy_records = [
        {"variant": "A0: Full V2 System", "precision_at_k": 0.8, "recall_at_k": 0.9, "mrr": 1.0, "ndcg_at_k": 0.85, "confidence": 0.80, "latency_ms": 12.0},
        {"variant": "A1: V2 w/o Query Traits", "precision_at_k": 0.75, "recall_at_k": 0.85, "mrr": 0.9, "ndcg_at_k": 0.80, "confidence": 0.75, "latency_ms": 11.5},
        {"variant": "A2: V2 w/o Evidence Judge", "precision_at_k": 0.70, "recall_at_k": 0.80, "mrr": 0.85, "ndcg_at_k": 0.75, "confidence": 0.50, "latency_ms": 5.0},
        {"variant": "A3: V2 w/o Confidence Mechanism", "precision_at_k": 0.80, "recall_at_k": 0.90, "mrr": 1.0, "ndcg_at_k": 0.85, "confidence": 0.50, "latency_ms": 12.0},
        {"variant": "A4: V2 w/o Historical Memory", "precision_at_k": 0.75, "recall_at_k": 0.85, "mrr": 0.9, "ndcg_at_k": 0.80, "confidence": 0.70, "latency_ms": 10.0},
        {"variant": "A5: Fixed Hybrid Baseline", "precision_at_k": 0.65, "recall_at_k": 0.75, "mrr": 0.80, "ndcg_at_k": 0.70, "confidence": 0.65, "latency_ms": 9.0}
    ]
    res = AblationStudyRunner.aggregate_ablation_results(dummy_records)
    assert res["variants_evaluated"] == len(AblationStudyRunner.VARIANTS)
    assert len(res["summary_table"]) == len(AblationStudyRunner.VARIANTS)

def test_statistical_validator():
    scores_a = [0.9, 0.85, 1.0, 0.95, 0.88, 0.92, 0.96, 0.90, 0.89, 0.94]
    scores_b = [0.6, 0.70, 0.65, 0.55, 0.68, 0.72, 0.61, 0.58, 0.64, 0.67]

    res = StatisticalValidator.compare_systems(
        scores_a, scores_b,
        system_a_name="V2 System",
        system_b_name="Fixed Hybrid",
        metric_name="nDCG@3"
    )
    assert "p_value" in res
    assert "ci_95_lower" in res
    assert "ci_95_upper" in res
    assert "effect_size_cohens_d" in res
    assert res["is_statistically_significant"] is True
    assert res["mean_system_a"] > res["mean_system_b"]

def test_statistical_validator_identical_inputs():
    scores_a = [0.8, 0.8, 0.8, 0.8, 0.8]
    scores_b = [0.8, 0.8, 0.8, 0.8, 0.8]

    res = StatisticalValidator.compare_systems(scores_a, scores_b, metric_name="MRR")
    assert res["mean_difference"] == 0.0
    assert res["p_value"] == 1.0
    assert res["is_statistically_significant"] is False

def test_oracle_router():
    cands = {
        "BM25 Retrieval": [{"chunk_id": "c1", "retrieval_time_ms": 2.0}],
        "Semantic Retrieval": [{"chunk_id": "c2", "retrieval_time_ms": 10.0}],
        "Hybrid Retrieval": [{"chunk_id": "c2", "retrieval_time_ms": 12.0}]
    }
    rel_ids = ["c2"]
    best_strat, oracle_m, all_m = OracleRouter.evaluate_candidate_strategies(cands, rel_ids)
    assert best_strat in ["Semantic Retrieval", "Hybrid Retrieval"]
    assert oracle_m["ndcg_at_k"] == 1.0
