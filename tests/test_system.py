import os
import sys
from pathlib import Path
import pytest

# Ensure workspace root is in python path
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

@pytest.fixture(scope="module")
def sample_files():
    """Ensure sample PDF and TXT exist for testing."""
    pdf_path = config.SAMPLE_DATA_DIR / "NovaTech_Research_Knowledge_Base.pdf"
    txt_path = config.SAMPLE_DATA_DIR / "test_questions.txt"
    generate_sample_pdf(pdf_path)
    generate_sample_questions(txt_path)
    return pdf_path, txt_path

def test_sample_generation(sample_files):
    pdf_path, txt_path = sample_files
    assert pdf_path.exists()
    assert txt_path.exists()
    assert pdf_path.stat().st_size > 0

def test_document_parser_and_chunker(sample_files):
    pdf_path, _ = sample_files
    doc_data = DocumentParser.parse_document(pdf_path)
    assert doc_data["file_type"] == "pdf"
    assert doc_data["num_pages"] > 0
    assert len(doc_data["full_text"]) > 100

    chunker = DocumentChunker(chunk_size=400, chunk_overlap=80)
    chunks = chunker.chunk_document(doc_data)
    assert len(chunks) > 0
    assert "chunk_id" in chunks[0]
    assert "text" in chunks[0]

def test_query_analyzer():
    res_kw = QueryAnalyzer.analyze("NovaSync v3.2 zero-trust encryption AES-256")
    assert res_kw["is_keyword_heavy"] is True

    res_sem = QueryAnalyzer.analyze("How does NovaTech ensure its green manufacturing processes protect the environment?")
    assert res_sem["is_semantic"] is True

    res_num = QueryAnalyzer.analyze("What is the Q3 2025 revenue figure and 34% R&D budget?")
    assert res_num["is_numerical"] is True

def test_retrievers_and_judge(sample_files):
    pdf_path, _ = sample_files
    doc_data = DocumentParser.parse_document(pdf_path)
    chunks = DocumentChunker().chunk_document(doc_data)

    bm25 = BM25Retriever()
    bm25.fit(chunks)
    bm25_res = bm25.search("NovaSolar-X panel efficiency", top_k=3)
    assert len(bm25_res) > 0
    assert "bm25_score" in bm25_res[0]

    semantic = SemanticRetriever()
    semantic.fit(chunks)
    sem_res = semantic.search("NovaSolar-X panel efficiency", top_k=3)
    assert len(sem_res) > 0
    assert "similarity_score" in sem_res[0]

    hybrid = HybridRetriever(bm25, semantic)
    hyb_res = hybrid.search("NovaSolar-X panel efficiency", top_k=3)
    assert len(hyb_res) > 0
    assert "combined_score" in hyb_res[0]

    # Test Judge
    q_analysis = QueryAnalyzer.analyze("NovaSolar-X panel efficiency")
    judge_output = EvidenceJudge.evaluate(
        query="NovaSolar-X panel efficiency",
        query_analysis=q_analysis,
        bm25_results=bm25_res,
        semantic_results=sem_res,
        hybrid_results=hyb_res,
        target_evidence_count=3
    )

    assert "selected_strategy" in judge_output
    assert len(judge_output["selected_evidence"]) > 0

    # Test Confidence
    conf = ConfidenceScorer.calculate_confidence(judge_output, q_analysis)
    assert 0.0 <= conf["confidence_score"] <= 1.0
    assert "%" in conf["confidence_percentage"]

    # Test Grounded Answer
    ans = GroundedAnswerGenerator.generate_answer(
        query="NovaSolar-X panel efficiency",
        selected_evidence=judge_output["selected_evidence"],
        confidence_info=conf
    )
    assert "answer" in ans
    assert len(ans["citations"]) > 0

def test_strategy_memory(tmp_path):
    mem_file = tmp_path / "test_memory.json"
    mem = RetrievalStrategyMemory(mem_file)
    q_analysis = QueryAnalyzer.analyze("What is AeroGuide drone speed?")
    conf = {"confidence_percentage": "88%", "confidence_score": 0.88}
    
    mem.record_query_experience(
        query="What is AeroGuide drone speed?",
        query_analysis=q_analysis,
        selected_strategy="Hybrid Retrieval",
        confidence_info=conf,
        latency_ms=12.5
    )

    stats = mem.get_memory_stats()
    assert stats["total_logged_queries"] == 1
    assert stats["strategy_distribution"].get("Hybrid Retrieval") == 1
