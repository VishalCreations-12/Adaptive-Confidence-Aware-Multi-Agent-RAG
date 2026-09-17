# V2 ADAPTIVE STRATEGY LEARNING ARCHITECTURE

## 1. Overview
The core research novelty of V2 is turning the passive JSON memory logger into an **active machine learning strategy selector** that learns from historical retrieval outcomes.

## 2. Learning Mechanism & Feature Space
The V2 Strategy Selector extracts a 12-dimensional numerical feature vector $X \in \mathbb{R}^{12}$ for every query:
1. `word_count`: Query length in words.
2. `is_keyword_heavy`: Binary indicator for uppercase model codes / acronyms.
3. `is_semantic`: Binary indicator for conceptual question prefixes.
4. `is_numerical`: Binary indicator for numbers, percentages, or units.
5. `is_comparison`: Binary indicator for comparative terms (`compare`, `vs`).
6. `is_multi_part`: Binary indicator for multi-part questions or conjunctions.
7. `is_factual`: Binary indicator for factual question prefixes.
8. `is_entity`: Binary indicator for proper nouns / leadership names.
9. `top_bm25_score`: Highest BM25 score magnitude.
10. `top_semantic_sim`: Highest cosine similarity score.
11. `score_diff`: $|S_{\text{bm25}}/10 - S_{\text{sem}}|$.
12. `bm25_sem_ratio`: $S_{\text{bm25}} / (10 \cdot S_{\text{sem}} + 1e-5)$.

## 3. Classifier Model
- **Algorithm:** `RandomForestClassifier(n_estimators=30, max_depth=5, random_state=42)`
- **Target Classes:** `BM25 Retrieval`, `Semantic Retrieval`, `Hybrid Retrieval`
- **Cold-Start Handling:** Falls back to deterministic heuristic choice (V1) if historical records $< 3$.

## 4. Transparent Reward Formula
$$\text{Reward} = 0.40 \cdot \text{MRR} + 0.35 \cdot \text{Recall@3} + 0.15 \cdot \text{Confidence} - 0.10 \cdot \min(1.0, \frac{\text{Latency}}{100\text{ms}})$$

## 5. Sequential Online Learning Simulation
For query $i$:
1. Predict strategy using model trained on queries $1 \dots i-1$.
2. Execute retrieval & judge evidence.
3. Compute reward & record query $i$ to memory.
4. Retrain classifier on updated memory.
