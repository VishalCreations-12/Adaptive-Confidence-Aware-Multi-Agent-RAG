import re
from pathlib import Path
from typing import Dict, Any, List
import pypdf

class DocumentParser:
    """Parses PDF and TXT documents into clean plain text with metadata."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean extracted document text."""
        if not text:
            return ""
        # Fix line splits and extra whitespace
        text = re.sub(r'\r\n|\r', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    @classmethod
    def parse_pdf(cls, file_path: Path) -> Dict[str, Any]:
        """Extract text page by page from a PDF file."""
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        reader = pypdf.PdfReader(str(file_path))
        pages_content = []
        full_text_list = []
        
        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            cleaned_page = cls.clean_text(page_text)
            if cleaned_page:
                pages_content.append({
                    "page_number": idx + 1,
                    "text": cleaned_page
                })
                full_text_list.append(f"--- Page {idx + 1} ---\n{cleaned_page}")

        full_text = "\n\n".join(full_text_list)
        return {
            "file_name": file_path.name,
            "file_path": str(file_path),
            "file_type": "pdf",
            "num_pages": len(reader.pages),
            "full_text": full_text,
            "pages": pages_content
        }

    @classmethod
    def parse_txt(cls, file_path: Path) -> Dict[str, Any]:
        """Extract text from a plain TXT file."""
        if not file_path.exists():
            raise FileNotFoundError(f"TXT file not found: {file_path}")

        content = file_path.read_text(encoding='utf-8', errors='ignore')
        cleaned_text = cls.clean_text(content)

        return {
            "file_name": file_path.name,
            "file_path": str(file_path),
            "file_type": "txt",
            "num_pages": 1,
            "full_text": cleaned_text,
            "pages": [{"page_number": 1, "text": cleaned_text}]
        }

    @classmethod
    def parse_document(cls, file_path: Path) -> Dict[str, Any]:
        """Auto-detect extension and parse file."""
        ext = file_path.suffix.lower()
        if ext == '.pdf':
            return cls.parse_pdf(file_path)
        elif ext in ['.txt', '.md']:
            return cls.parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Only PDF and TXT are supported.")
