"""Text chunking utilities for the RAG pipeline."""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from rag.loader import Document

DEFAULT_CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "1000"))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "150"))


@dataclass
class Chunk:
    content: str
    source: str
    index: int
    metadata: dict = field(default_factory=dict)


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Split text into overlapping chunks of at most chunk_size characters."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be non-negative and smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)
    step = chunk_size - chunk_overlap
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        if end == text_length:
            break
        start += step
    return chunks


def chunk_document(
    document: Document,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[Chunk]:
    """Split a single Document into Chunks."""
    chunk_size = chunk_size if chunk_size is not None else DEFAULT_CHUNK_SIZE
    chunk_overlap = chunk_overlap if chunk_overlap is not None else DEFAULT_CHUNK_OVERLAP
    pieces = chunk_text(document.content, chunk_size, chunk_overlap)
    return [
        Chunk(content=piece, source=document.source, index=i, metadata=dict(document.metadata))
        for i, piece in enumerate(pieces)
    ]


def chunk_documents(
    documents: list[Document],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[Chunk]:
    """Split multiple Documents into a single flat list of Chunks."""
    chunks = []
    for document in documents:
        chunks.extend(chunk_document(document, chunk_size, chunk_overlap))
    return chunks
