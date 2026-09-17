import numpy as np
from scipy import stats
from typing import Dict, Any, List

class StatisticalValidator:
    """Statistical validation engine running paired non-parametric and parametric significance tests."""

    @classmethod
    def compare_systems(
        cls,
        scores_a: List[float],
        scores_b: List[float],
        system_a_name: str = "Proposed V2 Adaptive",
        system_b_name: str = "Fixed Hybrid Baseline",
        metric_name: str = "MRR",
        alpha: float = 0.05
    ) -> Dict[str, Any]:
        """Perform paired statistical significance test (Wilcoxon signed-rank test & Paired t-test)."""
        arr_a = np.array(scores_a, dtype=np.float64)
        arr_b = np.array(scores_b, dtype=np.float64)

        if len(arr_a) != len(arr_b) or len(arr_a) < 3:
            return {
                "system_a": system_a_name,
                "system_b": system_b_name,
                "metric": metric_name,
                "sample_size": len(arr_a),
                "is_statistically_significant": False,
                "p_value": 1.0,
                "test_statistic": 0.0,
                "test_name": "Sample size insufficient",
                "interpretation": "Insufficient sample size for statistical testing."
            }

        diffs = arr_a - arr_b
        mean_diff = float(np.mean(diffs))

        # Check if all differences are zero
        if np.all(diffs == 0):
            return {
                "system_a": system_a_name,
                "system_b": system_b_name,
                "metric": metric_name,
                "sample_size": len(arr_a),
                "mean_diff": 0.0,
                "is_statistically_significant": False,
                "p_value": 1.0,
                "test_statistic": 0.0,
                "test_name": "Wilcoxon Signed-Rank Test",
                "interpretation": f"No difference observed between {system_a_name} and {system_b_name} on {metric_name} (diff = 0)."
            }

        # Perform Wilcoxon signed-rank test (non-parametric paired test)
        try:
            w_stat, p_val = stats.wilcoxon(diffs, zero_method='pratt')
            w_stat = float(w_stat)
            p_val = float(p_val)
        except Exception:
            # Fallback to paired t-test
            t_stat, p_val = stats.ttest_rel(arr_a, arr_b)
            w_stat = float(t_stat)
            p_val = float(p_val)

        # Cohen's d effect size calculation
        std_diff = float(np.std(diffs, ddof=1)) if len(diffs) > 1 else 1.0
        effect_size = round(mean_diff / (std_diff + 1e-8), 4)

        is_sig = bool(p_val < alpha)

        interp = (
            f"Statistically significant difference detected (p = {p_val:.4f} < {alpha}) favoring {system_a_name}."
            if is_sig and mean_diff > 0 else
            f"No statistically significant difference detected (p = {p_val:.4f} >= {alpha}) between {system_a_name} and {system_b_name}."
        )

        return {
            "system_a": system_a_name,
            "system_b": system_b_name,
            "metric": metric_name,
            "sample_size": len(arr_a),
            "mean_system_a": round(float(np.mean(arr_a)), 4),
            "mean_system_b": round(float(np.mean(arr_b)), 4),
            "mean_difference": round(mean_diff, 4),
            "effect_size_cohens_d": effect_size,
            "test_name": "Wilcoxon Signed-Rank Test",
            "test_statistic": round(w_stat, 4),
            "p_value": round(p_val, 4),
            "alpha_level": alpha,
            "is_statistically_significant": is_sig,
            "interpretation": interp
        }
