"""Helper utilities for document processing."""

import os
from pathlib import Path
from typing import List

from ..models.code_block import DocumentInfo


def get_document_type(file_path: str) -> str:
    """Determine document type from file extension."""
    ext = Path(file_path).suffix.lower()

    type_map = {
        '.md': 'markdown',
        '.markdown': 'markdown',
        '.rst': 'rst',
        '.txt': 'txt',
    }

    return type_map.get(ext, 'unknown')


def load_document(file_path: str) -> tuple[str, DocumentInfo]:
    """
    Load a document from file.

    Args:
        file_path: Path to the document

    Returns:
        Tuple of (content, DocumentInfo)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    doc_info = DocumentInfo(
        file_path=file_path,
        document_type=get_document_type(file_path)
    )

    return content, doc_info


def find_documents(directory: str, extensions: List[str] = None) -> List[str]:
    """
    Find all documentation files in a directory.

    Args:
        directory: Directory to search
        extensions: List of file extensions to search for (default: ['.md', '.rst', '.txt'])

    Returns:
        List of file paths
    """
    if extensions is None:
        extensions = ['.md', '.rst', '.txt']

    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, filename))

    return files


def get_parser(document_type: str):
    """Return a parser instance for the given document type."""
    from ..parsers import MarkdownParser, RSTParser

    if document_type == 'markdown':
        return MarkdownParser()
    if document_type == 'rst':
        return RSTParser()

    raise ValueError(f"Unsupported document type: {document_type}")


def parse_document(file_path: str):
    """Load and parse a document into code blocks."""
    content, doc_info = load_document(file_path)
    parser = get_parser(doc_info.document_type)
    return parser.parse(content, doc_info)
