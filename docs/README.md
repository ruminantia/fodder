# Fodder - Documentation

Welcome to the Fodder documentation! This project is a sophisticated Discord bot designed for audio transcription using the Qwen3 Omni model with intelligent chunk-aware processing.

## Documentation Structure

- **[Overview](overview.md)** - Project introduction and high-level architecture
- **[Installation Guide](installation.md)** - Complete setup instructions
- **[Configuration](configuration.md)** - Environment setup and customization
- **[Usage Guide](usage.md)** - How to use the bot effectively
- **[Development](development.md)** - Contributing and development guidelines
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[API Reference](api.md)** - Technical API documentation

## Quick Links

- [Project Repository](../README.md)
- [Docker Compose File](../docker-compose.yml)
- [Main Application Entry Point](../main.py)

## Features

- **Audio Transcription**: Automatic transcription of audio files sent to Discord
- **Smart Chunking**: Intelligent splitting of long audio files with context preservation
- **Async Processing**: Non-blocking operations to prevent Discord heartbeat issues
- **Docker Support**: Full containerization with Docker and Docker Compose
- **Channel-Specific Processing**: Dedicated #fodder channel for organized workflow
- **Message Splitting**: Automatic handling of Discord's 2000-character limit

## Project Structure

```
fodder/
├── src/                    # Source code
│   ├── discord_bot.py      # Discord bot implementation
│   ├── transcriber.py      # Audio transcription logic
│   └── audio_utils.py      # Audio processing utilities
├── docs/                   # This documentation
├── downloads/              # Temporary audio downloads
├── transcriptions/         # Completed transcriptions
├── temp_chunks/           # Temporary audio chunks
└── Configuration files
```

## Getting Started

1. **Quick Start**: See [Installation Guide](installation.md) for Docker setup
2. **Manual Setup**: Follow the manual installation instructions
3. **Configuration**: Set up your environment variables in [Configuration](configuration.md)
4. **Usage**: Learn how to use the bot in [Usage Guide](usage.md)

## Support

If you encounter issues:
1. Check the [Troubleshooting](troubleshooting.md) guide
2. Review the [Configuration](configuration.md) documentation
3. Examine the application logs using `./run-docker.sh logs`

## Contributing

Interested in contributing? Please see our [Development](development.md) guide for:
- Code standards
- Testing procedures
- Pull request guidelines

## License

This project is licensed under the terms specified in the main repository's LICENSE file (MIT).
