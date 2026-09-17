from typing import List, Dict, Any
import config

class DocumentChunker:
    """Splits document text into clean, metadata-enriched chunks for retrieval."""
    
    def __init__(self, chunk_size: int = config.CHUNK_SIZE, chunk_overlap: int = config.CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, doc_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk a document by pages with overlapping character sliding windows."""
        chunks = []
        doc_name = doc_data.get("file_name", "unknown_doc")
        global_chunk_idx = 0

        for page_info in doc_data.get("pages", []):
            page_num = page_info["page_number"]
            text = page_info["text"]
            
            if not text:
                continue

            # Split page text into overlapping windows
            start = 0
            text_len = len(text)

            while start < text_len:
                end = min(start + self.chunk_size, text_len)
                
                # If we're not at the end of text, try breaking at sentence boundary
                if end < text_len:
                    sentence_end = max(text.rfind('. ', start, end), text.rfind('\n', start, end))
                    if sentence_end != -1 and sentence_end > start + 100:
                        end = sentence_end + 1

                chunk_text = text[start:end].strip()
                
                if len(chunk_text) >= config.MIN_CHUNK_LEN:
                    global_chunk_idx += 1
                    chunks.append({
                        "chunk_id": f"{doc_name}_chunk_{global_chunk_idx}",
                        "global_index": global_chunk_idx - 1,
                        "doc_name": doc_name,
                        "page_number": page_num,
                        "text": chunk_text,
                        "char_length": len(chunk_text)
                    })

                if end >= text_len:
                    break
                start = end - self.chunk_overlap

        return chunks
