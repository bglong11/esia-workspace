# -*- coding: utf-8 -*-
"""
Chunk Monitor - Progress and Status Display for ESIA Extraction

Provides real-time monitoring and display of chunk processing progress
during fact extraction from ESIA documents.
"""

import sys
import os
from typing import Optional
from datetime import datetime
from pathlib import Path


class ChunkMonitor:
    """Monitor and display chunk processing progress in real-time."""

    def __init__(self, total_chunks: int, show_chunk_content: bool = True,
                 max_preview_chars: int = 150, verbose: bool = True):
        """
        Initialize chunk monitor.

        Args:
            total_chunks: Total number of chunks to process
            show_chunk_content: Whether to display chunk content preview
            max_preview_chars: Max characters to show in preview
            verbose: Whether to show detailed progress information
        """
        self.total_chunks = total_chunks
        self.show_chunk_content = show_chunk_content
        self.max_preview_chars = max_preview_chars
        self.verbose = verbose
        self.current_chunk = 0
        self.start_time = datetime.now()
        self.facts_extracted = 0
        self.chunk_times = []
        self.last_chunk_start = None

    def start_chunk(self, chunk_id: int, chunk_text: str) -> None:
        """
        Called when starting to process a chunk.

        Args:
            chunk_id: ID/number of the chunk
            chunk_text: Full text of the chunk
        """
        self.current_chunk = chunk_id
        self.last_chunk_start = datetime.now()

        # Calculate position and percentage
        position = chunk_id
        percentage = (position / self.total_chunks) * 100
        elapsed = self._format_duration(datetime.now() - self.start_time)
        eta = self._calculate_eta()

        # Create header
        print("\n" + "=" * 100)
        print(f"[CHUNK {position}/{self.total_chunks}] Processing... ({percentage:.1f}%)")
        print("=" * 100)

        # Show chunk preview if enabled
        if self.show_chunk_content:
            preview = self._create_preview(chunk_text)
            print(f"\n📄 Content Preview ({len(chunk_text)} chars):")
            print(f"   {preview}")
            print()

        # Show stats
        if self.verbose:
            print(f"⏱️  Elapsed: {elapsed}  |  ETA: {eta}")
            print()

    def end_chunk(self, chunk_id: int, facts_count: int, errors: int = 0) -> None:
        """
        Called when finishing processing a chunk.

        Args:
            chunk_id: ID/number of the chunk
            facts_count: Number of facts extracted from this chunk
            errors: Number of extraction errors in this chunk
        """
        if self.last_chunk_start:
            duration = datetime.now() - self.last_chunk_start
            self.chunk_times.append(duration.total_seconds())
        else:
            duration = None

        self.facts_extracted += facts_count

        # Print completion info
        if duration:
            duration_str = self._format_duration(duration)
            print(f"\n✅ Chunk {chunk_id} Complete")
            print(f"   • Time: {duration_str}")
            print(f"   • Facts extracted: {facts_count}")
            if errors > 0:
                print(f"   • Errors: {errors}")
        else:
            print(f"\n✅ Chunk {chunk_id} Complete")
            print(f"   • Facts extracted: {facts_count}")

        # Show cumulative stats
        if self.verbose:
            avg_time = sum(self.chunk_times) / len(self.chunk_times) if self.chunk_times else 0
            print(f"\n📊 Progress Summary:")
            print(f"   • Total facts extracted: {self.facts_extracted}")
            print(f"   • Average time/chunk: {avg_time:.1f}s")
            print(f"   • Remaining chunks: {self.total_chunks - chunk_id}")

        print()

    def skip_chunk(self, chunk_id: int, reason: str) -> None:
        """
        Called when skipping a chunk.

        Args:
            chunk_id: ID/number of the skipped chunk
            reason: Reason for skipping
        """
        print(f"\n⏭️  Chunk {chunk_id} Skipped")
        print(f"   Reason: {reason}")
        print()

    def error_chunk(self, chunk_id: int, error: str) -> None:
        """
        Called when an error occurs during chunk processing.

        Args:
            chunk_id: ID/number of the chunk with error
            error: Error message
        """
        print(f"\n❌ Chunk {chunk_id} Error")
        print(f"   Error: {error}")
        print()

    def checkpoint_saved(self, chunk_id: int, facts_count: int) -> None:
        """
        Called when a checkpoint is saved.

        Args:
            chunk_id: ID of chunk at checkpoint
            facts_count: Total facts saved
        """
        elapsed = self._format_duration(datetime.now() - self.start_time)
        print(f"\n💾 Checkpoint Saved")
        print(f"   • Chunks processed: {chunk_id}")
        print(f"   • Total facts extracted: {facts_count}")
        print(f"   • Elapsed time: {elapsed}")
        print()

    def summary(self, total_facts: int, duration: Optional[datetime] = None) -> None:
        """
        Print final summary statistics.

        Args:
            total_facts: Total facts extracted
            duration: Total processing duration
        """
        if duration is None:
            duration = datetime.now() - self.start_time

        duration_str = self._format_duration(duration)
        rate = total_facts / duration.total_seconds() if duration.total_seconds() > 0 else 0
        avg_time = sum(self.chunk_times) / len(self.chunk_times) if self.chunk_times else 0

        print("\n" + "=" * 100)
        print("EXTRACTION COMPLETE - SUMMARY")
        print("=" * 100)
        print(f"\n📊 Statistics:")
        print(f"   • Total chunks: {self.total_chunks}")
        print(f"   • Total facts: {total_facts}")
        print(f"   • Total time: {duration_str}")
        print(f"   • Average time/chunk: {avg_time:.1f}s")
        print(f"   • Facts per second: {rate:.2f}")
        print()

    def _create_preview(self, text: str) -> str:
        """
        Create a preview of chunk text.

        Args:
            text: Full text to preview

        Returns:
            Truncated preview string
        """
        if len(text) <= self.max_preview_chars:
            return text.replace('\n', ' ')[:self.max_preview_chars]

        # Truncate and add ellipsis
        preview = text[:self.max_preview_chars].replace('\n', ' ')
        # Try to truncate at word boundary
        last_space = preview.rfind(' ')
        if last_space > self.max_preview_chars - 50:
            preview = preview[:last_space] + "..."
        else:
            preview = preview + "..."

        return preview

    def _format_duration(self, duration) -> str:
        """Format a duration object as string."""
        total_seconds = duration.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def _calculate_eta(self) -> str:
        """Calculate and format estimated time of arrival."""
        if not self.chunk_times or self.current_chunk == 0:
            return "calculating..."

        avg_time = sum(self.chunk_times) / len(self.chunk_times)
        remaining_chunks = self.total_chunks - self.current_chunk
        remaining_seconds = avg_time * remaining_chunks

        if remaining_seconds < 0:
            return "done"

        return self._format_duration_seconds(remaining_seconds)

    def _format_duration_seconds(self, seconds: float) -> str:
        """Format seconds as duration string."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m"
        else:
            return f"{secs}s"


class SimpleProgressMonitor:
    """Lightweight progress monitor (minimal output)."""

    def __init__(self, total_chunks: int):
        """
        Initialize simple monitor.

        Args:
            total_chunks: Total number of chunks to process
        """
        self.total_chunks = total_chunks
        self.current_chunk = 0

    def start_chunk(self, chunk_id: int, chunk_text: str) -> None:
        """Log chunk start."""
        self.current_chunk = chunk_id
        percentage = (chunk_id / self.total_chunks) * 100
        print(f"[{chunk_id}/{self.total_chunks}] {percentage:.0f}% - Processing...", end='\r')

    def end_chunk(self, chunk_id: int, facts_count: int, errors: int = 0) -> None:
        """Log chunk end."""
        print(f"[{chunk_id}/{self.total_chunks}] ✅ {facts_count} facts extracted          ")

    def skip_chunk(self, chunk_id: int, reason: str) -> None:
        """Log skipped chunk."""
        print(f"[{chunk_id}/{self.total_chunks}] ⏭️  Skipped: {reason}")

    def error_chunk(self, chunk_id: int, error: str) -> None:
        """Log chunk error."""
        print(f"[{chunk_id}/{self.total_chunks}] ❌ Error: {error}")

    def checkpoint_saved(self, chunk_id: int, facts_count: int) -> None:
        """Log checkpoint."""
        print(f"[{chunk_id}/{self.total_chunks}] 💾 Checkpoint saved ({facts_count} facts)")

    def summary(self, total_facts: int, duration=None) -> None:
        """Print summary."""
        print(f"\n✅ Extraction complete: {total_facts} facts extracted")


def create_monitor(total_chunks: int, verbose: bool = True,
                   show_content: bool = True) -> ChunkMonitor:
    """
    Factory function to create appropriate monitor.

    Args:
        total_chunks: Total chunks to process
        verbose: Whether to show detailed output
        show_content: Whether to show chunk content preview

    Returns:
        ChunkMonitor or SimpleProgressMonitor instance
    """
    if verbose:
        return ChunkMonitor(total_chunks, show_chunk_content=show_content)
    else:
        return SimpleProgressMonitor(total_chunks)
