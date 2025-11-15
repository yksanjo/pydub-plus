"""
TikTok workflow example
"""

import asyncio
from pydub_plus.workflows import TikTokProcessor

async def example_create_clips():
    processor = TikTokProcessor()
    
    # Create 60-second clips from long audio
    clips = await processor.create_clips("long_audio.mp3", duration=60)
    
    # Export for TikTok
    output_files = await processor.export_for_tiktok(
        clips,
        "./tiktok_clips",
        format="mp3"
    )
    
    print(f"✓ Created {len(output_files)} TikTok clips")


async def example_with_fade_effects():
    processor = TikTokProcessor()
    
    # Create clips
    clips = await processor.create_clips("long_audio.mp3", duration=60)
    
    # Add fade effects to each clip
    processed_clips = []
    for clip in clips:
        faded = await processor.add_fade_effects(clip, fade_in=500, fade_out=500)
        processed_clips.append(faded)
    
    # Export
    await processor.export_for_tiktok(processed_clips, "./tiktok_clips")
    print("✓ Created clips with fade effects")


if __name__ == "__main__":
    print("TikTok workflow examples")
    print("Note: Update file paths before running")
    # asyncio.run(example_create_clips())

