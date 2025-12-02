#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 1: Docling Hybrid Chunking with Real Page Tracking

Converts PDF or DOCX to JSON with token-aware semantic chunks that preserve page numbers.
Optimized for fact extraction with DSPy in Step 2.

Features:
- Automatic DOCX to PDF conversion (DOCX files don't have pages)
- HybridChunker for token-aware, structure-preserving chunking (2500 tokens default)
- Real page numbers from Docling provenance (not guessed from chunk position)
- Table/image extraction with page tracking
- JSON export with complete metadata
- GPU acceleration support
- Exact token counting with tiktoken

Usage:
    python step1_docling_hybrid_chunking.py "document.pdf"
    python step1_docling_hybrid_chunking.py "document.docx"
    python step1_docling_hybrid_chunking.py "document.pdf" --gpu-mode cuda --chunk-max-tokens 3000
    python step1_docling_hybrid_chunking.py "document.docx" --enable-images --output-markdown
"""

import sys
import os
import io
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Iterator, Tuple, Any
from datetime import datetime
import argparse
import json
from tqdm import tqdm
import tempfile
import re

# CRITICAL: Disable CUDA to avoid heap corruption on post-reboot systems
# This prevents GPU initialization errors (exit code 3221225794)
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['TORCH_DEVICE'] = 'cpu'

# Configure UTF-8 output for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class DocumentChunk:
    """Semantic chunk with page tracking"""
    chunk_id: int
    page: int
    section: Optional[str]
    text: str
    token_count: int
    metadata: Dict

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class TableData:
    """Table with page number"""
    table_id: int
    page: int
    position: str
    content: str
    caption: Optional[str] = None
    metadata: Optional[Dict] = None

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ImageData:
    """Image with page number"""
    image_id: int
    page: int
    position: str
    filename: str
    description: Optional[str] = None
    metadata: Optional[Dict] = None

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ProcessingConfig:
    """Configuration for document processing"""
    # GPU settings
    use_gpu: str = 'cpu'  # 'auto', 'cuda', 'cpu' - Set to 'cpu' to avoid GPU heap corruption issues post-reboot

    # Chunking settings
    chunk_max_tokens: int = 2500
    tokenizer_model: str = 'gpt-4o'
    merge_peers: bool = True

    # Feature toggles
    enable_tables: bool = True
    enable_images: bool = False

    # Translation settings (NEW)
    translate_to_english: bool = False
    translation_provider: str = 'google'  # 'google', 'libretranslate'

    # Output settings
    output_json: bool = True
    output_markdown: bool = False

    verbose: bool = False


# ============================================================================
# DOCX to PDF Conversion
# ============================================================================

def convert_docx_to_pdf(docx_path: Path, verbose: bool = False) -> Path:
    """
    Convert DOCX file to PDF.
    DOCX files don't have pages, so we convert to PDF first to get page numbers.

    Args:
        docx_path: Path to DOCX file
        verbose: Print progress information

    Returns:
        Path to converted PDF file (in temp directory)
    """
    try:
        from docling.document_converter import DocumentConverter, DocxFormatOption
        from docling.datamodel.base_models import InputFormat
    except ImportError:
        print("✗ Error: docling package required for DOCX conversion")
        print("  Install with: pip install docling")
        sys.exit(1)

    if verbose:
        print(f"  Converting DOCX to PDF...")

    try:
        # Create converter for DOCX
        converter = DocumentConverter(
            format_options={
                InputFormat.DOCX: DocxFormatOption()
            }
        )

        # Convert DOCX to Docling document
        conv_result = converter.convert(str(docx_path))
        doc = conv_result.document

        # Create temporary PDF file
        temp_dir = Path(tempfile.gettempdir())
        pdf_path = temp_dir / f"{docx_path.stem}_converted.pdf"

        # Export to PDF
        with open(pdf_path, 'wb') as f:
            pdf_data = doc.export_to_pdf()
            f.write(pdf_data)

        if verbose:
            print(f"  ✓ DOCX converted to temporary PDF: {pdf_path.name}")

        return pdf_path

    except Exception as e:
        print(f"✗ Error converting DOCX to PDF: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# ============================================================================
# GPU Configuration
# ============================================================================

def create_gpu_converter(config: ProcessingConfig):
    """Create DocumentConverter with GPU settings"""
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions

    if config.verbose:
        print(f"  Configuring GPU mode: {config.use_gpu}")

    # Determine device
    if config.use_gpu == 'auto':
        device = "auto"
        device_name = "AUTO (will detect GPU)"
    elif config.use_gpu == 'cuda':
        device = "cuda"
        device_name = "CUDA (GPU)"
        # Verify CUDA is available
        try:
            import torch
            if not torch.cuda.is_available():
                print("  ⚠ WARNING: CUDA requested but not available. Falling back to CPU.")
                device = "cpu"
                device_name = "CPU (CUDA unavailable)"
        except ImportError:
            pass
    else:  # cpu
        device = "cpu"
        device_name = "CPU"

    if config.verbose:
        print(f"  Device: {device_name}")

    # Create accelerator options
    accelerator_options = AcceleratorOptions(
        device=device,
        num_threads=8
    )

    # Create pipeline options
    pipeline_options = PdfPipelineOptions(
        accelerator_options=accelerator_options,
        do_ocr=False,  # Skip OCR for speed
        do_table_structure=config.enable_tables
    )

    # Create converter with GPU-enabled pipeline
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    return converter


# ============================================================================
# HybridChunker Setup
# ============================================================================

def create_hybrid_chunker(config: ProcessingConfig):
    """Create HybridChunker with token-aware configuration"""
    try:
        from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
        from docling_core.transforms.chunker.tokenizer.openai import OpenAITokenizer
        import tiktoken
    except ImportError as e:
        print(f"✗ Missing required package for HybridChunker: {e}")
        print(f"  Install with: pip install 'docling-core[chunking-openai]' tiktoken")
        sys.exit(1)

    if config.verbose:
        print(f"  Initializing HybridChunker")
        print(f"    Max tokens: {config.chunk_max_tokens}")
        print(f"    Tokenizer: {config.tokenizer_model}")
        print(f"    Merge peers: {config.merge_peers}")

    try:
        # Get tiktoken encoding
        encoding = tiktoken.encoding_for_model(config.tokenizer_model)

        # Create OpenAI tokenizer with required parameters
        tokenizer = OpenAITokenizer(
            tokenizer=encoding,  # Changed: use 'tokenizer' parameter instead of 'encoding'
            max_tokens=config.chunk_max_tokens
        )

        # Create chunker
        chunker = HybridChunker(
            tokenizer=tokenizer,
            merge_peers=config.merge_peers
        )

        if config.verbose:
            print(f"  ✓ HybridChunker initialized successfully")

        return chunker, tokenizer
    except Exception as e:
        print(f"✗ Error initializing HybridChunker: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# ============================================================================
# Document Translation
# ============================================================================

def detect_language(text: str) -> Optional[str]:
    """
    Detect language of text using simple heuristics.
    Returns language code or None if English.

    Args:
        text: Text to detect language

    Returns:
        Language code (e.g., 'es', 'fr', 'id') or None if likely English
    """
    try:
        from langdetect import detect, DetectorFactory
        DetectorFactory.seed = 0
        lang = detect(text[:1000])  # Use first 1000 chars for detection
        return lang if lang != 'en' else None
    except:
        # Fallback: simple heuristic - check if English words dominate
        return None


def translate_text_to_english(text: str, provider: str = 'google', verbose: bool = False) -> Tuple[str, Optional[str]]:
    """
    Translate text to English if not already in English.

    Args:
        text: Text to translate
        provider: Translation provider ('google' or 'libretranslate')
        verbose: Print progress information

    Returns:
        Tuple of (translated_text, source_language_code)
        Returns (original_text, None) if already English or translation fails
    """
    # Detect source language
    source_lang = detect_language(text)

    if source_lang is None:
        # Already English or detection failed
        return text, None

    if verbose:
        print(f"    Translating from detected language: {source_lang}")

    try:
        if provider == 'google':
            return _translate_with_google(text, source_lang, verbose)
        elif provider == 'libretranslate':
            return _translate_with_libretranslate(text, source_lang, verbose)
        else:
            if verbose:
                print(f"    ⚠ Unknown translation provider: {provider}. Skipping translation.")
            return text, source_lang
    except Exception as e:
        if verbose:
            print(f"    ⚠ Translation failed: {e}. Using original text.")
        return text, source_lang


def _translate_with_google(text: str, source_lang: str, verbose: bool = False) -> Tuple[str, str]:
    """Translate using Google Translate API"""
    try:
        from google.cloud import translate_v2
    except ImportError:
        # Try alternative: google-generativeai
        try:
            import google.generativeai as genai
            from src.config import get_google_api_key

            api_key = get_google_api_key()
            if not api_key:
                raise Exception("GOOGLE_API_KEY not found")

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"Translate the following text from {source_lang} to English. Return ONLY the translated text, no explanations:\n\n{text[:2000]}"
            response = model.generate_content(prompt)
            translated = response.text

            if verbose:
                print(f"    ✓ Translated {len(text)} chars with Google Gemini API")
            return translated, source_lang
        except ImportError:
            raise Exception("Neither 'google-cloud-translate' nor 'google-generativeai' installed. Install with: pip install google-generativeai")

    # If google-cloud-translate is available
    try:
        client = translate_v2.Client()
        result = client.translate_text(
            source_language=source_lang,
            target_language='en',
            values=[text[:5000]]  # Google API has limits
        )
        translated = result[0]['translatedText']

        if verbose:
            print(f"    ✓ Translated {len(text)} chars with Google Cloud Translate")
        return translated, source_lang
    except Exception as e:
        raise Exception(f"Google Cloud Translate failed: {e}")


def _translate_with_libretranslate(text: str, source_lang: str, verbose: bool = False) -> Tuple[str, str]:
    """Translate using LibreTranslate API (free, self-hosted or public)"""
    try:
        import requests
    except ImportError:
        raise Exception("'requests' package required. Install with: pip install requests")

    try:
        # Try public LibreTranslate API (or use --libretranslate-url for self-hosted)
        url = "https://libretranslate.de/translate"
        payload = {
            "q": text[:5000],  # API has limits
            "source": source_lang,
            "target": "en",
            "format": "text"
        }

        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        translated = result.get('translatedText', text)

        if verbose:
            print(f"    ✓ Translated {len(text)} chars with LibreTranslate")
        return translated, source_lang
    except Exception as e:
        raise Exception(f"LibreTranslate failed: {e}")


def translate_docling_document(doc, config: ProcessingConfig, verbose: bool = False):
    """
    Translate Docling document text to English.
    Modifies document in-place if possible, or returns translated markdown.

    Args:
        doc: Docling Document object (from converter.convert())
        config: ProcessingConfig with translation settings
        verbose: Print progress information

    Returns:
        doc: Modified document (or original if translation disabled/failed)
        dict: Translation metadata {'source_language': code, 'translated': bool, ...}
    """
    translation_metadata = {
        'source_language': None,
        'translated': False,
        'provider': config.translation_provider,
        'error': None
    }

    if not config.translate_to_english:
        return doc, translation_metadata

    if verbose:
        print(f"  Translating document text to English...")

    try:
        # Export full document as markdown
        markdown_text = doc.export_to_markdown()

        # Detect language
        source_lang = detect_language(markdown_text)
        translation_metadata['source_language'] = source_lang

        if source_lang is None:
            if verbose:
                print(f"    Document appears to be in English. Skipping translation.")
            return doc, translation_metadata

        # Translate the markdown
        translated_markdown, detected_lang = translate_text_to_english(
            markdown_text,
            provider=config.translation_provider,
            verbose=verbose
        )

        if translated_markdown != markdown_text:
            if verbose:
                print(f"  ✓ Translation complete ({len(markdown_text)} → {len(translated_markdown)} chars)")
            translation_metadata['translated'] = True
            translation_metadata['source_language'] = detected_lang

            # NOTE: We return the original doc object but flag it for re-parsing
            # The actual document content will be updated via chunk text during extraction
            return doc, translation_metadata
        else:
            if verbose:
                print(f"    Translation returned same text. Using original.")
            return doc, translation_metadata

    except Exception as e:
        if verbose:
            print(f"  ⚠ Translation failed: {e}")
        translation_metadata['error'] = str(e)
        return doc, translation_metadata


# ============================================================================
# Chunk Extraction
# ============================================================================

def extract_chunks_with_pages(doc, chunker, tokenizer, verbose: bool = False, translated_text: Optional[str] = None) -> Iterator[DocumentChunk]:
    """
    Extract chunks using HybridChunker with real page numbers (Generator)

    Args:
        doc: Docling document
        chunker: HybridChunker instance
        tokenizer: OpenAI tokenizer
        verbose: Print progress
        translated_text: Optional translated markdown text (if translation occurred)
    """
    if verbose:
        print(f"  Extracting chunks with HybridChunker...")

    # Create iterator with optional tqdm progress bar
    chunk_iterator = chunker.chunk(doc)
    if verbose:
        chunk_iterator = tqdm(chunk_iterator, desc="    Processing chunks", unit=" chunk")

    for i, chunk in enumerate(chunk_iterator):
        # Extract page number from doc_items provenance
        # Each item in doc_items has provenance with page_no
        page_num = 1
        if chunk.meta.doc_items:
            # Get page from first item's provenance
            first_item = chunk.meta.doc_items[0]
            if hasattr(first_item, 'prov') and first_item.prov:
                page_num = first_item.prov[0].page_no

        # Extract section heading
        headings = chunk.meta.headings or []
        section = headings[0] if headings else None

        # Get exact token count
        try:
            token_count = len(tokenizer.encode(chunk.text))
        except:
            # Fallback: estimate tokens
            token_count = len(chunk.text.split())

        yield DocumentChunk(
            chunk_id=i,
            page=page_num,
            section=section,
            text=chunk.text,
            token_count=token_count,
            metadata={
                'headings': chunk.meta.headings or [],
                'captions': chunk.meta.captions or [],
                'doc_items_count': len(chunk.meta.doc_items) if chunk.meta.doc_items else 0,
                'origin': chunk.meta.origin.model_dump() if chunk.meta.origin else None
            }
        )


# ============================================================================
# Table Extraction
# ============================================================================

def extract_tables_with_pages(doc, verbose: bool = False) -> List[TableData]:
    """Extract tables with real page numbers from provenance"""
    try:
        from docling_core.types.doc import TableItem
    except ImportError:
        return []

    tables = []

    if verbose:
        print(f"  Extracting tables with page tracking...")

    # Create list of items with optional progress bar
    items = list(doc.iterate_items())
    if verbose:
        items_iter = tqdm(items, desc="    Processing items", unit=" item", disable=False)
    else:
        items_iter = items

    for item, level in items_iter:
        if isinstance(item, TableItem):
            # Get page from provenance
            page_num = item.prov[0].page_no if item.prov else 1

            # Export table to markdown
            try:
                table_md = item.export_to_markdown()
            except:
                table_md = str(item)

            tables.append(TableData(
                table_id=len(tables),
                page=page_num,
                position=f"table_{len(tables)}_page_{page_num}",
                content=table_md,
                caption=getattr(item, 'caption', None),
                metadata={
                    'bbox': item.prov[0].bbox.__dict__ if item.prov and item.prov[0].bbox else None
                }
            ))

    if verbose:
        print(f"  ✓ Extracted {len(tables)} tables")

    return tables


# ============================================================================
# Image Extraction
# ============================================================================

def extract_images_with_pages(doc, verbose: bool = False) -> List[ImageData]:
    """Extract images with real page numbers from provenance"""
    try:
        from docling_core.types.doc import PictureItem
    except ImportError:
        return []

    images = []

    if verbose:
        print(f"  Extracting images with page tracking...")

    # Create list of items with optional progress bar
    items = list(doc.iterate_items())
    if verbose:
        items_iter = tqdm(items, desc="    Processing items", unit=" item", disable=False)
    else:
        items_iter = items

    for item, level in items_iter:
        if isinstance(item, PictureItem):
            # Get page from provenance
            page_num = item.prov[0].page_no if item.prov else 1

            images.append(ImageData(
                image_id=len(images),
                page=page_num,
                position=f"image_{len(images)}_page_{page_num}",
                filename=f"image_{page_num}_{len(images)}.png",
                description=getattr(item, 'caption', None),
                metadata={
                    'bbox': item.prov[0].bbox.__dict__ if item.prov and item.prov[0].bbox else None
                }
            ))

    if verbose:
        print(f"  ✓ Extracted {len(images)} images")

    return images


# ============================================================================
# Statistics
# ============================================================================

def calculate_statistics(chunk_stats: Dict, tables: List[TableData], images: List[ImageData]) -> Dict:
    """Calculate processing statistics"""
    return {
        'total_chunks': chunk_stats['count'],
        'total_tables': len(tables),
        'total_images': len(images),
        'avg_tokens_per_chunk': chunk_stats['total_tokens'] / chunk_stats['count'] if chunk_stats['count'] else 0,
        'min_tokens_per_chunk': chunk_stats['min_tokens'],
        'max_tokens_per_chunk': chunk_stats['max_tokens'],
        'total_tokens': chunk_stats['total_tokens'],
        'pages_with_chunks': len(chunk_stats['pages']),
        'processing_timestamp': datetime.now().isoformat()
    }


# ============================================================================
# Main Processing
# ============================================================================

def process_document(
    input_path: Path,
    output_dir: Path,
    config: ProcessingConfig
) -> Tuple[Dict, Optional[Path]]:
    """
    Process PDF or DOCX with hybrid chunking and page tracking.
    Streams chunks to JSONL file to handle large documents.

    If input is DOCX, converts to PDF first (DOCX doesn't have pages).

    Args:
        input_path: Path to PDF or DOCX file
        output_dir: Directory for output files
        config: Processing configuration

    Returns:
        Tuple of (metadata dictionary, optional temporary PDF path if converted)
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Check if input is DOCX and convert to PDF if needed
    temp_pdf_path = None
    if input_path.suffix.lower() == '.docx':
        if config.verbose:
            print(f"\n{'='*80}")
            print(f"DOCX DETECTED - CONVERTING TO PDF")
            print(f"{'='*80}")
        temp_pdf_path = convert_docx_to_pdf(input_path, config.verbose)
        pdf_path = temp_pdf_path
        original_filename = input_path.name
    else:
        pdf_path = input_path
        original_filename = input_path.name

    if config.verbose:
        print(f"\n{'='*80}")
        print(f"DOCLING HYBRID CHUNKING (STREAMING MODE)")
        print(f"{'='*80}")
        print(f"\nInput: {original_filename}")
        print(f"Output: {output_dir}")

    # Step 1: Create converter with GPU support
    if config.verbose:
        print(f"\n[1/5] Creating DocumentConverter...")
    converter = create_gpu_converter(config)

    # Step 2: Convert document
    if config.verbose:
        print(f"\n[2/5] Converting PDF to Docling document...")
    try:
        conv_result = converter.convert(str(pdf_path))
        doc = conv_result.document
        if config.verbose:
            print(f"  ✓ Document converted")
            print(f"  Pages: {len(doc.pages)}")
    except Exception as e:
        print(f"✗ Error converting document: {e}")
        sys.exit(1)

    # Note: Translation will happen AFTER chunk extraction (line 760-762)
    # This preserves page number accuracy from Docling's provenance
    translation_metadata = {
        'source_language': None,
        'translated': False,
        'provider': config.translation_provider,
        'error': None
    }

    # Step 3: Setup HybridChunker
    if config.verbose:
        print(f"\n[3/5] Setting up HybridChunker...")
    chunker, tokenizer = create_hybrid_chunker(config)

    # Step 4: Extract chunks with page tracking (Streaming)
    if config.verbose:
        print(f"\n[4/5] Extracting chunks to JSONL...")
    
    jsonl_path = output_dir / f"{pdf_path.stem}_chunks.jsonl"
    
    chunk_stats = {
        'count': 0,
        'total_tokens': 0,
        'min_tokens': float('inf'),
        'max_tokens': 0,
        'pages': set()
    }

    try:
        # PHASE 1: Extract chunks and write original JSONL only
        # Translation (if enabled) happens in Phase 2 after this file is complete
        total_pages = len(doc.pages)
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            chunk_gen = extract_chunks_with_pages(doc, chunker, tokenizer, config.verbose)

            for chunk in chunk_gen:
                # Create chunk with original text (no translation yet)
                chunk_original = DocumentChunk(
                    chunk_id=chunk.chunk_id,
                    page=chunk.page,
                    section=chunk.section,
                    text=chunk.text,  # Original text
                    token_count=chunk.token_count,
                    metadata=chunk.metadata
                )

                # Write to original JSONL (always)
                f.write(json.dumps(chunk_original.to_dict(), ensure_ascii=False) + '\n')

                # Output progress every 10 chunks (so frontend can track progress)
                chunk_stats['count'] += 1
                if chunk_stats['count'] % 10 == 0:
                    # Print progress in a format the pipeline executor regex can parse
                    print(f"[PROGRESS] Page {chunk_original.page} of {total_pages}", flush=True)

                # Update stats
                chunk_stats['total_tokens'] += chunk_original.token_count
                chunk_stats['min_tokens'] = min(chunk_stats['min_tokens'], chunk_original.token_count)
                chunk_stats['max_tokens'] = max(chunk_stats['max_tokens'], chunk_original.token_count)
                chunk_stats['pages'].add(chunk_original.page)

        if chunk_stats['count'] == 0:
            chunk_stats['min_tokens'] = 0

        if config.verbose:
            print(f"  ✓ Streamed {chunk_stats['count']} chunks to {jsonl_path.name}")

    except Exception as e:
        print(f"✗ Error streaming chunks: {e}")
        sys.exit(1)

    # Step 5: Extract tables and images
    if config.verbose:
        print(f"\n[5/5] Extracting tables and images...")
    tables = extract_tables_with_pages(doc, config.verbose) if config.enable_tables else []
    images = extract_images_with_pages(doc, config.verbose) if config.enable_images else []

    # Build metadata structure
    metadata = {
        'document': {
            'original_filename': original_filename,
            'processed_filename': pdf_path.name,
            'filepath': str(pdf_path),
            'total_pages': len(doc.pages),
            'format': 'pdf',
            'converted_from_docx': temp_pdf_path is not None,
            'processed_at': datetime.now().isoformat(),
            'translation': translation_metadata  # Include translation metadata
        },
        'files': {
            'chunks': jsonl_path.name,
            'format': 'jsonl'
        },
        'tables': [table.to_dict() for table in tables],
        'images': [img.to_dict() for img in images],
        'statistics': calculate_statistics(chunk_stats, tables, images)
    }

    # Export markdown if requested
    if config.output_markdown:
        if config.verbose:
            print(f"\n[Export] Exporting markdown...")
        markdown = doc.export_to_markdown()
        md_path = output_dir / f"{input_path.stem}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        if config.verbose:
            print(f"  ✓ Markdown: {md_path}")

    # PHASE 2: Post-JSONL Translation (if enabled)
    # Translate the COMPLETE JSONL file AFTER original is written
    # This ensures absolute certainty that page numbers are preserved
    if config.translate_to_english:
        translation_metadata = translate_jsonl_to_english(
            jsonl_path,
            output_dir,
            config,
            verbose=config.verbose
        )
    else:
        translation_metadata = {
            'source_language': None,
            'translated': False,
            'provider': None,
            'error': None
        }

    return metadata, temp_pdf_path


def translate_jsonl_to_english(
    original_jsonl_path: Path,
    output_dir: Path,
    config: ProcessingConfig,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Translate a complete JSONL chunks file from original language to English.

    This function provides ABSOLUTE CERTAINTY for page number preservation by:
    1. Reading the complete, finalized JSONL file (all chunks already written)
    2. Detecting language from first chunk
    3. Translating ONLY the text field of each chunk
    4. Preserving ALL other fields exactly (page, section, metadata, chunk_id, token_count)
    5. Writing English JSONL with identical structure and page numbers

    Why Post-JSONL Translation:
    - Original JSONL is 100% complete before any translation starts
    - Page numbers from Docling provenance are never touched
    - Clear temporal separation of concerns (parsing vs translation)
    - Easy verification that both files have identical page numbers
    - Simpler debugging if page numbers ever become an issue

    Args:
        original_jsonl_path: Path to original chunks JSONL file (already complete)
        output_dir: Directory for output files
        config: ProcessingConfig with translation_provider setting
        verbose: Print progress messages

    Returns:
        Translation metadata dict with:
            - source_language: Detected language code (e.g., 'id', 'es', 'fr')
            - translated: True if translation succeeded, False otherwise
            - provider: Translation provider used ('google', 'libretranslate')
            - error: Error message if translation failed, None otherwise
            - chunks_translated: Number of chunks successfully translated
            - english_jsonl_path: Path to English JSONL file (if created)

    Example:
        >>> translation_meta = translate_jsonl_to_english(
        ...     Path("output/document_chunks.jsonl"),
        ...     Path("output"),
        ...     config,
        ...     verbose=True
        ... )
        >>> print(f"Translated {translation_meta['chunks_translated']} chunks")
    """
    translation_metadata = {
        'source_language': None,
        'translated': False,
        'provider': config.translation_provider,
        'error': None,
        'chunks_translated': 0,
        'english_jsonl_path': None
    }

    # Derive English JSONL path from original
    # Example: document_chunks.jsonl -> document_chunks_english.jsonl
    english_jsonl_path = Path(str(original_jsonl_path).replace('_chunks.jsonl', '_chunks_english.jsonl'))

    if verbose:
        print(f"\n[POST-TRANSLATION] Translating chunks to English...")
        print(f"  Input:  {original_jsonl_path.name}")
        print(f"  Output: {english_jsonl_path.name}")

    try:
        chunks = []

        # PHASE 2.1: Read original JSONL completely into memory
        if verbose:
            print(f"  [2.1/3] Loading original chunks from {original_jsonl_path.name}...")

        with open(original_jsonl_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                try:
                    chunk_dict = json.loads(line.strip())
                    chunks.append(chunk_dict)
                except json.JSONDecodeError as e:
                    if verbose:
                        print(f"    ⚠ Skipping malformed chunk at line {line_num}: {e}")
                    continue

        if len(chunks) == 0:
            if verbose:
                print(f"    ⚠ No chunks found in {original_jsonl_path.name}, skipping translation")
            return translation_metadata

        if verbose:
            print(f"    ✓ Loaded {len(chunks)} chunks")

        # PHASE 2.2: Detect language from first chunk
        if verbose:
            print(f"  [2.2/3] Detecting source language...")

        first_chunk_text = chunks[0].get('text', '')
        if not first_chunk_text:
            if verbose:
                print(f"    ⚠ First chunk has no text, skipping translation")
            return translation_metadata

        source_lang = detect_language(first_chunk_text)
        translation_metadata['source_language'] = source_lang

        if source_lang is None:
            # Already English or detection failed
            if verbose:
                print(f"    ✓ Detected: English (or detection failed) - no translation needed")
            return translation_metadata

        if verbose:
            print(f"    ✓ Detected: {source_lang}")

        # PHASE 2.3: Translate chunks and write English JSONL
        if verbose:
            print(f"  [2.3/3] Translating {len(chunks)} chunks to English...")
            print(f"    Provider: {config.translation_provider}")

        translated_count = 0
        error_count = 0

        with open(english_jsonl_path, 'w', encoding='utf-8') as f_english:
            for chunk_idx, chunk_dict in enumerate(chunks):
                try:
                    # Extract text field to translate
                    original_text = chunk_dict.get('text', '')

                    if not original_text:
                        # Empty chunk, write as-is
                        f_english.write(json.dumps(chunk_dict, ensure_ascii=False) + '\n')
                        continue

                    # Translate text field using existing function
                    translated_text, _ = translate_text_to_english(
                        original_text,
                        provider=config.translation_provider,
                        verbose=False  # Don't log each chunk individually
                    )

                    # Create translated chunk with SAME structure
                    # CRITICAL: All fields preserved except text
                    chunk_translated = {
                        **chunk_dict,  # Spread all original fields (page, section, metadata, etc.)
                        'text': translated_text  # ONLY replace text field
                    }

                    # Verify page number preserved (sanity check)
                    assert chunk_translated.get('page') == chunk_dict.get('page'), \
                        f"Page number changed during translation! Original: {chunk_dict.get('page')}, Translated: {chunk_translated.get('page')}"

                    # Write to English JSONL (preserve order, structure, metadata)
                    f_english.write(json.dumps(chunk_translated, ensure_ascii=False) + '\n')

                    translated_count += 1

                    # Progress update every 10 chunks
                    if verbose and chunk_idx > 0 and chunk_idx % 10 == 0:
                        print(f"    ... {chunk_idx}/{len(chunks)} chunks translated")

                except Exception as e:
                    error_count += 1
                    if verbose:
                        print(f"    ⚠ Translation failed for chunk {chunk_idx} (page {chunk_dict.get('page', '?')}): {e}")

                    # Write original chunk on error (preserve file completeness)
                    f_english.write(json.dumps(chunk_dict, ensure_ascii=False) + '\n')

                    if translation_metadata['error'] is None:
                        translation_metadata['error'] = f"Translation failed for {error_count} chunk(s)"

        # Mark translation successful
        translation_metadata['translated'] = True
        translation_metadata['chunks_translated'] = translated_count
        translation_metadata['english_jsonl_path'] = str(english_jsonl_path)

        if verbose:
            print(f"    ✓ Successfully translated {translated_count}/{len(chunks)} chunks")
            if error_count > 0:
                print(f"    ⚠ {error_count} chunks failed translation (original text preserved)")
            print(f"    ✓ English JSONL: {english_jsonl_path.name}")

    except FileNotFoundError as e:
        translation_metadata['error'] = f"Original JSONL file not found: {original_jsonl_path}"
        if verbose:
            print(f"    ✗ Error: {translation_metadata['error']}")

    except Exception as e:
        translation_metadata['error'] = f"Post-JSONL translation failed: {str(e)}"
        if verbose:
            print(f"    ✗ Error: {translation_metadata['error']}")

    return translation_metadata


# ============================================================================
# CLI
# ============================================================================

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Process PDF or DOCX with Docling HybridChunker and export to JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python step1_docling_hybrid_chunking.py document.pdf
  python step1_docling_hybrid_chunking.py document.docx
  python step1_docling_hybrid_chunking.py document.pdf --gpu-mode cuda
  python step1_docling_hybrid_chunking.py document.docx --chunk-max-tokens 3000 --enable-images
  python step1_docling_hybrid_chunking.py document.docx --output-markdown --verbose
        """
    )

    # Positional arguments
    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to PDF or DOCX file"
    )

    # Output options
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        default=Path("../data/outputs"),
        help="Output directory (default: ../data/outputs)"
    )

    # GPU options
    parser.add_argument(
        "--gpu-mode",
        choices=['auto', 'cuda', 'cpu'],
        default='auto',
        help="GPU mode: auto (detect), cuda (force GPU), cpu (force CPU) (default: auto)"
    )

    # Chunking options
    parser.add_argument(
        "--chunk-max-tokens",
        type=int,
        default=2500,
        help="Maximum tokens per chunk (default: 2500)"
    )

    parser.add_argument(
        "--tokenizer-model",
        default='gpt-4o',
        help="Tokenizer model for tiktoken (default: gpt-4o)"
    )

    parser.add_argument(
        "--no-merge-peers",
        action="store_true",
        help="Disable merging of small chunks with same metadata"
    )

    # Feature toggles
    parser.add_argument(
        "--enable-images",
        action="store_true",
        help="Extract images with page numbers (default: disabled)"
    )

    parser.add_argument(
        "--disable-tables",
        action="store_true",
        help="Disable table extraction (default: enabled)"
    )

    # Translation options (NEW)
    parser.add_argument(
        "--translate-to-english",
        action="store_true",
        help="Translate non-English document text to English before chunking (default: disabled)"
    )

    parser.add_argument(
        "--translation-provider",
        choices=['google', 'libretranslate'],
        default='google',
        help="Translation service provider: google (uses Google Gemini API) or libretranslate (free, open-source) (default: google)"
    )

    # Output options
    parser.add_argument(
        "--output-markdown",
        action="store_true",
        help="Also export markdown file"
    )

    parser.add_argument(
        "--no-json",
        action="store_true",
        help="Disable JSON output"
    )

    # Logging
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    # Validate input
    if not args.input_path.exists():
        print(f"✗ Error: Input file not found: {args.input_path}")
        sys.exit(1)

    # Validate file format
    valid_formats = ['.pdf', '.docx']
    if args.input_path.suffix.lower() not in valid_formats:
        print(f"✗ Error: Invalid file format. Supported formats: {', '.join(valid_formats)}")
        sys.exit(1)

    # Build config
    config = ProcessingConfig(
        use_gpu=args.gpu_mode,
        chunk_max_tokens=args.chunk_max_tokens,
        tokenizer_model=args.tokenizer_model,
        merge_peers=not args.no_merge_peers,
        enable_tables=not args.disable_tables,
        enable_images=args.enable_images,
        translate_to_english=args.translate_to_english,
        translation_provider=args.translation_provider,
        output_json=not args.no_json,
        output_markdown=args.output_markdown,
        verbose=args.verbose
    )

    # Process document
    temp_pdf_path = None
    try:
        result, temp_pdf_path = process_document(args.input_path, args.output_dir, config)
    except Exception as e:
        print(f"\n✗ Error processing document: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        # Clean up temporary PDF if it was created
        if temp_pdf_path and temp_pdf_path.exists():
            try:
                temp_pdf_path.unlink()
                if args.verbose:
                    print(f"\n  ✓ Cleaned up temporary PDF")
            except:
                pass

    # Export Metadata
    if config.output_json:
        meta_path = args.output_dir / f"{args.input_path.stem}_meta.json"
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Metadata exported: {meta_path}")
        print(f"✓ Original chunks: {result['files']['chunks']}")
        if config.translate_to_english:
            english_chunks_file = f"{args.input_path.stem}_chunks_english.jsonl"
            print(f"✓ English chunks:  {english_chunks_file}")

    # Print summary
    stats = result['statistics']
    print(f"\n{'='*80}")
    print(f"PROCESSING SUMMARY")
    print(f"{'='*80}")
    print(f"Document:        {result['document']['original_filename']}")
    print(f"Pages:           {result['document']['total_pages']}")
    print(f"Chunks:          {stats['total_chunks']}")
    print(f"Tables:          {stats['total_tables']}")
    print(f"Images:          {stats['total_images']}")
    print(f"Avg Tokens/Chunk:{stats['avg_tokens_per_chunk']:.0f}")
    print(f"Total Tokens:    {stats['total_tokens']:,}")
    print(f"Pages w/ Chunks: {stats['pages_with_chunks']}")
    print(f"\n✓ Processing complete!")
    print(f"{'='*80}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
