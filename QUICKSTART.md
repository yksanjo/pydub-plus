# Quick Start Guide

Get started with pydub-plus in minutes!

## Installation

```bash
# Basic installation
pip install pydub-plus

# With GPU support (requires CUDA)
pip install pydub-plus[gpu]

# With all features
pip install pydub-plus[all]
```

## Basic Usage

### 1. Simple Audio Processing (Same as pydub)

```python
from pydub_plus import AudioSegment

# Load audio
audio = AudioSegment.from_mp3("input.mp3")

# Process
normalized = audio.normalize()
faded = normalized.fade_in(2000).fade_out(2000)

# Export
faded.export("output.mp3", format="mp3")
```

### 2. GPU Acceleration

```python
from pydub_plus import AudioSegment
from pydub_plus.gpu import enable_gpu

# Enable GPU processing
enable_gpu()

# Load and process (automatically uses GPU)
audio = AudioSegment.from_file("large_file.wav")
processed = audio.normalize().high_pass_filter(3000)
processed.export("output.wav")
```

### 3. Async Processing

```python
import asyncio
from pydub_plus.async_ops import AudioSegmentAsync

async def main():
    # Load audio asynchronously
    audio = await AudioSegmentAsync.from_file_async("input.mp3")
    
    # Process asynchronously
    normalized = await audio.normalize_async()
    faded = await normalized.fade_in_async(2000)
    
    # Export asynchronously
    await faded.export_async("output.mp3")

asyncio.run(main())
```

### 4. REST API

```bash
# Start the API server
pydub-plus-api

# Or with custom settings
pydub-plus-api --host 0.0.0.0 --port 8000
```

Then use the API:

```bash
# Normalize audio
curl -X POST http://localhost:8000/api/normalize \
  -F "file=@audio.mp3" \
  -o normalized.mp3

# Convert format
curl -X POST http://localhost:8000/api/convert \
  -F "file=@audio.wav" \
  -F "format=mp3" \
  -o converted.mp3
```

### 5. CLI Usage

```bash
# Normalize a file
pydub-plus normalize input.mp3 -o output.mp3

# Convert format
pydub-plus convert input.wav output.mp3

# Batch process
pydub-plus batch ./audio ./processed --operation normalize

# YouTube workflow
pydub-plus youtube "https://youtube.com/watch?v=..." -o audio.mp3

# TikTok workflow
pydub-plus tiktok long_audio.mp3 --duration 60 --output-dir ./clips
```

### 6. YouTube Workflows

```python
import asyncio
from pydub_plus.workflows import YouTubeProcessor

async def main():
    processor = YouTubeProcessor()
    
    # Download audio
    audio = await processor.download_audio("https://youtube.com/watch?v=...")
    
    # Process for podcast
    podcast_audio = await processor.process_for_podcast(audio)
    await podcast_audio.export_async("podcast.mp3")

asyncio.run(main())
```

### 7. TikTok Workflows

```python
import asyncio
from pydub_plus.workflows import TikTokProcessor

async def main():
    processor = TikTokProcessor()
    
    # Create 60-second clips
    clips = await processor.create_clips("long_audio.mp3", duration=60)
    
    # Export for TikTok
    await processor.export_for_tiktok(clips, "./tiktok_clips")

asyncio.run(main())
```

### 8. Batch Processing

```python
import asyncio
from pydub_plus.batch import BatchProcessor

async def main():
    processor = BatchProcessor(max_workers=4)
    
    results = await processor.process_directory(
        input_dir="./audio",
        output_dir="./processed",
        operations=["normalize", "fade_in", "fade_out"]
    )
    
    print(f"Processed {sum(results.values())} files successfully")

asyncio.run(main())
```

## Next Steps

- Check out the [examples](examples/) directory for more use cases
- Read the [full documentation](docs/)
- Explore the [API reference](docs/API.md)

## Troubleshooting

### GPU not available?
- Make sure you have CUDA installed
- Install the correct CuPy version for your CUDA version:
  - `pip install cupy-cuda12x` for CUDA 12.x
  - `pip install cupy-cuda11x` for CUDA 11.x

### FFmpeg not found?
- Install FFmpeg: `brew install ffmpeg` (macOS) or `apt-get install ffmpeg` (Linux)
- Or download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Import errors?
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)

