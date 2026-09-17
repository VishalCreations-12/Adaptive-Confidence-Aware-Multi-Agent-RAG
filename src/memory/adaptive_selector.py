import os
import pickle
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Tuple
from sklearn.ensemble import RandomForestClassifier

import config

class AdaptiveStrategySelector:
    """V2 Machine Learning Strategy Selector learning from historical retrieval outcomes."""

    STRATEGIES = ["BM25 Retrieval", "Semantic Retrieval", "Hybrid Retrieval"]

    def __init__(self, model_path: Path = config.MEMORY_DIR / "adaptive_strategy_model.pkl"):
        self.model_path = model_path
        self.model = RandomForestClassifier(
            n_estimators=30,
            max_depth=5,
            random_state=42,
            min_samples_leaf=1
        )
        self.is_trained = False
        self._try_load_model()

    def _try_load_model(self):
        """Load pickled classifier if available."""
        if self.model_path.exists():
            try:
                with open(self.model_path, "rb") as f:
                    data = pickle.load(f)
                    self.model = data["model"]
                    self.is_trained = data.get("is_trained", False)
            except Exception:
                self.is_trained = False

    def save_model(self):
        """Persist trained classifier to disk."""
        try:
            with open(self.model_path, "wb") as f:
                pickle.dump({"model": self.model, "is_trained": self.is_trained}, f)
        except Exception as e:
            print(f"Warning: Failed to save adaptive selector model: {e}")

    @classmethod
    def extract_features(cls, query_analysis: Dict[str, Any], candidate_stats: Dict[str, float] = None) -> np.ndarray:
        """Extract a standardized 12-dimensional numerical feature vector for a query."""
        word_count = float(query_analysis.get("word_count", 0))
        is_keyword = 1.0 if query_analysis.get("is_keyword_heavy") else 0.0
        is_semantic = 1.0 if query_analysis.get("is_semantic") else 0.0
        is_numerical = 1.0 if query_analysis.get("is_numerical") else 0.0
        is_comparison = 1.0 if query_analysis.get("is_comparison") else 0.0
        is_multi_part = 1.0 if query_analysis.get("is_multi_part") else 0.0
        
        traits = query_analysis.get("characteristics", [])
        is_factual = 1.0 if "factual" in traits else 0.0
        is_entity = 1.0 if "entity-focused" in traits else 0.0

        # Candidate retriever quick statistics if provided
        stats = candidate_stats or {}
        top_bm25 = float(stats.get("top_bm25_score", 0.0))
        top_sem = float(stats.get("top_semantic_sim", 0.0))
        score_diff = abs(top_bm25 / 10.0 - top_sem)
        bm25_sem_ratio = top_bm25 / (top_sem * 10.0 + 1e-5)

        feature_vector = [
            word_count,
            is_keyword,
            is_semantic,
            is_numerical,
            is_comparison,
            is_multi_part,
            is_factual,
            is_entity,
            top_bm25,
            top_sem,
            score_diff,
            bm25_sem_ratio
        ]
        return np.array(feature_vector, dtype=np.float32)

    @classmethod
    def calculate_reward(cls, metrics: Dict[str, float], confidence_score: float, latency_ms: float) -> float:
        """Transparent multi-component reward metric in [0.0, 1.0].
        
        Reward = 0.40 * MRR + 0.35 * Recall@3 + 0.15 * Confidence - 0.10 * (Latency / 100ms)
        """
        mrr = float(metrics.get("mrr", 0.0))
        recall = float(metrics.get("recall_at_k", 0.0))
        conf = float(confidence_score)
        lat_penalty = min(1.0, float(latency_ms) / 100.0)

        raw_reward = (0.40 * mrr) + (0.35 * recall) + (0.15 * conf) - (0.10 * lat_penalty)
        return round(max(0.0, min(1.0, raw_reward)), 4)

    def fit(self, training_records: List[Dict[str, Any]]):
        """Train classifier on historical strategy memory records."""
        if len(training_records) < 3:
            self.is_trained = False
            return

        X = []
        y = []

        for rec in training_records:
            q_analysis = {
                "word_count": rec.get("word_count", len(rec.get("query", "").split())),
                "is_keyword_heavy": "keyword-heavy" in rec.get("characteristics", []),
                "is_semantic": "semantic" in rec.get("characteristics", []),
                "is_numerical": "numerical" in rec.get("characteristics", []),
                "is_comparison": "comparison" in rec.get("characteristics", []),
                "is_multi_part": "multi-part / multi-hop" in rec.get("characteristics", []),
                "characteristics": rec.get("characteristics", [])
            }
            stats = rec.get("candidate_stats", {})
            feat = self.extract_features(q_analysis, stats)
            
            strat = rec.get("selected_strategy", rec.get("actual_strategy", "Hybrid Retrieval"))
            if strat in self.STRATEGIES:
                X.append(feat)
                y.append(strat)

        if len(X) < 3 or len(set(y)) < 1:
            self.is_trained = False
            return

        X_arr = np.array(X, dtype=np.float32)
        y_arr = np.array(y)

        self.model.fit(X_arr, y_arr)
        self.is_trained = True
        self.save_model()

    def predict_strategy(
        self,
        query_analysis: Dict[str, Any],
        candidate_stats: Dict[str, float] = None,
        heuristic_fallback: str = "Hybrid Retrieval"
    ) -> Tuple[str, Dict[str, float]]:
        """Predict optimal retrieval strategy and probabilities."""
        if not self.is_trained:
            # Cold-start fallback to heuristic choice
            probs = {s: (1.0 if s == heuristic_fallback else 0.0) for s in self.STRATEGIES}
            return heuristic_fallback, probs

        feat = self.extract_features(query_analysis, candidate_stats).reshape(1, -1)
        pred_class = self.model.predict(feat)[0]

        prob_values = self.model.predict_proba(feat)[0]
        classes = list(self.model.classes_)
        
        probabilities = {}
        for s in self.STRATEGIES:
            if s in classes:
                idx = classes.index(s)
                probabilities[s] = round(float(prob_values[idx]), 3)
            else:
                probabilities[s] = 0.0

        return str(pred_class), probabilities
