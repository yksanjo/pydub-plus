"""CLI for API server"""

import uvicorn
import typer

app = typer.Typer()


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    reload: bool = typer.Option(False, help="Enable auto-reload"),
):
    """Start the pydub-plus API server"""
    from pydub_plus.api import create_app
    
    uvicorn.run(
        create_app,
        factory=True,
        host=host,
        port=port,
        reload=reload
    )


def main():
    app()


if __name__ == "__main__":
    main()

