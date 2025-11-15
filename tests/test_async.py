"""Tests for async operations"""

import pytest
import asyncio
from pathlib import Path
import tempfile
from pydub_plus.core import AudioSegment
from pydub_plus.async_ops import AudioSegmentAsync


@pytest.mark.asyncio
async def test_from_bytes_async():
    """Test loading audio from bytes"""
    # Create a simple audio segment
    audio = AudioSegment.silent(duration=1000)  # 1 second of silence
    
    # Export to bytes
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        audio.export(tmp.name, format='wav')
        tmp_path = tmp.name
    
    try:
        # Load asynchronously
        audio_async = await AudioSegmentAsync.from_file_async(tmp_path)
        assert audio_async.audio is not None
        assert len(audio_async.audio) == 1000
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@pytest.mark.asyncio
async def test_normalize_async():
    """Test async normalization"""
    # Create test audio
    audio = AudioSegment.silent(duration=1000)
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        audio.export(tmp.name, format='wav')
        tmp_path = tmp.name
    
    try:
        audio_async = await AudioSegmentAsync.from_file_async(tmp_path)
        normalized = await audio_async.normalize_async()
        assert normalized.audio is not None
    finally:
        Path(tmp_path).unlink(missing_ok=True)

