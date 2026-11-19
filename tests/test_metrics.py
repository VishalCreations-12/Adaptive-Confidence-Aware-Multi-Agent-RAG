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
    
    q1 = loader.get_query_by_id("Q001") or loader.get_query_by_id("Q01")
    assert q1 != {}
    assert "category" in q1

    gt = loader.get_ground_truth_for_query(q1["query_id"])
    assert "relevant_chunk_ids" in gt

def test_benchmark_splits():
    loader = BenchmarkLoader()
    train_data = loader.get_split_data("train")
    val_data = loader.get_split_data("val")
    test_data = loader.get_split_data("test")

    assert len(train_data) > 0
    assert len(val_data) > 0
    assert len(test_data) > 0
    assert len(train_data) + len(val_data) + len(test_data) == len(loader.queries)

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

def test_metrics_calculator_context_relevance():
    retrieved_chunks = [
        {"text": "NovaSync v3.2 uses AES-256-GCM zero-trust encryption."},
        {"text": "Throughput exceeds 10.4 Gbps with sub-5ms latency."}
    ]
    expected_kws = ["novasync", "aes-256", "throughput", "unrelated_keyword"]
    ctx_rel = RAGMetricsCalculator.calculate_context_relevance(retrieved_chunks, expected_kws)
    assert ctx_rel == 0.75  # 3 out of 4 matched

def test_metrics_calculator_edge_cases():
    # Empty retrieved
    assert RAGMetricsCalculator.calculate_precision_at_k([], ["c1"], k=3) == 0.0
    assert RAGMetricsCalculator.calculate_recall_at_k([], ["c1"], k=3) == 0.0
    assert RAGMetricsCalculator.calculate_mrr([], ["c1"]) == 0.0
    assert RAGMetricsCalculator.calculate_ndcg_at_k([], ["c1"], k=3) == 0.0
    assert RAGMetricsCalculator.calculate_context_relevance([], ["kw1"]) == 0.0

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
