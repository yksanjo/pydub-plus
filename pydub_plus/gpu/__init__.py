"""
GPU acceleration module using CuPy
"""

import numpy as np
from typing import Optional

_GPU_ENABLED = False
_GPU_AVAILABLE = False

try:
    import cupy as cp
    _GPU_AVAILABLE = True
except ImportError:
    cp = None


def is_gpu_available() -> bool:
    """Check if GPU (CuPy) is available"""
    return _GPU_AVAILABLE and cp is not None


def enable_gpu() -> bool:
    """
    Enable GPU acceleration globally
    
    Returns:
        True if GPU was enabled, False otherwise
    """
    global _GPU_ENABLED
    
    if not is_gpu_available():
        print("Warning: CuPy not available. Install with: pip install cupy-cuda12x")
        return False
    
    _GPU_ENABLED = True
    print(f"GPU acceleration enabled using {cp.cuda.Device(0).compute_capability}")
    return True


def disable_gpu():
    """Disable GPU acceleration globally"""
    global _GPU_ENABLED
    _GPU_ENABLED = False


def is_gpu_enabled() -> bool:
    """Check if GPU acceleration is currently enabled"""
    return _GPU_ENABLED and is_gpu_available()


def get_array_module(use_gpu: Optional[bool] = None):
    """
    Get the appropriate array module (numpy or cupy)
    
    Args:
        use_gpu: Override GPU setting. If None, uses global setting.
        
    Returns:
        numpy or cupy module
    """
    if use_gpu is None:
        use_gpu = is_gpu_enabled()
    
    if use_gpu and is_gpu_available():
        return cp
    return np


def to_gpu(arr: np.ndarray):
    """Convert numpy array to CuPy array"""
    if not is_gpu_available():
        return arr
    return cp.asarray(arr)


def to_cpu(arr):
    """Convert CuPy array to numpy array"""
    if hasattr(arr, 'get'):  # CuPy array
        return arr.get()
    return arr


def normalize_gpu(arr, target_db: float = -20.0):
    """
    Normalize audio array on GPU
    
    Args:
        arr: Audio array (numpy or CuPy)
        target_db: Target loudness in dB
        
    Returns:
        Normalized array
    """
    xp = get_array_module(hasattr(arr, 'get') if hasattr(arr, 'get') else False)
    
    # Convert to float32
    arr = xp.asarray(arr, dtype=xp.float32)
    
    # Calculate RMS
    rms = xp.sqrt(xp.mean(arr ** 2))
    
    if rms == 0:
        return arr
    
    # Calculate target RMS
    target_rms = 10 ** (target_db / 20.0)
    
    # Normalize
    normalized = arr * (target_rms / rms)
    
    # Clip to prevent clipping
    normalized = xp.clip(normalized, -1.0, 1.0)
    
    return normalized


def apply_gain_gpu(arr, gain_db: float):
    """
    Apply gain to audio array on GPU
    
    Args:
        arr: Audio array (numpy or CuPy)
        gain_db: Gain in dB
        
    Returns:
        Array with gain applied
    """
    xp = get_array_module(hasattr(arr, 'get') if hasattr(arr, 'get') else False)
    
    arr = xp.asarray(arr, dtype=xp.float32)
    gain_linear = 10 ** (gain_db / 20.0)
    
    return arr * gain_linear


__all__ = [
    "is_gpu_available",
    "enable_gpu",
    "disable_gpu",
    "is_gpu_enabled",
    "get_array_module",
    "to_gpu",
    "to_cpu",
    "normalize_gpu",
    "apply_gain_gpu",
]

