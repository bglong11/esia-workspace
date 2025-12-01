# ESIA Pipeline - Integrated CLI System

A professional, production-ready CLI application for automated ESIA document processing and analysis.

## Overview

The ESIA Pipeline orchestrates three integrated components into a seamless workflow:

1. **Fact Extraction**: Converts PDF/DOCX to structured facts using archetype-based extraction
2. **Output Sync**: Transfers extraction results to analysis component
3. **Quality Analysis**: Analyzes facts for consistency, compliance, and completeness

## Features

✅ **Professional CLI Interface** - Full argument parsing, help text, version info
✅ **Flexible Execution** - Run all steps or specific steps as needed
✅ **Structured Logging** - Debug, info, and error levels with timestamps
✅ **Configuration Management** - Environment variables and .env file support
✅ **Error Handling** - Validation, graceful failures, clear error messages
✅ **Multiple Outputs** - Interactive HTML dashboard and Excel workbook
✅ **Batch Processing Ready** - Designed for automation and integration
✅ **Backward Compatible** - Existing functionality preserved

## Quick Start

### 1. Setup
```bash
# Install dependencies
cd esia-fact-extractor-pipeline
pip install -r requirements.txt
cd ..

# Configure API keys
echo "GOOGLE_API_KEY=your_key" > .env
echo "OPENROUTER_API_KEY=your_key" >> .env
```

### 2. Run
```bash
# Full pipeline
python run-esia-pipeline.py

# Or specific steps
python run-esia-pipeline.py --steps 1,3 --verbose
```

### 3. View Results
```bash
# Open HTML dashboard
open esia-fact-analyzer/data/html/*.html

# Or check Excel file
ls esia-fact-analyzer/data/*.xlsx
```

## CLI Usage

### Basic Commands

```bash
# Run all steps (default)
python run-esia-pipeline.py

# Run specific steps
python run-esia-pipeline.py --steps 1          # Extract only
python run-esia-pipeline.py --steps 1,3        # Extract and analyze
python run-esia-pipeline.py --steps 3          # Analyze only

# With verbose logging
python run-esia-pipeline.py --verbose
python run-esia-pipeline.py --steps 1 -v       # Short form

# Custom document name
python run-esia-pipeline.py --pdf-stem "My_Document"

# Show version
python run-esia-pipeline.py --version

# Show help
python run-esia-pipeline.py --help
```

### Arguments

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `--steps` | - | str | `1,2,3` | Steps to run (1=extract, 2=sync, 3=analyze) |
| `--pdf-stem` | - | str | `ESIA_Report_Final_Elang AMNT` | Document filename stem |
| `--verbose` | `-v` | flag | false | Enable debug logging |
| `--version` | - | flag | - | Show version and exit |
| `--help` | `-h` | flag | - | Show help and exit |

## Configuration

### Environment Variables

Create a `.env` file in project root:

```env
# API Keys (required for extraction)
GOOGLE_API_KEY=your_google_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Pipeline Settings (optional)
PDF_STEM=ESIA_Report_Final_Elang AMNT
VERBOSE=false
```

### Create Sample Config

```bash
python -c "from config import Config; Config.create_sample_env('sample.env')"
```

## Pipeline Steps

### Step 1: Extract Facts
- Parses PDF/DOCX using Docling
- Chunks document semantically
- Maps sections to 50+ domain archetypes
- Extracts facts using DSPy signatures
- **Output**: chunks.jsonl, meta.json, facts_with_archetypes.json
- **Time**: 5-15 minutes

### Step 2: Sync Outputs
- Creates analyzer input directory
- Copies extraction outputs to analyzer
- Validates file integrity
- **Output**: Files in analyzer's input directory
- **Time**: <1 second

### Step 3: Analyze
- Checks consistency (finds contradictions)
- Validates units (detects mixed units)
- Checks compliance (vs IFC/World Bank standards)
- Analyzes gaps (finds missing content)
- **Output**: HTML dashboard, Excel workbook
- **Time**: 2-5 minutes

## Project Structure

```
esia-pipeline/
├── run-esia-pipeline.py              # Main CLI entry point
├── config.py                         # Configuration management
├── .env                              # Configuration file (create this)
│
├── README_INTEGRATION.md             # This file
├── CLI_USAGE.md                      # Comprehensive usage guide
├── QUICKSTART.md                     # 60-second setup
├── INTEGRATION_SUMMARY.md            # Architecture overview
│
├── esia-fact-extractor-pipeline/     # Component 1: Extraction
│   ├── step3_extraction_with_archetypes.py
│   ├── src/                          # Source modules
│   └── data/
│       ├── archetypes/               # 50+ domain definitions
│       └── hybrid_chunks_output/     # Extraction outputs
│
└── esia-fact-analyzer/               # Component 2: Analysis
    ├── analyze_esia_v2.py
    ├── esia_analyzer/                # Analysis modules
    └── data/
        ├── hybrid_chunks_output/     # Sync destination
        └── html/                     # HTML outputs
```

## Common Workflows

### Workflow 1: Process New Document
```bash
# 1. Place PDF in appropriate directory
cp ~/Downloads/my_esia.pdf data/pdfs/

# 2. Run full pipeline with custom name
python run-esia-pipeline.py --pdf-stem "Project_XYZ_ESIA"

# 3. View results
open esia-fact-analyzer/data/html/Project_XYZ_ESIA_review.html
```

### Workflow 2: Debug Extraction Issues
```bash
python run-esia-pipeline.py --steps 1 --verbose

# Check outputs
ls esia-fact-extractor-pipeline/hybrid_chunks_output/
```

### Workflow 3: Reanalyze Without Extraction
```bash
# After extraction, tweak analyzer settings and rerun
python run-esia-pipeline.py --steps 3 --verbose
```

### Workflow 4: Batch Process Multiple Documents
```bash
#!/bin/bash
for doc in ProjectA ProjectB ProjectC; do
    echo "Processing $doc..."
    python run-esia-pipeline.py --pdf-stem "$doc"
    echo "Done: $doc"
done
```

### Workflow 5: Monitor in Background
```bash
nohup python run-esia-pipeline.py --verbose > pipeline.log 2>&1 &

# Check progress
tail -f pipeline.log
```

## Output Files

### Extraction Outputs
- `{STEM}_chunks.jsonl` - Document chunks with metadata
- `{STEM}_meta.json` - Document-level metadata
- `esia_facts_with_archetypes.json` - Extracted facts by domain

### Analysis Outputs
- `{STEM}_review.html` - Interactive dashboard
  - Consistency findings
  - Unit standardization checks
  - Compliance status
  - Gap analysis
  - Page references
- `{STEM}_review.xlsx` - Detailed Excel workbook
  - Multiple worksheets
  - Formatted data
  - Ready for reports

## Requirements

### System
- Python 3.8+
- 2-4 GB RAM
- 500 MB - 2 GB disk space
- Internet connection (for LLM API)

### Python Packages
```
# Extractor (install in component directory)
docling>=1.0.0
docling-core[chunking-openai]>=1.0.0
tiktoken>=0.5.0
torch>=2.0.0
tqdm>=4.65.0

# CLI & Config
(Python standard library + optional python-dotenv)

# Analyzer
(Python standard library only)
```

### API Keys
- Google Gemini API key (for extraction) OR
- OpenRouter API key (alternative)

## Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Startup | <1s | Validation, argument parsing |
| Extract (Step 1) | 5-15 min | Depends on document size, LLM API |
| Sync (Step 2) | <1s | File copy operation |
| Analyze (Step 3) | 2-5 min | Rule-based, no external calls |
| **Total** | **8-20 min** | For typical 50-100 page document |

## Error Handling

### Common Issues and Solutions

**Error: "Extractor directory not found"**
```bash
# Verify structure
ls -la esia-fact-extractor-pipeline/
ls -la esia-fact-analyzer/
```

**Error: "Expected extractor output not found"**
```bash
# Run extraction with debug output
python run-esia-pipeline.py --steps 1 --verbose
```

**Error: "Analyzer failed"**
```bash
# Run analyzer directly
cd esia-fact-analyzer
python analyze_esia_v2.py --verbose
```

**No output files generated**
```bash
# Check output directories exist
ls -la esia-fact-extractor-pipeline/hybrid_chunks_output/
ls -la esia-fact-analyzer/data/html/
```

See `CLI_USAGE.md` for more troubleshooting.

## Documentation

### Files
- **QUICKSTART.md** - 60-second setup guide
- **CLI_USAGE.md** - Complete usage documentation with examples
- **INTEGRATION_SUMMARY.md** - Architecture and integration details
- **README_INTEGRATION.md** - This file

### Access Help
```bash
python run-esia-pipeline.py --help
cat QUICKSTART.md
cat CLI_USAGE.md
```

## Advanced Usage

### Programmatic Integration
```python
import subprocess
import sys

# Run pipeline
result = subprocess.run(
    [sys.executable, "run-esia-pipeline.py", "--steps", "1,3"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("Pipeline succeeded")
else:
    print("Pipeline failed:", result.stderr)
```

### Custom Logging
```python
from run_esia_pipeline import setup_logging, run_pipeline

logger = setup_logging(verbose=True)
run_pipeline([1, 2, 3], logger)
```

### Configuration Programmatically
```python
from config import Config
from pathlib import Path

config = Config()
api_keys = config.get_api_keys()
pipeline_config = config.get_pipeline_config()
```

## Contributing & Extending

### Adding New Features
1. Core CLI logic: `run-esia-pipeline.py`
2. Configuration: `config.py`
3. Component integration: Sync mechanisms in Step 2
4. Documentation: Update relevant markdown files

### Testing
```bash
# Test CLI arguments
python run-esia-pipeline.py --help
python run-esia-pipeline.py --version

# Test specific steps
python run-esia-pipeline.py --steps 1
python run-esia-pipeline.py --steps 3

# Test configuration
python -c "from config import Config; Config().get_api_keys()"
```

## Roadmap

### Current (v1.0)
✅ CLI interface with argument parsing
✅ Logging system
✅ Configuration management
✅ Error handling and validation
✅ Documentation

### Planned
- Progress bars with tqdm
- Async/parallel step execution
- Webhook notifications
- Database persistence
- Web dashboard for monitoring
- Docker containerization
- Additional export formats

## License

See LICENSE file (if present)

## Support

### Getting Help
1. Run `python run-esia-pipeline.py --help`
2. Read `CLI_USAGE.md` for detailed documentation
3. Check `QUICKSTART.md` for common tasks
4. See troubleshooting section in `CLI_USAGE.md`

### Reporting Issues
Include:
1. Full command used
2. Output with `--verbose` flag
3. Python version: `python --version`
4. Error messages and traceback
5. Document name and approximate size

## Version History

**v1.0** (Current)
- Initial CLI refactoring
- Configuration management
- Professional logging
- Comprehensive documentation

## Contact

For issues, questions, or contributions:
1. Check documentation first
2. Review error messages with `--verbose` flag
3. Verify configuration with `cat .env`
4. Test individual steps with `--steps` argument

---

## Getting Started

### Quick Link
```bash
# 1. Setup (30 seconds)
pip install -r esia-fact-extractor-pipeline/requirements.txt
echo "GOOGLE_API_KEY=your_key" > .env

# 2. Run (1 click)
python run-esia-pipeline.py

# 3. View results (open in browser)
open esia-fact-analyzer/data/html/*.html
```

### Next Steps
- Read `QUICKSTART.md` for immediate setup
- Read `CLI_USAGE.md` for comprehensive guide
- Run `python run-esia-pipeline.py --help` for command reference

---

**Created**: 2025
**Status**: Production Ready
**Maintained**: Active

For detailed usage: `cat CLI_USAGE.md` | For quick setup: `cat QUICKSTART.md`
