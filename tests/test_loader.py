from unittest.mock import MagicMock, patch

from rag.loader import Document, load_documents, load_pdf, load_text


def test_load_text(tmp_path):
    file_path = tmp_path / "note.txt"
    file_path.write_text("hello world", encoding="utf-8")

    doc = load_text(file_path)

    assert isinstance(doc, Document)
    assert doc.content == "hello world"
    assert doc.source == str(file_path)


def test_load_pdf_extracts_and_joins_pages(tmp_path):
    fake_pdf = tmp_path / "sample.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake")

    page1 = MagicMock()
    page1.extract_text.return_value = "page one"
    page2 = MagicMock()
    page2.extract_text.return_value = "page two"

    with patch("rag.loader.PdfReader") as mock_reader:
        mock_reader.return_value.pages = [page1, page2]
        doc = load_pdf(fake_pdf)

    assert doc.content == "page one\npage two"
    assert doc.metadata["page_count"] == 2


def test_load_documents_scans_supported_files_only(tmp_path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.md").write_text("ignored", encoding="utf-8")

    docs = load_documents(tmp_path)

    assert len(docs) == 1
    assert docs[0].content == "a"


def test_load_documents_empty_dir_returns_empty_list(tmp_path):
    assert load_documents(tmp_path) == []
