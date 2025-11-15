"""
Async processing example
"""

import asyncio
from pydub_plus.async_ops import AudioSegmentAsync

async def example_async_processing():
    # Load audio asynchronously
    audio = await AudioSegmentAsync.from_file_async("input.mp3")
    
    # Process asynchronously
    normalized = await audio.normalize_async()
    faded = await normalized.fade_in_async(2000)
    
    # Export asynchronously
    await faded.export_async("output.mp3")
    print("✓ Processed asynchronously")


async def example_batch_async():
    """Process multiple files concurrently"""
    files = ["audio1.mp3", "audio2.mp3", "audio3.mp3"]
    
    async def process_file(file_path):
        audio = await AudioSegmentAsync.from_file_async(file_path)
        normalized = await audio.normalize_async()
        output_path = f"processed_{file_path}"
        await normalized.export_async(output_path)
        return output_path
    
    # Process all files concurrently
    results = await asyncio.gather(*[process_file(f) for f in files])
    print(f"✓ Processed {len(results)} files concurrently")


if __name__ == "__main__":
    asyncio.run(example_async_processing())
    # asyncio.run(example_batch_async())

