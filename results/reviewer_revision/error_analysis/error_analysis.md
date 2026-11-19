# ERROR ANALYSIS & FAILURE MODE REPORT

**Date:** November 2026  
**Scope:** Held-Out Test Split ($N = 40$ queries)

---

## 1. Summary of Performance Differences

- **Total Held-Out Test Queries:** 40
- **Queries where V2 outperforms Fixed Hybrid:** 7 (17.5%)
- **Queries where V2 matches Fixed Hybrid:** 31 (77.5%)
- **Queries where V2 underperforms Fixed Hybrid:** 2 (5.0%)
- **Routing Agreement with Oracle Router:** 80.0% (32 / 40)

---

## 2. Failure Mode Analysis

### Failure Mode 1: Misclassification of Complex Multi-Part Inquiries
On highly structured queries that combine both exact numbers and semantic goals, the Random Forest selector occasionally over-indexes on numerical tokens ($x_4 = 1.0$) and selects BM25 instead of Hybrid or RRF fusion.

### Failure Mode 2: Cold-Start Penalty in Sparse Historical Regimes
When memory history is below 25 examples, the selector exhibits high variance and defaults to the heuristic fallback, failing to capitalize on candidate pool score disparities.

---

## 3. Notable Routing Examples

### Successful V2 Adaptive Routing:
- **[Q008 - keyword-heavy]** `ML-KEM Kyber-768 ML-DSA Dilithium-3 FIPS 140-3 Level 4 HSM`
  *Predicted:* `BM25 Retrieval` | *Oracle:* `BM25 Retrieval` | *V2 nDCG:* `1.000` vs *Hybrid nDCG:* `0.765`

- **[Q048 - semantic]** `Describe the post-quantum cryptographic migration strategy being implemented across server nodes.`
  *Predicted:* `BM25 Retrieval` | *Oracle:* `BM25 Retrieval` | *V2 nDCG:* `0.704` vs *Hybrid nDCG:* `0.469`

- **[Q075 - semantic]** `Can you elaborate on: Explain the capital expenditure planning supporting NovaTech's upcoming European robotics expansion.`
  *Predicted:* `Semantic Retrieval` | *Oracle:* `Semantic Retrieval` | *V2 nDCG:* `0.704` vs *Hybrid nDCG:* `0.531`


### V2 Suboptimal Routing Cases:
- **[Q151 - comparison]** `Compare the operational purpose and technical architecture of the NovaSolar-X module with the AeroGuide UAV.`
  *Predicted:* `Semantic Retrieval` | *Oracle:* `BM25 Retrieval` | *V2 nDCG:* `0.469` vs *Hybrid nDCG:* `0.704`

- **[Q156 - comparison]** `Contrast the computational latency of edge-based SLAM on the NV-X2 with cloud-tethered robotic processing.`
  *Predicted:* `BM25 Retrieval` | *Oracle:* `Semantic Retrieval` | *V2 nDCG:* `0.000` vs *Hybrid nDCG:* `0.387`

