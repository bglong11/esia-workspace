# ESIA Pipeline Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    ESIA PIPELINE CLI SYSTEM                     │
│                    (run-esia-pipeline.py)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Argument    │  │ Config Mgmt  │  │   Logging    │          │
│  │   Parsing    │  │  (config.py) │  │    System    │          │
│  │  (argparse)  │  └──────────────┘  │              │          │
│  └──────────────┘                     └──────────────┘          │
│         │                                     │                 │
│         └─────────────────┬───────────────────┘                 │
│                           │                                     │
│           ┌───────────────▼───────────────┐                     │
│           │  Unified Error Handling       │                     │
│           │  & Validation                 │                     │
│           └───────────────┬───────────────┘                     │
│                           │                                     │
│           ┌───────────────▼────────────────────┐                │
│           │  Pipeline Orchestration Logic      │                │
│           │  (run_pipeline function)           │                │
│           └───────────────┬────────────────────┘                │
│                           │                                     │
│        ┌──────────────────┼──────────────────┐                  │
│        │                  │                  │                  │
│   ┌────▼─────┐       ┌────▼─────┐      ┌────▼─────┐           │
│   │ Step 1   │       │ Step 2   │      │ Step 3   │           │
│   │ Extract  │       │  Sync    │      │ Analyze  │           │
│   └────┬─────┘       └────┬─────┘      └────┬─────┘           │
│        │                  │                  │                  │
└────────┼──────────────────┼──────────────────┼──────────────────┘
         │                  │                  │
         │                  │                  │
     ┌───▼─────────┐   ┌────▼──────┐   ┌──────▼────────┐
     │  EXTRACTOR  │   │    SYNC   │   │   ANALYZER    │
     │ COMPONENT   │──▶│ COMPONENT │──▶│  COMPONENT    │
     └─────────────┘   └───────────┘   └───────────────┘
```

## Detailed Component Architecture

### CLI Layer (run-esia-pipeline.py)

```
main()
  │
  ├─ parse_arguments()
  │   └─ Returns: args (Namespace with --steps, --pdf-stem, --verbose, etc.)
  │
  ├─ setup_logging(verbose)
  │   └─ Returns: logger (configured Logger instance)
  │
  ├─ validate_directories(logger)
  │   ├─ Checks: EXTRACTOR_DIR exists
  │   ├─ Checks: ANALYZER_DIR exists
  │   └─ Raises: FileNotFoundError if missing
  │
  ├─ validate_steps(steps_str)
  │   ├─ Parses: "1,2,3" → [1, 2, 3]
  │   ├─ Validates: All steps in {1, 2, 3}
  │   └─ Returns: Sorted list of steps
  │
  └─ run_pipeline(steps, logger)
      │
      ├─ IF 1 in steps: run_extractor(logger)
      │   ├─ Executes: subprocess.run(...step3_extraction_with_archetypes.py...)
      │   ├─ Logs: Progress at each stage
      │   └─ Returns: Chunks + metadata files
      │
      ├─ IF 2 in steps: sync_outputs_to_analyzer(logger)
      │   ├─ Creates: ANALYZER_INPUT_DIR
      │   ├─ Validates: Output files exist
      │   ├─ Copies: chunks.jsonl, meta.json
      │   └─ Returns: Files copied successfully
      │
      └─ IF 3 in steps: run_analyzer(logger)
          ├─ Executes: subprocess.run(...analyze_esia_v2.py...)
          ├─ Logs: Progress at each stage
          └─ Returns: HTML + Excel outputs
```

### Configuration Layer (config.py)

```
Config Class
  │
  ├─ __init__(config_dir=None)
  │   └─ Initializes and loads configuration
  │
  ├─ _load_config()
  │   ├─ Attempts: from dotenv import load_dotenv
  │   └─ Fallback: _load_env_file()
  │
  ├─ _load_env_file()
  │   ├─ Reads: .env file line by line
  │   ├─ Parses: KEY=VALUE format
  │   └─ Sets: os.environ variables
  │
  ├─ get(key, default=None)
  │   └─ Returns: os.environ.get(key, default)
  │
  ├─ get_pipeline_config()
  │   └─ Returns: Dict with extractor_dir, analyzer_dir, etc.
  │
  ├─ get_api_keys()
  │   └─ Returns: Dict with google_api_key, openrouter_api_key
  │
  ├─ validate_required_keys()
  │   └─ Returns: bool (True if at least one API key present)
  │
  └─ create_sample_env(output_path)
      └─ Writes: Sample .env file with all configuration options
```

### Logging Layer

```
Logger Setup
  │
  ├─ Handler: StreamHandler (stdout)
  ├─ Format: "%(asctime)s - %(levelname)s - %(message)s"
  ├─ Level: DEBUG (if --verbose) or INFO (default)
  │
  └─ Log Levels:
      ├─ DEBUG: Directory checks, file operations, detailed flow
      ├─ INFO: Step progress, status updates, summaries
      └─ ERROR: Failures, missing files, validation errors
```

### Data Flow Architecture

```
STEP 1: EXTRACTION
═════════════════
Input:
  └─ PDF/DOCX file from extractor's data directory

Process:
  ├─ step3_extraction_with_archetypes.py
  ├─ ArchetypeMapper (50+ domains)
  ├─ ESIAExtractor (40+ signatures)
  └─ DSPy LLM calls

Output:
  ├─ {STEM}_chunks.jsonl
  ├─ {STEM}_meta.json
  └─ esia_facts_with_archetypes.json


STEP 2: SYNCHRONIZATION
═══════════════════════
Input:
  ├─ EXTRACTOR_OUTPUT_DIR
  └─ ├─ {STEM}_chunks.jsonl
    └─ {STEM}_meta.json

Process:
  ├─ Create ANALYZER_INPUT_DIR
  ├─ Validate source files exist
  └─ Copy files with shutil.copy2()

Output:
  └─ ANALYZER_INPUT_DIR
      ├─ {STEM}_chunks.jsonl
      └─ {STEM}_meta.json


STEP 3: ANALYSIS
════════════════
Input:
  └─ ANALYZER_INPUT_DIR
      ├─ {STEM}_chunks.jsonl
      └─ {STEM}_meta.json

Process:
  ├─ ESIAReviewer.load_data()
  ├─ ESIAReviewer.categorize_facts()
  ├─ ESIAReviewer.check_consistency()
  ├─ ESIAReviewer.check_unit_standardization()
  ├─ ESIAReviewer.check_thresholds()
  ├─ ESIAReviewer.analyze_gaps()
  ├─ ESIAReviewer.export_html()
  └─ ESIAReviewer.export_excel()

Output:
  ├─ {STEM}_review.html
  └─ {STEM}_review.xlsx
```

## File Structure with Relationships

```
esia-pipeline/
│
├── run-esia-pipeline.py (MAIN CLI ENTRY POINT)
│   ├─ Imports: argparse, logging, subprocess, config
│   ├─ Defines: main(), parse_arguments(), setup_logging()
│   ├─ Orchestrates: run_extractor(), sync_outputs(), run_analyzer()
│   └─ Logs: All pipeline execution
│
├── config.py (CONFIGURATION MANAGEMENT)
│   ├─ Class: Config
│   ├─ Loads: .env files, environment variables
│   ├─ Provides: get(), get_pipeline_config(), get_api_keys()
│   └─ Imports: os, Path, dotenv (optional)
│
├── .env (CONFIGURATION FILE - CREATE THIS)
│   ├─ GOOGLE_API_KEY=...
│   ├─ OPENROUTER_API_KEY=...
│   └─ PDF_STEM=...
│
├── DOCUMENTATION/
│   ├── QUICKSTART.md (60-second setup)
│   ├── CLI_USAGE.md (complete guide)
│   ├── INTEGRATION_SUMMARY.md (architecture)
│   ├── README_INTEGRATION.md (main readme)
│   ├── ARCHITECTURE.md (this file)
│   └── IMPLEMENTATION_CHECKLIST.md (what was done)
│
├── esia-fact-extractor-pipeline/
│   ├── step3_extraction_with_archetypes.py (STEP 1 ENTRY)
│   │   ├─ Calls: ArchetypeMapper, ESIAExtractor
│   │   └─ Output: chunks.jsonl, meta.json
│   ├── src/
│   │   ├── esia_extractor.py (main extractor)
│   │   ├── archetype_mapper.py (domain mapping)
│   │   ├── generated_signatures.py (40+ signatures)
│   │   ├── llm_manager.py (LLM provider)
│   │   └── ... (other modules)
│   ├── data/
│   │   ├── archetypes/ (50+ domain definitions)
│   │   └── hybrid_chunks_output/ (extraction output)
│   └── requirements.txt (dependencies)
│
├── esia-fact-analyzer/
│   ├── analyze_esia_v2.py (STEP 3 ENTRY)
│   │   └─ Calls: ESIAReviewer.run_analysis()
│   ├── esia_analyzer/
│   │   ├── reviewer.py (main orchestrator)
│   │   ├── consistency.py (consistency checking)
│   │   ├── extraction.py (value extraction)
│   │   ├── thresholds.py (compliance checking)
│   │   ├── gaps.py (gap analysis)
│   │   ├── units.py (unit conversion)
│   │   ├── constants.py (reference data)
│   │   ├── cli.py (command interface)
│   │   └── exporters/ (HTML, Excel output)
│   └── data/
│       ├── hybrid_chunks_output/ (sync input)
│       └── html/ (analysis output)
│
└── data/ (optional shared data)
    ├── pdfs/ (input documents)
    └── extracted/ (backup extractions)
```

## Execution Flow Diagram

```
┌─────────────────────────────────┐
│  User runs CLI                  │
│  python run-esia-pipeline.py    │
└──────────────┬──────────────────┘
               │
      ┌────────▼─────────┐
      │ Parse Arguments  │
      │ (--steps, -v)    │
      └────────┬─────────┘
               │
      ┌────────▼──────────────────┐
      │ Setup Logging             │
      │ (INFO or DEBUG level)     │
      └────────┬──────────────────┘
               │
      ┌────────▼──────────────────┐
      │ Validate Directories      │
      │ (Check components exist)  │
      └────────┬──────────────────┘
               │
      ┌────────▼──────────────────┐
      │ Validate Steps            │
      │ (Parse, sort, validate)   │
      └────────┬──────────────────┘
               │
      ┌────────▼──────────────────┐
      │ run_pipeline()            │
      └────────┬──────────────────┘
               │
        ┌──────┴──────────────────────────────┐
        │                                     │
    ┌───▼───┐                            ┌───▼────┐
    │IF 1   │                            │IF 2    │
    │       │                            │        │
    │Step 1:│                            │Step 2: │
    │Extract│                            │Sync    │
    └───┬───┘                            └───┬────┘
        │                                    │
    ┌───▼────────────────────────┐   ┌──────▼──────────────┐
    │ subprocess.run(             │   │ Create input dir   │
    │   step3_extraction_...      │   │ Validate files     │
    │   cwd=EXTRACTOR_DIR         │   │ Copy files         │
    │ )                           │   └──────┬─────────────┘
    │                             │         │
    │ Output:                     │  ┌──────▼──────────────┐
    │ - chunks.jsonl              │  │IF 3                │
    │ - meta.json                 │  │                    │
    │                             │  │Step 3:             │
    └─────────────────────────────┘  │Analyze             │
                                     └──────┬─────────────┘
                                            │
                                   ┌────────▼────────────┐
                                   │ subprocess.run(     │
                                   │   analyze_esia_v2   │
                                   │   cwd=ANALYZER_DIR  │
                                   │ )                   │
                                   │                     │
                                   │ Output:             │
                                   │ - review.html       │
                                   │ - review.xlsx       │
                                   └────────┬────────────┘
                                            │
                                   ┌────────▼────────────┐
                                   │ Log Summary         │
                                   │ Report Success      │
                                   └────────┬────────────┘
                                            │
                                   ┌────────▼────────────┐
                                   │ Exit Code 0         │
                                   │ (Success)           │
                                   └─────────────────────┘
```

## Error Handling Flow

```
┌──────────────────────────────────┐
│ Pipeline Execution               │
└────────────┬─────────────────────┘
             │
        ┌────▼─────────────┐
        │ Try Block        │
        │ Execute steps    │
        └────┬─────────────┘
             │
    ┌────────┴────────────┐
    │                     │
┌───▼──┐             ┌────▼──────────────┐
│Success│            │Exception Caught   │
│       │            │                   │
│Return │         ┌──▼────┐             │
│Code 0 │         │Type?  │             │
└───────┘         └─┬─────┘             │
                  ┌─┴────────┬──────┬────┘
                  │          │      │
            ┌─────▼───┐ ┌────▼──┐ ┌▼──────┐
            │FileNot  │ │Value  │ │KeyboardInterrupt
            │Found    │ │Error  │ │
            │Error    │ │       │ │
            └────┬────┘ └───┬───┘ └──┬────┘
                 │          │        │
            ┌────▼───┐ ┌────▼──┐ ┌──▼────┐
            │Log     │ │Log    │ │Log    │
            │Error   │ │Error  │ │Info   │
            │Message │ │Trace  │ │"Inter"│
            └────┬───┘ └───┬───┘ └──┬────┘
                 │         │        │
            ┌────▼─────────▼────────▼──┐
            │ Exit Code 1 or 130        │
            │ (Failure/Interrupt)       │
            └──────────────────────────┘
```

## Integration Points

### Data Integration
```
Extractor Output          Analyzer Input
─────────────────         ──────────────
chunks.jsonl  ────SYNC─▶  chunks.jsonl
meta.json     ────SYNC─▶  meta.json
```

### Component Integration
```
run-esia-pipeline.py (CLI Orchestrator)
         │
         ├─ Extractor Component (subprocess call)
         │   └─ Manages LLM interactions, archetype mapping
         │
         ├─ Sync Component (file operations)
         │   └─ Validates and transfers intermediate data
         │
         └─ Analyzer Component (subprocess call)
             └─ Performs rule-based analysis, generates reports
```

### Configuration Integration
```
.env File
   │
   └─ config.py
       └─ run-esia-pipeline.py
           └─ run_extractor() / run_analyzer()
```

## Technology Stack

```
Layer              Technology         Purpose
─────────────────────────────────────────────────────
CLI Interface      argparse            Argument parsing
Configuration      os, dotenv          Environment setup
Logging            logging             Structured output
Process Control    subprocess          Run components
Error Handling     Exception/Try-Catch Error management
Data Format        JSONL/JSON          Component communication
LLM (Extract)      Gemini/OpenRouter   Fact extraction
Analysis (Analyze) Rule-based          Quality checking
Output             HTML/Excel          Result presentation
```

## Performance Architecture

```
Latency Profile:
┌─────────────────────────────────────┐
│ Startup        │ <1 second          │
├─────────────────────────────────────┤
│ Argument Parse │ <100ms             │
├─────────────────────────────────────┤
│ Step 1 Extract │ 5-15 minutes       │
│ (LLM dependent)│                    │
├─────────────────────────────────────┤
│ Step 2 Sync    │ <1 second          │
├─────────────────────────────────────┤
│ Step 3 Analyze │ 2-5 minutes        │
│ (Rule-based)   │                    │
├─────────────────────────────────────┤
│ Total          │ 8-20 minutes       │
└─────────────────────────────────────┘

Throughput:
- Single document: ~1 per 8-20 minutes
- Batch processing: Multiple documents sequentially
- Scalability: Add more servers for parallelization
```

## Extensibility Points

```
To extend the pipeline:

1. Add new CLI arguments
   └─ Modify: parse_arguments() in run-esia-pipeline.py

2. Add new configuration options
   └─ Modify: config.py (Config class)

3. Add new pipeline steps
   └─ Create: new step function
   └─ Add: to run_pipeline() conditional

4. Change extraction behavior
   └─ Modify: EXTRACTOR_DIR command or args

5. Change analysis behavior
   └─ Modify: ANALYZER_DIR command or args

6. Add new output formats
   └─ Modify: Analyzer's exporter modules
```

---

For implementation details, see: **IMPLEMENTATION_CHECKLIST.md**

For usage guide, see: **CLI_USAGE.md**

For quick start, see: **QUICKSTART.md**
