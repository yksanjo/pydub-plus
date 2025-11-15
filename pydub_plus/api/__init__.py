"""
REST API for audio processing
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import tempfile
from pathlib import Path
from pydub_plus.core import AudioSegment
from pydub_plus.async_ops import AudioSegmentAsync
import asyncio


def create_app() -> FastAPI:
    """Create FastAPI application"""
    app = FastAPI(
        title="pydub-plus API",
        description="REST API for audio processing with GPU acceleration and async support",
        version="0.1.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def root():
        return {
            "name": "pydub-plus API",
            "version": "0.1.0",
            "endpoints": {
                "process": "/api/process",
                "normalize": "/api/normalize",
                "convert": "/api/convert",
                "health": "/api/health"
            }
        }
    
    @app.get("/api/health")
    async def health():
        """Health check endpoint"""
        from pydub_plus.gpu import is_gpu_available
        return {
            "status": "healthy",
            "gpu_available": is_gpu_available()
        }
    
    @app.post("/api/process")
    async def process_audio(
        file: UploadFile = File(...),
        operation: str = Form("normalize"),
        format: Optional[str] = Form(None)
    ):
        """
        Process audio file with various operations
        
        Operations: normalize, fade_in, fade_out, high_pass, low_pass
        """
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            # Load audio
            audio_async = await AudioSegmentAsync.from_file_async(tmp_path)
            
            # Apply operation
            if operation == "normalize":
                result = await audio_async.normalize_async()
            elif operation == "fade_in":
                result = await audio_async.fade_in_async(2000)
            elif operation == "fade_out":
                result = await audio_async.fade_out_async(2000)
            elif operation == "high_pass":
                result = await audio_async.high_pass_filter_async(3000)
            elif operation == "low_pass":
                result = await audio_async.low_pass_filter_async(3000)
            else:
                raise HTTPException(status_code=400, f"Unknown operation: {operation}")
            
            # Export to temporary file
            output_format = format or Path(file.filename).suffix[1:] or "mp3"
            output_path = Path(tmp_path).with_suffix(f".{output_format}")
            await result.export_async(output_path, format=output_format)
            
            return FileResponse(
                str(output_path),
                media_type=f"audio/{output_format}",
                filename=f"processed.{output_format}"
            )
        finally:
            # Cleanup
            Path(tmp_path).unlink(missing_ok=True)
    
    @app.post("/api/normalize")
    async def normalize_audio(
        file: UploadFile = File(...),
        headroom: float = Form(0.1),
        format: Optional[str] = Form(None)
    ):
        """Normalize audio file"""
        return await process_audio(file, operation="normalize", format=format)
    
    @app.post("/api/convert")
    async def convert_audio(
        file: UploadFile = File(...),
        format: str = Form(...)
    ):
        """Convert audio format"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            audio_async = await AudioSegmentAsync.from_file_async(tmp_path)
            output_path = Path(tmp_path).with_suffix(f".{format}")
            await audio_async.export_async(output_path, format=format)
            
            return FileResponse(
                str(output_path),
                media_type=f"audio/{format}",
                filename=f"converted.{format}"
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    
    return app


def main():
    """CLI entry point for API server"""
    import uvicorn
    uvicorn.run("pydub_plus.api:create_app", factory=True, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()

