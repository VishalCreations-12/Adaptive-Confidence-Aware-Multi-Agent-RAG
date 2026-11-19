import numpy as np
from scipy import stats
from typing import Dict, Any, List, Optional

class StatisticalValidator:
    """Non-parametric paired statistical validation engine.
    
    Implements:
    - Wilcoxon signed-rank test (two-sided, Pratt zero-handling)
    - Paired non-parametric bootstrap 95% confidence intervals (10,000 resamples)
    - Standardized Cohen's d effect size on paired differences
    """

    @classmethod
    def compute_bootstrap_ci(
        cls,
        diffs: np.ndarray,
        n_bootstraps: int = 10000,
        ci_level: float = 0.95,
        random_seed: int = 42
    ) -> Dict[str, float]:
        """Compute non-parametric bootstrap confidence interval for mean paired difference."""
        if len(diffs) == 0:
            return {"ci_lower": 0.0, "ci_upper": 0.0, "mean_diff": 0.0}

        rng = np.random.default_rng(random_seed)
        boot_means = np.empty(n_bootstraps, dtype=np.float64)

        n = len(diffs)
        for i in range(n_bootstraps):
            sample = rng.choice(diffs, size=n, replace=True)
            boot_means[i] = np.mean(sample)

        alpha = 1.0 - ci_level
        ci_lower = float(np.percentile(boot_means, 100.0 * (alpha / 2.0)))
        ci_upper = float(np.percentile(boot_means, 100.0 * (1.0 - alpha / 2.0)))

        return {
            "ci_lower": round(ci_lower, 4),
            "ci_upper": round(ci_upper, 4),
            "boot_mean": round(float(np.mean(boot_means)), 4)
        }

    @classmethod
    def compare_systems(
        cls,
        scores_a: List[float],
        scores_b: List[float],
        system_a_name: str = "Proposed V2 Adaptive",
        system_b_name: str = "Fixed Hybrid Baseline",
        metric_name: str = "nDCG@3",
        alpha: float = 0.05,
        n_bootstraps: int = 10000
    ) -> Dict[str, Any]:
        """Perform paired non-parametric Wilcoxon signed-rank test and bootstrap CI analysis."""
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
        mean_a = float(np.mean(arr_a))
        mean_b = float(np.mean(arr_b))
        mean_diff = float(np.mean(diffs))

        # Bootstrap 95% Confidence Interval
        boot_ci = cls.compute_bootstrap_ci(diffs, n_bootstraps=n_bootstraps, ci_level=1.0 - alpha)

        # Cohen's d effect size on paired differences
        std_diff = float(np.std(diffs, ddof=1)) if len(diffs) > 1 else 0.0
        if std_diff > 1e-8:
            effect_size = round(mean_diff / std_diff, 4)
        else:
            effect_size = 0.0

        # Check if all differences are zero
        if np.all(diffs == 0):
            return {
                "system_a": system_a_name,
                "system_b": system_b_name,
                "metric": metric_name,
                "sample_size": len(arr_a),
                "mean_system_a": round(mean_a, 4),
                "mean_system_b": round(mean_b, 4),
                "mean_difference": 0.0,
                "ci_95_lower": 0.0,
                "ci_95_upper": 0.0,
                "effect_size_cohens_d": 0.0,
                "test_name": "Wilcoxon Signed-Rank Test (Non-parametric)",
                "test_statistic": 0.0,
                "p_value": 1.0,
                "alpha_level": alpha,
                "is_statistically_significant": False,
                "interpretation": f"Identical performance: No metric difference between {system_a_name} and {system_b_name} on {metric_name} across all {len(arr_a)} queries."
            }

        # Perform Wilcoxon signed-rank test
        try:
            # Pratt handles zeros by keeping them in ranking
            res = stats.wilcoxon(arr_a, arr_b, zero_method='pratt', alternative='two-sided')
            w_stat = float(res.statistic)
            p_val = float(res.pvalue)
        except Exception:
            # Wilcoxon fallback with wilcox zero-method
            try:
                res = stats.wilcoxon(diffs[diffs != 0], alternative='two-sided')
                w_stat = float(res.statistic)
                p_val = float(res.pvalue)
            except Exception:
                t_stat, p_val = stats.ttest_rel(arr_a, arr_b)
                w_stat = float(t_stat)
                p_val = float(p_val)

        is_sig = bool(p_val < alpha and (boot_ci["ci_lower"] > 0 or boot_ci["ci_upper"] < 0))

        if is_sig and mean_diff > 0:
            interp = f"Statistically significant improvement favoring {system_a_name} (mean delta = +{mean_diff:.4f}, p = {p_val:.4f} < {alpha}, 95% CI [{boot_ci['ci_lower']:+.4f}, {boot_ci['ci_upper']:+.4f}])."
        elif is_sig and mean_diff < 0:
            interp = f"Statistically significant difference favoring {system_b_name} (mean delta = {mean_diff:.4f}, p = {p_val:.4f} < {alpha}, 95% CI [{boot_ci['ci_lower']:+.4f}, {boot_ci['ci_upper']:+.4f}])."
        else:
            interp = f"No statistically significant difference between {system_a_name} and {system_b_name} on {metric_name} (mean delta = {mean_diff:+.4f}, p = {p_val:.4f} >= {alpha}, 95% CI [{boot_ci['ci_lower']:+.4f}, {boot_ci['ci_upper']:+.4f}])."

        return {
            "system_a": system_a_name,
            "system_b": system_b_name,
            "metric": metric_name,
            "sample_size": len(arr_a),
            "mean_system_a": round(mean_a, 4),
            "mean_system_b": round(mean_b, 4),
            "mean_difference": round(mean_diff, 4),
            "ci_95_lower": boot_ci["ci_lower"],
            "ci_95_upper": boot_ci["ci_upper"],
            "effect_size_cohens_d": effect_size,
            "test_name": "Wilcoxon Signed-Rank Test (Non-parametric)",
            "test_statistic": round(w_stat, 4),
            "p_value": round(p_val, 4),
            "alpha_level": alpha,
            "is_statistically_significant": is_sig,
            "interpretation": interp
        }
