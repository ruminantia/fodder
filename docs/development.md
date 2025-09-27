# Development Guide

## Overview

This guide provides comprehensive information for developers who want to contribute to, extend, or modify fodder. It covers the codebase structure, development setup, coding standards, testing procedures, and contribution guidelines.

## Development Environment Setup

### Prerequisites

- **Python 3.13+** with pip
- **Docker** and **Docker Compose** (for containerized development)
- **Git** for version control
- **FFmpeg** for audio processing tests

### Quick Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ruminantia/fodder
   ```

2. **Set up development environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate  # Windows

   # Install development dependencies
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

3. **Configure development settings**:
   ```bash
   cp .env.example .env.development
   # Edit with development credentials
   ```

### Development with Docker

For consistent development environments:

```bash
# Build development image
docker compose -f docker-compose.dev.yml build

# Start development environment
docker compose -f docker-compose.dev.yml up -d

# Access development container
docker compose -f docker-compose.dev.yml exec discord-bot bash
```

## Codebase Architecture

### Project Structure

```
src/
├── __init__.py              # Package initialization
├── discord.py               # Discord bot implementation
├── transcriber.py           # Audio transcription logic
└── audio_utils.py           # Audio processing utilities

docs/                        # Documentation
scripts/                     # Development scripts
```

### Core Components

#### Discord Bot (`discord.py`)
- **Purpose**: Handles Discord API interactions
- **Key Classes**: `discord.Client` extension
- **Main Features**: Message handling, file processing, error management

#### Transcriber (`transcriber.py`)
- **Purpose**: Manages audio transcription using Qwen3 Omni
- **Key Classes**: `Transcriber`
- **Main Features**: Chunk-aware prompting, async processing, context passing

#### Audio Utilities (`audio_utils.py`)
- **Purpose**: Handles audio file processing and chunking
- **Key Functions**: `chunk_audio()`, `get_audio_format()`
- **Main Features**: Multi-format support, intelligent chunking

### Data Flow

1. **Message Reception** → Discord bot receives audio attachment
2. **File Processing** → Audio downloaded and chunked if necessary
3. **Transcription** → Chunks sent to Qwen API with context
4. **Result Assembly** → Transcripts combined and formatted
5. **Delivery** → Results sent to Discord and saved locally

## Coding Standards

### Python Style Guide

Follow **PEP 8** with these project-specific conventions:

#### Naming Conventions
```python
# Variables and functions
variable_name = "snake_case"
function_name()

# Classes
class ClassName:  # PascalCase
    def method_name(self):  # snake_case
        pass

# Constants
CONSTANT_NAME = "UPPER_SNAKE_CASE"
```

#### Type Hints
```python
def process_audio(
    audio_path: str,
    chunk_length: int = 20
) -> List[str]:
    """Process audio file and return chunk paths."""
    pass
```

#### Documentation Standards

**Module Docstrings**:
```python
"""
Audio processing utilities for Ruminantia Fodder.

This module provides functions for handling various audio formats,
chunking long files, and preparing audio for transcription.
"""
```

**Function Docstrings**:
```python
def chunk_audio(audio_path: str, chunk_length_s: int = 20) -> list[str]:
    """
    Split audio file into smaller chunks if it exceeds specified duration.

    Args:
        audio_path: Path to the audio file to process
        chunk_length_s: Maximum chunk length in seconds (default: 20)

    Returns:
        List of paths to audio chunk files

    Raises:
        AudioProcessingError: If audio file cannot be processed
    """
```

### Async/Await Patterns

Use async/await for all I/O operations:

```python
async def process_message(message: discord.Message) -> None:
    """Process incoming Discord message asynchronously."""
    try:
        # Async file operations
        await message.attachments[0].save("temp_audio.wav")

        # Async API calls
        transcription = await transcriber.transcribe("temp_audio.wav")

        # Async Discord responses
        await message.channel.send(f"Transcription: {transcription}")

    except Exception as e:
        logger.error(f"Message processing failed: {e}")
```

### Error Handling

**Use specific exceptions**:
```python
class AudioProcessingError(Exception):
    """Base exception for audio processing errors."""
    pass

class TranscriptionError(Exception):
    """Exception for transcription failures."""
    pass
```

**Proper error handling**:
```python
try:
    result = await risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise ProcessingError("Failed to process audio") from e
except AnotherError as e:
    # Handle differently
    pass
finally:
    await cleanup_resources()
```

## Testing

### Test Structure

#### Unit Tests
```python
# tests/test_audio_utils.py
import pytest
from src.audio_utils import chunk_audio

class TestAudioUtils:
    def test_chunk_audio_short_file(self, tmp_path):
        """Test that short files are not chunked."""
        # Test implementation
        pass

    def test_chunk_audio_long_file(self):
        """Test that long files are properly chunked."""
        pass
```

#### Integration Tests
```python
# tests/test_transcriber.py
class TestTranscriberIntegration:
    @pytest.mark.asyncio
    async def test_transcribe_with_mock_api(self):
        """Test transcription with mocked API responses."""
        pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_audio_utils.py

# Run with coverage
pytest --cov=src

# Run with specific markers
pytest -m "not slow"
```

### Mocking External Services

```python
@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    with patch('src.transcriber.AsyncOpenAI') as mock:
        mock_instance = mock.return_value
        # Configure mock responses
        yield mock_instance

@pytest.mark.asyncio
async def test_transcribe_success(mock_openai_client):
    """Test successful transcription."""
    # Test implementation with mocked client
    pass
```

## Development Workflow

### Feature Development

1. **Create feature branch**:
   ```bash
   git checkout -b feature/audio-format-support
   ```

2. **Implement changes** with tests:
   ```python
   # Add new functionality
   # Write corresponding tests
   ```

3. **Run tests and linting**:
   ```bash
   pytest
   flake8 src/
   mypy src/
   ```

4. **Update documentation**:
   ```bash
   # Update relevant docs
   # Add changelog entry if needed
   ```

### Code Review Process

1. **Create pull request** with clear description
2. **Ensure all tests pass**
3. **Update documentation** if needed
4. **Request review** from maintainers
5. **Address feedback** and make necessary changes

### Commit Message Convention

Use conventional commit messages:
```
feat: add support for WEBM audio format
fix: resolve memory leak in audio chunking
docs: update API documentation
test: add integration tests for transcriber
refactor: improve error handling in discord.py
```

## Debugging and Troubleshooting

### Common Development Issues

#### Docker Issues
```bash
# Clean rebuild
docker compose down
docker system prune -a
docker compose build --no-cache

# Debug container
docker compose logs -f
docker compose exec discord-bot bash
```

#### Python Dependency Issues
```bash
# Clear cache and reinstall
pip cache purge
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

### Debugging Techniques

#### Logging Configuration
```python
import logging

# Development logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

#### Interactive Debugging
```python
import pdb

def problematic_function():
    # Set breakpoint
    pdb.set_trace()
    # Debug interactively
```

## Performance Optimization

### Code Profiling

```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()

    # Code to profile

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

### Memory Optimization

```python
import tracemalloc

def check_memory_usage():
    tracemalloc.start()

    # Code to monitor

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    for stat in top_stats[:10]:
        print(stat)
```

## API Development

### Adding New Features

#### Example: Adding New Audio Format
1. **Update format mapping** in `audio_utils.py`
2. **Add tests** for the new format
3. **Update documentation** with supported formats
4. **Test with sample files**

#### Example: Adding Bot Command
1. **Add command handler** in `discord.py`
2. **Implement command logic**
3. **Add help text** and documentation
4. **Test command functionality**

### Extension Points

#### Custom Transcription Providers
```python
class CustomTranscriber(Transcriber):
    """Custom transcriber implementation."""

    async def transcribe(self, audio_path: str) -> str:
        """Custom transcription logic."""
        # Implementation
        pass
```

#### Audio Processing Plugins
```python
def custom_audio_processor(audio_path: str) -> AudioSegment:
    """Custom audio processing logic."""
    # Implementation
    pass
```

## Security Considerations

### Code Security

- **Never hardcode API keys** - use environment variables
- **Validate all user inputs** before processing
- **Use secure file handling** practices
- **Regular dependency updates** for security patches

### API Security

```python
# Secure API key handling
api_key = os.getenv('QWEN_API_KEY')
if not api_key:
    raise SecurityError("API key not configured")

# Input validation
def validate_audio_file(file_path: str) -> bool:
    """Validate audio file before processing."""
    # Check file type, size, etc.
    pass
```

## Deployment Considerations

### Development vs Production

**Development Configuration**:
```python
# Development-specific settings
DEBUG = True
LOG_LEVEL = 'DEBUG'
API_TIMEOUT = 120  # Longer timeouts for debugging
```

**Production Configuration**:
```python
# Production-specific settings
DEBUG = False
LOG_LEVEL = 'WARNING'
API_TIMEOUT = 60  # Shorter timeouts for reliability
```

### Environment-Specific Code

```python
import os

if os.getenv('ENVIRONMENT') == 'development':
    # Development-specific code
    enable_debug_logging()
else:
    # Production code
    enable_production_logging()
```

## Contributing Guidelines

### Before Contributing

1. **Check existing issues** and pull requests
2. **Discuss major changes** with maintainers first
3. **Ensure code quality** meets project standards
4. **Test thoroughly** on different environments

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass for all affected functionality
- [ ] Documentation updated if needed
- [ ] Changelog entry added for significant changes
- [ ] No breaking changes without major version bump

### Maintenance Responsibilities

- **Regular dependency updates**
- **Security vulnerability monitoring**
- **Performance monitoring and optimization**
- **User issue triage and resolution**

This development guide provides comprehensive information for contributing to Ruminantia Fodder. For operational guidance, see the [Usage Guide](usage.md). For configuration details, refer to the [Configuration Guide](configuration.md).
