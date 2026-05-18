"""Markdown parser for extracting code blocks from markdown documents."""

import ast
import re
from typing import List
from abc import ABC, abstractmethod

from ..models.code_block import CodeBlock, DocumentInfo


class BaseParser(ABC):
    """Abstract base class for document parsers."""

    @abstractmethod
    def parse(self, content: str, doc_info: DocumentInfo) -> List[CodeBlock]:
        """Parse document content and extract code blocks."""
        pass

    @staticmethod
    def _extract_imports(code: str) -> List[str]:
        """Extract import statements from Python code."""
        import_pattern = r"^(?:from|import)\s+[\w\.]+(?:\s+import\s+[\w\*,\s]+)?"
        matches = re.findall(import_pattern, code, re.MULTILINE)
        return [match.strip() for match in matches]

    @staticmethod
    def _is_comment_only(code: str, language: str) -> bool:
        """Check whether the code block contains only comments or whitespace."""
        if language.lower() != "python":
            return False

        for line in code.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith('#'):
                continue
            return False

        return True

    @classmethod
    def _clean_code(cls, code: str, language: str) -> str:
        """Normalize and clean Python code blocks for execution."""
        if language.lower() != "python":
            return code.strip()

        cleaned_lines: List[str] = []
        for line in code.splitlines():
            stripped = line.strip()
            if not stripped:
                cleaned_lines.append('')
                continue

            if stripped.startswith('#'):
                continue
            if stripped.startswith('$') or stripped.startswith('!') or stripped.startswith('%'):
                continue
            if stripped.startswith('>>>'):
                cleaned_lines.append(stripped[4:].rstrip())
                continue
            if stripped.startswith('...'):
                cleaned_lines.append(stripped[4:].rstrip())
                continue

            cleaned_lines.append(line)

        cleaned = '\n'.join(cleaned_lines).strip()
        return cleaned

    @staticmethod
    def _syntax_valid(code: str, language: str) -> bool | None:
        """Check Python syntax validity using the ast module."""
        if language.lower() != 'python':
            return None

        if not code.strip():
            return None

        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    @staticmethod
    def _is_executable(code: str, language: str) -> bool:
        """Determine if code block is independently executable."""
        if language.lower() != 'python':
            return True

        return not BaseParser._is_comment_only(code, language)

    @staticmethod
    def _sanitize_path(file_path: str) -> str:
        """Sanitize file path for use in identifiers."""
        return re.sub(r'[\\/\.]+', '_', file_path).strip('_')


class MarkdownParser(BaseParser):
    """Parser for Markdown documents."""

    # Pattern for fenced code blocks: ```language ... ```
    FENCE_PATTERN = r"```([a-z0-9]*)\n(.*?)\n```"

    def __init__(self):
        self.fence_regex = re.compile(self.FENCE_PATTERN, re.DOTALL | re.IGNORECASE)

    def parse(self, content: str, doc_info: DocumentInfo) -> List[CodeBlock]:
        """
        Extract code blocks from markdown content.

        Args:
            content: The markdown document content
            doc_info: Metadata about the document

        Returns:
            List of CodeBlock objects found in the document
        """
        blocks: List[CodeBlock] = []
        block_counter = 0

        for match in self.fence_regex.finditer(content):
            block_counter += 1
            language = match.group(1).strip() or 'text'
            code_content = match.group(2)

            start_line = content[:match.start()].count('\n') + 1
            end_line = content[:match.end()].count('\n') + 1

            block_id = f"{self._sanitize_path(doc_info.file_path)}_block_{block_counter}"

            cleaned_content = self._clean_code(code_content, language)
            syntax_valid = self._syntax_valid(cleaned_content, language)
            imports = self._extract_imports(cleaned_content) if language.lower() == 'python' else []
            is_executable = self._is_executable(cleaned_content, language)

            block = CodeBlock(
                block_id=block_id,
                content=code_content,
                cleaned_content=cleaned_content,
                syntax_valid=syntax_valid,
                language=language,
                file_path=doc_info.file_path,
                start_line=start_line,
                end_line=end_line,
                imports=imports,
                is_executable=is_executable,
            )
            blocks.append(block)

        return blocks
