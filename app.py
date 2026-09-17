import os
import sys
import time
import json
import pandas as pd
from pathlib import Path
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
from src.judge.evidence_judge import EvidenceJudge
from src.confidence.confidence_scorer import ConfidenceScorer
from src.generation.answer_generator import GroundedAnswerGenerator
from src.evaluation.baseline_comparator import BaselineComparator
from src.memory.strategy_memory import RetrievalStrategyMemory
from src.memory.adaptive_selector import AdaptiveStrategySelector
from src.evaluation.benchmark_loader import BenchmarkLoader
from src.evaluation.metrics_calculator import RAGMetricsCalculator

# Set Streamlit Page Config
st.set_page_config(
    page_title="Adaptive Multi-Agent RAG | V2 Research System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Aesthetic CSS Styling
st.markdown("""
<style>
    /* Dark Research Theme Styling */
    .stApp {
        background-color: #0B0F17;
        color: #E2E8F0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Header Card */
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
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: #FFFFFF;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        float: right;
    }

    /* Metric & Status Cards */
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

    /* Retriever Cards */
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
    
    /* V2 Selector & Memory Cards */
    .v2-box {
        background: linear-gradient(135deg, #064E3B 0%, #0F172A 100%);
        border: 1px solid #10B981;
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    
    /* Confidence Meter */
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
    <span class="badge-v2">V2 Adaptive Research Edition</span>
    <h1 class="main-title">Adaptive Confidence-Aware Multi-Agent Retrieval System</h1>
    <p class="subtitle">Predictive Strategy Learning, Multi-Agent Evidence Judging, and Grounded QA</p>
</div>
""", unsafe_allow_html=True)


# --- SIDEBAR ---
with st.sidebar:
    st.header("📄 Knowledge Base Ingestion")
    
    if st.button("✨ Load Automatic Sample Knowledge Base", use_container_width=True, type="primary"):
        if not config.SAMPLE_PDF_PATH.exists():
            from sample_data.generate_sample import generate_sample_pdf, generate_sample_questions
            generate_sample_pdf(config.SAMPLE_PDF_PATH)
            generate_sample_questions(config.SAMPLE_QUESTIONS_PATH)
        
        process_and_index_file(config.SAMPLE_PDF_PATH)
        st.success(f"Indexed sample: '{config.SAMPLE_PDF_PATH.name}'")

    st.markdown("---")
    
    uploaded_file = st.file_uploader("Upload PDF or TXT document", type=["pdf", "txt"])
    if uploaded_file is not None:
        save_path = config.CACHE_DIR / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if not any(d["file_name"] == uploaded_file.name for d in st.session_state.documents):
            process_and_index_file(save_path)
            st.success(f"Successfully processed: {uploaded_file.name}")

    st.markdown("### 📊 System Status")
    if st.session_state.is_indexed:
        st.success("✅ Retrievers Ready & Indexed")
        st.metric("Total Documents", len(st.session_state.documents))
        st.metric("Total Chunks", len(st.session_state.chunks))
    else:
        st.warning("⚠️ No documents indexed yet.")

    st.markdown("---")
    st.markdown("### 🧠 V2 Meta-Learner Status")
    selector_trained = st.session_state.adaptive_selector.is_trained
    if selector_trained:
        st.success("🟢 ML Strategy Selector Active")
    else:
        st.info("🟡 Cold-Start / Heuristic Mode (Memory < 3 entries)")

    st.markdown("---")
    st.markdown("### ⚙️ Retriever Hyperparameters")
    hybrid_alpha = st.slider("BM25 Weight (α)", 0.0, 1.0, config.DEFAULT_HYBRID_ALPHA, 0.05)
    hybrid_beta = st.slider("Semantic Weight (β)", 0.0, 1.0, config.DEFAULT_HYBRID_BETA, 0.05)
    top_k_val = st.slider("Top Candidates per Retriever (k)", 2, 8, config.TOP_K_RETRIEVAL, 1)


# --- MAIN CONTENT AREA ---

recommended_questions = [
    "Select a sample test question...",
    "NovaSync v3.2 zero-trust encryption AES-256 throughput latency Proof-of-State",
    "What is the warranty period and energy efficiency of the NovaSolar-X solar panel?",
    "How does NovaTech ensure its green manufacturing processes protect the environment and reduce waste?",
    "What is the Q3 2025 revenue figure and the percentage of revenue allocated to R&D?",
    "Who are the CEO and CTO of NovaTech, and where is the enterprise headquartered?",
    "Compare the operational characteristics of the NovaSolar-X solar panel with the AeroGuide drone swarm system.",
    "How do NovaTech's sustainability goals align with its financial investments and upcoming 2026 European expansion milestones?",
    "What battery flight duration, top speed, and neural processor specs are defined for NovaTech's autonomous products?"
]

selected_sample_q = st.selectbox("💡 Quick Test Questions (Select to auto-fill):", recommended_questions)

user_query = st.text_input(
    "🔍 Enter Research Question:",
    value="" if selected_sample_q == "Select a sample test question..." else selected_sample_q,
    placeholder="e.g. What is the efficiency rating of the NovaSolar-X module?"
)

if user_query:
    if not st.session_state.is_indexed:
        st.error("Please load or upload a document first before querying.")
    else:
        start_total_time = time.time()

        # 1. QUERY TRAIT ANALYSIS
        query_analysis = QueryAnalyzer.analyze(user_query)

        # 2. MULTI-AGENT RETRIEVAL EXECUTION
        hybrid_agent = HybridRetriever(st.session_state.bm25_agent, st.session_state.semantic_agent)
        
        bm25_results = st.session_state.bm25_agent.search(user_query, top_k=top_k_val)
        semantic_results = st.session_state.semantic_agent.search(user_query, top_k=top_k_val)
        hybrid_results = hybrid_agent.search(user_query, top_k=top_k_val, alpha=hybrid_alpha, beta=hybrid_beta)

        candidate_stats = {
            "top_bm25_score": bm25_results[0]["bm25_score"] if bm25_results else 0.0,
            "top_semantic_sim": semantic_results[0]["similarity_score"] if semantic_results else 0.0
        }

        # 3. V1 HEURISTIC vs V2 LEARNED STRATEGY SELECTION
        judge_v1_output = EvidenceJudge.evaluate(
            query=user_query,
            query_analysis=query_analysis,
            bm25_results=bm25_results,
            semantic_results=semantic_results,
            hybrid_results=hybrid_results,
            target_evidence_count=3
        )

        pred_strategy, strat_probs = st.session_state.adaptive_selector.predict_strategy(
            query_analysis=query_analysis,
            candidate_stats=candidate_stats,
            heuristic_fallback=judge_v1_output["selected_strategy"]
        )

        # 4. FINAL EVIDENCE JUDGING & CONFIDENCE SCORING
        judge_output = dict(judge_v1_output)
        judge_output["selected_strategy"] = pred_strategy
        
        if pred_strategy == "BM25 Retrieval":
            primary_evidence = bm25_results
        elif pred_strategy == "Semantic Retrieval":
            primary_evidence = semantic_results
        else:
            primary_evidence = hybrid_results

        confidence_info = ConfidenceScorer.calculate_confidence(judge_output, query_analysis)

        # 5. ANSWER GENERATION
        final_answer = GroundedAnswerGenerator.generate_answer(
            query=user_query,
            selected_evidence=judge_output["selected_evidence"],
            confidence_info=confidence_info
        )

        total_latency_ms = (time.time() - start_total_time) * 1000.0

        # Compute empirical reward & update Strategy Memory
        dummy_metrics = {"mrr": 1.0, "recall_at_k": 1.0}
        reward_score = AdaptiveStrategySelector.calculate_reward(dummy_metrics, confidence_info["confidence_score"], total_latency_ms)

        st.session_state.strategy_memory.record_query_experience(
            query=user_query,
            query_analysis=query_analysis,
            selected_strategy=pred_strategy,
            confidence_info=confidence_info,
            latency_ms=total_latency_ms
        )

        # Retrain V2 Selector on updated memory
        st.session_state.adaptive_selector.fit(st.session_state.strategy_memory.history)

        # 6. BASELINE COMPARISON METRICS
        baseline_comp = BaselineComparator.compare_retrievers(
            query=user_query,
            bm25_results=bm25_results,
            semantic_results=semantic_results,
            hybrid_results=hybrid_results,
            proposed_judge_results=judge_output,
            total_pipeline_latency_ms=total_latency_ms
        )

        # --- DISPLAY RESULTS PIPELINE ---
        st.markdown("---")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"<div class='stat-card'><div class='stat-val'>{len(query_analysis['characteristics'])}</div><div class='stat-lbl'>Query Traits</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='stat-card'><div class='stat-val'>{pred_strategy}</div><div class='stat-lbl'>V2 Predicted Strategy</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='stat-card'><div class='stat-val'>{confidence_info['confidence_percentage']}</div><div class='stat-lbl'>Evidence Confidence</div></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div class='stat-card'><div class='stat-val'>{total_latency_ms:.1f} ms</div><div class='stat-lbl'>Pipeline Latency</div></div>", unsafe_allow_html=True)

        st.markdown("### 🔎 Query Analysis & Traits")
        st.info(f"**Detected Traits:** {', '.join([f'`{c}`' for c in query_analysis['characteristics']])}")

        # V2 Learned Strategy Selector Breakdown
        st.markdown(
            f"<div class='v2-box'>"
            f"<h4 style='color:#A7F3D0; margin:0 0 8px 0;'>🤖 V2 Learned Strategy Selector Breakdown</h4>"
            f"<p style='margin:0 0 10px 0; color:#CBD5E1; font-size:14px;'>"
            f"<strong>Predicted Strategy:</strong> <code>{pred_strategy}</code> "
            f"<small>(V1 Heuristic Choice: {judge_v1_output['selected_strategy']})</small><br/>"
            f"<strong>Model Status:</strong> {'RandomForest Classifier Trained' if st.session_state.adaptive_selector.is_trained else 'Cold-Start Heuristic Fallback'}"
            f"</p>"
            f"</div>",
            unsafe_allow_html=True
        )

        st.markdown("#### Strategy Probability Distribution")
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1:
            st.progress(strat_probs.get("BM25 Retrieval", 0.0), text=f"BM25 Retrieval ({strat_probs.get('BM25 Retrieval', 0.0)*100:.1f}%)")
        with p_col2:
            st.progress(strat_probs.get("Semantic Retrieval", 0.0), text=f"Semantic Retrieval ({strat_probs.get('Semantic Retrieval', 0.0)*100:.1f}%)")
        with p_col3:
            st.progress(strat_probs.get("Hybrid Retrieval", 0.0), text=f"Hybrid Retrieval ({strat_probs.get('Hybrid Retrieval', 0.0)*100:.1f}%)")

        # Multi-Agent Retrieval Agent Outputs
        st.markdown("### 🤖 Multi-Agent Retrieval Outputs")
        tab1, tab2, tab3 = st.tabs(["⚡ Agent 1: BM25 Keyword", "🧠 Agent 2: Semantic Vector", "🔀 Agent 3: Hybrid Fusion"])

        with tab1:
            if bm25_results:
                st.caption(f"Retrieval Latency: {bm25_results[0]['retrieval_time_ms']} ms")
                for item in bm25_results:
                    st.markdown(
                        f"<div class='retriever-card'>"
                        f"<strong>Chunk ID:</strong> <code>{item['chunk_id']}</code> (Page {item['page_number']}) "
                        f"<span class='score-tag'>BM25 Score: {item['bm25_score']:.3f}</span><br/>"
                        f"<p style='margin-top:6px; font-size:13px; color:#CBD5E1;'>{item['text']}</p>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

        with tab2:
            if semantic_results:
                st.caption(f"Retrieval Latency: {semantic_results[0]['retrieval_time_ms']} ms")
                for item in semantic_results:
                    st.markdown(
                        f"<div class='retriever-card'>"
                        f"<strong>Chunk ID:</strong> <code>{item['chunk_id']}</code> (Page {item['page_number']}) "
                        f"<span class='score-tag'>Cosine Similarity: {item['similarity_score']:.4f}</span><br/>"
                        f"<p style='margin-top:6px; font-size:13px; color:#CBD5E1;'>{item['text']}</p>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

        with tab3:
            if hybrid_results:
                st.caption(f"Retrieval Latency: {hybrid_results[0]['retrieval_time_ms']} ms")
                for item in hybrid_results:
                    st.markdown(
                        f"<div class='retriever-card'>"
                        f"<strong>Chunk ID:</strong> <code>{item['chunk_id']}</code> (Page {item['page_number']}) "
                        f"<span class='score-tag'>Combined Score: {item['combined_score']:.4f}</span> "
                        f"<small>(BM25 norm: {item['bm25_norm']} | Sem norm: {item['semantic_norm']})</small><br/>"
                        f"<p style='margin-top:6px; font-size:13px; color:#CBD5E1;'>{item['text']}</p>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

        # Evidence Judge & Filtering Breakdown
        st.markdown("### ⚖️ Evidence Judge Evaluation")
        j_col1, j_col2 = st.columns(2)
        with j_col1:
            st.markdown("#### ✅ Selected Evidence (Passed Judge)")
            for item in judge_output["selected_evidence"]:
                st.success(
                    f"**{item['chunk_id']}** (Page {item['page_number']}) | Evidence Score: `{item['judge_evidence_score']:.3f}`\n\n"
                    f"_{item['text']}_"
                )

        with j_col2:
            st.markdown("#### ❌ Filtered / Rejected Candidate Evidence")
            if judge_output["rejected_evidence"]:
                for item in judge_output["rejected_evidence"]:
                    st.error(
                        f"**{item['chunk_id']}** | Reason: `{item.get('rejection_reason', 'Lower rank')}`\n\n"
                        f"_{item['text'][:120]}..._"
                    )
            else:
                st.write("No candidate chunks were rejected.")

        # Evidence Confidence Score
        st.markdown("### 🎯 Evidence Confidence Score")
        conf_col1, conf_col2 = st.columns([1, 2])
        with conf_col1:
            st.markdown(
                f"<div class='confidence-meter'>"
                f"<div class='confidence-num'>{confidence_info['confidence_percentage']}</div>"
                f"<div style='color:#10B981; font-weight:600; font-size:14px;'>{confidence_info['confidence_level']} EVIDENCE CONFIDENCE</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with conf_col2:
            st.markdown("#### Signal Composition Breakdown")
            sigs = confidence_info.get("signals", {})
            st.progress(sigs.get("score_strength_factor", 0.0), text=f"Top Evidence Score Strength ({sigs.get('score_strength_factor', 0.0):.2f})")
            st.progress(sigs.get("consensus_factor", 0.0), text=f"Inter-Agent Consensus Ratio ({sigs.get('consensus_factor', 0.0):.2f})")
            st.progress(sigs.get("keyword_coverage_factor", 0.0), text=f"Query Keyword Coverage ({sigs.get('keyword_coverage_factor', 0.0):.2f})")

        # Final Grounded Answer
        st.markdown("### 📝 Final Grounded Answer")
        st.markdown(
            f"<div style='background:#1E293B; border:1px solid #10B981; border-radius:10px; padding:20px; color:#F8FAFC; font-size:15px; line-height:1.6;'>"
            f"{final_answer['answer']}"
            f"</div>",
            unsafe_allow_html=True
        )


# --- RESEARCH EXPERIMENTAL BENCHMARK DASHBOARD ---
st.markdown("---")
with st.expander("📊 RESEARCH DASHBOARD: Five-Way Baseline & Benchmark Results", expanded=False):
    st.markdown("### 🔬 Five-Way Baseline Quantitative Comparison")
    
    summary_path = config.BASE_DIR / "data" / "results" / "summary_metrics.json"
    if summary_path.exists():
        with open(summary_path, "r", encoding="utf-8") as f:
            sum_data = json.load(f)
        st.dataframe(pd.DataFrame(sum_data), use_container_width=True)
    else:
        st.info("Run `python scripts/run_full_experiments.py` to populate baseline benchmark results.")

    st.markdown("---")
    st.markdown("### 🧪 Ablation Study Summary")
    ablation_path = config.BASE_DIR / "data" / "results" / "ablation_results.json"
    if ablation_path.exists():
        with open(ablation_path, "r", encoding="utf-8") as f:
            ab_data = json.load(f)
        st.dataframe(pd.DataFrame(ab_data["summary_table"]), use_container_width=True)

    st.markdown("---")
    st.markdown("### 📈 Publication Research Plot Gallery")
    plots_dir = config.BASE_DIR / "data" / "results" / "plots"
    p1 = plots_dir / "01_five_way_metrics_comparison.png"
    p2 = plots_dir / "02_latency_comparison.png"
    p3 = plots_dir / "03_strategy_selection_distribution.png"
    p4 = plots_dir / "04_sequential_learning_reward_curve.png"

    g_col1, g_col2 = st.columns(2)
    with g_col1:
        if p1.exists():
            st.image(str(p1), caption="Figure 1: Five-Way Retrieval Quality Comparison", use_container_width=True)
        if p3.exists():
            st.image(str(p3), caption="Figure 3: V2 Strategy Selection Distribution", use_container_width=True)
    with g_col2:
        if p2.exists():
            st.image(str(p2), caption="Figure 2: Execution Latency Comparison", use_container_width=True)
        if p4.exists():
            st.image(str(p4), caption="Figure 4: V2 Sequential Learning Reward Trajectory", use_container_width=True)
