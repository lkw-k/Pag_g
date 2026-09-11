"""Document loading utilities for the RAG pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from pypdf import PdfReader


@dataclass
class Document:
    content: str
    source: str
    metadata: dict = field(default_factory=dict)


def load_pdf(path: Path | str) -> Document:
    """Load a single PDF file and extract its text content."""
    path = Path(path)
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    content = "\n".join(pages)
    return Document(content=content, source=str(path), metadata={"page_count": len(reader.pages)})
