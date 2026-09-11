import pytest

from rag.chunker import chunk_document, chunk_documents, chunk_text
from rag.loader import Document


def test_chunk_text_splits_with_overlap():
    text = "abcdefghij"  # 10 chars

    chunks = chunk_text(text, chunk_size=4, chunk_overlap=1)

    assert chunks == ["abcd", "defg", "ghij"]


def test_chunk_text_exact_length_single_chunk():
    text = "abcd"

    chunks = chunk_text(text, chunk_size=4, chunk_overlap=1)

    assert chunks == ["abcd"]


def test_chunk_text_rejects_non_positive_chunk_size():
    with pytest.raises(ValueError):
        chunk_text("abc", chunk_size=0, chunk_overlap=0)


def test_chunk_text_rejects_overlap_too_large():
    with pytest.raises(ValueError):
        chunk_text("abc", chunk_size=4, chunk_overlap=4)


def test_chunk_document_preserves_source_and_metadata():
    document = Document(content="abcdefgh", source="note.txt", metadata={"page_count": 1})

    chunks = chunk_document(document, chunk_size=4, chunk_overlap=0)

    assert [c.content for c in chunks] == ["abcd", "efgh"]
    assert [c.index for c in chunks] == [0, 1]
    assert all(c.source == "note.txt" for c in chunks)
    assert all(c.metadata == {"page_count": 1} for c in chunks)


def test_chunk_documents_flattens_across_documents():
    docs = [
        Document(content="abcd", source="a.txt", metadata={}),
        Document(content="wxyz", source="b.txt", metadata={}),
    ]

    chunks = chunk_documents(docs, chunk_size=4, chunk_overlap=0)

    assert [c.source for c in chunks] == ["a.txt", "b.txt"]
    assert [c.content for c in chunks] == ["abcd", "wxyz"]
