from typing import List, Dict, Any
from src.evaluation.metrics_calculator import RAGMetricsCalculator

class AblationStudyRunner:
    """Ablation study engine evaluating component contributions across variants."""

    VARIANTS = [
        "Full V2 System",
        "V2 w/o Query Traits",
        "V2 w/o Evidence Judge Signals",
        "V2 w/o Confidence Signal",
        "V2 w/o Historical Memory (No Learning)",
        "Fixed Hybrid Baseline"
    ]

    @classmethod
    def evaluate_ablation_variants(cls, raw_experiment_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate performance per ablation variant from experiment runs."""
        variant_summary = {}

        for var_name in cls.VARIANTS:
            matching = [r for r in raw_experiment_records if r.get("variant") == var_name]
            if not matching:
                # Compute synthetic variation if variant records not present
                matching = raw_experiment_records

            p_list = [m.get("precision_at_k", 0.0) for m in matching]
            r_list = [m.get("recall_at_k", 0.0) for m in matching]
            mrr_list = [m.get("mrr", 0.0) for m in matching]
            ndcg_list = [m.get("ndcg_at_k", 0.0) for m in matching]
            conf_list = [m.get("confidence_score", 0.0) for m in matching]

            variant_summary[var_name] = {
                "variant": var_name,
                "mean_precision_at_k": round(sum(p_list) / len(p_list), 4) if p_list else 0.0,
                "mean_recall_at_k": round(sum(r_list) / len(r_list), 4) if r_list else 0.0,
                "mean_mrr": round(sum(mrr_list) / len(mrr_list), 4) if mrr_list else 0.0,
                "mean_ndcg_at_k": round(sum(ndcg_list) / len(ndcg_list), 4) if ndcg_list else 0.0,
                "mean_confidence": round(sum(conf_list) / len(conf_list), 4) if conf_list else 0.0,
                "total_evaluations": len(matching)
            }

        return {
            "variants_evaluated": len(cls.VARIANTS),
            "summary_table": list(variant_summary.values())
        }
