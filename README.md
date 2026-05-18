# PyDocCheck

Automated Documentation Code Validator for Python

## Project Overview

PyDocCheck is a tool that automatically validates Python code examples embedded in documentation (README.md, .rst files, etc.) to ensure they remain executable and up-to-date.

## Current Stage: Document Parsing & Code Extraction

This is the initial development phase focusing on:
- Extracting code blocks from Markdown and RST documents
- Preprocessing and normalizing extracted code
- Building metadata for code traceability

## Project Structure

```
pydoccheck/
├── src/
│   └── pydoccheck/
│       ├── parsers/           # Document parsers (Markdown, RST)
│       ├── models/            # Data models (CodeBlock, DocumentInfo)
│       └── utils/             # Helper utilities
├── tests/
│   ├── fixtures/              # Test data and sample documents
│   └── test_*.py              # Test files
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Getting Started

### Installation

```bash
cd c:\Users\백지유\Desktop\pydoccheck
pip install -r requirements.txt
```

### Running Tests

```bash
pytest tests/test_markdown_parser.py -v
```

### Basic Usage

```python
from pydoccheck.parsers import MarkdownParser
from pydoccheck.utils.helpers import load_document

# Load document
content, doc_info = load_document("path/to/file.md")

# Parse code blocks
parser = MarkdownParser()
blocks = parser.parse(content, doc_info)

# Access extracted code
for block in blocks:
    print(f"Block {block.block_id}: {block.language}")
    print(f"Lines {block.start_line}-{block.end_line}")
    print(f"Imports: {block.imports}")
    print(f"Executable: {block.is_executable}")
```

## Development Timeline

- **Week 1**: Design document structure and parser interfaces
- **Week 2**: Implement Markdown/RST code extraction engine
- **Week 3**: Add metadata mapping logic
- **Week 4**: Code preprocessing (comment removal, etc.)
- **Week 5**: Code snippet optimization
- **Week 6**: Syntax validation
- **Week 7**: Integration with execution sandbox
- **Week 8**: Final validation and reporting

## Testing with Dummy Data

Sample documentation files are provided in `tests/fixtures/sample_docs/`:
- `sample_simple.md` - Basic examples
- `sample_complex.md` - Examples with errors
- `sample_rst.rst` - reStructuredText format

Run tests to validate the parser implementation:
```bash
pytest tests/ -v --tb=short
```

## Team Members

- 정민경: Document analysis & data collection (This module)
- 백지유: Document parsing & code preprocessing
- 강인후: Execution environment & test engine
- 조혜준: Result analysis & reporting

## Next Steps

1. Run the test suite to validate current implementation
2. Expand parser to handle edge cases
3. Implement code preprocessing logic
4. Integrate with execution engine
