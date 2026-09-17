import os
import sys
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.evaluation.ablation_study import AblationStudyRunner
from src.evaluation.statistical_test import StatisticalValidator

def test_ablation_study_runner():
    dummy_records = [
        {"variant": "Full V2 System", "precision_at_k": 0.8, "recall_at_k": 0.9, "mrr": 1.0, "ndcg_at_k": 0.85, "confidence_score": 0.80},
        {"variant": "Fixed Hybrid Baseline", "precision_at_k": 0.6, "recall_at_k": 0.7, "mrr": 0.75, "ndcg_at_k": 0.65, "confidence_score": 0.60}
    ]
    res = AblationStudyRunner.evaluate_ablation_variants(dummy_records)
    assert res["variants_evaluated"] == len(AblationStudyRunner.VARIANTS)
    assert len(res["summary_table"]) == len(AblationStudyRunner.VARIANTS)

def test_statistical_validator():
    scores_a = [0.9, 0.85, 1.0, 0.95, 0.88, 0.92, 0.96, 0.90, 0.89, 0.94]
    scores_b = [0.6, 0.70, 0.65, 0.55, 0.68, 0.72, 0.61, 0.58, 0.64, 0.67]

    res = StatisticalValidator.compare_systems(
        scores_a, scores_b,
        system_a_name="V2 System",
        system_b_name="Fixed Hybrid",
        metric_name="MRR"
    )
    assert "p_value" in res
    assert res["is_statistically_significant"] is True
    assert res["mean_system_a"] > res["mean_system_b"]
