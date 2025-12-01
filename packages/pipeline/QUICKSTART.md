# ESIA Pipeline - Quick Start Guide

## 60-Second Setup

### 1. Install Dependencies
```bash
# Install extractor dependencies
cd esia-fact-extractor-pipeline
pip install -r requirements.txt

# Back to root
cd ..
```

### 2. Create Configuration
```bash
# Create .env file with your API keys
cat > .env << EOF
GOOGLE_API_KEY=your_google_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
PDF_STEM=ESIA_Report_Final_Elang AMNT
VERBOSE=false
EOF
```

### 3. Run Pipeline
```bash
python run-esia-pipeline.py
```

Done! The pipeline will:
1. Extract facts from your PDF
2. Sync outputs to the analyzer
3. Generate HTML dashboard and Excel report

## Common Commands

### Full Pipeline
```bash
python run-esia-pipeline.py
```

### Extract Only
```bash
python run-esia-pipeline.py --steps 1
```

### Analyze Only (reuse previous extraction)
```bash
python run-esia-pipeline.py --steps 3
```

### With Verbose Output
```bash
python run-esia-pipeline.py --verbose
```

### Custom Document
```bash
python run-esia-pipeline.py --pdf-stem "My_Document_Name"
```

### Show Help
```bash
python run-esia-pipeline.py --help
```

## Output Locations

After running, you'll find:

### Extraction Results
```
esia-fact-extractor-pipeline/hybrid_chunks_output/
├── ESIA_Report_Final_Elang AMNT_chunks.jsonl
├── ESIA_Report_Final_Elang AMNT_meta.json
└── esia_facts_with_archetypes.json
```

### Analysis Results
```
esia-fact-analyzer/data/html/
└── ESIA_Report_Final_Elang_AMNT_review.html

esia-fact-analyzer/data/
└── ESIA_Report_Final_Elang_AMNT_review.xlsx
```

Open the HTML file in your browser for interactive dashboard!

## Troubleshooting

### Pipeline Not Found
```bash
# Verify you're in the right directory
pwd  # Should show: .../esia-pipeline

# Verify files exist
ls run-esia-pipeline.py
```

### API Key Error
```bash
# Add to .env file:
GOOGLE_API_KEY=your_key
# or
OPENROUTER_API_KEY=your_key
```

### Extraction Fails
```bash
# Debug extraction step
python run-esia-pipeline.py --steps 1 --verbose
```

### Analysis Fails
```bash
# Check if extraction output exists
ls esia-fact-extractor-pipeline/hybrid_chunks_output/

# Debug analysis step
python run-esia-pipeline.py --steps 3 --verbose
```

## Next Steps

1. **Read Full Documentation**: See `CLI_USAGE.md` for complete guide
2. **Understand Architecture**: See `INTEGRATION_SUMMARY.md` for detailed overview
3. **Process Your Document**: Place PDF in appropriate directory and run pipeline
4. **Review Results**: Open generated HTML dashboard in browser
5. **Export Findings**: Use Excel file for reports and further analysis

## Pipeline Architecture (Quick Reference)

```
PDF Input
   ↓
[STEP 1] Extract Facts
   ↓ outputs chunks.jsonl + meta.json
[STEP 2] Sync to Analyzer
   ↓ copies files
[STEP 3] Analyze & Report
   ↓ generates HTML + Excel
HTML Dashboard + Excel Report
```

## Performance

- **Total Time**: 8-20 minutes (depends on document size)
- **Extraction**: 5-15 minutes
- **Sync**: <1 second
- **Analysis**: 2-5 minutes

## Key Features

✅ Single Command Execution
✅ Selective Step Running
✅ Comprehensive Logging
✅ Configuration Management
✅ Error Handling
✅ Interactive HTML Output
✅ Excel Export
✅ Batch Processing Ready

## Support

**Help Command**:
```bash
python run-esia-pipeline.py --help
```

**Full Documentation**:
```bash
cat CLI_USAGE.md
cat INTEGRATION_SUMMARY.md
```

**Debug Mode**:
```bash
python run-esia-pipeline.py --verbose
```

---

**Ready to start?** Run: `python run-esia-pipeline.py`
