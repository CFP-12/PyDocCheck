"""RST (reStructuredText) parser for extracting code blocks from documentation."""

import re
from typing import List

from .markdown_parser import BaseParser
from ..models.code_block import CodeBlock, DocumentInfo


class RSTParser(BaseParser):
    """Parser for reStructuredText documents."""

    CODEBLOCK_PATTERN = (
        r"^\.\.\s+code-block::\s+([a-z0-9]+)\s*\n"
        r"(?:^[ \t]*:[^\n]*\n)*"
        r"\n"
        r"((?:^[ \t]{4}.*\n?)+)"
    )

    def __init__(self):
        self.codeblock_regex = re.compile(self.CODEBLOCK_PATTERN, re.MULTILINE)

    def parse(self, content: str, doc_info: DocumentInfo) -> List[CodeBlock]:
        """
        Extract code blocks from RST content.

        Args:
            content: The RST document content
            doc_info: Metadata about the document

        Returns:
            List of CodeBlock objects found in the document
        """
        blocks: List[CodeBlock] = []
        block_counter = 0

        for match in self.codeblock_regex.finditer(content):
            block_counter += 1
            language = match.group(1).strip() or 'text'
            code_block = match.group(2)
            code_content = self._unindent(code_block)

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

    @staticmethod
    def _unindent(text: str) -> str:
        """Remove leading indentation from RST code block."""
        lines = text.split('\n')
        if lines and not lines[0].strip():
            lines = lines[1:]

        min_indent = float('inf')
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                min_indent = min(min_indent, indent)

        if min_indent == float('inf'):
            min_indent = 0

        unindented = [
            line[min_indent:] if len(line) >= min_indent else line
            for line in lines
        ]

        return '\n'.join(unindented).strip()
