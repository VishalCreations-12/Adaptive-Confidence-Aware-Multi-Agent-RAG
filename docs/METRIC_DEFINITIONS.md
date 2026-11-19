# FORMAL RETRIEVAL & EVALUATION METRIC DEFINITIONS

**Document Version:** 2.0  
**Associated Modules:** `src/evaluation/metrics_calculator.py`, `src/evaluation/oracle_router.py`, `src/memory/adaptive_selector.py`

---

## 1. Overview

This document specifies the exact mathematical formulations, boundary conditions, input requirements, and aggregation procedures for all performance metrics used across baseline comparisons, ablation studies, and statistical significance testing.

Let:
- $Q$ denote the evaluation query set with size $N = |Q|$.
- For a query $q \in Q$, let $\mathcal{R}_q = [d_{(1)}, d_{(2)}, \dots, d_{(K)}]$ denote the ranked list of retrieved chunk identifiers returned by a system at cutoff $K$ (default $K = 3$).
- Let $\mathcal{G}_q \subset \mathcal{D}$ denote the non-empty ground-truth set of relevant chunk identifiers for query $q$.
- Let $\mathbb{I}(\cdot)$ denote the binary indicator function, taking value 1 if the condition is satisfied and 0 otherwise.

---

## 2. Core Metrics

### 2.1 Precision@K ($\text{P@}K$)
Precision at rank cutoff $K$ measures the fraction of retrieved items within the top-$K$ slots that are genuinely relevant to query $q$.

$$\text{P@}K(q) = \frac{1}{K} \sum_{i=1}^K \mathbb{I}(d_{(i)} \in \mathcal{G}_q)$$

- **Input:** Ranked list of retrieved chunk IDs $\mathcal{R}_q$, ground-truth relevant chunk IDs $\mathcal{G}_q$, cutoff $K \in \mathbb{N}^+$.
- **Range:** $[0.0, 1.0]$. Higher is better.
- **Edge Cases:** If $\mathcal{R}_q = \emptyset$ or $\mathcal{G}_q = \emptyset$, $\text{P@}K(q) = 0.0$.
- **Mean Aggregate:** $\text{P@}K = \frac{1}{N} \sum_{q \in Q} \text{P@}K(q)$.

---

### 2.2 Recall@K ($\text{R@}K$)
Recall at rank cutoff $K$ measures the fraction of all known relevant items that were successfully retrieved in the top-$K$ slots.

$$\text{R@}K(q) = \frac{1}{|\mathcal{G}_q|} \sum_{i=1}^K \mathbb{I}(d_{(i)} \in \mathcal{G}_q)$$

- **Input:** Ranked list of retrieved chunk IDs $\mathcal{R}_q$, ground-truth relevant chunk IDs $\mathcal{G}_q$, cutoff $K \in \mathbb{N}^+$.
- **Range:** $[0.0, 1.0]$. Higher is better.
- **Edge Cases:** If $\mathcal{R}_q = \emptyset$, $\text{R@}K(q) = 0.0$.
- **Mean Aggregate:** $\text{R@}K = \frac{1}{N} \sum_{q \in Q} \text{R@}K(q)$.

---

### 2.3 Mean Reciprocal Rank (MRR)
Reciprocal Rank measures the reciprocal of the rank position of the **first** relevant chunk retrieved.

$$\text{RR}(q) = \begin{cases} 
\frac{1}{\min \{ i \in \{1, \dots, |\mathcal{R}_q|\} \mid d_{(i)} \in \mathcal{G}_q \}} & \text{if } \exists d_{(i)} \in \mathcal{G}_q \\ 
0.0 & \text{otherwise} 
\end{cases}$$

$$\text{MRR} = \frac{1}{N} \sum_{q \in Q} \text{RR}(q)$$

- **Input:** Ranked retrieved list $\mathcal{R}_q$, ground truth $\mathcal{G}_q$.
- **Range:** $[0.0, 1.0]$. Higher is better.
- **Note on Reviewer 2.3:** On trivial benchmarks, if all retrievers place a relevant document at rank 1, $\text{RR}(q) = 1.0$ for all systems, destroying discriminative power. On our expanded 200-query benchmark with hard distractors, reciprocal ranks differentiate methods that rank the primary relevant chunk at rank 1 vs rank 2 or 3.

---

### 2.4 Normalized Discounted Cumulative Gain at K ($\text{nDCG@}K$)
$\text{nDCG@}K$ evaluates ranking quality by penalizing relevant documents appearing lower in the ranked list with a logarithmic discount.

$$\text{DCG@}K(q) = \sum_{i=1}^K \frac{\mathbb{I}(d_{(i)} \in \mathcal{G}_q)}{\log_2(i + 1)}$$

$$\text{IDCG@}K(q) = \sum_{i=1}^{\min(K, |\mathcal{G}_q|)} \frac{1}{\log_2(i + 1)}$$

$$\text{nDCG@}K(q) = \begin{cases} 
\frac{\text{DCG@}K(q)}{\text{IDCG@}K(q)} & \text{if } \text{IDCG@}K(q) > 0 \\ 
0.0 & \text{otherwise} 
\end{cases}$$

- **Input:** Ranked retrieved list $\mathcal{R}_q$, ground truth $\mathcal{G}_q$, cutoff $K$.
- **Range:** $[0.0, 1.0]$. Higher is better.
- **Mean Aggregate:** $\text{nDCG@}K = \frac{1}{N} \sum_{q \in Q} \text{nDCG@}K(q)$.

---

### 2.5 Context Relevance
Context Relevance assesses the coverage of essential informative query terms and expected factual keywords within the retrieved text blocks.

Let $\mathcal{W}_q = \{w_1, w_2, \dots, w_M\}$ be the set of pre-validated query-grounded essential keywords (technical identifiers, numbers, key entities, and core attributes) associated with query $q$. Let $\mathcal{T}(\mathcal{R}_q) = \bigcup_{c \in \mathcal{R}_q} \text{text}(c)$ be the concatenated text of the top-$K$ retrieved chunks.

$$\text{Context Relevance}(q) = \frac{1}{|\mathcal{W}_q|} \sum_{w \in \mathcal{W}_q} \mathbb{I}(w \text{ is a substring of } \mathcal{T}(\mathcal{R}_q)_{\text{lowercase}})$$

- **Type:** Deterministic, rule-based lexical coverage metric.
- **Range:** $[0.0, 1.0]$. Higher is better.
- **Ground Truth Dependency:** Requires pre-validated query keywords $\mathcal{W}_q$ defined in `ground_truth.json`.
- **Rationale:** Guarantees that the retrieved context actually contains the specific data points (e.g. `AES-256`, `28.4%`, `Elena Rostova`) needed for the generator to formulate an unhallucinated, fully grounded answer.

---

### 2.6 Routing Accuracy
Routing Accuracy evaluates whether the routing selector predicted the optimal retrieval strategy for a query.

$$\text{Routing Accuracy}(q) = \mathbb{I}(\hat{S}(q) = S^*(q))$$

$$\text{Overall Routing Accuracy} = \frac{1}{N} \sum_{q \in Q} \mathbb{I}(\hat{S}(q) = S^*(q))$$

where:
- $\hat{S}(q) \in \mathcal{S}$ is the strategy predicted by the routing module.
- $S^*(q) \in \mathcal{S}$ is the Oracle retrieval strategy for query $q$ (defined below).
- **Separation:** Enforced strictly across Train, Validation, and Held-Out Test splits to prevent data leakage.

---

### 2.7 Oracle Strategy ($S^*$) & Oracle Router
The Oracle Strategy for query $q$ is defined as the candidate retrieval strategy that achieves the highest performance according to the objective ranking metric (primarily $\text{nDCG@}3$, with tie-breaking on $\text{P@}3$ and latency):

$$S^*(q) = \arg\max_{S \in \mathcal{S}} \left[ \text{nDCG@}3(S, q) + 10^{-4} \cdot \text{P@}3(S, q) - 10^{-6} \cdot \text{Latency}(S, q) \right]$$

The **Oracle Router** represents an idealized theoretical upper bound that always selects $S^*(q)$. Measuring the performance gap between $\hat{S}$ and $S^*$ reveals the theoretical headroom available for adaptive query routing.

---

### 2.8 Pipeline Latency
The wall-clock execution time required to process a query through the retrieval pipeline:

$$\text{Latency}(q) = t_{\text{end}}(q) - t_{\text{start}}(q) \quad [\text{milliseconds (ms)}]$$

Includes:
- Feature extraction / query trait analysis.
- Candidate scoring / index retrieval.
- Strategy selection / fusion.
- Evidence judging and confidence scoring.

---

### 2.9 Multi-Component Reward Function
The scalar feedback signal used to evaluate the desirability of a retrieval event:

$$\text{Reward}(q) = w_1 \cdot \text{nDCG@}3(q) + w_2 \cdot \text{Recall@}3(q) + w_3 \cdot \text{Confidence}(q) + w_4 \cdot R_{\text{lat}}(q)$$

where $w_1 = 0.40, w_2 = 0.35, w_3 = 0.15, w_4 = 0.10$, and $R_{\text{lat}}(q) = \frac{1}{1 + \text{Latency}(q)/250.0} \in (0, 1]$.
Documented in detail in `docs/REWARD_DESIGN.md`.
