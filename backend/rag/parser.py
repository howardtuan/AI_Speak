"""Document parsing utilities for PDF and DOCX files."""
import logging

logger = logging.getLogger(__name__)


def parse_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    import fitz  # PyMuPDF

    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()


def parse_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    from docx import Document

    doc = Document(file_path)
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text)
    return text.strip()


def parse_document(file_path: str, file_type: str) -> str:
    """Parse a document and return its text content."""
    parsers = {
        "pdf": parse_pdf,
        "docx": parse_docx,
    }
    parser = parsers.get(file_type.lower())
    if parser is None:
        raise ValueError(f"Unsupported file type: {file_type}")
    return parser(file_path)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
