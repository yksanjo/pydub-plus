"""
Batch audio processor
"""

import asyncio
from pathlib import Path
from typing import List, Optional, Dict
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from pydub_plus.async_ops import AudioSegmentAsync


class BatchProcessor:
    """Batch processor for audio files"""
    
    def __init__(self, max_workers: int = 4):
        """
        Initialize batch processor
        
        Args:
            max_workers: Maximum number of concurrent workers
        """
        self.max_workers = max_workers
    
    async def process_directory(self,
                               input_dir: str,
                               output_dir: str,
                               operations: List[str],
                               output_format: Optional[str] = None,
                               pattern: str = "*.*") -> Dict[str, bool]:
        """
        Process all audio files in a directory
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            operations: List of operations to apply
            output_format: Output format (auto-detected if None)
            pattern: File pattern to match
            
        Returns:
            Dictionary mapping file paths to success status
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all audio files
        audio_files = list(input_path.glob(pattern))
        
        # Filter to common audio formats
        audio_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.ogg', '.aac'}
        audio_files = [f for f in audio_files if f.suffix.lower() in audio_extensions]
        
        results = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ) as progress:
            task = progress.add_task("Processing files...", total=len(audio_files))
            
            # Process files with concurrency limit
            semaphore = asyncio.Semaphore(self.max_workers)
            
            async def process_file(file_path: Path):
                async with semaphore:
                    try:
                        await self._process_single_file(
                            file_path, output_path, operations, output_format
                        )
                        results[str(file_path)] = True
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
                        results[str(file_path)] = False
                    finally:
                        progress.update(task, advance=1)
            
            # Process all files
            await asyncio.gather(*[process_file(f) for f in audio_files])
        
        return results
    
    async def _process_single_file(self,
                                   input_file: Path,
                                   output_dir: Path,
                                   operations: List[str],
                                   output_format: Optional[str]):
        """Process a single audio file"""
        # Load audio
        audio = await AudioSegmentAsync.from_file_async(input_file)
        
        # Apply operations
        for operation in operations:
            if operation == "normalize":
                audio = await audio.normalize_async()
            elif operation == "fade_in":
                audio = await audio.fade_in_async(2000)
            elif operation == "fade_out":
                audio = await audio.fade_out_async(2000)
            elif operation == "high_pass":
                audio = await audio.high_pass_filter_async(3000)
            elif operation == "low_pass":
                audio = await audio.low_pass_filter_async(3000)
            # Add more operations as needed
        
        # Determine output format
        if output_format:
            format_ext = output_format
        else:
            format_ext = input_file.suffix[1:] or "mp3"
        
        # Export
        output_file = output_dir / f"{input_file.stem}.{format_ext}"
        await audio.export_async(output_file, format=format_ext)

