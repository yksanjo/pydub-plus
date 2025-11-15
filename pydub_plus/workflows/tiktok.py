"""
TikTok audio processing workflows
"""

import asyncio
from pathlib import Path
from typing import List
from pydub_plus.async_ops import AudioSegmentAsync


class TikTokProcessor:
    """Processor for TikTok audio workflows"""
    
    def __init__(self, max_duration_ms: int = 60000):
        """
        Initialize TikTok processor
        
        Args:
            max_duration_ms: Maximum clip duration in milliseconds (default 60s)
        """
        self.max_duration_ms = max_duration_ms
    
    async def create_clips(self, 
                          input_file: str,
                          duration: int = 60,
                          overlap: int = 0) -> List[AudioSegmentAsync]:
        """
        Create clips from audio file
        
        Args:
            input_file: Input audio file path
            duration: Clip duration in seconds
            overlap: Overlap between clips in seconds
            
        Returns:
            List of AudioSegmentAsync clips
        """
        audio = await AudioSegmentAsync.from_file_async(input_file)
        duration_ms = duration * 1000
        overlap_ms = overlap * 1000
        clips = []
        
        start = 0
        while start < len(audio.audio):
            end = min(start + duration_ms, len(audio.audio))
            
            loop = asyncio.get_event_loop()
            clip_audio = await loop.run_in_executor(
                None,
                lambda: audio.audio[start:end]
            )
            clips.append(AudioSegmentAsync(clip_audio))
            
            start = end - overlap_ms
        
        return clips
    
    async def export_for_tiktok(self,
                               clips: List[AudioSegmentAsync],
                               output_dir: str,
                               format: str = "mp3",
                               prefix: str = "tiktok_clip") -> List[Path]:
        """
        Export clips in TikTok-ready format
        
        Args:
            clips: List of AudioSegmentAsync clips
            output_dir: Output directory
            format: Output format
            prefix: Filename prefix
            
        Returns:
            List of output file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        output_files = []
        
        for i, clip in enumerate(clips):
            # Ensure clip is within TikTok limits
            if len(clip.audio) > self.max_duration_ms:
                # Trim to max duration
                loop = asyncio.get_event_loop()
                trimmed = await loop.run_in_executor(
                    None,
                    lambda: clip.audio[:self.max_duration_ms]
                )
                clip = AudioSegmentAsync(trimmed)
            
            # Normalize for TikTok
            clip = await clip.normalize_async()
            
            # Export
            output_file = output_path / f"{prefix}_{i+1:03d}.{format}"
            await clip.export_async(output_file, format=format)
            output_files.append(output_file)
        
        return output_files
    
    async def add_fade_effects(self, clip: AudioSegmentAsync,
                              fade_in: int = 500,
                              fade_out: int = 500) -> AudioSegmentAsync:
        """
        Add fade in/out effects for TikTok
        
        Args:
            clip: AudioSegmentAsync clip
            fade_in: Fade in duration in ms
            fade_out: Fade out duration in ms
            
        Returns:
            Clip with fade effects
        """
        result = await clip.fade_in_async(fade_in)
        result = await result.fade_out_async(fade_out)
        return result

