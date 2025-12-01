# Chunk Monitoring - Quick Start

## What Is It?

Real-time progress display that shows you what's happening during fact extraction, chunk by chunk.

## What You'll See

```
====================================================================================================
[CHUNK 1/50] Processing... (2.0%)
====================================================================================================

📄 Content Preview (3840 chars):
   The Environmental and Social Impact Assessment (ESIA) for the NATARBORA Project...

⏱️  Elapsed: 0s  |  ETA: 8m 45s

✅ Chunk 1 Complete
   • Time: 3.2s
   • Facts extracted: 5

📊 Progress Summary:
   • Total facts extracted: 5
   • Average time/chunk: 3.2s
   • Remaining chunks: 49
```

## How to Use

Just run normally - monitoring is automatic:

```bash
python run_data_pipeline.py "My Document.pdf"
```

That's it! You'll see detailed progress as each chunk is processed.

## What Each Section Shows

### Header
- **Chunk number**: Which chunk is being processed
- **Progress %**: How far through the document you are
- **Status**: "Processing..." while working

### Content Preview
- **First 150 chars** of the chunk
- Helps you understand what the extraction is looking at
- Shows document structure as it progresses

### Timing
- **Elapsed**: How long extraction has been running
- **ETA**: Estimated time to completion (gets more accurate as processing continues)

### Completion Info
- **Time**: How long this chunk took to process
- **Facts**: Number of facts extracted from this chunk
- **Errors**: Any errors encountered (0 = none)

### Progress Summary
- **Total facts**: How many facts extracted so far
- **Average time**: How long chunks typically take
- **Remaining**: How many chunks left to process

## Key Indicators

| Icon | Meaning |
|------|---------|
| ✅ | Chunk completed successfully |
| ❌ | Error occurred in chunk (continues with next) |
| 💾 | Checkpoint saved (every 5 chunks) |
| 📄 | Content preview of chunk |
| ⏱️ | Timing information |
| 📊 | Progress statistics |

## Examples

### Example 1: Small Document (10 chunks)

```
[CHUNK 1/10] Processing... (10.0%)
✅ Chunk 1 Complete - 5 facts extracted
[CHUNK 2/10] Processing... (20.0%)
✅ Chunk 2 Complete - 3 facts extracted
...
EXTRACTION COMPLETE - SUMMARY
• Total facts: 47
• Total time: 45s
• Average time/chunk: 4.5s
```

### Example 2: Medium Document (50 chunks)

```
[CHUNK 1/50] Processing... (2.0%)
⏱️ Elapsed: 0s | ETA: 8m 45s
✅ Chunk 1 Complete - 5 facts

[CHUNK 2/50] Processing... (4.0%)
⏱️ Elapsed: 3s | ETA: 8m 42s
✅ Chunk 2 Complete - 3 facts

[CHUNK 5/50] Processing... (10.0%)
💾 Checkpoint Saved - 23 facts total
...

EXTRACTION COMPLETE - SUMMARY
• Total chunks: 50
• Total facts: 247
• Total time: 2m 30s
• Average time/chunk: 3.0s
• Facts per second: 1.65
```

### Example 3: Resuming from Checkpoint

If you interrupted and resume:

```
[INFO] Found checkpoint - resuming from chunk 26
[CHUNK 26/100] Processing... (26.0%)
⏱️ Elapsed: 0s | ETA: 3m 45s (from chunk 26)
✅ Chunk 26 Complete - 4 facts

[CHUNK 27/100] Processing... (27.0%)
...

💾 Checkpoint Saved - 187 facts total (30 chunks done)

EXTRACTION COMPLETE - SUMMARY
• Total chunks: 100
• Total facts: 387 (187 from resume)
• Total time: 4m 15s
• Average time/chunk: 2.55s
```

## Understanding the Progress

### ETA Interpretation

- **ETA: calculating...** - Still processing first few chunks, estimate will appear soon
- **ETA: 5m 30s** - About 5.5 minutes remaining based on current speed
- **ETA: 2s** - Almost done!

**Note:** ETA is an estimate and may vary. Very large or complex chunks take longer.

### Facts Per Second

Shows extraction efficiency:
- **0.5 facts/sec** - Slower (large/complex chunks)
- **1-2 facts/sec** - Normal (typical documents)
- **2+ facts/sec** - Fast (small/simple chunks)

### Time Per Chunk

Shows processing speed:
- **2-4 seconds** - Fast extraction
- **4-8 seconds** - Normal speed
- **8+ seconds** - Slower (maybe complex content or LLM latency)

## Tips for Monitoring

### 1. Review Content Previews
The preview helps you understand what's being extracted:
```
📄 Content Preview: "Section 3: Environmental Impacts. Air quality...
```
This tells you the extraction is working through relevant sections.

### 2. Watch for Errors
If you see ❌, the extraction continues but that chunk may have failed:
```
❌ Chunk 15 Error
   Error: JSON parsing failed
```
Usually doesn't affect final results - the system continues.

### 3. Monitor ETA for Long Documents
For 200+ chunks, ETA helps you know how long to wait:
```
⏱️ Elapsed: 15m | ETA: 45m  (Total ~1 hour)
```

### 4. Check Final Statistics
The summary gives you quality metrics:
```
📊 Statistics:
   • Facts per second: 1.8
   • Average time/chunk: 3.0s
```
Slower = more complex extraction happening.

## Keyboard Shortcuts

During extraction:

| Key | Action |
|-----|--------|
| Ctrl+C | Pause and save checkpoint (resume later) |
| Ctrl+Z | Same as Ctrl+C (if on Windows) |

Interrupt anytime - your progress is saved!

## Common Questions

**Q: Why is ETA different than I expected?**
A: ETA is based on average of completed chunks. Early chunks may differ from later ones.

**Q: Can I pause the extraction?**
A: Yes! Press Ctrl+C. The extraction saves a checkpoint and you can resume later.

**Q: What if I see an error?**
A: Errors are logged but don't stop extraction. Check the final summary for success count.

**Q: Is monitoring slowing down extraction?**
A: No, monitoring has negligible performance impact (< 0.1% CPU).

**Q: Why is content preview sometimes short?**
A: Limited to first ~150 characters to keep display clean. Full chunk is being processed.

## Customization

### If You Want Less Output

The monitoring is automatic, but you can customize it. Edit `esia_extractor.py`:

```python
# Change this line (around 1089):
monitor = create_monitor(len(chunks), verbose=True, show_content=True)

# To minimal output:
monitor = create_monitor(len(chunks), verbose=False)
```

### If You Want More Detail

The default shows plenty of detail. For custom monitoring, see [CHUNK_MONITORING.md](CHUNK_MONITORING.md).

## File Size Reference

If you want to estimate extraction time:

| Document Size | Chunks | Est. Time | Notes |
|---|---|---|---|
| 10 KB | 3 | 10s | Very small |
| 50 KB | 12 | 45s | Small |
| 100 KB | 25 | 1m 45s | Medium |
| 200 KB | 50 | 2m 30s | Medium-large |
| 500 KB | 125 | 6m 30s | Large |
| 1 MB | 250 | 12m 30s | Very large |

*Times vary based on content complexity and LLM response time*

## Support & Troubleshooting

**Monitor not showing?**
- Check you're running in an interactive terminal
- Verify Python 3.6+ is installed
- Try running with smaller document first

**Output looks garbled?**
- Ensure UTF-8 encoding enabled
- Try with `verbose=False` for simpler output

**Extraction seems slow?**
- Check ETA - usually accurate
- Large documents naturally take longer
- LLM latency affects speed (OpenRouter, etc.)

## Next Steps

1. **Run extraction**: `python run_data_pipeline.py "doc.pdf"`
2. **Watch progress**: Monitor shows real-time status
3. **Review summary**: Check final statistics
4. **Check results**: Files saved in output directory

## Links

- Full Guide: [CHUNK_MONITORING.md](CHUNK_MONITORING.md)
- Main Docs: [README.md](README.md)
- Configuration: [.env](.env)

---

**Tip:** The monitoring helps you understand document structure and extraction quality. Run your first document with monitoring to see what's being extracted!
