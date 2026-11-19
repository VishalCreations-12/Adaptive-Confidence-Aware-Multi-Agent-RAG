# CHANGELOG: PEER-REVIEW REVISION v2.0

**Project:** Adaptive Confidence-Aware Retriever Selection for Retrieval-Augmented Generation  
**Date:** November 2026  
**Status:** Major Architectural, Empirical, and Documentation Overhaul

All notable changes across code, benchmark datasets, experimental protocols, statistical analyses, testing suites, and documentation are documented in this file.

---

## [2.0.0] - 2026-11

### Added
- **Reciprocal Rank Fusion (RRF) Baseline:** Standard rank fusion ($k=60$) combining BM25 and dense bi-encoder rankings (`src/retrieval/rrf_agent.py`).
- **Tuned Hybrid Baseline:** Validation-optimized grid search over $(\alpha, \beta)$ fusion weights frozen prior to test set evaluation (`src/retrieval/tuned_hybrid_agent.py`).
- **Oracle Router:** Theoretical upper-bound router computing best-performing strategy per query according to objective nDCG@3 (`src/evaluation/oracle_router.py`).
- **10x Expanded Benchmark:** Expanded dataset to 200 diverse queries across 6 categories (keyword-heavy, semantic, numerical, factual, comparison, multi-part) with gold-standard relevance qrels (`sample_data/generate_expanded_benchmark.py`).
- **Expanded Knowledge Base:** 12-page comprehensive technical research compendium generating 38 dense chunks across 12 technical domains (`sample_data/generate_sample.py`).
- **Strict Data Splits:** Enforced 60% Train (120 queries) / 20% Validation (40 queries) / 20% Held-Out Test (40 queries) protocol.
- **Bootstrap Significance Testing:** 10,000-resample non-parametric paired bootstrap confidence intervals for mean difference interpretation.
- **Cohen's d Effect Size:** Standardized effect size calculation on paired difference vectors.
- **Integrity Test Suite:** Added `tests/test_ablation_integrity.py` to prevent synthetic scalar subtraction.
- **Orchestration Pipeline:** Single master execution pipeline `scripts/run_reviewer_revision.py`.

### Changed
- **Reward Latency Formulation:** Replaced hard-clipped 100ms penalty with smooth, continuous, strictly monotonic latency discount: $R_{\text{lat}}(\text{lat}) = \frac{1}{1 + \text{latency\_ms} / 250.0} \in (0, 1]$.
- **Target Strategy Definition:** Trained V2 selector strictly on Oracle Strategy targets on the training set, eliminating circular self-training.
- **Streamlit Web Platform:** Upgraded `app.py` with 7 dedicated research navigation tabs, live 8-way comparisons, real ablation results, and memory sweep visualizations.
- **Project Terminology:** Replaced "autonomous multi-agent system" with technically accurate terminology: "retrieval strategies", "adaptive routing selector", and "evidence judge".

### Fixed
- **Constructed / Fabricated Ablations:** Completely removed synthetic scalar subtraction (`row['mrr'] - 0.05`, etc.) from `scripts/run_full_experiments.py`.
- **Degenerate Significance Testing:** Fixed $p = 1.0000$ by evaluating multi-metric paired difference vectors (P@3, R@3, nDCG@3) with Pratt zero-handling.
- **MRR Ceiling Artifact:** Expanded corpus with challenging distractors, establishing real discriminative variance across systems.
- **Data Leakage in Strategy Accuracy:** Separated Train (89.2%), Validation (80.0%), and Held-Out Test (80.0%) routing accuracies.

### Removed
- Removed hard-coded scalar subtractions and synthetic variation fallbacks in `src/evaluation/ablation_study.py`.
- Removed unsubstantiated claims regarding agent autonomy.
- Removed first-person singular pronouns across all documentation.

### Experiment
- **8-Way Main System Comparison:** Evaluated BM25, Dense, Fixed Hybrid, RRF, Tuned Hybrid, Proposed V1, Proposed V2, and Oracle Router across 200 benchmark queries.
- **Real Independent Ablation Study:** Executed variants A0 through A5 with true modular component disabling on the held-out test set.
- **Historical Memory Sweep:** Systematically evaluated history sizes $N \in \{0, 10, 25, 50, 100, 120\}$ to isolate memory dynamics.
- **Reward Weight Sensitivity:** Evaluated Default, Quality-Heavy, Latency-Heavy, and Trust-Heavy reward profiles on validation data.

### Evaluation
- Standardized per-query result schema logging 18 fields per query execution.
- Exported all results into structured hierarchy: `results/reviewer_revision/{raw, aggregated, statistics, ablation, routing, oracle, memory, error_analysis, figures, tables}`.

### Testing
- Expanded test suite to 21 automated unit and integration tests with 100% pass rate.

### Documentation
- Authored `docs/REVIEWER_REVISION_AUDIT.md`.
- Authored `docs/REVIEWER_ISSUE_TRACKER.md`.
- Authored `docs/REVIEWER_RESPONSE_MATRIX.md`.
- Authored `docs/SELECTOR_FEATURES.md`.
- Authored `docs/METRIC_DEFINITIONS.md`.
- Authored `docs/REWARD_DESIGN.md`.
- Authored `docs/STATISTICAL_ANALYSIS.md`.
- Authored `docs/ARCHITECTURE.md`.
- Authored `docs/PAPER_REVISION_PLAN.md`.
- Authored `results/reviewer_revision/RESEARCH_FINDINGS.md`.
- Authored `results/reviewer_revision/PAPER_RESULTS_SUMMARY.md`.
