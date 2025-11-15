"""Tests for GPU acceleration module"""

import pytest
import numpy as np
from pydub_plus.gpu import (
    is_gpu_available,
    enable_gpu,
    disable_gpu,
    is_gpu_enabled,
    get_array_module,
    to_gpu,
    to_cpu,
)


def test_gpu_availability():
    """Test GPU availability check"""
    available = is_gpu_available()
    assert isinstance(available, bool)


def test_gpu_enable_disable():
    """Test enabling/disabling GPU"""
    original_state = is_gpu_enabled()
    
    enable_gpu()
    assert is_gpu_enabled() == is_gpu_available()
    
    disable_gpu()
    assert not is_gpu_enabled()
    
    # Restore original state
    if original_state:
        enable_gpu()


def test_get_array_module():
    """Test getting array module"""
    xp = get_array_module()
    assert xp is not None
    
    # Should return numpy if GPU not available
    if not is_gpu_available():
        assert xp == np


def test_to_gpu_to_cpu():
    """Test GPU/CPU array conversion"""
    arr = np.array([1, 2, 3, 4, 5])
    
    # Convert to GPU (if available)
    gpu_arr = to_gpu(arr)
    
    # Convert back to CPU
    cpu_arr = to_cpu(gpu_arr)
    
    np.testing.assert_array_equal(arr, cpu_arr)

