"""
Basic usage examples for pydub-plus
"""

from pydub_plus.core import AudioSegment

# Example 1: Load and normalize audio
def example_normalize():
    audio = AudioSegment.from_mp3("input.mp3")
    normalized = audio.normalize()
    normalized.export("output.mp3", format="mp3")
    print("✓ Normalized audio saved")


# Example 2: Apply effects
def example_effects():
    audio = AudioSegment.from_wav("input.wav")
    
    # Apply multiple effects
    processed = (
        audio
        .normalize()
        .fade_in(2000)
        .fade_out(2000)
        .high_pass_filter(3000)
        .low_pass_filter(8000)
    )
    
    processed.export("output.wav", format="wav")
    print("✓ Processed audio with effects")


# Example 3: Convert format
def example_convert():
    audio = AudioSegment.from_file("input.wav")
    audio.export("output.mp3", format="mp3", bitrate="192k")
    print("✓ Converted to MP3")


if __name__ == "__main__":
    print("Basic usage examples")
    print("Note: Update file paths before running")

