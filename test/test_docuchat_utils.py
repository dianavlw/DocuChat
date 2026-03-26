import pytest
from docuchat_utils import extract_text_from_reader, clean_text, chunk_text


class MockPage:
    def __init__(self, text):
        self._text = text

    def extract_text(self):
        return self._text


class MockReader:
    def __init__(self, pages):
        self.pages = pages


def test_extract_text_from_reader_returns_combined_text():
    reader = MockReader([
        MockPage("hello world."),
        MockPage("this is pg. 2."),
    ])
    result = extract_text_from_reader(reader)
    assert result == "hello world.\nthis is pg. 2."


def test_extract_text_from_reader_skips_empty_pages():
    reader = MockReader([
        MockPage("First page."),
        MockPage(None),
        MockPage("Third page."),
    ])
    result = extract_text_from_reader(reader)
    assert result == "First page.\nThird page."


def test_clean_text_removes_extra_whitespace():
    text = "Hello    hihihi.\n\nTHis is a     test."
    result = clean_text(text)
    assert result == "Hello hihihi. THis is a test."


def test_clean_text_handles_empty_string():
    assert clean_text("") == ""


def test_chunk_text_splits_text_into_chunks():
    text = "a" * 1000
    chunks = chunk_text(text, chunk_size=300, overlap=50)
    assert len(chunks) > 1
    assert all(len(chunk) <= 300 for chunk in chunks)


def test_chunk_text_returns_empty_list_for_blank_text():
    assert chunk_text("   ") == []


def test_chunk_text_raises_error_if_overlap_too_large():
    with pytest.raises(ValueError):
        chunk_text("Hello world", chunk_size=100, overlap=100)


def test_chunk_text_creates_overlap_between_chunks():
    text = "abcdefghijklmnopqrstuvwxyz" * 20
    chunks = chunk_text(text, chunk_size=50, overlap=10)
    assert len(chunks) > 1
    assert chunks[0][-10:] == chunks[1][:10]