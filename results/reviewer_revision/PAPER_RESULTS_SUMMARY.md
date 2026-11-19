# PAPER-READY EXPERIMENTAL RESULTS SUMMARY
**Single Source of Truth for Revised Paper Manuscript**

---

## 1. Experimental Overview
- **Knowledge Base Corpus:** 12-page comprehensive technical research compendium (38 chunks).
- **Evaluation Benchmark:** 200 multi-domain queries across 6 categories.
- **Data Splits:**
  - Training Split: 120 queries (60.0%)
  - Validation Split: 40 queries (20.0%)
  - Held-Out Test Split: 40 queries (20.0%)
- **Rank Cutoff:** $K = 3$ across all systems.
- **Significance Test:** Paired Wilcoxon signed-rank test (two-sided, Pratt zero-handling) + 10,000-resample bootstrap 95% CIs.

---

## 2. Master System Comparison (Held-Out Test Split, N = 40)

| System | Precision@3 | Recall@3 | MRR | nDCG@3 | Context Relevance | Latency (ms) | Reward |
|---|---|---|---|---|---|---|---|
| **BM25 Baseline** | 0.5667 | 0.6536 | 0.8708 | 0.7026 | 0.8888 | 2.5 | 0.6838 |
| **Dense Baseline** | 0.5167 | 0.5849 | 0.8542 | 0.6549 | 0.8012 | 10.5 | 0.6452 |
| **Fixed Hybrid Baseline** | 0.5250 | 0.6071 | 0.8708 | 0.6689 | 0.9138 | 13.0 | 0.6726 |
| **RRF Fusion Baseline** | 0.5583 | 0.6438 | 0.8458 | 0.6902 | 0.8950 | 14.5 | 0.6979 |
| **Tuned Hybrid Baseline** | 0.5250 | 0.6071 | 0.8708 | 0.6689 | 0.9138 | 13.2 | 0.6756 |
| **Proposed V1 (Heuristic)** | 0.5167 | 0.5946 | 0.8708 | 0.6593 | 0.9075 | 12.2 | 0.6663 |
| **Proposed V2 (Learned Adaptive)** | **0.5500** | **0.6265** | **0.8833** | **0.6929** | **0.8950** | **14.6** | **0.6926** |
| **Oracle Router (Ceiling)** | *0.6167* | *0.6982* | *0.9333* | *0.7664* | *0.8888* | *14.0* | *0.7731* |

---

## 3. Real Independent Ablation Suite (Held-Out Test Split, N = 40)

| Ablation Variant | Mean P@3 | Mean Recall@3 | Mean MRR | Mean nDCG@3 | Mean Context Relevance |
|---|---|---|---|---|---|
| **A0: Full V2 System** | 0.5500 | 0.6265 | 0.8833 | 0.6929 | 0.8950 |
| **A1: V2 w/o Query Traits** | 0.5500 | 0.6265 | 0.8833 | 0.6929 | 0.8950 |
| **A2: V2 w/o Evidence Judge** | 0.5833 | 0.6641 | 0.8833 | 0.7202 | 0.8825 |
| **A3: V2 w/o Confidence Mechanism** | 0.5500 | 0.6265 | 0.8833 | 0.6929 | 0.8950 |
| **A4: V2 w/o Historical Memory** | 0.5083 | 0.5863 | 0.8708 | 0.6534 | 0.9075 |
| **A5: Fixed Hybrid Baseline** | 0.5250 | 0.6071 | 0.8708 | 0.6689 | 0.9138 |

---

## 4. Routing Generalization Evaluation
- **Train Routing Accuracy:** **89.2%** ($N = 120$)
- **Validation Routing Accuracy:** **80.0%** ($N = 40$)
- **Held-Out Test Routing Accuracy:** **80.0%** ($N = 40$)
- **Oracle Routing Headroom:** Oracle nDCG@3 (0.7664) vs V2 nDCG@3 (0.6929) = **+0.0735** delta.
