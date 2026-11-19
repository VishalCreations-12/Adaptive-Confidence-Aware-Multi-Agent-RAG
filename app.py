import os
import sys
import time
import json
from pathlib import Path
import pandas as pd
import streamlit as st

# Add current directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config
from src.ingestion.parser import DocumentParser
from src.ingestion.chunker import DocumentChunker
from src.query_analysis.analyzer import QueryAnalyzer
from src.retrieval.bm25_agent import BM25Retriever
from src.retrieval.semantic_agent import SemanticRetriever
from src.retrieval.hybrid_agent import HybridRetriever
from src.retrieval.rrf_agent import RRFRetriever
from src.retrieval.tuned_hybrid_agent import TunedHybridRetriever
from src.judge.evidence_judge import EvidenceJudge
from src.confidence.confidence_scorer import ConfidenceScorer
from src.generation.answer_generator import GroundedAnswerGenerator
from src.memory.strategy_memory import RetrievalStrategyMemory
from src.memory.adaptive_selector import AdaptiveStrategySelector

# Page Configuration
st.set_page_config(
    page_title="Adaptive Confidence-Aware Retrieval System | Research Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Aesthetic Academic CSS Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0B0F17;
        color: #E2E8F0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    .main-title {
        color: #F8FAFC;
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0 0 6px 0;
    }
    .subtitle {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 400;
        margin: 0;
    }
    .badge-v2 {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
        color: #FFFFFF;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        float: right;
    }
    .stat-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .stat-val {
        font-size: 22px;
        font-weight: 700;
        color: #38BDF8;
    }
    .stat-lbl {
        font-size: 11px;
        color: #94A3B8;
        text-transform: uppercase;
        margin-top: 4px;
    }
    .retriever-card {
        background: #182232;
        border: 1px solid #28374D;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 10px;
    }
    .score-tag {
        background: #0F172A;
        border: 1px solid #3B82F6;
        color: #60A5FA;
        font-weight: 600;
        font-size: 12px;
        padding: 2px 8px;
        border-radius: 4px;
    }
    .v2-box {
        background: linear-gradient(135deg, #064E3B 0%, #0F172A 100%);
        border: 1px solid #10B981;
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    .confidence-meter {
        background: #0F172A;
        border: 1px solid #10B981;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
    }
    .confidence-num {
        font-size: 36px;
        font-weight: 800;
        color: #34D399;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "documents" not in st.session_state:
    st.session_state.documents = []
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "bm25_agent" not in st.session_state:
    st.session_state.bm25_agent = BM25Retriever()
if "semantic_agent" not in st.session_state:
    st.session_state.semantic_agent = SemanticRetriever()
if "strategy_memory" not in st.session_state:
    st.session_state.strategy_memory = RetrievalStrategyMemory()
if "adaptive_selector" not in st.session_state:
    # Load trained model if available from revision
    rev_model = BASE_DIR / "results" / "reviewer_revision" / "routing" / "v2_adaptive_model.pkl"
    if rev_model.exists():
        st.session_state.adaptive_selector = AdaptiveStrategySelector(rev_model)
    else:
        st.session_state.adaptive_selector = AdaptiveStrategySelector()
if "is_indexed" not in st.session_state:
    st.session_state.is_indexed = False

def process_and_index_file(file_path: Path):
    doc_data = DocumentParser.parse_document(file_path)
    chunker = DocumentChunker()
    doc_chunks = chunker.chunk_document(doc_data)

    st.session_state.documents.append(doc_data)
    st.session_state.chunks.extend(doc_chunks)

    with st.spinner("Building BM25 and Vector FAISS indexes..."):
        st.session_state.bm25_agent.fit(st.session_state.chunks)
        st.session_state.semantic_agent.fit(st.session_state.chunks)
        st.session_state.is_indexed = True

# --- HEADER ---
st.markdown("""
<div class="main-header">
    <span class="badge-v2">Peer-Reviewed Revision v2.0</span>
    <h1 class="main-title">Adaptive Confidence-Aware Retrieval System</h1>
    <p class="subtitle">Query-Conditioned Retriever Routing, Multi-Signal Evidence Judging, and Grounded Generation</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("📄 Knowledge Base Ingestion")
    
    if st.button("✨ Load Comprehensive Research Knowledge Base", use_container_width=True, type="primary"):
        pdf_path = config.SAMPLE_DATA_DIR / "NovaTech_Research_Knowledge_Base.pdf"
        if not pdf_path.exists():
            from sample_data.generate_sample import generate_sample_pdf, generate_sample_questions
            generate_sample_pdf(pdf_path)
            generate_sample_questions(config.SAMPLE_DATA_DIR / "test_questions.txt")
        
        process_and_index_file(pdf_path)
        st.success(f"Indexed: '{pdf_path.name}' ({len(st.session_state.chunks)} chunks)")

    st.markdown("---")
    uploaded_file = st.file_uploader("Upload PDF or TXT Document", type=["pdf", "txt"])
    if uploaded_file is not None:
        save_path = config.CACHE_DIR / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if not any(d["file_name"] == uploaded_file.name for d in st.session_state.documents):
            process_and_index_file(save_path)
            st.success(f"Processed & Indexed: {uploaded_file.name}")

    st.markdown("### 📊 System Status")
    if st.session_state.is_indexed:
        st.success("✅ Retrievers Ready & Indexed")
        st.metric("Total Documents", len(st.session_state.documents))
        st.metric("Total Chunks", len(st.session_state.chunks))
    else:
        st.warning("⚠️ No documents indexed yet. Click button above.")

    st.markdown("---")
    st.markdown("### 🧠 Adaptive Routing Status")
    selector_trained = st.session_state.adaptive_selector.is_trained
    if selector_trained:
        st.success("🟢 ML Strategy Selector Active")
    else:
        st.info("🟡 Cold-Start / Heuristic Mode")

    st.markdown("---")
    st.markdown("### ⚙️ Retriever Hyperparameters")
    hybrid_alpha = st.slider("BM25 Weight (α)", 0.0, 1.0, 0.50, 0.05)
    hybrid_beta = st.slider("Semantic Weight (β)", 0.0, 1.0, 0.50, 0.05)
    top_k_val = st.slider("Candidate Cutoff (k)", 2, 8, config.TOP_K_RETRIEVAL, 1)

# --- NAVIGATION TABS ---
nav_tabs = st.tabs([
    "🔍 Live Retrieval & QA Demo",
    "📊 Benchmark Comparison (8 Systems)",
    "🔀 Adaptive Routing & Oracle",
    "🧪 Empirical Ablation Study",
    "📈 Memory Learning Curve",
    "📖 Methodology & Metrics",
    "🔁 Reproducibility & Audit"
])

# ==============================================================================
# TAB 1: LIVE RETRIEVAL & QA DEMO
# ==============================================================================
with nav_tabs[0]:
    recommended_questions = [
        "Select a sample test question...",
        "NovaSync v3.2 AES-256-GCM Curve25519 Ed25519 zero-trust",
        "What is the peak energy conversion efficiency percentage of the NovaSolar-X Model NS-520-QX panel?",
        "How does the monolithic silicon-perovskite tandem design reduce thermalization energy losses?",
        "What were the Q3 2025 quarterly revenue and year-over-year revenue growth percentage?",
        "Who are the Chief Executive Officer and Chief Technology Officer of NovaTech Applied Intelligence Labs?",
        "Compare the operational characteristics and hardware of NovaSolar-X solar panels with the AeroGuide drone swarm.",
        "What battery chemistry, maximum flight speed, sensor payloads, and neural processors power Project AeroGuide?",
        "Describe how decentralized peer-to-peer drone swarms coordinate autonomous search and rescue missions without cloud servers."
    ]

    selected_sample_q = st.selectbox("💡 Quick Test Queries (Auto-fill):", recommended_questions)
    user_query = st.text_input(
        "Enter Research Query:",
        value="" if selected_sample_q == "Select a sample test question..." else selected_sample_q,
        placeholder="e.g. What is the peak energy conversion efficiency percentage of the NovaSolar-X module?"
    )

    if user_query:
        if not st.session_state.is_indexed:
            st.error("Please click 'Load Comprehensive Research Knowledge Base' in the sidebar first.")
        else:
            start_total_time = time.time()

            # 1. Trait Analysis
            query_analysis = QueryAnalyzer.analyze(user_query)

            # 2. Candidate Retrieval
            bm25_res = st.session_state.bm25_agent.search(user_query, top_k=top_k_val)
            sem_res = st.session_state.semantic_agent.search(user_query, top_k=top_k_val)
            fhyb = HybridRetriever(st.session_state.bm25_agent, st.session_state.semantic_agent)
            hyb_res = fhyb.search(user_query, top_k=top_k_val, alpha=hybrid_alpha, beta=hybrid_beta)
            rrf = RRFRetriever(st.session_state.bm25_agent, st.session_state.semantic_agent, rrf_k=60)
            rrf_res = rrf.search(user_query, top_k=top_k_val)

            candidate_stats = {
                "top_bm25_score": bm25_res[0]["bm25_score"] if bm25_res else 0.0,
                "top_semantic_sim": sem_res[0]["similarity_score"] if sem_res else 0.0
            }

            # 3. Strategy Selection
            judge_v1_output = EvidenceJudge.evaluate(
                query=user_query,
                query_analysis=query_analysis,
                bm25_results=bm25_res,
                semantic_results=sem_res,
                hybrid_results=hyb_res,
                target_evidence_count=3
            )

            pred_strategy, strat_probs = st.session_state.adaptive_selector.predict_strategy(
                query_analysis=query_analysis,
                candidate_stats=candidate_stats,
                heuristic_fallback=judge_v1_output["selected_strategy"]
            )

            # 4. Target Execution & Evidence Judging
            if pred_strategy == "BM25 Retrieval":
                target_pool = bm25_res
            elif pred_strategy == "Semantic Retrieval":
                target_pool = sem_res
            elif pred_strategy == "RRF Retrieval":
                target_pool = rrf_res
            else:
                target_pool = hyb_res

            judge_output = EvidenceJudge.evaluate(
                query=user_query,
                query_analysis=query_analysis,
                bm25_results=bm25_res,
                semantic_results=sem_res,
                hybrid_results=hyb_res,
                target_evidence_count=3
            )
            judge_output["selected_strategy"] = pred_strategy

            confidence_info = ConfidenceScorer.calculate_confidence(judge_output, query_analysis)

            # 5. Answer Generation
            final_answer = GroundedAnswerGenerator.generate_answer(
                query=user_query,
                selected_evidence=judge_output["selected_evidence"],
                confidence_info=confidence_info
            )

            total_latency_ms = (time.time() - start_total_time) * 1000.0

            # Display Stats
            st.markdown("---")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"<div class='stat-card'><div class='stat-val'>{len(query_analysis['characteristics'])}</div><div class='stat-lbl'>Detected Traits</div></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='stat-card'><div class='stat-val'>{pred_strategy}</div><div class='stat-lbl'>Selected Strategy</div></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='stat-card'><div class='stat-val'>{confidence_info['confidence_percentage']}</div><div class='stat-lbl'>Evidence Confidence</div></div>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<div class='stat-card'><div class='stat-val'>{total_latency_ms:.1f} ms</div><div class='stat-lbl'>Pipeline Latency</div></div>", unsafe_allow_html=True)

            st.markdown("### 🔎 Query Trait Analysis")
            st.info(f"**Identified Characteristics:** {', '.join([f'`{c}`' for c in query_analysis['characteristics']])}")

            # Routing Probability
            st.markdown("### 🔀 Strategy Routing Probabilities")
            p_cols = st.columns(4)
            for idx, strat in enumerate(["BM25 Retrieval", "Semantic Retrieval", "Hybrid Retrieval", "RRF Retrieval"]):
                with p_cols[idx]:
                    st.progress(strat_probs.get(strat, 0.0), text=f"{strat} ({strat_probs.get(strat, 0.0)*100:.1f}%)")

            # Evidence Judge Display
            st.markdown("### ⚖️ Evidence Judge Evaluation & Filtering")
            j1, j2 = st.columns(2)
            with j1:
                st.markdown("#### ✅ Selected Chunks (Passed Verification)")
                for item in judge_output["selected_evidence"]:
                    st.success(f"**Chunk ID:** `{item['chunk_id']}` | Score: `{item['judge_evidence_score']:.3f}`\n\n{item['text']}")
            with j2:
                st.markdown("#### ❌ Filtered Candidate Chunks")
                if judge_output["rejected_evidence"]:
                    for item in judge_output["rejected_evidence"]:
                        st.warning(f"**Chunk ID:** `{item['chunk_id']}` | Reason: `{item.get('rejection_reason', 'Lower rank')}`\n\n{item['text'][:120]}...")
                else:
                    st.write("No candidate chunks rejected.")

            # Grounded Answer
            st.markdown("### 📝 Grounded Answer Output")
            st.markdown(f"<div style='background:#1E293B; border:1px solid #10B981; border-radius:10px; padding:20px;'>{final_answer['answer']}</div>", unsafe_allow_html=True)

# ==============================================================================
# TAB 2: BENCHMARK COMPARISON (8 SYSTEMS)
# ==============================================================================
with nav_tabs[1]:
    st.header("📊 Benchmark Comparison Across 8 Retrieval Systems")
    st.markdown("Quantitative evaluation measured on the **Held-Out Test Split (N = 40)** and the **Full 200-Query Benchmark**.")

    test_sum_file = BASE_DIR / "results" / "reviewer_revision" / "aggregated" / "held_out_test_summary_metrics.json"
    all_sum_file = BASE_DIR / "results" / "reviewer_revision" / "aggregated" / "full_benchmark_summary_metrics.json"

    if test_sum_file.exists():
        with open(test_sum_file, "r", encoding="utf-8") as f:
            t_data = json.load(f)
        st.subheader("1. Primary Held-Out Test Split Results (Strict Generalization)")
        st.dataframe(pd.DataFrame(t_data), use_container_width=True)

    if all_sum_file.exists():
        with open(all_sum_file, "r", encoding="utf-8") as f:
            a_data = json.load(f)
        st.subheader("2. Full Benchmark Aggregate Results (N = 200 Queries)")
        st.dataframe(pd.DataFrame(a_data), use_container_width=True)

    st.markdown("---")
    st.subheader("📈 Publication Research Figures")
    fig1 = BASE_DIR / "results" / "reviewer_revision" / "figures" / "01_eight_way_metrics_comparison.png"
    fig2 = BASE_DIR / "results" / "reviewer_revision" / "figures" / "02_latency_comparison.png"
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        if fig1.exists():
            st.image(str(fig1), caption="Figure 1: Eight-Way Retrieval Performance Comparison", use_container_width=True)
    with c_f2:
        if fig2.exists():
            st.image(str(fig2), caption="Figure 2: Pipeline Latency Comparison", use_container_width=True)

# ==============================================================================
# TAB 3: ADAPTIVE ROUTING & ORACLE HEADROOM
# ==============================================================================
with nav_tabs[2]:
    st.header("🔀 Adaptive Strategy Routing & Oracle Analysis")
    st.markdown("Evaluates whether query-conditioned routing learns genuine routing policies and measures theoretical headroom.")

    routing_file = BASE_DIR / "results" / "reviewer_revision" / "routing" / "routing_accuracy_report.json"
    if routing_file.exists():
        with open(routing_file, "r", encoding="utf-8") as f:
            r_rep = json.load(f)
        
        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            st.metric("Training Routing Accuracy", f"{r_rep['train_routing_accuracy']*100:.1f}%", f"{r_rep['train_queries']} queries")
        with rc2:
            st.metric("Validation Routing Accuracy", f"{r_rep['val_routing_accuracy']*100:.1f}%", f"{r_rep['val_queries']} queries")
        with rc3:
            st.metric("Held-Out Test Accuracy", f"{r_rep['test_routing_accuracy']*100:.1f}%", f"{r_rep['test_queries']} queries")

    st.markdown("---")
    fig3 = BASE_DIR / "results" / "reviewer_revision" / "figures" / "03_strategy_selection_distribution.png"
    fig6 = BASE_DIR / "results" / "reviewer_revision" / "figures" / "06_performance_by_query_type.png"
    cf3, cf4 = st.columns(2)
    with cf3:
        if fig3.exists():
            st.image(str(fig3), caption="Figure 3: Predicted vs Oracle Strategy Distribution", use_container_width=True)
    with cf4:
        if fig6.exists():
            st.image(str(fig6), caption="Figure 4: Performance Stratified by Query Category", use_container_width=True)

# ==============================================================================
# TAB 4: EMPIRICAL ABLATION STUDY
# ==============================================================================
with nav_tabs[3]:
    st.header("🧪 Real Modular Ablation Study (Zero Synthetic Subtraction)")
    st.markdown("Independent execution of variants A0 through A5 on the held-out test split.")

    ab_file = BASE_DIR / "results" / "reviewer_revision" / "ablation" / "real_ablation_summary.json"
    if ab_file.exists():
        with open(ab_file, "r", encoding="utf-8") as f:
            ab_data = json.load(f)
        st.dataframe(pd.DataFrame(ab_data["summary_table"]), use_container_width=True)

    fig5 = BASE_DIR / "results" / "reviewer_revision" / "figures" / "05_ablation_study_comparison.png"
    if fig5.exists():
        st.image(str(fig5), caption="Figure 5: Empirical Component Contribution on nDCG@3", use_container_width=True)

# ==============================================================================
# TAB 5: MEMORY LEARNING CURVE
# ==============================================================================
with nav_tabs[4]:
    st.header("📈 Historical Strategy Memory Dynamics")
    st.markdown("Investigation of Reviewer 2 concern regarding whether historical memory helps or hurts performance.")

    mem_file = BASE_DIR / "results" / "reviewer_revision" / "memory" / "memory_sweep_results.json"
    if mem_file.exists():
        with open(mem_file, "r", encoding="utf-8") as f:
            m_data = json.load(f)
        st.dataframe(pd.DataFrame(m_data), use_container_width=True)

    fig4 = BASE_DIR / "results" / "reviewer_revision" / "figures" / "04_memory_sweep_learning_curve.png"
    if fig4.exists():
        st.image(str(fig4), caption="Figure 6: Memory History Learning Curve on Routing Accuracy & nDCG@3", use_container_width=True)

# ==============================================================================
# TAB 6: METHODOLOGY & METRICS
# ==============================================================================
with nav_tabs[5]:
    st.header("📖 Methodology, Mathematical Formulas, and Feature Specifications")
    
    st.markdown("""
    ### 1. 12-Dimensional Random Forest Selector Features
    The adaptive selector extracts a standardized 12-dimensional vector combining **8 structural query traits** with **4 preliminary candidate statistics**:
    - **$x_1$:** `word_count` (total whitespace tokens)
    - **$x_2$:** `is_keyword` (presence of exact technical acronyms, codes, version numbers)
    - **$x_3$:** `is_semantic` (interrogative conceptual terms: how, why, explain, describe)
    - **$x_4$:** `is_numerical` (presence of digits, %, $, physical units)
    - **$x_5$:** `is_comparison` (comparative indicators: compare, versus, differ)
    - **$x_6$:** `is_multi_part` (multi-hop / conjunction indicators)
    - **$x_7$:** `is_factual` (direct fact interrogatives: what, who, where, when)
    - **$x_8$:** `is_entity` (capitalized named entities or executive roles)
    - **$x_9$:** `top_bm25` (highest Okapi BM25 candidate score)
    - **$x_{10}$:** `top_sem` (highest FAISS cosine similarity score)
    - **$x_{11}$:** `score_diff` ($|x_9 / 10.0 - x_{10}|$)
    - **$x_{12}$:** `bm25_sem_ratio` ($x_9 / (10 \cdot x_{10} + 10^{-5})$)

    ### 2. Smooth Monotonic Reward Function
    $$\\text{Reward} = 0.40 \\cdot \\text{nDCG@}3 + 0.35 \\cdot \\text{Recall@}3 + 0.15 \\cdot \\text{Confidence} + 0.10 \\cdot R_{\\text{lat}}(\\text{lat})$$
    where $R_{\\text{lat}}(\\text{lat}) = \\frac{1}{1 + \\text{latency\\_ms} / 250.0} \\in (0, 1]$.

    ### 3. Non-Parametric Statistical Testing
    Paired two-sided **Wilcoxon signed-rank tests** with Pratt zero-handling and **10,000-resample bootstrap 95% confidence intervals** over per-query metric differences.
    """)

# ==============================================================================
# TAB 7: REPRODUCIBILITY & AUDIT
# ==============================================================================
with nav_tabs[6]:
    st.header("🔁 Reproducibility Protocol & Artifact Verification")
    st.markdown("""
    All experiments are 100% deterministic, local (zero external API calls), and reproducible via:
    ```bash
    # Run full reviewer revision experiment suite
    python scripts/run_reviewer_revision.py

    # Run automated test suite
    pytest -v
    ```
    ### Generated Artifacts Checklist:
    - `results/reviewer_revision/raw/master_per_query_results.csv`
    - `results/reviewer_revision/aggregated/held_out_test_summary_metrics.json`
    - `results/reviewer_revision/ablation/real_ablation_summary.json`
    - `results/reviewer_revision/routing/routing_accuracy_report.json`
    - `results/reviewer_revision/statistics/statistical_test_results.json`
    - `results/reviewer_revision/RESEARCH_FINDINGS.md`
    - `results/reviewer_revision/PAPER_RESULTS_SUMMARY.md`
    """)
