import json
from pathlib import Path
from typing import Dict, Any, List
import config

class BenchmarkLoader:
    """Loader utility for internal research benchmark dataset and ground truth annotations."""

    def __init__(
        self,
        queries_path: Path = config.BASE_DIR / "data" / "benchmarks" / "benchmark_queries.json",
        ground_truth_path: Path = config.BASE_DIR / "data" / "benchmarks" / "ground_truth.json"
    ):
        self.queries_path = queries_path
        self.ground_truth_path = ground_truth_path
        self.queries: List[Dict[str, Any]] = []
        self.ground_truth: Dict[str, Any] = {}
        self.load_benchmark()

    def load_benchmark(self):
        """Load benchmark queries and ground truth from JSON files."""
        if self.queries_path.exists():
            content = self.queries_path.read_text(encoding='utf-8')
            self.queries = json.loads(content)
        
        if self.ground_truth_path.exists():
            content = self.ground_truth_path.read_text(encoding='utf-8')
            parsed = json.loads(content)
            self.ground_truth = parsed.get("ground_truth", {})

    def get_query_by_id(self, query_id: str) -> Dict[str, Any]:
        """Get query dictionary by ID."""
        for q in self.queries:
            if q.get("query_id") == query_id:
                return q
        return {}

    def get_ground_truth_for_query(self, query_id: str) -> Dict[str, Any]:
        """Get ground truth metadata for a given query ID."""
        return self.ground_truth.get(query_id, {})

    def get_all_benchmark_data(self) -> List[Dict[str, Any]]:
        """Combine queries with their corresponding ground truth records."""
        combined = []
        for q in self.queries:
            qid = q.get("query_id")
            gt = self.get_ground_truth_for_query(qid)
            item = dict(q)
            item["relevant_chunk_ids"] = gt.get("relevant_chunk_ids", [])
            item["primary_chunk_id"] = gt.get("primary_chunk_id", "")
            item["optimal_strategy"] = gt.get("optimal_strategy", "Hybrid Retrieval")
            item["expected_keywords"] = gt.get("expected_keywords", [])
            combined.append(item)
        return combined
