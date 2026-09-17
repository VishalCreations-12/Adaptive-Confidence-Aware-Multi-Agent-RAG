from typing import List, Dict, Any
import config

class ConfidenceScorer:
    """Calculates multi-factor Evidence Confidence Score based on empirical retrieval signals."""

    @classmethod
    def calculate_confidence(
        cls,
        judge_results: Dict[str, Any],
        query_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compute Evidence Confidence score from judge metrics."""
        selected_evidence = judge_results.get("selected_evidence", [])
        
        if not selected_evidence:
            return {
                "confidence_score": 0.0,
                "confidence_percentage": "0%",
                "confidence_level": "VERY LOW",
                "signals": {}
            }

        # Signal 1: Top candidate score strength
        top_chunk_score = selected_evidence[0].get("judge_evidence_score", 0.0)
        score_strength_factor = min(1.0, top_chunk_score / 0.85)

        # Signal 2: Cross-agent consensus ratio
        agreements = [c.get("cross_agent_agreement", 1) for c in selected_evidence]
        avg_agreement = sum(agreements) / len(agreements) if agreements else 1.0
        consensus_factor = min(1.0, avg_agreement / 2.5)

        # Signal 3: Keyword coverage in evidence
        coverages = [c.get("keyword_coverage", 0.5) for c in selected_evidence]
        coverage_factor = sum(coverages) / len(coverages) if coverages else 0.5

        # Signal 4: Inter-chunk score consistency (low variance is better)
        scores = [c.get("judge_evidence_score", 0.0) for c in selected_evidence]
        if len(scores) > 1:
            score_diff = abs(scores[0] - scores[-1])
            spread_factor = max(0.0, 1.0 - (score_diff * 1.5))
        else:
            spread_factor = 0.8

        weights = config.CONFIDENCE_WEIGHTS
        raw_confidence = (
            weights["score_strength"] * score_strength_factor +
            weights["consensus_ratio"] * consensus_factor +
            weights["keyword_coverage"] * coverage_factor +
            weights["score_spread"] * spread_factor
        )

        # Clamp between 0.15 and 0.98 for realistic evidence confidence bound
        final_confidence = round(max(0.15, min(0.98, raw_confidence)), 2)
        pct_str = f"{int(final_confidence * 100)}%"

        if final_confidence >= 0.80:
            level = "HIGH"
        elif final_confidence >= 0.55:
            level = "MODERATE"
        else:
            level = "LOW"

        return {
            "confidence_score": final_confidence,
            "confidence_percentage": pct_str,
            "confidence_level": level,
            "signals": {
                "score_strength_factor": round(score_strength_factor, 3),
                "consensus_factor": round(consensus_factor, 3),
                "keyword_coverage_factor": round(coverage_factor, 3),
                "score_spread_factor": round(spread_factor, 3)
            }
        }
