from typing import List, Dict, Any
import re
from src.query_analysis.analyzer import QueryAnalyzer

class EvidenceJudge:
    """Intelligent Evidence Judge evaluating multi-agent candidate pools."""

    @staticmethod
    def _compute_keyword_coverage(query: str, text: str) -> float:
        """Compute the fraction of query terms present in text."""
        query_words = set(re.findall(r'\w+', query.lower()))
        # Filter out common stop words
        stopwords = {'what', 'is', 'the', 'of', 'and', 'a', 'in', 'to', 'for', 'with', 'on', 'at', 'from', 'by', 'an', 'are'}
        meaningful_words = {w for w in query_words if len(w) > 2 and w not in stopwords}
        
        if not meaningful_words:
            return 1.0
        
        text_words = set(re.findall(r'\w+', text.lower()))
        matched = meaningful_words.intersection(text_words)
        return len(matched) / len(meaningful_words)

    @classmethod
    def evaluate(
        cls,
        query: str,
        query_analysis: Dict[str, Any],
        bm25_results: List[Dict[str, Any]],
        semantic_results: List[Dict[str, Any]],
        hybrid_results: List[Dict[str, Any]],
        target_evidence_count: int = 3
    ) -> Dict[str, Any]:
        """Evaluate candidate pools from BM25, Semantic, and Hybrid retrievers."""
        
        # Extract top candidate chunk_ids per retriever
        bm25_top_ids = [c["chunk_id"] for c in bm25_results[:3]]
        sem_top_ids = [c["chunk_id"] for c in semantic_results[:3]]
        hybrid_top_ids = [c["chunk_id"] for c in hybrid_results[:3]]

        # Consensus calculations
        all_top_ids = set(bm25_top_ids + sem_top_ids + hybrid_top_ids)
        overlap_bm25_sem = len(set(bm25_top_ids).intersection(set(sem_top_ids)))
        overlap_sem_hybrid = len(set(sem_top_ids).intersection(set(hybrid_top_ids)))
        overlap_bm25_hybrid = len(set(bm25_top_ids).intersection(set(hybrid_top_ids)))

        consensus_high = (overlap_bm25_sem >= 2 or overlap_sem_hybrid >= 2 or overlap_bm25_hybrid >= 2)

        # Decide optimal strategy based on query analysis & empirical signals
        is_keyword = query_analysis.get("is_keyword_heavy", False)
        is_semantic = query_analysis.get("is_semantic", False)
        is_numerical = query_analysis.get("is_numerical", False)

        selected_strategy = "Hybrid Retrieval"
        strategy_reasoning = ""

        if is_keyword and not is_semantic:
            # Check if BM25 score magnitude is strong
            top_bm25_score = bm25_results[0]["bm25_score"] if bm25_results else 0
            if top_bm25_score > 3.5:
                selected_strategy = "BM25 Retrieval"
                strategy_reasoning = f"Query is keyword-dense and top BM25 match achieved strong term frequency score ({top_bm25_score:.2f})."
            else:
                selected_strategy = "Hybrid Retrieval"
                strategy_reasoning = "Query contains explicit keywords, but Hybrid retrieval provides optimal coverage of surrounding text."
        elif is_semantic and not is_keyword:
            top_sem_score = semantic_results[0]["similarity_score"] if semantic_results else 0
            if top_sem_score > 0.75:
                selected_strategy = "Semantic Retrieval"
                strategy_reasoning = f"Query demands conceptual understanding; Semantic agent identified relevant contextual chunk (similarity: {top_sem_score:.3f})."
            else:
                selected_strategy = "Hybrid Retrieval"
                strategy_reasoning = "Query is conceptual, but score fusion ensures high precision."
        else:
            selected_strategy = "Hybrid Retrieval"
            strategy_reasoning = "Query combines multiple traits (keywords/concepts/numerical); Hybrid search balances exact matching with conceptual similarity."

        # Pick primary pool based on selected strategy
        if selected_strategy == "BM25 Retrieval":
            primary_pool = bm25_results
        elif selected_strategy == "Semantic Retrieval":
            primary_pool = semantic_results
        else:
            primary_pool = hybrid_results

        # Deduplicate and evaluate each chunk across candidates
        seen_texts = set()
        selected_evidence = []
        rejected_evidence = []

        # Merge candidate pools prioritizing primary pool
        merged_candidates = list(primary_pool)
        for pool in [hybrid_results, semantic_results, bm25_results]:
            for chunk in pool:
                if chunk["chunk_id"] not in [c["chunk_id"] for c in merged_candidates]:
                    merged_candidates.append(chunk)

        for chunk in merged_candidates:
            cid = chunk["chunk_id"]
            text_snippet = chunk["text"]
            
            # Check duplicate text snippet
            normalized_snippet = text_snippet[:100].lower()
            if normalized_snippet in seen_texts:
                rejected_chunk = dict(chunk)
                rejected_chunk["rejection_reason"] = "Duplicate snippet content."
                rejected_evidence.append(rejected_chunk)
                continue

            # Evaluate agreement & keyword coverage
            cross_retriever_count = (1 if cid in bm25_top_ids else 0) + \
                                    (1 if cid in sem_top_ids else 0) + \
                                    (1 if cid in hybrid_top_ids else 0)
            
            coverage = cls._compute_keyword_coverage(query, text_snippet)

            # Judge score formula (weighted sum of signals)
            bm25_val = chunk.get("bm25_norm", chunk.get("bm25_score", 0.0) / 10.0)
            sem_val = chunk.get("similarity_score", 0.0)
            
            chunk_judge_score = (0.40 * sem_val) + (0.35 * min(1.0, bm25_val)) + (0.15 * coverage) + (0.10 * (cross_retriever_count / 3.0))

            chunk_eval = dict(chunk)
            chunk_eval["keyword_coverage"] = round(coverage, 2)
            chunk_eval["cross_agent_agreement"] = cross_retriever_count
            chunk_eval["judge_evidence_score"] = round(chunk_judge_score, 4)

            if len(selected_evidence) < target_evidence_count and chunk_judge_score >= 0.25:
                selected_evidence.append(chunk_eval)
                seen_texts.add(normalized_snippet)
            else:
                rejected_chunk = dict(chunk_eval)
                if chunk_judge_score < 0.25:
                    rejected_chunk["rejection_reason"] = f"Low evidence score ({chunk_judge_score:.3f})."
                else:
                    rejected_chunk["rejection_reason"] = f"Exceeded top-{target_evidence_count} evidence capacity."
                rejected_evidence.append(rejected_chunk)

        # Average judge score of selected evidence
        avg_evidence_score = (
            sum(c["judge_evidence_score"] for c in selected_evidence) / len(selected_evidence)
            if selected_evidence else 0.0
        )

        judge_explanation = (
            f"**Evidence Selection Rationale:**\n\n"
            f"- **Selected Strategy:** {selected_strategy}. {strategy_reasoning}\n"
            f"- **Inter-Agent Consensus:** {overlap_bm25_sem}/3 overlap between BM25 and Semantic top results. "
            f"Overall consensus level: {'HIGH' if consensus_high else 'MODERATE'}.\n"
            f"- **Selection Metrics:** Screened {len(merged_candidates)} candidate chunks across all 3 retrieval agents. "
            f"Selected top {len(selected_evidence)} chunks with average evidence score of {avg_evidence_score:.3f}.\n"
            f"- **Filtering Action:** Rejected {len(rejected_evidence)} lower-ranked or redundant chunks."
        )

        return {
            "selected_strategy": selected_strategy,
            "selected_evidence": selected_evidence,
            "rejected_evidence": rejected_evidence,
            "overall_evidence_score": round(avg_evidence_score, 4),
            "consensus_high": consensus_high,
            "bm25_sem_overlap": overlap_bm25_sem,
            "explanation": judge_explanation
        }
