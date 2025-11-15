"""
Main CLI for pydub-plus
"""

import typer
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer(help="pydub-plus: Enhanced audio processing CLI")
console = Console()


@app.command()
def normalize(
    input_file: Path = typer.Argument(..., help="Input audio file"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
    headroom: float = typer.Option(0.1, "--headroom", help="Normalization headroom"),
):
    """Normalize audio file"""
    from pydub_plus.core import AudioSegment
    
    output = output_file or input_file.with_stem(f"{input_file.stem}_normalized")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Normalizing audio...", total=None)
        
        audio = AudioSegment.from_file(str(input_file))
        normalized = audio.normalize(headroom=headroom)
        normalized.export(str(output), format=output.suffix[1:])
        
        progress.update(task, completed=True)
    
    console.print(f"[green]✓[/green] Normalized audio saved to: {output}")


@app.command()
def convert(
    input_file: Path = typer.Argument(..., help="Input audio file"),
    output_file: Path = typer.Argument(..., help="Output audio file"),
):
    """Convert audio format"""
    from pydub_plus.core import AudioSegment
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Converting audio...", total=None)
        
        audio = AudioSegment.from_file(str(input_file))
        output_format = output_file.suffix[1:]
        audio.export(str(output_file), format=output_format)
        
        progress.update(task, completed=True)
    
    console.print(f"[green]✓[/green] Converted audio saved to: {output_file}")


@app.command()
def batch(
    input_dir: Path = typer.Argument(..., help="Input directory"),
    output_dir: Path = typer.Argument(..., help="Output directory"),
    operation: str = typer.Option("normalize", "--operation", "-op", help="Operation to apply"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format"),
):
    """Batch process audio files"""
    from pydub_plus.batch import BatchProcessor
    import asyncio
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processor = BatchProcessor()
    
    async def run():
        await processor.process_directory(
            input_dir=str(input_dir),
            output_dir=str(output_dir),
            operations=[operation],
            output_format=format
        )
    
    asyncio.run(run())
    console.print(f"[green]✓[/green] Batch processing complete")


@app.command()
def youtube(
    url: str = typer.Argument(..., help="YouTube URL"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
    extract_audio: bool = typer.Option(True, "--extract-audio/--no-extract-audio", help="Extract audio only"),
):
    """Download and process YouTube audio"""
    from pydub_plus.workflows import YouTubeProcessor
    import asyncio
    
    processor = YouTubeProcessor()
    
    async def run():
        audio = await processor.download_audio(url)
        if output_file:
            await audio.export_async(output_file)
            console.print(f"[green]✓[/green] Audio saved to: {output_file}")
        else:
            console.print("[yellow]Audio downloaded but no output file specified[/yellow]")
    
    asyncio.run(run())


@app.command()
def tiktok(
    input_file: Path = typer.Argument(..., help="Input audio/video file"),
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", "-o", help="Output directory"),
    duration: int = typer.Option(60, "--duration", "-d", help="Clip duration in seconds"),
    format: str = typer.Option("mp3", "--format", "-f", help="Output format"),
):
    """Create TikTok-ready audio clips"""
    from pydub_plus.workflows import TikTokProcessor
    import asyncio
    
    output_dir = output_dir or Path("tiktok_clips")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processor = TikTokProcessor()
    
    async def run():
        clips = await processor.create_clips(str(input_file), duration=duration)
        await processor.export_for_tiktok(clips, str(output_dir), format=format)
        console.print(f"[green]✓[/green] Created {len(clips)} clips in: {output_dir}")
    
    asyncio.run(run())


if __name__ == "__main__":
    app()

