# Resume & Progress Bar Guide

## New Features Added

### 1. Progress Bar (tqdm)
Shows real-time progress when processing large ESIA documents.

### 2. Automatic Checkpointing
Saves progress every 5 chunks - never lose work from interruptions!

### 3. Resume Capability
Resume from where you left off after interruptions or errors.

---

## Installation

For progress bar support:
```bash
pip install tqdm
```

Without tqdm, the script still works but shows simpler progress output.

---

## Usage

### Normal Usage (with Auto-Resume)
```bash
python esia_extractor.py TL_IPP_ESIA.md ./output_tl
```

If interrupted, simply run the same command again - you'll be prompted to resume.

### Example Output with Progress Bar

```
================================================================================
ESIA Fact Extraction Pipeline
================================================================================

[1/7] Configuring Qwen2.5:7B-Instruct via Ollama...

[2/7] Loading markdown from TL_IPP_ESIA.md...
  Loaded 176002 characters

[3/7] Chunking text...
  Created 46 chunks

[4/7] Extracting facts from chunks...
Processing chunks:  22%|████▍              | 10/46 [02:15<08:05, 13.5s/chunk]
```

---

## Interruption & Resume

### Scenario 1: Manual Interruption (Ctrl+C)

```bash
# You're processing a large document
python esia_extractor.py large_esia.md ./output

# Press Ctrl+C to stop
^C
[INTERRUPTED] Saving checkpoint...
  Checkpoint saved. Resume by running the same command.
  Processed 15/46 chunks so far.
```

**To resume:**
```bash
# Run the exact same command
python esia_extractor.py large_esia.md ./output

# You'll see:
[RESUME] Found checkpoint with 245 facts from 15 chunks
         Last saved: 2025-10-24T20:15:30.123456
         Resume from checkpoint? (y/n): y
  Resuming from chunk 16/46
```

### Scenario 2: Unexpected Error

If the extraction crashes (network issue, memory error, etc.):
```bash
[ERROR] Connection timeout
  Saving checkpoint...
```

The checkpoint is automatically saved. Just re-run:
```bash
python esia_extractor.py large_esia.md ./output
```

### Scenario 3: Starting Fresh

If you want to start over (not resume):
```bash
# When prompted:
Resume from checkpoint? (y/n): n
         Starting fresh extraction...
```

Or manually delete the checkpoint:
```bash
# Windows
del output\.checkpoint.pkl

# Linux/Mac
rm output/.checkpoint.pkl
```

---

## Checkpoint Details

### What Gets Saved
- All facts extracted so far
- Number of chunks processed
- Timestamp of last save

### Save Frequency
Automatically saves every **5 chunks** (configurable in code).

### Checkpoint Location
`.checkpoint.pkl` in your output directory

Example:
```
output_tl/
├── .checkpoint.pkl          ← Hidden checkpoint file
├── esia_mentions.csv        ← Generated after completion
├── esia_consolidated.csv    ← Generated after completion
└── esia_replacement_plan.csv ← Generated after completion
```

### Automatic Cleanup
Checkpoint is automatically deleted when extraction completes successfully.

---

## Advanced Configuration

### Change Checkpoint Frequency

Edit `esia_extractor.py` line 626:
```python
# Save every 10 chunks instead of 5
if (i + 1) % 10 == 0:
    save_checkpoint(output_dir, all_facts, i + 1)
```

### Disable Auto-Resume

Modify the function call in code:
```python
process_esia_document(markdown_file, output_directory, resume=False)
```

---

## Performance Tips

### For Large Documents (100+ chunks)

1. **Use checkpointing** - Essential for very large documents
2. **Monitor progress** - Install tqdm for visual feedback
3. **Check Ollama performance**:
   ```bash
   # In another terminal
   ollama ps
   ```
4. **Reduce chunk size** if memory is an issue:
   ```python
   chunks = chunk_markdown(text, max_chars=2000)  # Smaller chunks
   ```

### Estimated Processing Times

| Document Size | Chunks | Estimated Time* |
|--------------|--------|----------------|
| 50 KB | 12 | 1-2 minutes |
| 100 KB | 25 | 2-5 minutes |
| 200 KB | 50 | 5-10 minutes |
| 500 KB | 125 | 15-30 minutes |

*Depends on Ollama performance and system specs

---

## Troubleshooting

### "Checkpoint file corrupted"
Delete `.checkpoint.pkl` and start fresh:
```bash
del output\.checkpoint.pkl
python esia_extractor.py document.md ./output
```

### "Can't save checkpoint - permission denied"
Ensure output directory is writable:
```bash
# Check permissions
ls -l output/  # Linux/Mac
dir output\    # Windows
```

### Progress bar not showing
Install tqdm:
```bash
pip install tqdm
```

### "Resume from checkpoint?" prompt doesn't appear
This means:
- No checkpoint file exists, OR
- Resume is disabled, OR
- Checkpoint is from a different document

---

## Example Workflow

### Processing a Large ESIA (46 chunks)

```bash
# Start extraction
PS F:\DSPY\learning> python esia_extractor.py TL_IPP_ESIA.md ./output_tl

[4/7] Extracting facts from chunks...
Processing chunks:  22%|████▍              | 10/46 [02:15<08:05, 13.5s/chunk]

# Internet drops... Press Ctrl+C
^C
[INTERRUPTED] Saving checkpoint...
  Processed 10/46 chunks so far.

# Fix internet, resume
PS F:\DSPY\learning> python esia_extractor.py TL_IPP_ESIA.md ./output_tl

[RESUME] Found checkpoint with 163 facts from 10 chunks
         Resume from checkpoint? (y/n): y

[4/7] Extracting facts from chunks...
Processing chunks: 100%|███████████████████| 36/36 [08:12<00:00, 13.7s/chunk]

  Extracted 682 total facts

[5/7] Clustering facts by signature...
  Found 342 unique fact signatures

[6/7] Generating output tables...

[7/7] Saving CSV files...
  [OK] output_tl\esia_mentions.csv
  [OK] output_tl\esia_consolidated.csv
  [OK] output_tl\esia_replacement_plan.csv

================================================================================
Pipeline complete!
================================================================================
```

---

## Benefits

✅ **Never lose progress** - Checkpoints every 5 chunks
✅ **Resume anytime** - From interruptions or errors
✅ **Visual feedback** - Progress bar shows time remaining
✅ **Automatic cleanup** - Checkpoints deleted on success
✅ **No manual intervention** - Works automatically

---

## Technical Details

### Checkpoint Format
Binary pickle file containing:
```python
{
    'facts': List[Fact],           # All extracted facts
    'processed_chunks': int,       # Number completed
    'timestamp': str               # ISO format datetime
}
```

### Error Handling
- KeyboardInterrupt (Ctrl+C) → Save and exit cleanly
- Exceptions → Save checkpoint then re-raise
- Successful completion → Delete checkpoint

---

**Your ESIA extraction is now interruption-proof! 🚀**
