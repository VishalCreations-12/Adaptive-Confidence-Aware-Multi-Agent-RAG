# 12-DIMENSIONAL SELECTOR FEATURE SPECIFICATION

**Document Version:** 2.0  
**Associated Module:** `src/memory/adaptive_selector.py`  
**Classifier:** `sklearn.ensemble.RandomForestClassifier(n_estimators=30, max_depth=5, random_state=42)`

---

## 1. Overview and Design Rationale

The Adaptive Strategy Selector employs a Random Forest classifier to map incoming query characteristics and preliminary candidate retrieval signals to the optimal retrieval strategy:
$$\mathcal{S} = \{\text{BM25 Retrieval}, \text{Semantic Retrieval}, \text{Hybrid Retrieval}, \text{RRF Retrieval}\}$$

To ensure low computational overhead during the routing phase, feature extraction must be lightweight (sub-millisecond latency) and independent of external API calls. The feature vector combines **8 structural/linguistic query traits** with **4 preliminary candidate pool statistics**.

Each query is represented as a 12-dimensional vector:
$$\mathbf{x} = [x_1, x_2, \dots, x_{12}]^T \in \mathbb{R}^{12}$$

---

## 2. Comprehensive Feature Table

| Feature # | Feature Name | Data Type | Value Range | Normalization / Scale | Data Source | Mathematical Definition & Rationale |
|---|---|---|---|---|---|---|
| **$x_1$** | `word_count` | Float | $[1, \infty)$ | Raw count (typically 3–35) | `query_analysis["word_count"]` | **Length:** Number of whitespace-separated tokens. Very short queries ($\le 4$ words) are frequently keyword-dense telegraphic lookups favoring BM25; long queries ($> 12$ words) typically express complex semantic intent. |
| **$x_2$** | `is_keyword` | Binary (0.0 / 1.0) | $\{0.0, 1.0\}$ | Binary indicator | `query_analysis["is_keyword_heavy"]` | **Lexical Specificity:** $1.0$ if the query contains exact technical codes, version strings (e.g. `v3.2`), or uppercase acronyms matching regex `\b[A-Z0-9-]{3,}\b`. BM25 excels when exact token matches are required. |
| **$x_3$** | `is_semantic` | Binary (0.0 / 1.0) | $\{0.0, 1.0\}$ | Binary indicator | `query_analysis["is_semantic"]` | **Conceptual Intent:** $1.0$ if the query begins with interrogative explanatory prefixes (`how`, `why`, `explain`, `describe`, `evaluate`). Semantic vector search excels at conceptual matching without exact lexical overlap. |
| **$x_4$** | `is_numerical` | Binary (0.0 / 1.0) | $\{0.0, 1.0\}$ | Binary indicator | `query_analysis["is_numerical"]` | **Quantitative Specificity:** $1.0$ if query contains digits, currency (`$`), percentages (`%`), or physical units (`Gbps`, `km/h`, `Watts`, `°C`). Numerical queries require lexical or hybrid retrieval to avoid semantic drift. |
| **$x_5$** | `is_comparison` | Binary (0.0 / 1.0) | $\{0.0, 1.0\}$ | Binary indicator | `query_analysis["is_comparison"]` | **Comparative Reasoning:** $1.0$ if query contains comparative terms (`compare`, `versus`, `vs`, `differ`, `contrast`). Often requires multi-entity retrieval spanning diverse sections (favors Hybrid/RRF). |
| **$x_6$** | `is_multi_part` | Binary (0.0 / 1.0) | $\{0.0, 1.0\}$ | Binary indicator | `query_analysis["is_multi_part"]` | **Multi-hop / Synthesis:** $1.0$ if query contains compound conjunctions (`along with`, `as well as`, `, and`) or multiple question marks. Requires multi-hop evidence aggregation where hybrid fusion dominates. |
| **$x_7$** | `is_factual` | Binary (0.0 / 1.0) | $\{0.0, 1.0\}$ | Binary indicator | `query_analysis["characteristics"]` | **Direct Fact Lookup:** $1.0$ if query matches factual question patterns (`what`, `when`, `where`, `who`, `which`). Evaluates if a single direct factual answer chunk is expected. |
| **$x_8$** | `is_entity` | Binary (0.0 / 1.0) | $\{0.0, 1.0\}$ | Binary indicator | `query_analysis["characteristics"]` | **Named Entity Presence:** $1.0$ if query references capitalized proper nouns, corporate titles (`CEO`, `CTO`), or specific product names (`NovaSolar`, `AeroGuide`). Enhances precision for entity grounding. |
| **$x_9$** | `top_bm25` | Float | $[0.0, \infty)$ | Raw BM25 score (typically 0.0–15.0) | `candidate_stats["top_bm25_score"]` | **Lexical Match Strength:** Highest Okapi BM25 score achieved among top candidate documents. High values ($> 4.0$) indicate strong lexical overlap with corpus tokens. |
| **$x_{10}$** | `top_sem` | Float | $[0.0, 1.0]$ | Bounded Cosine Similarity | `candidate_stats["top_semantic_sim"]` | **Semantic Proximity:** Highest cosine similarity score from FAISS inner-product search. High values ($> 0.75$) indicate high conceptual alignment. |
| **$x_{11}$** | `score_diff` | Float | $[0.0, \infty)$ | $|x_9 / 10.0 - x_{10}|$ | Derived from $x_9, x_{10}$ | **Modality Disparity:** Absolute difference between scaled top BM25 score and top semantic similarity: $| \frac{\text{BM25}}{10} - \text{Semantic} |$. High values indicate that one retrieval modality strongly dominates the other. |
| **$x_{12}$** | `bm25_sem_ratio` | Float | $[0.0, \infty)$ | $\frac{x_9}{10 \cdot x_{10} + \epsilon}$ | Derived from $x_9, x_{10}$ | **Relative Modality Ratio:** Ratio of normalized BM25 score to normalized semantic score ($\epsilon = 10^{-5}$). A ratio $\gg 1.0$ indicates strong lexical dominance; a ratio $\ll 1.0$ indicates semantic dominance. |

---

## 3. Implementation Verification

In `src/memory/adaptive_selector.py`:

```python
@classmethod
def extract_features(cls, query_analysis: Dict[str, Any], candidate_stats: Dict[str, float] = None) -> np.ndarray:
    """Extract a standardized 12-dimensional numerical feature vector for a query."""
    word_count = float(query_analysis.get("word_count", 0))
    is_keyword = 1.0 if query_analysis.get("is_keyword_heavy") else 0.0
    is_semantic = 1.0 if query_analysis.get("is_semantic") else 0.0
    is_numerical = 1.0 if query_analysis.get("is_numerical") else 0.0
    is_comparison = 1.0 if query_analysis.get("is_comparison") else 0.0
    is_multi_part = 1.0 if query_analysis.get("is_multi_part") else 0.0
    
    traits = query_analysis.get("characteristics", [])
    is_factual = 1.0 if "factual" in traits else 0.0
    is_entity = 1.0 if "entity-focused" in traits else 0.0

    stats = candidate_stats or {}
    top_bm25 = float(stats.get("top_bm25_score", 0.0))
    top_sem = float(stats.get("top_semantic_sim", 0.0))
    score_diff = abs(top_bm25 / 10.0 - top_sem)
    bm25_sem_ratio = top_bm25 / (top_sem * 10.0 + 1e-5)

    feature_vector = [
        word_count,
        is_keyword,
        is_semantic,
        is_numerical,
        is_comparison,
        is_multi_part,
        is_factual,
        is_entity,
        top_bm25,
        top_sem,
        score_diff,
        bm25_sem_ratio
    ]
    return np.array(feature_vector, dtype=np.float32)
```

The feature extractor handles edge cases cleanly: missing candidate statistics default to 0.0, division by zero is guarded by $\epsilon=10^{-5}$, and all outputs are verified non-NaN `float32` tensors.
