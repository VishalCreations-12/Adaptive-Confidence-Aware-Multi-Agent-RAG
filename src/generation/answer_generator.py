import re
from typing import List, Dict, Any

class GroundedAnswerGenerator:
    """Generates structured, strictly evidence-grounded answers based on selected chunks."""

    @classmethod
    def generate_answer(
        cls,
        query: str,
        selected_evidence: List[Dict[str, Any]],
        confidence_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize answer directly from selected evidence chunks with explicit citations."""
        if not selected_evidence:
            return {
                "answer": "No sufficient evidence was found in the indexed knowledge base to answer this query.",
                "supporting_evidence": [],
                "citations": []
            }

        # Build citations and sentence-level evidence extractions
        supporting_snippets = []
        citations = []
        synthesized_paragraphs = []

        query_terms = set(re.findall(r'\w+', query.lower()))
        stopwords = {'what', 'is', 'the', 'of', 'and', 'a', 'in', 'to', 'for', 'with', 'on', 'at', 'from', 'by', 'an', 'are'}
        meaningful_terms = {w for w in query_terms if len(w) > 2 and w not in stopwords}

        for idx, chunk in enumerate(selected_evidence):
            doc_name = chunk.get("doc_name", "Document")
            page_num = chunk.get("page_number", 1)
            chunk_id = chunk.get("chunk_id", f"chunk_{idx+1}")
            text = chunk.get("text", "")

            citation_str = f"[{doc_name} (Page {page_num}, ID: {chunk_id})]"
            citations.append(citation_str)

            # Find key sentences in chunk matching query terms
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 10]
            matched_sentences = []
            
            for sentence in sentences:
                sent_words = set(re.findall(r'\w+', sentence.lower()))
                if meaningful_terms and sent_words.intersection(meaningful_terms):
                    matched_sentences.append(sentence)

            if not matched_sentences:
                matched_sentences = sentences[:2]  # Fallback to lead sentences

            snippet_text = " ".join(matched_sentences[:2])
            supporting_snippets.append({
                "source": citation_str,
                "snippet": snippet_text,
                "full_text": text,
                "evidence_score": chunk.get("judge_evidence_score", 0.0)
            })

            synthesized_paragraphs.append(f"• **From {citation_str}:** {snippet_text}")

        # Assemble final answer body
        final_answer_text = (
            f"Based on the dynamically selected evidence (Confidence: {confidence_info.get('confidence_percentage', 'N/A')}), "
            f"the knowledge base indicates:\n\n" + "\n\n".join(synthesized_paragraphs)
        )

        return {
            "answer": final_answer_text,
            "supporting_snippets": supporting_snippets,
            "citations": citations,
            "confidence": confidence_info.get("confidence_percentage", "N/A"),
            "confidence_level": confidence_info.get("confidence_level", "MODERATE")
        }
