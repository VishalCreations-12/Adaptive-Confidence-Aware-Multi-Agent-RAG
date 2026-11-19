# REPRODUCIBILITY GUIDE: ADAPTIVE RETRIEVER SELECTION SYSTEM (V2)

This document provides complete, deterministic instructions to reproduce all benchmark datasets, model training, candidate retrieval evaluations, modular ablations, memory sweeps, statistical analyses, publication figures, and the Streamlit research dashboard.

---

## 1. System Environment & Prerequisites

- **Operating System:** Windows 10/11, Ubuntu 20.04+, or macOS 12+
- **Python Version:** Python 3.10+ (Tested on Python 3.10.11)
- **Deterministic Random Seed:** `42` (Enforced across NumPy, Scikit-Learn, and Python random)
- **Primary Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors)
- **External API Dependency:** **ZERO** (100% local CPU/GPU execution; no OpenAI/Anthropic API keys required)

---

## 2. Installation & Dependency Setup

```bash
# Clone or navigate to the repository directory
cd Adaptive-Confidence-Aware-Multi-Agent-RAG-main

# Create and activate a clean virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### Core Requirements (`requirements.txt`):
- `streamlit>=1.30.0`
- `sentence-transformers>=2.2.0`
- `faiss-cpu>=1.7.4`
- `rank-bm25>=0.2.2`
- `scikit-learn>=1.3.0`
- `scipy>=1.11.0`
- `pypdf>=3.17.0`
- `reportlab>=4.0.0`
- `pandas>=2.0.0`
- `numpy>=1.24.0`
- `matplotlib>=3.7.0`
- `pytest>=7.4.0`

---

## 3. Dataset & Benchmark Generation

To regenerate the 12-page comprehensive research knowledge base PDF and the 200-query benchmark dataset from scratch:

```bash
python sample_data/generate_expanded_benchmark.py
```

### Expected Output:
- PDF generated: `sample_data/NovaTech_Research_Knowledge_Base.pdf` (38 chunks parsed)
- Benchmark queries: `data/benchmarks/benchmark_queries.json` (200 queries)
- Gold-standard qrels: `data/benchmarks/ground_truth.json` (Train: 120, Val: 40, Test: 40)

---

## 4. Master Experiment Execution

To execute the complete research pipeline:
1. Ingestion & indexing (BM25 + FAISS)
2. Validation tuning for Tuned Hybrid weights
3. Oracle strategy extraction across all queries
4. V2 Adaptive Selector training (Train split)
5. 8-Way baseline comparison (Held-out Test split + Full benchmark)
6. Real independent ablation suite (A0–A5)
7. Historical memory sweep ($N \in \{0, 10, 25, 50, 100, 120\}$)
8. Paired Wilcoxon signed-rank tests + 10,000-resample bootstrap 95% CIs
9. Error analysis and failure mode extraction
10. Automatic publication figures & markdown tables

Run:
```bash
python scripts/run_reviewer_revision.py
```

Execution time: ~25–40 seconds on standard CPU.

---

## 5. Automated Testing Suite

To verify system integrity, metric accuracy, feature extraction dimensions, and confirm zero synthetic scalar subtraction:

```bash
pytest -v
```

Expected result: **21 passed in ~20s**.

---

## 6. Interactive Web Research Dashboard

To launch the interactive Streamlit research platform:

```bash
streamlit run app.py
```
Open browser to `http://localhost:8501`.

---

## 7. Results Directory Hierarchy

All outputs are saved deterministically to `results/reviewer_revision/`:
```text
results/reviewer_revision/
├── raw/
│   ├── master_per_query_results.csv
│   └── held_out_test_per_query_results.csv
├── aggregated/
│   ├── held_out_test_summary_metrics.json
│   └── full_benchmark_summary_metrics.json
├── ablation/
│   ├── real_ablation_summary.json
│   └── real_ablation_summary.csv
├── routing/
│   ├── routing_accuracy_report.json
│   └── v2_adaptive_model.pkl
├── oracle/
│   └── oracle_strategies.json
├── memory/
│   ├── memory_sweep_results.json
│   └── memory_sweep_results.csv
├── statistics/
│   ├── statistical_test_results.json
│   └── statistical_summary.csv
├── error_analysis/
│   ├── error_analysis.json
│   └── error_analysis.md
├── figures/
│   ├── 01_eight_way_metrics_comparison.png
│   ├── 02_latency_comparison.png
│   ├── 03_strategy_selection_distribution.png
│   ├── 04_memory_sweep_learning_curve.png
│   ├── 05_ablation_study_comparison.png
│   └── 06_performance_by_query_type.png
├── tables/
│   ├── table_a_main_benchmark.md
│   ├── table_b_ablation_study.md
│   ├── table_c_routing_performance.md
│   ├── table_d_statistical_comparisons.md
│   └── table_e_memory_analysis.md
├── RESEARCH_FINDINGS.md
└── PAPER_RESULTS_SUMMARY.md
```
