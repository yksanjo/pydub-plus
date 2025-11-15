"""
YouTube audio processing workflows
"""

import asyncio
from pathlib import Path
from typing import Optional
import yt_dlp
from pydub_plus.async_ops import AudioSegmentAsync
import tempfile


class YouTubeProcessor:
    """Processor for YouTube audio workflows"""
    
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(tempfile.gettempdir()) / "pydub_plus_youtube"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def download_audio(self, url: str, format: str = "bestaudio/best") -> AudioSegmentAsync:
        """
        Download audio from YouTube URL
        
        Args:
            url: YouTube URL
            format: Audio format preference
            
        Returns:
            AudioSegmentAsync instance
        """
        ydl_opts = {
            'format': format,
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        loop = asyncio.get_event_loop()
        
        # Download in thread pool
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                # Replace extension with mp3
                filename = Path(filename).with_suffix('.mp3')
                return str(filename)
        
        file_path = await loop.run_in_executor(None, download)
        return await AudioSegmentAsync.from_file_async(file_path)
    
    async def process_for_podcast(self, audio: AudioSegmentAsync, 
                                  normalize: bool = True,
                                  fade_in: int = 2000,
                                  fade_out: int = 2000) -> AudioSegmentAsync:
        """
        Process audio for podcast format
        
        Args:
            audio: AudioSegmentAsync instance
            normalize: Whether to normalize
            fade_in: Fade in duration in ms
            fade_out: Fade out duration in ms
            
        Returns:
            Processed AudioSegmentAsync
        """
        result = audio
        
        if normalize:
            result = await result.normalize_async()
        
        if fade_in:
            result = await result.fade_in_async(fade_in)
        
        if fade_out:
            result = await result.fade_out_async(fade_out)
        
        return result
    
    async def extract_segment(self, audio: AudioSegmentAsync,
                             start_ms: int,
                             end_ms: int) -> AudioSegmentAsync:
        """
        Extract a segment from audio
        
        Args:
            audio: AudioSegmentAsync instance
            start_ms: Start time in milliseconds
            end_ms: End time in milliseconds
            
        Returns:
            Extracted segment
        """
        loop = asyncio.get_event_loop()
        segment = await loop.run_in_executor(
            None,
            lambda: audio.audio[start_ms:end_ms]
        )
        return AudioSegmentAsync(segment)

