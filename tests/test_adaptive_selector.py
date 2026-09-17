import os
import sys
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.memory.adaptive_selector import AdaptiveStrategySelector
from src.query_analysis.analyzer import QueryAnalyzer

def test_feature_extraction():
    q_analysis = QueryAnalyzer.analyze("NovaSync v3.2 AES-256 zero-trust throughput")
    features = AdaptiveStrategySelector.extract_features(q_analysis)
    assert len(features) == 12
    assert features[1] == 1.0  # is_keyword_heavy

def test_reward_calculation():
    metrics = {"mrr": 1.0, "recall_at_k": 1.0}
    reward = AdaptiveStrategySelector.calculate_reward(metrics, confidence_score=0.85, latency_ms=20.0)
    assert 0.0 <= reward <= 1.0
    assert reward > 0.7

def test_adaptive_selector_cold_start_and_fit(tmp_path):
    model_file = tmp_path / "test_model.pkl"
    selector = AdaptiveStrategySelector(model_file)
    
    q_analysis = QueryAnalyzer.analyze("What is NovaSolar efficiency?")
    strat, probs = selector.predict_strategy(q_analysis, heuristic_fallback="BM25 Retrieval")
    assert strat == "BM25 Retrieval"
    assert selector.is_trained is False

    # Simulate training dataset
    records = [
        {"query": "NovaSync AES-256", "characteristics": ["keyword-heavy"], "selected_strategy": "BM25 Retrieval"},
        {"query": "How to protect environment", "characteristics": ["semantic"], "selected_strategy": "Semantic Retrieval"},
        {"query": "What is revenue Q3", "characteristics": ["factual", "numerical"], "selected_strategy": "Hybrid Retrieval"},
        {"query": "Compare solar panel and drone", "characteristics": ["comparison"], "selected_strategy": "Hybrid Retrieval"}
    ]
    
    selector.fit(records)
    assert selector.is_trained is True

    # Test prediction post-training
    strat_post, probs_post = selector.predict_strategy(q_analysis)
    assert strat_post in AdaptiveStrategySelector.STRATEGIES
    assert len(probs_post) == 3
