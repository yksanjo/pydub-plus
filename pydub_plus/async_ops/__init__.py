"""
Async operations for audio processing
"""

import asyncio
from pathlib import Path
from typing import Optional, Union
import aiofiles
from pydub_plus.core import AudioSegment, AudioSegmentPlus


class AudioSegmentAsync:
    """
    Async wrapper for AudioSegment operations
    """
    
    def __init__(self, audio_segment: Union[AudioSegment, AudioSegmentPlus]):
        self._audio = audio_segment
    
    @classmethod
    async def from_file_async(cls, file_path: Union[str, Path], 
                              format: Optional[str] = None) -> 'AudioSegmentAsync':
        """
        Load audio file asynchronously
        
        Args:
            file_path: Path to audio file
            format: Audio format (auto-detected if None)
        """
        file_path = Path(file_path)
        
        # Read file asynchronously
        async with aiofiles.open(file_path, 'rb') as f:
            data = await f.read()
        
        # Load in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        audio = await loop.run_in_executor(
            None,
            lambda: AudioSegment.from_file(file_path, format=format)
        )
        
        return cls(audio)
    
    @classmethod
    async def from_bytes_async(cls, data: bytes, format: str) -> 'AudioSegmentAsync':
        """
        Load audio from bytes asynchronously
        
        Args:
            data: Audio data bytes
            format: Audio format
        """
        from io import BytesIO
        
        loop = asyncio.get_event_loop()
        audio = await loop.run_in_executor(
            None,
            lambda: AudioSegment.from_file(BytesIO(data), format=format)
        )
        
        return cls(audio)
    
    async def export_async(self, 
                          out_path: Union[str, Path],
                          format: Optional[str] = None,
                          **kwargs) -> Path:
        """
        Export audio file asynchronously
        
        Args:
            out_path: Output file path
            format: Output format (auto-detected from extension if None)
            **kwargs: Additional export parameters
        """
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Export in thread pool
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: self._audio.export(str(out_path), format=format, **kwargs)
        )
        
        return out_path
    
    async def normalize_async(self, headroom: float = 0.1) -> 'AudioSegmentAsync':
        """Normalize audio asynchronously"""
        loop = asyncio.get_event_loop()
        normalized = await loop.run_in_executor(
            None,
            lambda: self._audio.normalize(headroom=headroom)
        )
        return AudioSegmentAsync(normalized)
    
    async def apply_gain_async(self, gain: float) -> 'AudioSegmentAsync':
        """Apply gain asynchronously"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self._audio.apply_gain(gain)
        )
        return AudioSegmentAsync(result)
    
    async def fade_in_async(self, duration: int) -> 'AudioSegmentAsync':
        """Fade in asynchronously"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self._audio.fade_in(duration)
        )
        return AudioSegmentAsync(result)
    
    async def fade_out_async(self, duration: int) -> 'AudioSegmentAsync':
        """Fade out asynchronously"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self._audio.fade_out(duration)
        )
        return AudioSegmentAsync(result)
    
    async def high_pass_filter_async(self, cutoff: int) -> 'AudioSegmentAsync':
        """Apply high-pass filter asynchronously"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self._audio.high_pass_filter(cutoff)
        )
        return AudioSegmentAsync(result)
    
    async def low_pass_filter_async(self, cutoff: int) -> 'AudioSegmentAsync':
        """Apply low-pass filter asynchronously"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self._audio.low_pass_filter(cutoff)
        )
        return AudioSegmentAsync(result)
    
    def __getattr__(self, name):
        """Delegate other attributes to underlying AudioSegment"""
        return getattr(self._audio, name)
    
    @property
    def audio(self) -> AudioSegment:
        """Get underlying AudioSegment"""
        return self._audio


__all__ = ["AudioSegmentAsync"]

