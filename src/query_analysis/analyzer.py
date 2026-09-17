import re
from typing import Dict, Any, List

class QueryAnalyzer:
    """Analyzes user query characteristics to inform evidence judging and strategy selection."""

    @staticmethod
    def analyze(query: str) -> Dict[str, Any]:
        """Analyze query features and determine likely query type."""
        query_str = query.strip()
        query_lower = query_str.lower()
        
        word_count = len(query_str.split())
        
        # Characteristic flags
        has_keywords = bool(re.search(r'\b[A-Z0-9-]{3,}\b|\b[a-z]+-\d+\b|\bv\d+\.\d+\b', query_str))
        has_numbers = bool(re.search(r'\d+|\$|%|°C|km/h|Gbps|Watts', query_str, re.IGNORECASE))
        has_comparison = any(term in query_lower for term in ['compare', 'versus', 'vs', 'difference', 'differ', 'contrast'])
        has_semantic = any(query_lower.startswith(prefix) for prefix in ['how', 'why', 'explain', 'describe', 'evaluate'])
        has_factual = any(query_lower.startswith(prefix) for prefix in ['what', 'when', 'where', 'who', 'which'])
        has_entity = any(term in query_lower for term in ['ceo', 'cto', 'headquarter', 'boston', 'novatech', 'aeroguide', 'novasolar']) or bool(re.search(r'\b[A-Z][a-z]+\b', query_str))
        has_multi_part = any(conj in query_lower for conj in [' and ', ' along with ', ' as well as ', ', and ']) or query_str.count('?') > 1

        # Categorize primary characteristics
        characteristics = []
        if has_keywords or (word_count < 6 and not has_semantic):
            characteristics.append("keyword-heavy")
        if has_semantic or word_count > 10:
            characteristics.append("semantic")
        if has_factual:
            characteristics.append("factual")
        if has_numbers:
            characteristics.append("numerical")
        if has_entity:
            characteristics.append("entity-focused")
        if has_comparison:
            characteristics.append("comparison")
        if has_multi_part:
            characteristics.append("multi-part / multi-hop")

        if not characteristics:
            characteristics = ["general-semantic"]

        return {
            "query": query_str,
            "word_count": word_count,
            "characteristics": characteristics,
            "is_keyword_heavy": "keyword-heavy" in characteristics,
            "is_semantic": "semantic" in characteristics,
            "is_numerical": "numerical" in characteristics,
            "is_comparison": "comparison" in characteristics,
            "is_multi_part": "multi-part / multi-hop" in characteristics
        }
