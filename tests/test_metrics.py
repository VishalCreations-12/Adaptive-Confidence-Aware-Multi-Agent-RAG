import os
import sys
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.evaluation.metrics_calculator import RAGMetricsCalculator
from src.evaluation.benchmark_loader import BenchmarkLoader


def test_benchmark_loader():
    loader = BenchmarkLoader()
    queries = loader.queries
    assert len(queries) >= 20
    
    q1 = loader.get_query_by_id("Q01")
    assert q1["category"] == "keyword-heavy"

    gt = loader.get_ground_truth_for_query("Q01")
    assert "relevant_chunk_ids" in gt

def test_metrics_calculator_basic():
    retrieved = ["chunk_1", "chunk_2", "chunk_3"]
    relevant = ["chunk_2", "chunk_5"]

    p3 = RAGMetricsCalculator.calculate_precision_at_k(retrieved, relevant, k=3)
    r3 = RAGMetricsCalculator.calculate_recall_at_k(retrieved, relevant, k=3)
    mrr = RAGMetricsCalculator.calculate_mrr(retrieved, relevant)
    ndcg3 = RAGMetricsCalculator.calculate_ndcg_at_k(retrieved, relevant, k=3)

    assert p3 == pytest.approx(1/3, abs=1e-3)
    assert r3 == pytest.approx(1/2, abs=1e-3)
    assert mrr == pytest.approx(1/2, abs=1e-3)
    assert ndcg3 > 0.0

def test_metrics_calculator_edge_cases():
    # Empty retrieved
    assert RAGMetricsCalculator.calculate_precision_at_k([], ["c1"], k=3) == 0.0
    assert RAGMetricsCalculator.calculate_recall_at_k([], ["c1"], k=3) == 0.0
    assert RAGMetricsCalculator.calculate_mrr([], ["c1"]) == 0.0
    assert RAGMetricsCalculator.calculate_ndcg_at_k([], ["c1"], k=3) == 0.0

    # Empty relevant
    assert RAGMetricsCalculator.calculate_precision_at_k(["c1"], [], k=3) == 0.0
    assert RAGMetricsCalculator.calculate_recall_at_k(["c1"], [], k=3) == 0.0

    # k = 0
    assert RAGMetricsCalculator.calculate_precision_at_k(["c1"], ["c1"], k=0) == 0.0

    # Perfect retrieval
    retrieved = ["c1", "c2"]
    relevant = ["c1", "c2"]
    assert RAGMetricsCalculator.calculate_precision_at_k(retrieved, relevant, k=2) == 1.0
    assert RAGMetricsCalculator.calculate_recall_at_k(retrieved, relevant, k=2) == 1.0
    assert RAGMetricsCalculator.calculate_mrr(retrieved, relevant) == 1.0
    assert RAGMetricsCalculator.calculate_ndcg_at_k(retrieved, relevant, k=2) == 1.0
