# ESIA Fact Extractor

> Automated extraction of quantitative and categorical facts from Environmental and Social Impact Assessment (ESIA) documents using DSPy and Ollama.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🤖 **LLM-Powered Extraction** - Uses DSPy with multiple LLM providers (Ollama, OpenAI, Claude, Gemini)
- 📊 **Structured Output** - Generates 4 CSV files: all facts, consolidated facts, replacement plan, project factsheet
- 🏗️ **LLM-Based Categorization** - Uses DSPy to intelligently organize facts into 8 logical project sections
- ⚡ **Smart Caching** - Reduces LLM API calls by 37-80% through intelligent fact deduplication
- 🔄 **Unit Normalization** - Supports 80+ units with automatic conversion
- 🎯 **Conflict Detection** - Identifies inconsistencies across document mentions
- 💾 **Checkpoint/Resume** - Auto-saves every 5 chunks, resume after interruptions
- 📈 **Progress Tracking** - Real-time progress bar with cache statistics and ETA
- 🔌 **Multi-LLM Support** - Switch providers with one config change (Ollama, OpenAI, Claude, Gemini)

## Quick Start

### Prerequisites

1. **Ollama** with Qwen2.5:7B-Instruct
   ```bash
   ollama pull qwen2.5:7b-instruct
   ollama serve
   ```

2. **Python Dependencies**
   ```bash
   pip install dspy-ai pandas tqdm
   ```

### Basic Usage

```bash
python esia_extractor.py document.md ./output
```

### Example Output

```
================================================================================
ESIA Fact Extraction Pipeline
================================================================================

[1/7] Configuring Claude 3 via Anthropic...
[2/7] Loading markdown from document.md...
  Loaded 99276 characters

[3/7] Chunking text...
  Created 25 chunks

[4/7] Extracting facts from chunks...
Processing chunks:  100%|██████████| 25/25 [15:32<00:00, 37.30s/chunk]

  Extracted 108 total facts

[5/9] Clustering facts by signature...
  Found 107 unique fact signatures

[6/9] Categorizing facts by project section...
  Categorizing:  100%|██████████| 107/107 [02:15<00:00, 1.26 facts/s]
  Categorized 107 unique facts
  Cache: 42/107 hits (39.3%)
  Confidence: 89 high, 16 medium, 2 low

[7/9] Generating output tables...

[8/9] Generating factsheet...
  Organized into 8 categories:
    - Project Overview: 12 facts
    - Project Description: 18 facts
    - Environmental Impacts: 34 facts
    - Social Impacts: 16 facts
    - Economic Impacts: 8 facts
    - Health & Safety: 12 facts
    - Governance & Management: 5 facts
    - Risks & Issues: 2 facts

[9/9] Saving CSV files...
  [OK] output/esia_mentions.csv
  [OK] output/esia_consolidated.csv
  [OK] output/esia_replacement_plan.csv
  [OK] output/project_factsheet.csv

================================================================================
SUMMARY
================================================================================
Total facts extracted: 108
Unique signatures: 107
Conflicts detected: 0

================================================================================
Pipeline complete!
================================================================================
```

## Output Files

### 1. esia_mentions.csv
All fact occurrences with context:
- `signature`: Canonical fact identifier
- `name`: Original fact name
- `value_normalized`: Value in canonical units
- `unit_normalized`: Canonical unit
- `evidence`: Source text quote
- `page`: Page/chunk number

### 2. esia_consolidated.csv
One row per unique fact:
- `signature`: Fact identifier
- `occurrences`: Number of mentions
- `min_value`, `max_value`: Range of values
- `has_conflict`: Boolean conflict flag
- `conflict_description`: Details if conflicting

### 3. esia_replacement_plan.csv
Document editing instructions:
- `signature`: Fact identifier
- `regex_patterns`: Patterns to find occurrences
- `replacement_rule`: Editing instructions

### 4. project_factsheet.csv
Facts organized by project section (LLM-categorized):
- `category`: Primary category (8 categories: Project Overview, Project Description, Environmental Impacts, Social Impacts, Economic Impacts, Health & Safety, Governance & Management, Risks & Issues)
- `subcategory`: Specific subcategory (32 total subcategories)
- `fact_name`: Fact title
- `value`: Fact value
- `unit`: Unit of measurement
- `occurrences`: Number of mentions
- `has_conflict`: Boolean conflict flag
- `confidence`: Categorization confidence (high/medium/low)
- `rationale`: Brief explanation of categorization
- `signature`: Unique fact identifier

This file is ideal for creating project factsheets suitable for ESIA client deliverables.

## Advanced Features

### Resume After Interruption

If extraction is interrupted (Ctrl+C, crash, etc.), just re-run:
```bash
python esia_extractor.py document.md ./output
# Prompted: Resume from checkpoint? (y/n): y
```

### Supported Units (80+)

**Mass**: kg, t, Mt, g, mg
**Area**: ha, km², m², acres
**Power**: MW, kW, GW
**Energy**: MWh, GWh, kWh
**Volume**: L, mL, m³
**Flow**: m³/s, L/s, ML/d
**Concentration**: mg/L, ppm, ppb, µg/L
**Temperature**: °C, degC
**Pressure**: kPa, MPa, bar
**Chemistry**: pH, %S

[See full list](esia_extractor.py#L73-L180)

### Add Custom Units

Edit `esia_extractor.py`:
```python
UNIT_CONVERSIONS = {
    'your_unit': ('canonical_unit', conversion_factor),
    # Example:
    'gal': ('L', 3.78541),
}
```

## Documentation

- **[Quick Reference](QUICK_REFERENCE.md)** - One-page command reference
- **[Resume Guide](RESUME_GUIDE.md)** - Checkpoint/resume details
- **[Full Documentation](README_ESIA.md)** - Complete system docs
- **[Quick Start](QUICKSTART.md)** - Getting started guide
- **[Improvements](IMPROVEMENTS_SUMMARY.md)** - What's new

## Architecture

```
Input: ESIA Markdown
        ↓
    Chunking (4000 chars)
        ↓
    LLM Extraction (Qwen2.5:7B)
        ↓
    Unit Normalization
        ↓
    Fact Clustering
        ↓
    Conflict Detection
        ↓
    CSV Outputs

## Automation and Verification

- **Step 3: Analysis & Checklist** – After running `step2_extract_facts.py`, execute `python step3_analyze_facts.py <output_dir>` to have DSPy consolidate the `esia_mentions.csv` data and produce `verification_report.md` (analysis + prioritized verification checklist). This makes the entire pipeline end-to-end, so reviewers can jump directly to a single report rather than digging through CSVs.

- **Requirements File** – Install `pip install -r requirements.txt` in a venv before using the pipeline; the file bundles the Docling/DSPy stack plus pandas, tqdm, dotenv, onnxruntime, and rapidocr to ensure both extraction and analysis steps have the libraries they need.

## One-step Pipeline

Use `run_data_pipeline.py` to run the entire workflow (doc conversion → extraction → analysis/report) with a single command. Provide the PDF path plus the LLM provider/model you want to use:

```
python run_data_pipeline.py your_test.pdf --provider openai --model gpt-4o-mini
```

The script internally calls `step1_pdf_to_markdown.py`, `step2_extract_facts.py`, and `step3_analyze_facts.py`, creates the markdown and output directories, and leaves the verification checklist (`verification_report.md`) plus all CSVs in `output_<pdf_stem>` (or an optional `--output-dir` you specify). This is ideal for end-to-end automation or CI workflows.
```

## Performance

| Document Size | Chunks | Estimated Time |
|--------------|--------|----------------|
| 50 KB | ~12 | 1-3 minutes |
| 100 KB | ~25 | 3-6 minutes |
| 200 KB | ~50 | 6-15 minutes |
| 500 KB | ~125 | 15-35 minutes |

*Times vary based on hardware and Ollama configuration*

## Configuration

### Chunk Size
```python
chunks = chunk_markdown(text, max_chars=4000)
```

### Checkpoint Frequency
```python
if (i + 1) % 5 == 0:  # Every 5 chunks
    save_checkpoint(...)
```

### Conflict Threshold
```python
def detect_conflicts(cluster, tolerance=0.02):  # 2% tolerance
```

## Example Use Cases

- Environmental impact assessments
- Social impact reports
- Engineering project reports
- Mining feasibility studies
- Infrastructure ESIAs
- Any technical document with quantitative data

## Technology Stack

- **DSPy** - LLM orchestration framework
- **Ollama** - Local LLM runtime
- **Qwen2.5:7B-Instruct** - Fact extraction model
- **Pandas** - Data processing
- **tqdm** - Progress bars

## Troubleshooting

### "Connection refused"
```bash
ollama serve
```

### "Model not found"
```bash
ollama pull qwen2.5:7b-instruct
```

### "No progress bar"
```bash
pip install tqdm
```

### Checkpoint corrupted
```bash
rm output/.checkpoint.pkl
```

## Contributing

Contributions welcome! Areas for improvement:
- Add more unit types
- Improve JSON parsing robustness
- Add PDF input support
- Parallel chunk processing
- Web UI

## License

MIT License - See [LICENSE](LICENSE) file

## Citation

If you use this in research, please cite:
```bibtex
@software{esia_extractor,
  title = {ESIA Fact Extractor},
  year = {2025},
  url = {https://github.com/yourusername/esia-extractor}
}
```

## Acknowledgments

- Built with [DSPy](https://github.com/stanfordnlp/dspy)
- Powered by [Ollama](https://ollama.ai)
- Uses [Qwen2.5](https://huggingface.co/Qwen) models

## Support

- 📖 [Documentation](README_ESIA.md)
- 💬 [Issues](https://github.com/yourusername/esia-extractor/issues)
- ⭐ Star this repo if you find it useful!

---

**Built with ❤️ for environmental and social impact professionals**
