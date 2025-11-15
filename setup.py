"""Setup script for pydub-plus"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="pydub-plus",
    version="0.1.0",
    description="Enhanced pydub with GPU acceleration, async processing, REST API, and batch workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/pydub-plus",
    packages=find_packages(exclude=["tests", "examples", "docs", "pydub-original"]),
    python_requires=">=3.8",
    install_requires=[
        # Note: pydub code is included in pydub_plus/core, so we don't need it as a dependency
        "numpy>=1.21.0",
        "aiofiles>=23.0.0",
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "python-multipart>=0.0.6",
        "click>=8.1.7",
        "rich>=13.7.0",
        "typer>=0.9.0",
        "yt-dlp>=2023.11.16",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
    ],
    extras_require={
        "gpu": [
            "cupy-cuda12x>=12.0.0",
        ],
        "all": [
            "cupy-cuda12x>=12.0.0",
            "moviepy>=1.0.3",
        ],
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.11.0",
            "ruff>=0.1.6",
            "mypy>=1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pydub-plus-api=pydub_plus.api.cli:main",
            "pydub-plus=pydub_plus.cli.main:app",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
    ],
    keywords="audio processing pydub gpu async api cli youtube tiktok",
)

