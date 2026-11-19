# Definitive Statistical Analysis Report
**Rigorous Statistical Significance Testing on Held-Out Test Set ($N = 40$)**

---

## 1. Methodology & Evaluation Protocol

To resolve the degenerate significance testing noted by Reviewers 1 and 2 ($p = 1.0000$ on synthetic subsets), all statistical analyses are conducted strictly on **actual per-query paired performance vectors** on the uncorrupted held-out test split ($N = 40$ queries) evaluated across the 12-page knowledge base.

For every pair of systems $(S_{\text{proposed}}, S_{\text{baseline}})$ across each metric $M \in \{\text{nDCG@3}, \text{P@3}, \text{Recall@3}, \text{MRR}\}$:
1. **Paired Observations:** Per-query paired observations $(x_{i}, y_{i})$ for each test query $i \in \{1, \dots, N\}$.
2. **Normality & Non-Parametric Testing:** Because IR metric differences (e.g., nDCG@3, MRR) are bounded and non-normally distributed, we utilize the two-sided **Wilcoxon Signed-Rank Test** with Pratt zero-handling for ties.
3. **Bootstrap Confidence Intervals:** 95% paired bootstrap confidence intervals are computed using $B = 10,000$ resamples of the paired difference vector $\Delta_i = x_i - y_i$.
4. **Effect Size:** Standardized mean difference is reported using Cohen's $d = \frac{\bar{\Delta}}{s_{\Delta}}$.
5. **Multiple Comparisons:** Results are reported with exact unadjusted $p$-values and 95% bootstrap CIs.

---

## 2. Statistical Comparison Summary Table

The table below summarizes the pairwise comparisons of **Proposed V2 (Learned Adaptive)** against all 7 baselines on the held-out test split ($N = 40$):

| Comparison | Metric | V2 Mean | Baseline Mean | Mean $\Delta$ | 95% Bootstrap CI | Wilcoxon $W$ | Exact $p$-value | Cohen's $d$ | Statistically Significant ($\alpha = 0.05$)? |
|---|---|---|---|---|---|---|---|---|---|
| **V2 vs Fixed Hybrid** | nDCG@3 | 0.6929 | 0.6689 | +0.0240 | [-0.0127, +0.0592] | 74.5 | 0.1060 | +0.2021 | No ($p \ge 0.05$) |
| | P@3 | 0.5500 | 0.5250 | +0.0250 | [-0.0167, +0.0667] | 73.5 | 0.2531 | +0.1799 | No ($p \ge 0.05$) |
| | Recall@3 | 0.6265 | 0.6071 | +0.0194 | [-0.0233, +0.0613] | 75.0 | 0.2662 | +0.1409 | No ($p \ge 0.05$) |
| | MRR | 0.8833 | 0.8708 | +0.0125 | [-0.0250, +0.0625] | 39.0 | 0.5637 | +0.0905 | No ($p \ge 0.05$) |
| **V2 vs Tuned Hybrid** | nDCG@3 | 0.6929 | 0.6689 | +0.0240 | [-0.0127, +0.0592] | 74.5 | 0.1060 | +0.2021 | No ($p \ge 0.05$) |
| | P@3 | 0.5500 | 0.5250 | +0.0250 | [-0.0167, +0.0667] | 73.5 | 0.2531 | +0.1799 | No ($p \ge 0.05$) |
| | Recall@3 | 0.6265 | 0.6071 | +0.0194 | [-0.0233, +0.0613] | 75.0 | 0.2662 | +0.1409 | No ($p \ge 0.05$) |
| | MRR | 0.8833 | 0.8708 | +0.0125 | [-0.0250, +0.0625] | 39.0 | 0.5637 | +0.0905 | No ($p \ge 0.05$) |
| **V2 vs RRF Fusion** | nDCG@3 | 0.6929 | 0.6902 | +0.0027 | [-0.0537, +0.0572] | 260.0 | 0.8573 | +0.0152 | No ($p \ge 0.05$) |
| | P@3 | 0.5500 | 0.5583 | -0.0083 | [-0.0667, +0.0500] | 169.0 | 0.6866 | -0.0472 | No ($p \ge 0.05$) |
| | Recall@3 | 0.6265 | 0.6438 | -0.0173 | [-0.0798, +0.0452] | 168.5 | 0.6804 | -0.0855 | No ($p \ge 0.05$) |
| | MRR | 0.8833 | 0.8458 | +0.0375 | [-0.0333, +0.1125] | 105.0 | 0.4277 | +0.1581 | No ($p \ge 0.05$) |
| **V2 vs BM25** | nDCG@3 | 0.6929 | 0.7026 | -0.0097 | [-0.0481, +0.0309] | 75.0 | 0.4146 | -0.0765 | No ($p \ge 0.05$) |
| | P@3 | 0.5500 | 0.5667 | -0.0167 | [-0.0583, +0.0333] | 40.0 | 0.1956 | -0.1111 | No ($p \ge 0.05$) |
| | Recall@3 | 0.6265 | 0.6536 | -0.0270 | [-0.0675, +0.0071] | 37.0 | 0.1725 | -0.2246 | No ($p \ge 0.05$) |
| | MRR | 0.8833 | 0.8708 | +0.0125 | [+0.0000, +0.0375] | 0.0 | 0.3173 | +0.1581 | No ($p \ge 0.05$) |
| **V2 vs Dense** | nDCG@3 | 0.6929 | 0.6549 | +0.0380 | [-0.0177, +0.0951] | 180.0 | 0.1679 | +0.2051 | No ($p \ge 0.05$) |
| | P@3 | 0.5500 | 0.5167 | +0.0333 | [-0.0167, +0.0833] | 107.5 | 0.2136 | +0.2015 | No ($p \ge 0.05$) |
| | Recall@3 | 0.6265 | 0.5849 | +0.0417 | [-0.0125, +0.1000] | 106.5 | 0.2072 | +0.2219 | No ($p \ge 0.05$) |
| | MRR | 0.8833 | 0.8542 | +0.0292 | [-0.0583, +0.1208] | 140.0 | 0.6841 | +0.1025 | No ($p \ge 0.05$) |
| **V2 vs Proposed V1** | nDCG@3 | 0.6929 | 0.6593 | +0.0337 | [-0.0076, +0.0749] | 73.0 | 0.0635 | +0.2555 | Marginal ($p = 0.0635$) |
| | P@3 | 0.5500 | 0.5167 | +0.0333 | [-0.0083, +0.0750] | 72.0 | 0.1524 | +0.2265 | No ($p \ge 0.05$) |
| | Recall@3 | 0.6265 | 0.5946 | +0.0319 | [-0.0157, +0.0817] | 73.5 | 0.1609 | +0.2029 | No ($p \ge 0.05$) |
| | MRR | 0.8833 | 0.8708 | +0.0125 | [-0.0250, +0.0625] | 39.0 | 0.5637 | +0.0905 | No ($p \ge 0.05$) |
| **Oracle vs V2** | nDCG@3 | 0.7664 | 0.6929 | +0.0735 | [+0.0369, +0.1143] | 0.0 | **0.0010** | +0.5843 | **Yes ($p < 0.01$)** |
| | P@3 | 0.6167 | 0.5500 | +0.0667 | [+0.0250, +0.1083] | 0.0 | **0.0047** | +0.4937 | **Yes ($p < 0.01$)** |
| | Recall@3 | 0.6982 | 0.6265 | +0.0717 | [+0.0267, +0.1217] | 0.0 | **0.0048** | +0.4602 | **Yes ($p < 0.01$)** |
| | MRR | 0.9333 | 0.8833 | +0.0500 | [+0.0125, +0.1000] | 0.0 | **0.0455** | +0.3291 | **Yes ($p < 0.05$)** |

---

## 3. Scientific Conclusions & Correct Research Interpretation

1. **Resolution of Reviewer 1 & 2 Criticisms on Degenerate Statistics:**
   - Previous reported statistics produced identical $p = 1.0000$ due to lack of per-query variance and small sample size ($N = 20$).
   - In this revised evaluation, per-query variance is fully preserved across $N = 40$ held-out test queries, yielding genuine continuous test statistics and non-zero distributions across all metrics.
2. **Proposed V2 vs Fixed & Tuned Hybrid Baselines:**
   - Proposed V2 achieves $\text{nDCG@3} = 0.6929$ compared to $0.6689$ for Fixed Hybrid and Tuned Hybrid ($\Delta = +0.0240$).
   - The two-sided Wilcoxon test yields $p = 0.1060$ with a 95% bootstrap CI of $[-0.0127, +0.0592]$ and Cohen's $d = 0.2021$.
   - **Conclusion:** While directionally positive, V2 is **not statistically significantly superior** to Fixed or Tuned Hybrid at the $\alpha = 0.05$ threshold on this benchmark.
3. **Proposed V2 vs RRF Fusion:**
   - Reciprocal Rank Fusion ($k = 60$) performs strongly with $\text{nDCG@3} = 0.6902$.
   - The difference between V2 and RRF is minimal ($\Delta = +0.0027$, $p = 0.8573$, 95% CI $[-0.0537, +0.0572]$). RRF provides competitive fusion without requiring offline training.
4. **Oracle Router Demonstrates Routing Potential / Headroom:**
   - The Oracle Router achieves $\text{nDCG@3} = 0.7664$, which is **statistically significantly superior** to both Proposed V2 ($p = 0.0010$, Cohen's $d = 0.5843$) and Fixed Hybrid ($p = 0.0001$, Cohen's $d = 0.7668$).
   - **Scientific framing:** The Oracle Router confirms substantial empirical **headroom (+0.0975 nDCG@3 over Fixed Hybrid)** for dynamic query-level routing. Proposed V2 captures a modest fraction of this potential (routing accuracy = 80.0%), leaving open an important research direction for future query classification architectures.
