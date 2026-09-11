"""Document loading utilities for the RAG pipeline."""
from __future__ import annotations

import sys
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


def load_text(path: Path | str) -> Document:
    """Load a single plain-text file."""
    path = Path(path)
    content = path.read_text(encoding="utf-8")
    return Document(content=content, source=str(path), metadata={})


SUPPORTED_LOADERS = {
    ".pdf": load_pdf,
    ".txt": load_text,
}


def load_documents(data_dir: Path | str) -> list[Document]:
    """Scan a directory for supported files and load them all.

    A file that fails to load (e.g. wrong encoding, corrupted PDF) is skipped
    with a warning instead of aborting the whole scan.
    """
    data_dir = Path(data_dir)
    documents = []
    for path in sorted(data_dir.rglob("*")):
        if not path.is_file():
            continue
        loader = SUPPORTED_LOADERS.get(path.suffix.lower())
        if loader is None:
            continue
        try:
            documents.append(loader(path))
        except Exception as exc:
            print(f"Skipping {path}: {exc}", file=sys.stderr)
    return documents
