#!/usr/bin/env python
"""Quick test to verify the parser works without pytest."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pydoccheck.parsers import MarkdownParser
from pydoccheck.models.code_block import DocumentInfo
from pydoccheck.utils.helpers import load_document

def test_simple_markdown():
    """Test parsing a simple markdown file."""
    print("\n" + "="*60)
    print("Testing Markdown Parser with sample_simple.md")
    print("="*60)
    
    file_path = Path(__file__).parent / "tests/fixtures/sample_docs/sample_simple.md"
    content, doc_info = load_document(str(file_path))
    
    parser = MarkdownParser()
    blocks = parser.parse(content, doc_info)
    
    print(f"\n✓ Found {len(blocks)} code blocks\n")
    
    for i, block in enumerate(blocks, 1):
        print(f"Block {i}:")
        print(f"  ID: {block.block_id}")
        print(f"  Language: {block.language}")
        print(f"  Lines: {block.start_line}-{block.end_line}")
        print(f"  Imports: {block.imports}")
        print(f"  Executable: {block.is_executable}")
        print(f"  Content preview: {block.content[:50]}...")
        print()
    
    assert len(blocks) == 3, f"Expected 3 blocks, got {len(blocks)}"
    print("✓ Simple markdown test PASSED")


def test_complex_markdown():
    """Test parsing a complex markdown file."""
    print("\n" + "="*60)
    print("Testing Markdown Parser with sample_complex.md")
    print("="*60)
    
    file_path = Path(__file__).parent / "tests/fixtures/sample_docs/sample_complex.md"
    content, doc_info = load_document(str(file_path))
    
    parser = MarkdownParser()
    blocks = parser.parse(content, doc_info)
    
    print(f"\n✓ Found {len(blocks)} code blocks\n")
    
    for i, block in enumerate(blocks, 1):
        print(f"Block {i}:")
        print(f"  ID: {block.block_id}")
        print(f"  Language: {block.language}")
        print(f"  Imports: {block.imports}")
        print(f"  Executable: {block.is_executable}")
        print()
    
    # Check that imports are extracted
    import_blocks = [b for b in blocks if b.imports]
    assert len(import_blocks) > 0, "No import blocks found"
    
    # Check for pandas import
    has_pandas = any("pandas" in imp for block in import_blocks for imp in block.imports)
    assert has_pandas, "Pandas import not found"
    
    print("✓ Complex markdown test PASSED")


def test_rst_parser():
    """Test parsing RST file."""
    print("\n" + "="*60)
    print("Testing RST Parser with sample_rst.rst")
    print("="*60)
    
    from pydoccheck.parsers import RSTParser
    
    file_path = Path(__file__).parent / "tests/fixtures/sample_docs/sample_rst.rst"
    content, doc_info = load_document(str(file_path))
    
    parser = RSTParser()
    blocks = parser.parse(content, doc_info)
    
    print(f"\n✓ Found {len(blocks)} code blocks\n")
    
    for i, block in enumerate(blocks, 1):
        print(f"Block {i}:")
        print(f"  ID: {block.block_id}")
        print(f"  Language: {block.language}")
        print(f"  Content: {block.content[:60]}...")
        print()
    
    assert len(blocks) > 0, "No RST blocks found"
    print("✓ RST parser test PASSED")


if __name__ == "__main__":
    try:
        test_simple_markdown()
        test_complex_markdown()
        test_rst_parser()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n프로젝트 구조가 정상적으로 작동합니다!\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
