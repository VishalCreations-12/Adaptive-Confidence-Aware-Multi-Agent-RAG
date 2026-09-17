import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
import config

class RetrievalStrategyMemory:
    """Strategy Memory store tracking historical query decisions for future meta-learning."""

    def __init__(self, memory_file: Path = config.MEMORY_FILE_PATH):
        self.memory_file = memory_file
        self.history: List[Dict[str, Any]] = self._load_memory()

    def _load_memory(self) -> List[Dict[str, Any]]:
        """Load history from JSON file if exists."""
        if self.memory_file.exists():
            try:
                content = self.memory_file.read_text(encoding='utf-8')
                return json.loads(content)
            except Exception:
                return []
        return []

    def record_query_experience(
        self,
        query: str,
        query_analysis: Dict[str, Any],
        selected_strategy: str,
        confidence_info: Dict[str, Any],
        latency_ms: float
    ):
        """Record query attempt and strategy choice into memory."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "characteristics": query_analysis.get("characteristics", []),
            "selected_strategy": selected_strategy,
            "evidence_confidence": confidence_info.get("confidence_percentage", "N/A"),
            "confidence_score": confidence_info.get("confidence_score", 0.0),
            "latency_ms": round(latency_ms, 2)
        }
        self.history.append(entry)
        
        # Keep last 100 historical queries
        if len(self.history) > 100:
            self.history = self.history[-100:]

        try:
            self.memory_file.write_text(json.dumps(self.history, indent=2), encoding='utf-8')
        except Exception as e:
            print(f"Warning: Failed to save strategy memory: {e}")

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get summary analytics of recorded strategy memory."""
        if not self.history:
            return {"total_logged_queries": 0, "strategy_distribution": {}}
        
        counts = {}
        for entry in self.history:
            strat = entry.get("selected_strategy", "Unknown")
            counts[strat] = counts.get(strat, 0) + 1

        return {
            "total_logged_queries": len(self.history),
            "strategy_distribution": counts,
            "recent_entries": self.history[-5:]
        }
