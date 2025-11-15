"""
YouTube workflow example
"""

import asyncio
from pydub_plus.workflows import YouTubeProcessor

async def example_download_and_process():
    processor = YouTubeProcessor()
    
    # Download audio from YouTube
    url = "https://youtube.com/watch?v=..."  # Replace with actual URL
    audio = await processor.download_audio(url)
    
    # Process for podcast
    podcast_audio = await processor.process_for_podcast(
        audio,
        normalize=True,
        fade_in=2000,
        fade_out=2000
    )
    
    # Export
    await podcast_audio.export_async("podcast.mp3")
    print("✓ Downloaded and processed YouTube audio")


async def example_extract_segment():
    processor = YouTubeProcessor()
    
    # Download full audio
    audio = await processor.download_audio("https://youtube.com/watch?v=...")
    
    # Extract a 30-second segment (from 1:00 to 1:30)
    segment = await processor.extract_segment(audio, start_ms=60000, end_ms=90000)
    
    # Export segment
    await segment.export_async("segment.mp3")
    print("✓ Extracted segment")


if __name__ == "__main__":
    print("YouTube workflow examples")
    print("Note: Update YouTube URL before running")
    # asyncio.run(example_download_and_process())

