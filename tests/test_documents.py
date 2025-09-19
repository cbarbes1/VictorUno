"""Test document processing functionality."""

import pytest
import tempfile
from pathlib import Path

from victoruno.integrations.documents import DocumentProcessor
from victoruno.core.config import Config


@pytest.fixture
def document_processor():
    """Create a document processor instance for testing."""
    config = Config()
    return DocumentProcessor(config)


@pytest.fixture
def sample_text_file():
    """Create a sample text file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a sample text file for testing.\nIt has multiple lines.\n")
        return Path(f.name)


@pytest.mark.asyncio
async def test_process_text_file(document_processor, sample_text_file):
    """Test processing a text file."""
    try:
        result = await document_processor.process_document(sample_text_file)
        
        assert result["success"] is True
        assert result["filename"] == sample_text_file.name
        assert "sample text file" in result["content"]
        assert result["word_count"] > 0
        assert result["char_count"] > 0
    
    finally:
        # Clean up
        if sample_text_file.exists():
            sample_text_file.unlink()


@pytest.mark.asyncio
async def test_process_nonexistent_file(document_processor):
    """Test processing a file that doesn't exist."""
    nonexistent_file = Path("/nonexistent/file.txt")
    
    result = await document_processor.process_document(nonexistent_file)
    
    assert result["success"] is False
    assert "not found" in result["message"].lower()


def test_supported_formats(document_processor):
    """Test getting supported file formats."""
    formats = document_processor.get_supported_formats()
    
    assert isinstance(formats, list)
    assert "txt" in formats
    assert "md" in formats


def test_is_supported_format(document_processor):
    """Test checking if a file format is supported."""
    assert document_processor.is_supported_format(Path("test.txt")) is True
    assert document_processor.is_supported_format(Path("test.md")) is True
    assert document_processor.is_supported_format(Path("test.xyz")) is False


@pytest.mark.asyncio
async def test_extract_keywords(document_processor):
    """Test keyword extraction from text."""
    text = "Python programming is great. Python is a versatile programming language."
    
    keywords = await document_processor.extract_keywords(text)
    
    assert isinstance(keywords, list)
    assert "python" in keywords
    assert "programming" in keywords


@pytest.mark.asyncio
async def test_summarize_document(document_processor):
    """Test document summarization."""
    long_text = "This is a long text. " * 100  # Create a long text
    
    summary = await document_processor.summarize_document(long_text, max_length=50)
    
    assert len(summary) <= 500  # Should be reasonably short
    assert "content truncated" in summary.lower()