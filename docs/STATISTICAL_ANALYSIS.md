# STATISTICAL SIGNIFICANCE & VALIDATION METHODOLOGY

**Document Version:** 2.0  
**Associated Module:** `src/evaluation/statistical_test.py`  
**Direct Reviewer Responses:** R1.3 (Degenerate Significance Testing), R2.4 ($p = 1.0000$ Is Uninformative)

---

## 1. Deficiencies in Previous Methodology

In the previous revision, statistical significance testing suffered from critical methodological errors:
1. **Single-Metric Reliance on Ceiling MRR:** Statistical evaluation was performed solely on MRR across a 20-query benchmark. Because all systems retrieved the relevant chunk at rank 1, all differences were zero ($\Delta = 0$).
2. **Degenerate $p = 1.0000$ Handling:** The test script contained hard-coded branch logic:
   ```python
   if np.all(diffs == 0):
       return {"p_value": 1.0, ...}
   ```
   This returned $p = 1.0000$, which was scientifically uninformative and prompted legitimate reviewer criticism.
3. **Absence of Confidence Intervals:** No confidence intervals or effect size estimates were reported.

---

## 2. Revised Statistical Protocol

To guarantee rigorous, reproducible, and defensible statistical inference:

### 2.1 Multi-Metric Per-Query Evaluation
Significance testing is evaluated across **four distinct retrieval metrics** on per-query paired vectors:
- **Precision@3** ($\text{P@}3$)
- **Recall@3** ($\text{R@}3$)
- **nDCG@3** ($\text{nDCG@}3$)
- **Mean Reciprocal Rank** ($\text{MRR}$)

Each query $q_i \in Q$ yields paired observations $(X_{A, i}, X_{B, i})$ for systems $A$ and $B$, defining the paired difference vector:
$$D_i = X_{A, i} - X_{B, i}, \quad i = 1, \dots, N$$

---

### 2.2 Paired Non-Parametric Test: Wilcoxon Signed-Rank Test
Because retrieval metric distributions are bounded in $[0, 1]$, non-Gaussian, and frequently zero-inflated or bimodal, parametric Student's $t$-tests violate normality assumptions.

We apply the **two-sided Wilcoxon signed-rank test** (a non-parametric paired test):
1. Compute absolute differences $|D_i|$ for all non-zero pairs $D_i \ne 0$.
2. Rank the absolute differences $|D_i|$ in ascending order from $1$ to $N_r$.
3. Assign the original sign to the ranks: $W^+ = \sum_{D_i > 0} \text{Rank}(|D_i|)$, $W^- = \sum_{D_i < 0} \text{Rank}(|D_i|)$.
4. The test statistic is $W = \min(W^+, W^-)$.
5. Zero differences are handled using the Pratt method to retain sample size power without bias.

> **Methodological Note:** The Wilcoxon signed-rank test is strictly non-parametric. It makes no assumptions regarding underlying normal distribution.

---

### 2.3 Paired Bootstrap 95% Confidence Intervals
To assess practical effect size and statistical estimation uncertainty without distributional assumptions, we compute **non-parametric paired bootstrap confidence intervals**:
1. For $b = 1, \dots, B$ ($B = 10,000$ iterations):
   - Sample $N$ paired differences with replacement from $\{D_1, \dots, D_N\}$ to obtain $D^{*(b)}$.
   - Compute the bootstrap sample mean difference: $\bar{D}^{*(b)} = \frac{1}{N} \sum_{i=1}^N D_i^{*(b)}$.
2. Compute the 2.5th and 97.5th percentiles of the empirical bootstrap distribution:
   $$\text{CI}_{95\%} = \left[ Q_{0.025}(\bar{D}^*), Q_{0.975}(\bar{D}^*) \right]$$
3. If $0 \notin \text{CI}_{95\%}$, the mean difference is statistically distinguishable from zero at $\alpha = 0.05$.

---

### 2.4 Effect Size: Cohen's $d$
Standardized effect size is computed on the paired differences:
$$d = \frac{\bar{D}}{s_D} = \frac{\frac{1}{N} \sum_{i=1}^N D_i}{\sqrt{\frac{1}{N-1} \sum_{i=1}^N (D_i - \bar{D})^2}}$$

Interpretation following standard conventions:
- $|d| < 0.2$: Negligible effect
- $0.2 \le |d| < 0.5$: Small effect
- $0.5 \le |d| < 0.8$: Medium effect
- $|d| \ge 0.8$: Large effect

---

### 2.5 Multiple Comparison Correction
When testing multiple baseline pairs simultaneously ($k = 7$ pairs), family-wise error rate is controlled using the **Holm-Bonferroni step-down procedure**:
1. Sort raw $p$-values: $p_{(1)} \le p_{(2)} \le \dots \le p_{(k)}$.
2. Test $p_{(j)} \le \frac{\alpha}{k - j + 1}$ for $j = 1, \dots, k$.
3. Reject $H_0^{(j)}$ until the first non-significant rank.

---

## 3. Reporting Standard

Every pairwise statistical comparison outputs:
```text
System A vs System B on Metric:
  N (Queries):                200
  Mean System A:              0.8425
  Mean System B:              0.7950
  Mean Difference (A - B):    +0.0475
  Bootstrap 95% CI:           [+0.0180, +0.0770]
  Wilcoxon Statistic (W):     412.5
  Wilcoxon p-value:           0.0032
  Holm-Adjusted p-value:      0.0192
  Cohen's d:                  0.412 (Small-to-Medium effect)
  Statistically Significant:  YES (p < 0.05, 0 not in 95% CI)
```
