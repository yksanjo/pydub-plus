"""
Core audio processing module - extends pydub's AudioSegment

This module contains the original pydub code plus enhancements.
The original pydub code is from: https://github.com/jiaaro/pydub
"""

# Import original pydub AudioSegment from the copied source
# This maintains the original pydub functionality
from pydub_plus.core.audio_segment import AudioSegment as _AudioSegment
from typing import Optional, Union, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    import cupy

# Re-export original AudioSegment for compatibility
# Users can use AudioSegment exactly as they would with pydub
AudioSegment = _AudioSegment

# Re-export other pydub modules
from pydub_plus.core import (
    effects,
    exceptions,
    generators,
    playback,
    silence,
    utils,
)


class AudioSegmentPlus(_AudioSegment):
    """
    Enhanced AudioSegment with additional features while maintaining
    full compatibility with pydub's AudioSegment
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._use_gpu = False
    
    def enable_gpu(self):
        """Enable GPU processing for this audio segment"""
        self._use_gpu = True
        return self
    
    def disable_gpu(self):
        """Disable GPU processing for this audio segment"""
        self._use_gpu = False
        return self
    
    def get_array(self, use_gpu: Optional[bool] = None) -> Union[np.ndarray, 'cupy.ndarray']:
        """
        Get audio data as numpy array (or CuPy array if GPU enabled)
        
        Args:
            use_gpu: Override GPU setting for this call
            
        Returns:
            numpy array or CuPy array
        """
        use_gpu = use_gpu if use_gpu is not None else self._use_gpu
        
        if use_gpu:
            try:
                import cupy as cp
                # Convert to CuPy array
                arr = np.array(self.get_array_of_samples())
                return cp.asarray(arr)
            except ImportError:
                # Fallback to numpy if CuPy not available
                return np.array(self.get_array_of_samples())
        else:
            return np.array(self.get_array_of_samples())
    
    @classmethod
    def from_array(cls, arr: Union[np.ndarray, 'cupy.ndarray'], 
                   frame_rate: int = 44100, 
                   channels: int = 2,
                   sample_width: int = 2) -> 'AudioSegmentPlus':
        """
        Create AudioSegment from array (numpy or CuPy)
        
        Args:
            arr: Audio data array
            frame_rate: Sample rate
            channels: Number of channels
            sample_width: Bytes per sample
        """
        # Convert CuPy array to numpy if needed
        if hasattr(arr, 'get'):  # CuPy array
            arr = arr.get()
        
        # Reshape if needed
        if channels > 1 and len(arr.shape) == 1:
            arr = arr.reshape(-1, channels)
        
        # Convert to bytes
        if arr.dtype != np.int16:
            arr = (arr * 32767).astype(np.int16)
        
        # Use pydub's from_ndarray method
        return cls._from_ndarray(arr, frame_rate=frame_rate, channels=channels, 
                                 sample_width=sample_width)
