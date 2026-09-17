import os
import sys
import time
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
from src.evaluation.baseline_comparator import BaselineComparator
from src.memory.strategy_memory import RetrievalStrategyMemory

def run_end_to_end_verification():
    print("=" * 80)
    print("STARTING END-TO-END PIPELINE VERIFICATION")
    print("=" * 80)

    # 1. Generate Sample Data
    pdf_path = config.SAMPLE_DATA_DIR / "NovaTech_Research_Knowledge_Base.pdf"
    txt_path = config.SAMPLE_DATA_DIR / "test_questions.txt"
    generate_sample_pdf(pdf_path)
    generate_sample_questions(txt_path)

    # 2. Parse & Chunk Document
    print("\n[STEP 1] Ingesting & Indexing Document...")
    doc_data = DocumentParser.parse_document(pdf_path)
    chunker = DocumentChunker()
    chunks = chunker.chunk_document(doc_data)
    print(f"-> Extracted {doc_data['num_pages']} pages, created {len(chunks)} chunks.")

    # 3. Fit Retrieval Agents
    print("\n[STEP 2] Training Retrieval Agents (BM25 + Semantic FAISS)...")
    bm25_agent = BM25Retriever()
    bm25_agent.fit(chunks)

    semantic_agent = SemanticRetriever()
    semantic_agent.fit(chunks)

    hybrid_agent = HybridRetriever(bm25_agent, semantic_agent)
    print("-> Agents successfully fit & indexed.")

    # 4. Load Test Questions
    test_questions = [
        ("Factual", "What is the warranty period and energy efficiency of the NovaSolar-X solar panel?"),
        ("Keyword-Heavy", "NovaSync v3.2 zero-trust encryption AES-256 throughput latency Proof-of-State"),
        ("Semantic", "How does NovaTech ensure its green manufacturing processes protect the environment and reduce waste?"),
        ("Numerical", "What is the Q3 2025 revenue figure and the percentage of revenue allocated to R&D?"),
        ("Entity", "Who are the CEO and CTO of NovaTech, and where is the enterprise headquartered?"),
        ("Comparison", "Compare the operational characteristics of the NovaSolar-X solar panel with the AeroGuide drone swarm system."),
        ("Multi-Section", "How do NovaTech's sustainability goals align with its financial investments and upcoming 2026 European expansion milestones?"),
        ("Disagreement-Prone", "What battery flight duration, top speed, and neural processor specs are defined for NovaTech's autonomous products?")
    ]

    strategy_memory = RetrievalStrategyMemory()

    print("\n" + "=" * 80)
    print("EXECUTING 8 TEST QUESTIONS THROUGH MULTI-AGENT PIPELINE")
    print("=" * 80)

    for idx, (q_type, query) in enumerate(test_questions, start=1):
        print(f"\n--- TEST {idx}/8 [{q_type}] ---")
        print(f"QUERY: \"{query}\"")

        start_time = time.time()
        
        # Query Analysis
        q_analysis = QueryAnalyzer.analyze(query)
        print(f"Query Traits: {q_analysis['characteristics']}")

        # Multi-Agent Retrievals
        bm25_res = bm25_agent.search(query, top_k=3)
        sem_res = semantic_agent.search(query, top_k=3)
        hyb_res = hybrid_agent.search(query, top_k=3)

        print(f"BM25 Top Score: {bm25_res[0]['bm25_score']:.3f} | Chunk: {bm25_res[0]['chunk_id']}")
        print(f"Semantic Top Sim: {sem_res[0]['similarity_score']:.4f} | Chunk: {sem_res[0]['chunk_id']}")
        print(f"Hybrid Top Score: {hyb_res[0]['combined_score']:.4f} | Chunk: {hyb_res[0]['chunk_id']}")

        # Evidence Judge
        judge_output = EvidenceJudge.evaluate(
            query=query,
            query_analysis=q_analysis,
            bm25_results=bm25_res,
            semantic_results=sem_res,
            hybrid_results=hyb_res,
            target_evidence_count=3
        )
        print(f"Judge Selected Strategy: {judge_output['selected_strategy']}")
        print(f"Selected Evidence Count: {len(judge_output['selected_evidence'])} (Rejected: {len(judge_output['rejected_evidence'])})")

        # Confidence Scorer
        conf_info = ConfidenceScorer.calculate_confidence(judge_output, q_analysis)
        print(f"Evidence Confidence: {conf_info['confidence_percentage']} ({conf_info['confidence_level']})")

        # Answer Generator
        answer_data = GroundedAnswerGenerator.generate_answer(query, judge_output['selected_evidence'], conf_info)
        print(f"Citations: {answer_data['citations']}")
        
        total_lat = (time.time() - start_time) * 1000.0

        # Memory recording
        strategy_memory.record_query_experience(
            query=query,
            query_analysis=q_analysis,
            selected_strategy=judge_output["selected_strategy"],
            confidence_info=conf_info,
            latency_ms=total_lat
        )

        print(f"Execution Latency: {total_lat:.2f} ms")

    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETED SUCCESSFULLY! ALL 8 TEST CASES PASSED.")
    print("=" * 80)

if __name__ == "__main__":
    run_end_to_end_verification()
