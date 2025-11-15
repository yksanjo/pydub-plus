# Contributing to pydub-plus

Thank you for your interest in contributing to pydub-plus! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/pydub-plus.git
   cd pydub-plus
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks (optional):**
   ```bash
   pre-commit install
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where possible
- Format code with `black` (line length: 100)
- Lint with `ruff`
- Type check with `mypy`

```bash
# Format code
black pydub_plus tests examples

# Lint
ruff check pydub_plus tests examples

# Type check
mypy pydub_plus
```

## Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Aim for good test coverage

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=pydub_plus --cov-report=html
```

## Submitting Changes

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write code
   - Add tests
   - Update documentation

3. **Commit your changes:**
   ```bash
   git commit -m "Add: description of your feature"
   ```

4. **Push and create a Pull Request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Pull Request Guidelines

- Provide a clear description of changes
- Reference any related issues
- Ensure tests pass
- Update documentation as needed
- Keep PRs focused and reasonably sized

## Areas for Contribution

- GPU acceleration improvements
- Additional async operations
- New workflow modules
- Performance optimizations
- Documentation improvements
- Bug fixes
- Test coverage

## Questions?

Open an issue for questions or discussions about contributions.

Thank you for contributing! 🎉

