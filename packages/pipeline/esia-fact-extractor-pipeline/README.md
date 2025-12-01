# Step 1: Enhanced Docling Convertor

Convert PDF and DOCX documents into semantically meaningful, token-aware chunks with accurate page tracking. Designed as the first step in a multi-step document intelligence pipeline (feeds into DSPy for fact extraction in Step 2).

## Features

- **Multi-format Support**: Process both PDF and DOCX files
- **Automatic DOCX to PDF Conversion**: DOCX files are automatically converted to PDF to enable page tracking
- **Token-Aware Semantic Chunking**: Uses HybridChunker with configurable token limits (default: 2,500 tokens)
- **Accurate Page Tracking**: Real page numbers extracted from document provenance, not guessed
- **Table & Image Extraction**: Automatically extracts tables and images with page references
- **GPU Acceleration**: Optional GPU support (CUDA/CPU fallback)
- **Streaming Output**: Memory-efficient JSONL format for large documents
- **Comprehensive Metadata**: Detailed statistics and document information
- **Optional Markdown Export**: Convert documents to markdown format

## Installation

### Prerequisites

- Python 3.8+
- CUDA 11.8+ (optional, for GPU acceleration)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd step1_enhanced_docling_convertor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install docling docling-core[chunking-openai] tiktoken torch tqdm
```

## Quick Start

### Basic Usage

Process a PDF file:
```bash
python step1_docling_hybrid_chunking.py ./data/inputs/pdfs/document.pdf
```

Process a DOCX file (automatically converts to PDF):
```bash
python step1_docling_hybrid_chunking.py ./data/inputs/docs/document.docx
```

### Output Files

- `document_chunks.jsonl` - Semantic chunks (one JSON object per line)
- `document_meta.json` - Metadata with statistics, tables, and images
- `document.md` - (Optional) Full markdown conversion

## Configuration

### Command-Line Options

```bash
python step1_docling_hybrid_chunking.py input_file [OPTIONS]

Positional Arguments:
  input_file                Path to PDF or DOCX file

Options:
  -o, --output-dir DIR      Output directory (default: hybrid_chunks_output)
  --gpu-mode {auto,cuda,cpu}
                            GPU acceleration mode (default: auto)
  --chunk-max-tokens N      Maximum tokens per chunk (default: 2500)
  --tokenizer-model MODEL   Tokenizer model for tiktoken (default: gpt-4o)
  --no-merge-peers          Disable merging of small chunks
  --enable-images           Extract images with page tracking
  --disable-tables          Disable table extraction
  --output-markdown         Export markdown version of document
  --no-json                 Disable JSON metadata output
  -v, --verbose             Verbose output
  -h, --help                Show help message
```

### Usage Examples

**Default processing (PDF):**
```bash
python step1_docling_hybrid_chunking.py report.pdf
```

**DOCX with GPU acceleration:**
```bash
python step1_docling_hybrid_chunking.py document.docx --gpu-mode cuda
```

**Custom chunk size with image extraction:**
```bash
python step1_docling_hybrid_chunking.py document.pdf --chunk-max-tokens 3000 --enable-images
```

**Full featured (GPU, images, markdown, verbose):**
```bash
python step1_docling_hybrid_chunking.py document.docx --gpu-mode cuda --enable-images --output-markdown --verbose
```

**Custom output directory:**
```bash
python step1_docling_hybrid_chunking.py document.pdf -o ./data/outputs/processed_docs
```

## Output Format

### Chunks JSONL File

Each line is a complete JSON object representing a chunk:

```json
{
  "chunk_id": 0,
  "page": 1,
  "section": "Introduction",
  "text": "The content of this semantic chunk...",
  "token_count": 2450,
  "metadata": {
    "headings": ["Introduction", "Background"],
    "captions": [],
    "doc_items_count": 5,
    "origin": {...}
  }
}
```

### Metadata JSON File

Comprehensive document metadata:

```json
{
  "document": {
    "original_filename": "document.docx",
    "processed_filename": "document_converted.pdf",
    "filepath": "/path/to/file.pdf",
    "total_pages": 42,
    "format": "pdf",
    "converted_from_docx": true,
    "processed_at": "2024-01-15T10:30:45.123456"
  },
  "files": {
    "chunks": "document_chunks.jsonl",
    "format": "jsonl"
  },
  "tables": [
    {
      "table_id": 0,
      "page": 5,
      "position": "table_0_page_5",
      "content": "| Column 1 | Column 2 |\n|----------|----------|\n| Data 1   | Data 2   |",
      "caption": "Table Title",
      "metadata": {"bbox": {...}}
    }
  ],
  "images": [
    {
      "image_id": 0,
      "page": 3,
      "position": "image_0_page_3",
      "filename": "image_3_0.png",
      "description": "Image caption",
      "metadata": {"bbox": {...}}
    }
  ],
  "statistics": {
    "total_chunks": 18,
    "total_tables": 3,
    "total_images": 5,
    "avg_tokens_per_chunk": 2380.5,
    "min_tokens_per_chunk": 1500,
    "max_tokens_per_chunk": 2800,
    "total_tokens": 42849,
    "pages_with_chunks": 42,
    "processing_timestamp": "2024-01-15T10:30:45.123456"
  }
}
```

## How It Works

### Processing Pipeline

1. **Input Detection** - Identifies file format (PDF or DOCX)
2. **DOCX Conversion** (if needed) - Converts DOCX to PDF in temporary directory
3. **Document Parsing** - Uses Docling's DocumentConverter with optional GPU acceleration
4. **Semantic Chunking** - HybridChunker creates structure-aware chunks respecting token limits
5. **Page Tracking** - Extracts real page numbers from document provenance
6. **Table/Image Extraction** - Identifies and exports tables (Markdown) and images with metadata
7. **Statistics Calculation** - Computes comprehensive processing metrics
8. **Output Generation** - Streams chunks to JSONL and exports metadata JSON
9. **Cleanup** - Removes temporary files (converted PDFs, etc.)

### Why DOCX Needs Conversion

DOCX files are XML-based and don't have inherent page boundaries. Converting to PDF:
- Establishes clear page structure
- Enables accurate page number tracking for chunks
- Allows consistent processing with Docling's page-aware pipeline

## Architecture

### Core Components

**Data Classes:**
- `DocumentChunk` - Semantic chunk with page and token metadata
- `TableData` - Table with page and position information
- `ImageData` - Image with page and bounding box information
- `ProcessingConfig` - Configuration parameters

**Key Functions:**
- `convert_docx_to_pdf()` - DOCX to PDF conversion
- `create_gpu_converter()` - Initialize Docling converter with GPU settings
- `create_hybrid_chunker()` - Setup token-aware chunking engine
- `extract_chunks_with_pages()` - Generate semantic chunks with page numbers
- `extract_tables_with_pages()` - Extract tables with metadata
- `extract_images_with_pages()` - Extract images with metadata
- `process_document()` - Main orchestration pipeline

## Performance Considerations

### Memory Efficiency
- Streaming JSONL output prevents loading entire document into memory
- Suitable for processing very large documents (100+ MB)

### GPU Optimization
- Automatic GPU detection with `--gpu-mode auto`
- Force CPU mode with `--gpu-mode cpu` if needed
- Typical speedup: 3-5x faster with GPU on large documents

### Chunk Size Impact
- **Smaller chunks** (1000 tokens): More chunks, finer granularity, slower processing
- **Larger chunks** (3500 tokens): Fewer chunks, less overhead, may lose context boundaries
- **Default** (2500 tokens): Balanced for most use cases

## Integration with DSPy

This tool outputs chunks specifically formatted for DSPy's fact extraction pipeline (Step 2):

```python
# Example: Loading chunks for DSPy
import json

chunks = []
with open('document_chunks.jsonl') as f:
    for line in f:
        chunks.append(json.loads(line))

# Process with DSPy
for chunk in chunks:
    result = dspy_pipeline(
        context=chunk['text'],
        page=chunk['page'],
        section=chunk['section']
    )
```

## Troubleshooting

### CUDA Not Available

If you see "CUDA requested but not available":
```bash
python step1_docling_hybrid_chunking.py document.pdf --gpu-mode cpu
```

### Missing Dependencies

Install all dependencies:
```bash
pip install -r requirements.txt
```

### DOCX Conversion Issues

Ensure Docling is properly installed:
```bash
pip install --upgrade docling docling-core
```

### Large Document Processing

For very large files, monitor memory and use:
```bash
python step1_docling_hybrid_chunking.py large_file.pdf --chunk-max-tokens 2000
```

## Project Structure

```
step1_enhanced_docling_convertor/
├── step1_docling_hybrid_chunking.py  # Main application (660 lines)
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
├── claude.md                          # Claude Code integration guide
└── hybrid_chunks_output/              # Default output directory (created at runtime)
```

## Technical Details

### Token Counting

Uses OpenAI's tiktoken library for accurate token counting:
- Model: `gpt-4o` (configurable)
- Exact token count per chunk
- Fallback to word count if tokenizer fails

### Page Number Extraction

Real page numbers from Docling's provenance metadata:
- Not estimated or guessed
- Extracted from `doc.pages` structure
- Includes bounding box information when available

### Chunk Merging

Optional peer merging combines small adjacent chunks:
- Enabled by default
- Improves output quality by preventing fragmentation
- Disable with `--no-merge-peers` if needed

## Limitations

- DOCX conversion may lose some formatting (acceptable for content extraction)
- Large complex tables may not convert to Markdown perfectly
- Image extraction requires image support in Docling
- Page layout analysis depends on document quality

## Future Enhancements

- [ ] Support for additional formats (PPTX, HTML, RTF)
- [ ] Custom chunking strategies
- [ ] Multi-language support with language-specific tokenizers
- [ ] Parallel processing for multiple documents
- [ ] Web API for document processing
- [ ] Integration with vector databases

## License

[Add your license here]

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section

## Acknowledgments

- Built on [Docling](https://github.com/DS4SD/docling) for PDF/document processing
- Uses [HybridChunker](https://github.com/DS4SD/docling/tree/main/core/src/docling_core/transforms/chunker) for semantic chunking
- Token counting via [OpenAI's tiktoken](https://github.com/openai/tiktoken)
