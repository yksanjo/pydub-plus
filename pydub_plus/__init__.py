"""
pydub-plus: Enhanced pydub with GPU acceleration, async processing, REST API, and batch workflows

This is a fork of pydub (https://github.com/jiaaro/pydub) with additional features.
"""

__version__ = "0.1.0"

# Import original pydub AudioSegment from our forked core
from pydub_plus.core import AudioSegment, AudioSegmentPlus

# Export enhanced modules
from pydub_plus.gpu import enable_gpu, is_gpu_available
from pydub_plus.async_ops import AudioSegmentAsync

# Re-export original pydub modules for compatibility
from pydub_plus.core import (
    effects,
    exceptions,
    generators,
    playback,
    silence,
    utils,
)

__all__ = [
    "AudioSegment",
    "AudioSegmentPlus",
    "AudioSegmentAsync",
    "enable_gpu",
    "is_gpu_available",
    "effects",
    "exceptions",
    "generators",
    "playback",
    "silence",
    "utils",
]

