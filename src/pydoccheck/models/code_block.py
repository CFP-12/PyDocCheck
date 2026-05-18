"""Data models for code blocks extracted from documentation."""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class CodeBlock:
    """Represents a single code block extracted from documentation."""
    
    block_id: str  # Unique identifier (e.g., "doc1_block_1")
    content: str  # The actual code content
    language: str  # Programming language (e.g., "python", "javascript")
    
    # Metadata
    file_path: str  # Path to the source file
    start_line: int  # Starting line number in the source file
    end_line: int  # Ending line number in the source file
    
    # Extracted information
    imports: List[str]  # List of import statements found
    is_executable: bool  # Whether the code is independently executable
    
    # Optional processing flags
    cleaned_content: Optional[str] = None  # Content after pre-processing
    syntax_valid: Optional[bool] = None  # Whether syntax is valid
    
    def __str__(self) -> str:
        return f"CodeBlock({self.block_id}) - {self.language} - Lines {self.start_line}-{self.end_line}"


@dataclass
class DocumentInfo:
    """Metadata about the source document."""
    
    file_path: str
    document_type: str  # "markdown", "rst", "txt"
    url: Optional[str] = None
    encoding: str = "utf-8"
    
    def __str__(self) -> str:
        return f"Document({self.file_path}) - {self.document_type}"
