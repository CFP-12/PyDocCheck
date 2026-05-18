"""Tests for the RST parser."""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pydoccheck.parsers import RSTParser
from pydoccheck.models.code_block import DocumentInfo
from pydoccheck.utils.helpers import load_document, parse_document


@pytest.fixture
def parser():
    """Create an RSTParser instance."""
    return RSTParser()


@pytest.fixture
def sample_docs_dir():
    """Get the sample docs directory path."""
    return Path(__file__).parent / "fixtures" / "sample_docs"


def test_parse_simple_rst(parser, sample_docs_dir):
    """Test parsing a simple RST file."""
    file_path = sample_docs_dir / "sample_rst.rst"
    content, doc_info = load_document(str(file_path))

    blocks = parser.parse(content, doc_info)

    assert len(blocks) == 3
    assert all(block.language == "python" for block in blocks)
    assert all(block.is_executable for block in blocks)
    assert all(block.syntax_valid is True for block in blocks)
    assert all(block.cleaned_content for block in blocks)

    assert "print(\"Hello from RST!\")" in blocks[0].cleaned_content
    assert "squares =" in blocks[1].cleaned_content
    assert "person =" in blocks[2].cleaned_content


def test_parse_document_helper(sample_docs_dir):
    """Test the helper convenience parser path."""
    file_path = sample_docs_dir / "sample_rst.rst"
    blocks = parse_document(str(file_path))

    assert len(blocks) == 3
    assert blocks[0].file_path.endswith("sample_rst.rst")
    assert blocks[0].start_line > 0
    assert blocks[0].end_line >= blocks[0].start_line


if __name__ == "__main__":
    pytest.main([__file__, "-v"])