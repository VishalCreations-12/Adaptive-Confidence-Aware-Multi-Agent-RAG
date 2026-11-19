# SYSTEM ARCHITECTURE & TERMINOLOGY SPECIFICATION

**Document Version:** 2.0  
**Direct Reviewer Response:** R1.5 (Multi-Agent Terminology Overstatement)

---

## 1. Architectural Overview

The **Adaptive Confidence-Aware Retrieval System** is an intelligent retrieval and evidence routing framework designed to optimize context selection for Retrieval-Augmented Generation (RAG). The system replaces static, one-size-fits-all retrieval with an **adaptive, query-conditioned routing architecture** evaluated by a multi-signal **Evidence Judge** and an **Evidence Confidence Scorer**.

```
                         ┌─────────────────────────┐
                         │       User Query        │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │  Query Trait Analyzer   │
                         │  (8 Linguistic Traits)  │
                         └────────────┬────────────┘
                                      │
       ┌──────────────────────────────┼──────────────────────────────┐
       │                              │                              │
       ▼                              ▼                              ▼
┌──────────────┐              ┌──────────────┐              ┌──────────────┐
│ BM25 Lexical │              │ Dense Vector │              │ Hybrid Fusion│
│  Retriever   │              │  (FAISS/L2)  │              │ (Score/RRF)  │
└──────┬───────┘              └──────┬───────┘              └──────┬───────┘
       │                             │                             │
       └─────────────────────────────┼─────────────────────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │    Preliminary Statistics   │
                      │  (Top Scores, Score Ratios) │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │ Adaptive Strategy Selector  │
                      │  (12-Feature Random Forest) │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │    Target Evidence Pool     │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │     Evidence Evaluator      │
                      │   (Consensus, De-duping)    │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │  Evidence Confidence Scorer │
                      │  (Strength, Coverage, Var)  │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │  Grounded Answer Generation │
                      │  (Extractive Synthesis)     │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │ Historical Strategy Memory  │
                      │ (Trajectory Logging/Re-fit) │
                      └─────────────────────────────┘
```

---

## 2. Component Specifications

### 2.1 Ingestion & Indexing Engine
- **Document Parser (`src/ingestion/parser.py`):** Ingests PDF and text files, standardizes whitespace, and extracts page-level metadata using `pypdf`.
- **Document Chunker (`src/ingestion/chunker.py`):** Segments documents into overlapping character chunks ($500$ chars with $100$ char overlap) with sentence-boundary heuristics.
- **Lexical Index:** In-memory Okapi BM25 (`rank-bm25`) constructed over whitespace and punctuation tokenized text.
- **Dense Vector Index:** 384-dimensional dense vectors generated via `SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')`, L2-normalized and indexed in FAISS (`IndexFlatIP`).

### 2.2 Query Trait Analyzer (`src/query_analysis/analyzer.py`)
Extracts 8 linguistic and structural features:
- Word count, lexical keyword density, semantic interrogative intent, numerical indicators, comparative structure, multi-hop syntax, direct fact patterns, and named entity presence.

### 2.3 Candidate Retrieval Strategies (`src/retrieval/`)
1. **BM25 Retriever (`bm25_agent.py`):** Term frequency-inverse document frequency scoring for exact technical codes and identifiers.
2. **Dense Retriever (`semantic_agent.py`):** Bi-encoder cosine similarity search for conceptual, paraphrased queries.
3. **Fixed Hybrid Retriever (`hybrid_agent.py`):** MinMax normalized linear score combination ($\alpha = 0.5, \beta = 0.5$).
4. **Tuned Hybrid Retriever (`tuned_hybrid_agent.py`):** Validation-optimized grid search over $(\alpha, \beta)$ parameters.
5. **Reciprocal Rank Fusion Retriever (`rrf_agent.py`):** Rank-based fusion using standard reciprocal rank discounting ($k = 60$).

### 2.4 Evidence Judge (`src/judge/evidence_judge.py`)
Screens candidate pools, verifies inter-strategy agreement, computes query keyword coverage, and filters duplicate or low-scoring passages.

### 2.5 Confidence Scorer (`src/confidence/confidence_scorer.py`)
Computes an empirical evidence reliability score based on top candidate score strength, consensus ratio, keyword coverage, and score spread.

### 2.6 Adaptive Strategy Selector (`src/memory/adaptive_selector.py`)
A Random Forest classifier that takes the 12-dimensional feature vector (8 query traits + 4 candidate pool statistics) and routes the query to the highest-utility strategy.

### 2.7 Strategy Memory (`src/memory/strategy_memory.py`)
Logs query experiences, predicted vs actual strategies, rewards, and latencies into persistent memory for sequential updates.

---

## 3. Project Terminology Alignment (Addressing Reviewer 1.5)

In response to Reviewer 1's feedback regarding terminology overstatement, we formally distinguish between:
- **Autonomous Agents:** Systems that exhibit goal-directed reasoning, environment observation, multi-step planning, tool use, and inter-agent communication.
- **Retrieval Strategies / Modules:** Individual deterministic or vector scoring algorithms (BM25, dense vector search, hybrid fusion) executed within a controlled pipeline.

| Old Terminology | Revised Accurate Terminology | Architectural Justification |
|---|---|---|
| "Multi-Agent System" | **Adaptive Retrieval Selection Framework** | The retrievers do not communicate autonomously; they are candidate strategies evaluated by an adaptive router. |
| "BM25 Agent" | **BM25 Retriever / Strategy** | Algorithmic lexical ranking function. |
| "Semantic Agent" | **Dense Vector Retriever / Strategy** | Bi-encoder FAISS vector search. |
| "Hybrid Agent" | **Hybrid Fusion Retriever** | Score fusion algorithm. |
| "Agent Committee" | **Candidate Retrieval Pool** | Multi-strategy candidate candidate set. |
| "Agent Consensus" | **Cross-Retriever Agreement** | Overlap in top-$K$ document IDs across ranking lists. |

This revised terminology reflects scientific accuracy and prevents unjustified overclaiming.
