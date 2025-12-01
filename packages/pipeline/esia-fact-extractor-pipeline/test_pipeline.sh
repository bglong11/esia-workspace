#!/bin/bash

# Test script for Post-JSONL Translation Pipeline
cd /m/GitHub/esia-fact-extractor-pipeline

echo "=========================================="
echo "Post-JSONL Translation Pipeline Test"
echo "=========================================="
echo ""
echo "Document: ESIA_Report_Final_Elang AMNT.pdf"
echo "Size: 7.3M, Pages: 458"
echo "Start time: $(date)"
echo ""

# Run pipeline without translation
echo "Phase 1 Test: Creating original JSONL..."
python step1_docling_hybrid_chunking.py \
  "data/inputs/pdfs/ESIA_Report_Final_Elang AMNT.pdf" \
  --verbose

echo ""
echo "Phase 1 Complete at: $(date)"
echo ""

# Check output
if [ -f "hybrid_chunks_output/ESIA_Report_Final_Elang AMNT_chunks.jsonl" ]; then
  echo "✓ Original JSONL created successfully"
  echo "  File: hybrid_chunks_output/ESIA_Report_Final_Elang AMNT_chunks.jsonl"
  echo "  Chunks: $(wc -l < 'hybrid_chunks_output/ESIA_Report_Final_Elang AMNT_chunks.jsonl')"

  # Show first chunk summary
  echo ""
  echo "First chunk summary:"
  jq 'limit(1; .[] | {chunk_id, page, section, text_length: (.text | length)})' \
    'hybrid_chunks_output/ESIA_Report_Final_Elang AMNT_chunks.jsonl'

  echo ""
  echo "Page numbers:"
  jq '.page' 'hybrid_chunks_output/ESIA_Report_Final_Elang AMNT_chunks.jsonl' | sort -u | head -10
else
  echo "✗ Original JSONL not created"
fi

echo ""
echo "Test complete at: $(date)"
