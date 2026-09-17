# QUICK FACULTY REVISION SHEET (V2 ADAPTIVE RAG EDITION)

**Project Title:** Adaptive Confidence-Aware Multi-Agent Retrieval System for RAG  
**Short Title:** Adaptive Multi-Agent RAG V2  
**Student:** Vishal S (22MIS1165) | **Guide:** Dr. Malini A  

---

### Core Viva Q&A (Short & Clear)

1. **Q: What is the main objective of this project?**  
   *A:* To build an adaptive retrieval-augmented generation (RAG) system that uses a committee of 3 retrievers (BM25, Semantic FAISS, MinMax Hybrid), an Evidence Judge, a Confidence Scorer, and a machine learning strategy selector to dynamically pick the best retrieval strategy for any query.

2. **Q: What is the main research contribution / novelty?**  
   *A:* Operating a multi-agent retrieval committee whose strategy selection is dynamically predicted by a Random Forest meta-classifier trained on historical query experiences, evidence judge signals, and empirical confidence rewards.

3. **Q: What are the three retrieval agents?**  
   *1. BM25 (`rank_bm25`):* Exact keyword search.  
   *2. Semantic Vector (`FAISS` + `all-MiniLM-L6-v2`):* 384-dim dense vector cosine similarity (100% local).  
   *3. MinMax Hybrid Fusion:* MinMax normalized weighted sum ($0.5 \times \text{BM25} + 0.5 \times \text{Semantic}$).

4. **Q: How does the V2 system learn over time?**  
   *A:* After each query, the system evaluates the retrieved evidence against ground truth or empirical confidence, calculates a transparent reward ($\text{Reward} = 0.40 \cdot \text{MRR} + 0.35 \cdot \text{Recall} + 0.15 \cdot \text{Confidence} - 0.10 \cdot \text{Latency Penalty}$), logs the experience to Strategy Memory, and retrains the ML selector.

5. **Q: How does answer generation work without external API costs?**  
   *A:* Extractive sentence-level synthesis. The generator extracts exact matching sentences from judged evidence chunks and attaches explicit page and chunk citations. **$0.00 API cost, 100% offline.**

6. **Q: What systems were evaluated in your five-way baseline comparison?**  
   *1. BM25-Only Baseline*  
   *2. Semantic-Only Baseline*  
   *3. Fixed Hybrid Baseline*  
   *4. Proposed V1 Heuristic System*  
   *5. Proposed V2 Learned Adaptive System*

7. **Q: What metrics were evaluated?**  
   *A:* Precision@3, Recall@3, MRR (Mean Reciprocal Rank), nDCG@3, Context Relevance, Strategy Selection Accuracy, Evidence Confidence, and Latency.

8. **Q: Did all system unit tests pass?**  
   *A:* Yes, 13 out of 13 Pytest unit tests passed (100% pass rate).

9. **Q: Where can faculty view live benchmark results and plots?**  
   *A:* In the interactive Streamlit dashboard (`app.py`) under the "RESEARCH DASHBOARD" tab, and in `data/results/plots/`.
