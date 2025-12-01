# Pipeline Directory Refactoring

## Overview
The ESIA pipeline has been refactored to use simplified folder structure for better file management and clearer separation of concerns.

## Changes Made

### Directory Structure

**Before:**
```
data/
├── pdfs/          (uploaded PDFs)
├── outputs/       (pipeline outputs)
├── metadata/      (execution metadata)
└── ...other folders
```

**After:**
```
data/
├── pdf/           (uploaded PDFs)
└── output/        (ALL pipeline outputs and metadata)
    ├── metadata/  (execution metadata)
    └── ...pipeline results
```

## File Changes

### 1. **server.js** (server.js:14-18, 78, 123)
- Changed upload directory from `./data/pdfs` to `./data/pdf`
- Updated file serving route from `/data/pdfs` to `/data/pdf`
- Updated response path from `/data/pdfs/{filename}` to `/data/pdf/{filename}`

### 2. **pipeline.config.js** (pipeline.config.js:42, 45, 34)
- Changed output directory from `./data/outputs` to `./data/output`
- Changed metadata directory from `./data/metadata` to `./data/output/metadata`
- Updated comment references from `data/pdfs/` to `data/pdf/`

### 3. **pipelineExecutor.js**
- No direct changes needed - automatically uses `pipelineConfig.outputDir`
- All pipeline outputs now go to the unified `./data/output` directory

## Benefits

1. **Simplified Structure** - Single `pdf` folder for uploads, single `output` folder for all results
2. **Unified Output** - All pipeline outputs (chunks, facts, analysis) in one place
3. **Metadata Colocated** - Execution metadata lives in the output folder
4. **Easier Cleanup** - Can delete entire output folder to reset pipeline state
5. **Better Organization** - Clear separation: `pdf` = input, `output` = results

## Notes

- Old directories (`data/pdfs`, `data/outputs`) still exist for backward compatibility
- New directories (`data/pdf`, `data/output`) are automatically created if missing
- Pipeline now uploads to `./data/pdf/{timestamp}-{filename}.pdf`
- All outputs are saved to `./data/output/`
- Metadata is stored in `./data/output/metadata/`

## How It Works

1. User uploads PDF → stored in `./data/pdf/`
2. Pipeline processes PDF → outputs to `./data/output/`
3. Frontend can access results from `./data/output/` directory
4. Metadata from execution is stored in `./data/output/metadata/`

## Future Improvements

- [ ] Add cleanup script to remove old outputs
- [ ] Implement output file compression
- [ ] Add dashboard to view available outputs
- [ ] Implement result archiving to external storage
