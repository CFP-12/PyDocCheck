"""Tests for the Markdown parser."""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pydoccheck.parsers import MarkdownParser
from pydoccheck.models.code_block import DocumentInfo
from pydoccheck.utils.helpers import load_document


@pytest.fixture
def parser():
    """Create a MarkdownParser instance."""
    return MarkdownParser()


@pytest.fixture
def sample_docs_dir():
    """Get the sample docs directory path."""
    return Path(__file__).parent / "fixtures" / "sample_docs"


def test_parse_simple_markdown(parser, sample_docs_dir):
    """Test parsing a simple markdown file."""
    file_path = sample_docs_dir / "sample_simple.md"
    content, doc_info = load_document(str(file_path))
    
    blocks = parser.parse(content, doc_info)
    
    # Should find 3 code blocks
    assert len(blocks) == 3
    
    # Check first block
    assert blocks[0].language == "python"
    assert "Hello, World!" in blocks[0].content
    assert blocks[0].is_executable
    
    # Check second block
    assert "name = " in blocks[1].content
    assert blocks[1].is_executable
    
    # Check third block
    assert "fruits = " in blocks[2].content
    assert blocks[2].is_executable


def test_parse_complex_markdown(parser, sample_docs_dir):
    """Test parsing a more complex markdown file."""
    file_path = sample_docs_dir / "sample_complex.md"
    content, doc_info = load_document(str(file_path))
    
    blocks = parser.parse(content, doc_info)
    
    # Should find multiple code blocks
    assert len(blocks) > 0
    
    # Check that imports are extracted
    import_blocks = [b for b in blocks if b.imports]
    assert len(import_blocks) > 0
    assert any("pandas" in imp for block in import_blocks for imp in block.imports)
    
    # The comment-only block should be identified but not executable
    comment_blocks = [b for b in blocks if not b.is_executable]
    assert len(comment_blocks) == 1
    assert comment_blocks[0].cleaned_content == ""
    assert comment_blocks[0].syntax_valid is None
    
    # Check block identifiers are unique
    block_ids = [b.block_id for b in blocks]
    assert len(block_ids) == len(set(block_ids))


def test_extract_imports(parser):
    """Test import extraction."""
    code = """import pandas as pd
import numpy as np
from os.path import join
"""
    imports = parser._extract_imports(code)
    
    assert len(imports) == 3
    assert "import pandas" in imports
    assert "import numpy" in imports
    assert "from os.path import join" in imports


def test_is_executable(parser):
    """Test executable code detection."""
    # Should be executable
    assert parser._is_executable("print('hello')", "python")
    
    # Should not be executable (comment only)
    assert not parser._is_executable("# just a comment", "python")
    
    # Non-Python is always executable
    assert parser._is_executable("", "javascript")


def test_metadata(parser, sample_docs_dir):
    """Test that metadata is correctly captured."""
    file_path = sample_docs_dir / "sample_simple.md"
    content, doc_info = load_document(str(file_path))
    
    blocks = parser.parse(content, doc_info)
    
    for block in blocks:
        # Check metadata fields
        assert block.block_id
        assert block.file_path
        assert block.start_line > 0
        assert block.end_line >= block.start_line
        assert block.language == "python"
        assert block.cleaned_content is not None
        assert block.syntax_valid in (True, False, None)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
