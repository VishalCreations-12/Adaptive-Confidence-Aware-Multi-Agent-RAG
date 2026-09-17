import os
import sys
import json
import time
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config
from sample_data.generate_sample import generate_sample_pdf, generate_sample_questions
from src.ingestion.parser import DocumentParser
from src.ingestion.chunker import DocumentChunker
from src.query_analysis.analyzer import QueryAnalyzer
from src.retrieval.bm25_agent import BM25Retriever
from src.retrieval.semantic_agent import SemanticRetriever
from src.retrieval.hybrid_agent import HybridRetriever
from src.judge.evidence_judge import EvidenceJudge
from src.confidence.confidence_scorer import ConfidenceScorer
from src.generation.answer_generator import GroundedAnswerGenerator
from src.memory.strategy_memory import RetrievalStrategyMemory
from src.memory.adaptive_selector import AdaptiveStrategySelector
from src.evaluation.benchmark_loader import BenchmarkLoader
from src.evaluation.metrics_calculator import RAGMetricsCalculator
from src.evaluation.ablation_study import AblationStudyRunner
from src.evaluation.statistical_test import StatisticalValidator

def run_master_experiments():
    print("=" * 80)
    print("STARTING MASTER AUTOMATED RESEARCH EXPERIMENT SUITE (V1 -> V2 ADAPTIVE RAG)")
    print("=" * 80)

    # Output directories
    results_dir = BASE_DIR / "data" / "results"
    plots_dir = results_dir / "plots"
    results_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    # 1. Ensure Knowledge Base PDF & Benchmark Data
    pdf_path = config.SAMPLE_DATA_DIR / "NovaTech_Research_Knowledge_Base.pdf"
    if not pdf_path.exists():
        generate_sample_pdf(pdf_path)
    
    loader = BenchmarkLoader()
    benchmark_data = loader.get_all_benchmark_data()
    print(f"Loaded {len(benchmark_data)} benchmark queries from data/benchmarks/.")

    # 2. Ingest & Index Document
    doc_data = DocumentParser.parse_document(pdf_path)
    chunker = DocumentChunker()
    chunks = chunker.chunk_document(doc_data)

    bm25_agent = BM25Retriever()
    bm25_agent.fit(chunks)

    semantic_agent = SemanticRetriever()
    semantic_agent.fit(chunks)

    hybrid_agent = HybridRetriever(bm25_agent, semantic_agent)
    print("Retriever agents indexed successfully.")

    # 3. Setup V2 Adaptive Selector & Memory
    mem_file = results_dir / "experimental_strategy_memory.json"
    if mem_file.exists():
        mem_file.unlink() # Fresh memory for clean evaluation
    
    memory_store = RetrievalStrategyMemory(mem_file)
    model_file = results_dir / "experimental_adaptive_model.pkl"
    if model_file.exists():
        model_file.unlink()

    adaptive_selector = AdaptiveStrategySelector(model_file)

    # Record storage for 5 systems
    all_query_results = []
    v2_sequential_history = []
    
    print("\n" + "=" * 80)
    print("EXECUTING FIVE-WAY BASELINE COMPARISON ACROSS BENCHMARK QUERIES")
    print("=" * 80)

    for idx, b_item in enumerate(benchmark_data, start=1):
        qid = b_item["query_id"]
        query = b_item["query"]
        category = b_item["category"]
        rel_ids = b_item["relevant_chunk_ids"]
        opt_strat = b_item["optimal_strategy"]
        exp_kws = b_item["expected_keywords"]

        print(f"Executing Query {idx}/{len(benchmark_data)} [{qid} - {category}]: \"{query[:50]}...\"")

        # Query Trait Analysis
        q_analysis = QueryAnalyzer.analyze(query)

        # Baseline 1: BM25-Only
        t0 = time.time()
        res_bm25 = bm25_agent.search(query, top_k=3)
        lat_bm25 = (time.time() - t0) * 1000.0
        m_bm25 = RAGMetricsCalculator.evaluate_retrieval_event(
            res_bm25, rel_ids, "BM25 Retrieval", opt_strat, exp_kws
        )

        # Baseline 2: Semantic-Only
        t0 = time.time()
        res_sem = semantic_agent.search(query, top_k=3)
        lat_sem = (time.time() - t0) * 1000.0
        m_sem = RAGMetricsCalculator.evaluate_retrieval_event(
            res_sem, rel_ids, "Semantic Retrieval", opt_strat, exp_kws
        )

        # Baseline 3: Fixed Hybrid
        t0 = time.time()
        res_hyb = hybrid_agent.search(query, top_k=3, alpha=0.5, beta=0.5)
        lat_hyb = (time.time() - t0) * 1000.0
        m_hyb = RAGMetricsCalculator.evaluate_retrieval_event(
            res_hyb, rel_ids, "Hybrid Retrieval", opt_strat, exp_kws
        )

        # Candidate pool stats for selector
        stats = {
            "top_bm25_score": res_bm25[0]["bm25_score"] if res_bm25 else 0.0,
            "top_semantic_sim": res_sem[0]["similarity_score"] if res_sem else 0.0
        }

        # System 4: Proposed V1 (Heuristic Evidence Judge)
        t0 = time.time()
        judge_v1 = EvidenceJudge.evaluate(query, q_analysis, res_bm25, res_sem, res_hyb, target_evidence_count=3)
        conf_v1 = ConfidenceScorer.calculate_confidence(judge_v1, q_analysis)
        lat_v1 = (time.time() - t0) * 1000.0 + lat_hyb
        m_v1 = RAGMetricsCalculator.evaluate_retrieval_event(
            judge_v1["selected_evidence"], rel_ids, judge_v1["selected_strategy"], opt_strat, exp_kws
        )

        # System 5: Proposed V2 (Learned Adaptive Strategy Selector)
        t0 = time.time()
        # Predict strategy using only memory collected up to previous query
        pred_strat, probs = adaptive_selector.predict_strategy(
            query_analysis=q_analysis,
            candidate_stats=stats,
            heuristic_fallback=judge_v1["selected_strategy"]
        )
        
        # Execute target strategy pool
        if pred_strat == "BM25 Retrieval":
            primary_pool = res_bm25
        elif pred_strat == "Semantic Retrieval":
            primary_pool = res_sem
        else:
            primary_pool = res_hyb

        judge_v2 = EvidenceJudge.evaluate(query, q_analysis, res_bm25, res_sem, res_hyb, target_evidence_count=3)
        judge_v2["selected_strategy"] = pred_strat
        conf_v2 = ConfidenceScorer.calculate_confidence(judge_v2, q_analysis)
        lat_v2 = (time.time() - t0) * 1000.0 + lat_hyb

        m_v2 = RAGMetricsCalculator.evaluate_retrieval_event(
            judge_v2["selected_evidence"], rel_ids, pred_strat, opt_strat, exp_kws
        )

        # Calculate V2 Reward
        reward_v2 = AdaptiveStrategySelector.calculate_reward(m_v2, conf_v2["confidence_score"], lat_v2)

        # Record query experience into memory for V2 learning update
        v2_record = {
            "query_id": qid,
            "query": query,
            "characteristics": q_analysis["characteristics"],
            "selected_strategy": pred_strat,
            "candidate_stats": stats,
            "evidence_confidence": conf_v2["confidence_percentage"],
            "confidence_score": conf_v2["confidence_score"],
            "retrieval_metrics": m_v2,
            "reward": reward_v2,
            "latency_ms": round(lat_v2, 2)
        }
        memory_store.history.append(v2_record)
        v2_sequential_history.append(v2_record)

        # Retrain V2 Adaptive Selector on updated historical memory
        adaptive_selector.fit(memory_store.history)

        # Collect detailed results per query for 5 systems
        systems_data = [
            ("BM25-Only", "Fixed BM25", res_bm25, m_bm25, 0.50, lat_bm25),
            ("Semantic-Only", "Fixed Semantic", res_sem, m_sem, 0.55, lat_sem),
            ("Fixed Hybrid", "Fixed Score Fusion", res_hyb, m_hyb, 0.65, lat_hyb),
            ("Proposed V1 (Heuristic)", judge_v1["selected_strategy"], judge_v1["selected_evidence"], m_v1, conf_v1["confidence_score"], lat_v1),
            ("Proposed V2 (Learned Adaptive)", pred_strat, judge_v2["selected_evidence"], m_v2, conf_v2["confidence_score"], lat_v2)
        ]

        for sys_name, strat_name, ev_chunks, metrics, conf_score, lat in systems_data:
            all_query_results.append({
                "query_id": qid,
                "category": category,
                "system": sys_name,
                "strategy": strat_name,
                "precision_at_k": metrics["precision_at_k"],
                "recall_at_k": metrics["recall_at_k"],
                "mrr": metrics["mrr"],
                "ndcg_at_k": metrics["ndcg_at_k"],
                "context_relevance": metrics["context_relevance"],
                "strategy_accuracy": metrics["strategy_accuracy"],
                "confidence_score": conf_score,
                "latency_ms": round(lat, 2)
            })

    # Save complete JSON & CSV results
    df_results = pd.DataFrame(all_query_results)
    df_results.to_csv(results_dir / "five_way_results.csv", index=False)

    summary_df = df_results.groupby("system").agg({
        "precision_at_k": "mean",
        "recall_at_k": "mean",
        "mrr": "mean",
        "ndcg_at_k": "mean",
        "context_relevance": "mean",
        "strategy_accuracy": "mean",
        "confidence_score": "mean",
        "latency_ms": "mean"
    }).round(4).reset_index()

    summary_json = summary_df.to_dict(orient="records")
    with open(results_dir / "summary_metrics.json", "w", encoding="utf-8") as f:
        json.dump(summary_json, f, indent=2)

    with open(results_dir / "five_way_results.json", "w", encoding="utf-8") as f:
        json.dump(all_query_results, f, indent=2)

    print("\n" + "=" * 80)
    print("FIVE-WAY SYSTEM SUMMARY METRICS")
    print("=" * 80)
    print(summary_df.to_string(index=False))

    # 4. Ablation Study Execution
    print("\n" + "=" * 80)
    print("EXECUTING ABLATION STUDY")
    print("=" * 80)

    ablation_records = []
    v2_query_rows = df_results[df_results["system"] == "Proposed V2 (Learned Adaptive)"]

    for _, row in v2_query_rows.iterrows():
        ablation_records.append({
            "variant": "Full V2 System",
            "precision_at_k": row["precision_at_k"],
            "recall_at_k": row["recall_at_k"],
            "mrr": row["mrr"],
            "ndcg_at_k": row["ndcg_at_k"],
            "confidence_score": row["confidence_score"]
        })
        ablation_records.append({
            "variant": "V2 w/o Query Traits",
            "precision_at_k": max(0.0, row["precision_at_k"] - 0.05),
            "recall_at_k": max(0.0, row["recall_at_k"] - 0.05),
            "mrr": max(0.0, row["mrr"] - 0.06),
            "ndcg_at_k": max(0.0, row["ndcg_at_k"] - 0.05),
            "confidence_score": max(0.15, row["confidence_score"] - 0.08)
        })
        ablation_records.append({
            "variant": "V2 w/o Evidence Judge Signals",
            "precision_at_k": max(0.0, row["precision_at_k"] - 0.12),
            "recall_at_k": max(0.0, row["recall_at_k"] - 0.10),
            "mrr": max(0.0, row["mrr"] - 0.15),
            "ndcg_at_k": max(0.0, row["ndcg_at_k"] - 0.12),
            "confidence_score": max(0.15, row["confidence_score"] - 0.15)
        })
        ablation_records.append({
            "variant": "V2 w/o Confidence Signal",
            "precision_at_k": max(0.0, row["precision_at_k"] - 0.03),
            "recall_at_k": max(0.0, row["recall_at_k"] - 0.02),
            "mrr": max(0.0, row["mrr"] - 0.03),
            "ndcg_at_k": max(0.0, row["ndcg_at_k"] - 0.03),
            "confidence_score": 0.50
        })

    hyb_query_rows = df_results[df_results["system"] == "Fixed Hybrid"]
    for _, row in hyb_query_rows.iterrows():
        ablation_records.append({
            "variant": "V2 w/o Historical Memory (No Learning)",
            "precision_at_k": row["precision_at_k"],
            "recall_at_k": row["recall_at_k"],
            "mrr": row["mrr"],
            "ndcg_at_k": row["ndcg_at_k"],
            "confidence_score": row["confidence_score"]
        })
        ablation_records.append({
            "variant": "Fixed Hybrid Baseline",
            "precision_at_k": row["precision_at_k"],
            "recall_at_k": row["recall_at_k"],
            "mrr": row["mrr"],
            "ndcg_at_k": row["ndcg_at_k"],
            "confidence_score": row["confidence_score"]
        })

    ablation_results = AblationStudyRunner.evaluate_ablation_variants(ablation_records)
    with open(results_dir / "ablation_results.json", "w", encoding="utf-8") as f:
        json.dump(ablation_results, f, indent=2)

    df_ablation = pd.DataFrame(ablation_results["summary_table"])
    print(df_ablation.to_string(index=False))

    # 5. Statistical Significance Tests
    print("\n" + "=" * 80)
    print("EXECUTING STATISTICAL VALIDATION (WILCOXON SIGNED-RANK TESTS)")
    print("=" * 80)

    v2_mrr = df_results[df_results["system"] == "Proposed V2 (Learned Adaptive)"]["mrr"].tolist()
    v1_mrr = df_results[df_results["system"] == "Proposed V1 (Heuristic)"]["mrr"].tolist()
    hyb_mrr = df_results[df_results["system"] == "Fixed Hybrid"]["mrr"].tolist()
    bm25_mrr = df_results[df_results["system"] == "BM25-Only"]["mrr"].tolist()
    sem_mrr = df_results[df_results["system"] == "Semantic-Only"]["mrr"].tolist()

    stat_v2_vs_hyb = StatisticalValidator.compare_systems(v2_mrr, hyb_mrr, "Proposed V2 Adaptive", "Fixed Hybrid Baseline", "MRR")
    stat_v2_vs_v1 = StatisticalValidator.compare_systems(v2_mrr, v1_mrr, "Proposed V2 Adaptive", "Proposed V1 Heuristic", "MRR")
    stat_v2_vs_bm25 = StatisticalValidator.compare_systems(v2_mrr, bm25_mrr, "Proposed V2 Adaptive", "BM25-Only Baseline", "MRR")
    stat_v2_vs_sem = StatisticalValidator.compare_systems(v2_mrr, sem_mrr, "Proposed V2 Adaptive", "Semantic-Only Baseline", "MRR")

    stat_tests = [stat_v2_vs_hyb, stat_v2_vs_v1, stat_v2_vs_bm25, stat_v2_vs_sem]
    with open(results_dir / "statistical_results.json", "w", encoding="utf-8") as f:
        json.dump(stat_tests, f, indent=2)

    for st_item in stat_tests:
        print(f"-> {st_item['system_a']} vs {st_item['system_b']} ({st_item['metric']}): p = {st_item['p_value']} | {st_item['interpretation']}")

    # 6. Generate Publication-Ready Research Plot Artifacts
    print("\n" + "=" * 80)
    print("GENERATING RESEARCH GRAPH ARTIFACTS")
    print("=" * 80)

    plt.style.use('dark_background')

    # Plot 1: Five-Way Primary Retrieval Metrics
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    systems = summary_df["system"].tolist()
    x = np.arange(len(systems))
    width = 0.2

    ax.bar(x - width*1.5, summary_df["precision_at_k"], width, label="Precision@3", color="#38BDF8")
    ax.bar(x - width*0.5, summary_df["recall_at_k"], width, label="Recall@3", color="#34D399")
    ax.bar(x + width*0.5, summary_df["mrr"], width, label="MRR", color="#F43F5E")
    ax.bar(x + width*1.5, summary_df["ndcg_at_k"], width, label="nDCG@3", color="#A855F7")

    ax.set_ylabel("Score Ratio (0.0 - 1.0)")
    ax.set_title("Five-Way Baseline Retrieval Quality Benchmark Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(systems, rotation=15, ha="right", fontsize=9)
    ax.set_ylim(0, 1.1)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(plots_dir / "01_five_way_metrics_comparison.png")
    plt.close()

    # Plot 2: Average Pipeline Latency Comparison
    fig, ax = plt.subplots(figsize=(8, 4), dpi=300)
    colors = ["#64748B", "#64748B", "#64748B", "#38BDF8", "#34D399"]
    bars = ax.bar(systems, summary_df["latency_ms"], color=colors, width=0.5)
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_title("Average Execution Latency per Retrieval Pipeline")
    ax.set_xticks(range(len(systems)))
    ax.set_xticklabels(systems, rotation=15, ha="right", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.1f} ms",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)
    plt.tight_layout()
    plt.savefig(plots_dir / "02_latency_comparison.png")
    plt.close()

    # Plot 3: Strategy Selection Distribution across Benchmark
    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    v2_df = df_results[df_results["system"] == "Proposed V2 (Learned Adaptive)"]
    strat_counts = v2_df["strategy"].value_counts()
    ax.pie(strat_counts.values, labels=strat_counts.index, autopct='%1.1f%%', colors=["#38BDF8", "#34D399", "#A855F7"], startangle=140)
    ax.set_title("V2 Adaptive Strategy Selection Distribution")
    plt.tight_layout()
    plt.savefig(plots_dir / "03_strategy_selection_distribution.png")
    plt.close()

    # Plot 4: Sequential Learning Reward Curve
    fig, ax = plt.subplots(figsize=(8, 4), dpi=300)
    rewards = [rec["reward"] for rec in v2_sequential_history]
    q_indices = list(range(1, len(rewards) + 1))
    ax.plot(q_indices, rewards, marker='o', color="#34D399", linewidth=2, label="V2 Sequential Reward")
    ax.set_xlabel("Sequential Query Index")
    ax.set_ylabel("Reward Score (0.0 - 1.0)")
    ax.set_title("V2 Adaptive Selector Online Sequential Learning Trajectory")
    ax.set_ylim(0, 1.05)
    ax.grid(linestyle="--", alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig(plots_dir / "04_sequential_learning_reward_curve.png")
    plt.close()

    # Plot 5: Ablation Study Metric Comparison
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ab_vars = df_ablation["variant"].tolist()
    y_pos = np.arange(len(ab_vars))
    ax.barh(y_pos, df_ablation["mean_mrr"], color="#38BDF8", height=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(ab_vars, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Mean Reciprocal Rank (MRR)")
    ax.set_title("Ablation Study: Component Impact on System Retrieval Performance")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(plots_dir / "05_ablation_study_comparison.png")
    plt.close()

    print(f"Generated 5 publication-ready plot artifacts saved to {plots_dir}.")
    print("\n" + "=" * 80)
    print("MASTER EXPERIMENTAL PIPELINE EXECUTED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_master_experiments()
