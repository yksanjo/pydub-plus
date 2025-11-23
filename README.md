# pydub-plus 🎵

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![GitHub stars](https://img.shields.io/github/stars/yksanjo/pydub-plus?style=social)](https://github.com/yksanjo/pydub-plus/stargazers) [![GitHub forks](https://img.shields.io/github/forks/yksanjo/pydub-plus.svg)](https://github.com/yksanjo/pydub-plus/network/members)
[![GitHub issues](https://img.shields.io/github/issues/yksanjo/pydub-plus.svg)](https://github.com/yksanjo/pydub-plus/issues) [![Last commit](https://img.shields.io/github/last-commit/yksanjo/pydub-plus.svg)](https://github.com/yksanjo/pydub-plus/commits/main)


> An enhanced fork of [pydub](https://github.com/jiaaro/pydub) with GPU acceleration, async processing, REST API, CLI tools, and batch workflows for modern AI/creator applications.

## Why Fork pydub?

- ✅ **Extremely simple, readable Python codebase** - Easy to understand and extend
- ✅ **High user adoption** - Battle-tested library with active community
- ✅ **Easy entry points** - Simple architecture makes adding features straightforward
- ✅ **Perfect for AI/creator tools** - No deep DSP knowledge required

## 🚀 New Features

### 1. GPU Acceleration (CuPy)
Process audio operations on GPU for 10-100x speedup on large files:
```python
from pydub_plus import AudioSegment
from pydub_plus.gpu import enable_gpu

enable_gpu()  # Use CuPy for GPU acceleration
audio = AudioSegment.from_file("large_audio.wav")
processed = audio.normalize()  # Runs on GPU automatically
```

### 2. Async Processing
Perfect for web agents and async applications:
```python
import asyncio
from pydub_plus.async_ops import AudioSegmentAsync

async def main():
    audio = await AudioSegmentAsync.from_file_async("audio.mp3")
    normalized = await audio.normalize_async()
    await normalized.export_async("output.mp3")
```

### 3. REST API Wrapper
FastAPI-based REST API for audio processing:
```bash
# Start the API server
pydub-plus-api

# Process audio via HTTP
curl -X POST http://localhost:8000/api/process \
  -F "file=@audio.mp3" \
  -F "operation=normalize"
```

### 4. Cursor-Powered CLI
Interactive CLI for audio processing:
```bash
# Interactive mode
pydub-plus

# Batch processing
pydub-plus batch --input-dir ./audio --output-dir ./processed --operation normalize

# YouTube/TikTok workflows
pydub-plus youtube --url "https://youtube.com/watch?v=..." --extract-audio
pydub-plus tiktok --input video.mp4 --format mp3 --duration 60
```

### 5. Batch YouTube/TikTok Workflows
Specialized tools for content creators:
```python
from pydub_plus.workflows import YouTubeProcessor, TikTokProcessor

# YouTube workflow
youtube = YouTubeProcessor()
audio = await youtube.download_audio("https://youtube.com/watch?v=...")
processed = await youtube.process_for_podcast(audio)

# TikTok workflow
tiktok = TikTokProcessor()
clips = await tiktok.create_clips("long_audio.mp3", duration=60)
await tiktok.export_for_tiktok(clips, format="mp3")
```

## 📦 Installation

```bash
# Basic installation
pip install pydub-plus

# With GPU support (requires CUDA)
pip install pydub-plus[gpu]

# With all features
pip install pydub-plus[all]
```

## 🎯 Quick Start

### Basic Usage (Same as pydub)
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

### GPU Acceleration
```python
from pydub_plus import AudioSegment
from pydub_plus.gpu import enable_gpu

enable_gpu()  # Enable GPU processing
audio = AudioSegment.from_file("large_file.wav")
# All operations automatically use GPU when available
processed = audio.normalize().high_pass_filter(3000)
```

### Async Processing
```python
import asyncio
from pydub_plus.async_ops import AudioSegmentAsync

async def process():
    audio = await AudioSegmentAsync.from_file("input.mp3")
    result = await audio.normalize_async()
    await result.export_async("output.mp3")

asyncio.run(process())
```

### REST API
```python
# Start server
from pydub_plus.api import create_app
app = create_app()

# Or use CLI
# pydub-plus-api --port 8000
```

### Batch Processing
```python
from pydub_plus.batch import BatchProcessor

processor = BatchProcessor()
await processor.process_directory(
    input_dir="./audio",
    output_dir="./processed",
    operations=["normalize", "fade_in", "fade_out"]
)
```

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md)
- [Original pydub Credits](ORIGINAL_PYDUB_CREDITS.md)
- [Fork Notes](FORK_NOTES.md)
- [Contributing](CONTRIBUTING.md)

## 🏗️ Architecture

```
pydub-plus/
├── pydub_plus/
│   ├── core/                # Original pydub code (forked)
│   │   ├── audio_segment.py # Core AudioSegment class
│   │   ├── effects.py       # Audio effects
│   │   └── ...              # Other pydub modules
│   ├── gpu/                 # GPU acceleration with CuPy
│   ├── async_ops/           # Async processing
│   ├── api/                 # REST API (FastAPI)
│   ├── cli/                 # CLI tools
│   ├── workflows/           # YouTube/TikTok workflows
│   └── batch/               # Batch processing
├── examples/                # Example scripts
├── tests/                   # Test suite
└── docs/                    # Documentation
```

## 🔧 Requirements

- Python 3.8+
- numpy (for array operations)
- ffmpeg (for audio format conversion)

Optional:
- CuPy (for GPU acceleration)
- FastAPI (for REST API)
- yt-dlp (for YouTube workflows)
- aiofiles (for async file operations)

## 🤝 Contributing

Contributions welcome! This is a fork focused on modern enhancements while maintaining compatibility with pydub.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

Same as pydub - MIT License

## 🙏 Credits

- Original [pydub](https://github.com/jiaaro/pydub) by James Robert
- Enhanced with modern features for AI/creator tools
- See [ORIGINAL_PYDUB_CREDITS.md](ORIGINAL_PYDUB_CREDITS.md) for details

## 🗺️ Roadmap

- [x] Fork original pydub codebase
- [x] GPU acceleration with CuPy
- [x] Async processing support
- [x] REST API wrapper
- [x] CLI tools
- [x] YouTube/TikTok workflows
- [ ] Cloud storage integration (S3, GCS)
- [ ] Real-time audio processing
- [ ] WebAssembly build for browser use
- [ ] Integration with AI audio models
