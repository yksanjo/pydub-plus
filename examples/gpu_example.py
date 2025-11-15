"""
GPU acceleration example
"""

from pydub_plus import AudioSegment
from pydub_plus.gpu import enable_gpu, is_gpu_available

def example_gpu_processing():
    # Check if GPU is available
    if not is_gpu_available():
        print("GPU not available. Install CuPy for GPU support.")
        return
    
    # Enable GPU acceleration
    enable_gpu()
    
    # Load audio (will use GPU for processing)
    audio = AudioSegment.from_file("large_audio.wav")
    
    # Process with GPU acceleration
    processed = audio.normalize()
    
    # Export
    processed.export("output.wav", format="wav")
    print("✓ Processed with GPU acceleration")


if __name__ == "__main__":
    example_gpu_processing()

