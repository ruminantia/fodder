# Fodder - Discord Audio Transcription Bot

<div align="center">

![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)
![Python](https://img.shields.io/badge/python-3.13+-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Qwen](https://img.shields.io/badge/Qwen3--Omni-AI%20Transcription-blue?style=for-the-badge)

A sophisticated Discord bot for high-quality audio transcription using state-of-the-art AI with intelligent chunk-aware processing and context preservation. Features separate input/output channels, reaction-based status updates, and multi-container volume sharing for easy integration with other services.

[📚 Documentation](docs/README.md)

[🚀 Quick Start](docs/overview.md)

[⚙️ Configuration](docs/configuration.md)

[🐛 Issues](https://github.com/ruminantia/fodder/issues)

</div>

## ✨ Features

### 🎯 Intelligent Audio Processing
- **Smart Chunking**: Automatically splits long audio files (>20 seconds) with context preservation
- **Multi-Format Support**: WAV, MP3, OGG, FLAC, AAC, M4A, WMA formats
- **Context-Aware Transcription**: Maintains narrative continuity across multiple chunks
- **Quality Optimization**: WAV processing for optimal transcription quality

### 🤖 Seamless Discord Integration
- **Dual-Channel Workflow**: Input in #fodder channel, output in #transcriptions channel
- **Status Reactions**: Real-time emoji reactions (⏳/✅/❌) for processing status
- **Async Processing**: Non-blocking operations prevent Discord heartbeat issues
- **Message Splitting**: Automatic handling of Discord's 2000-character limit
- **Error Resilience**: Continues processing even if individual chunks fail

### 🐳 Production-Ready Deployment
- **Docker Containerization**: Full container support with Docker Compose
- **Persistent Storage**: Data preservation across container restarts
- **Multi-Container Access**: Named volumes for easy integration with other services
- **Auto-Restart**: Automatic recovery from failures
- **Comprehensive Logging**: Detailed monitoring and debugging capabilities

## 🚀 Quick Start

### Prerequisites
- **Discord Bot Token** from [Discord Developer Portal](https://discord.com/developers/applications)
- **Qwen API Key** from [DashScope](https://dashscope.aliyuncs.com/) or other provider
- **Docker** and **Docker Compose** (recommended) or **Python 3.13+**

### Docker Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/ruminantia/fodder.git
cd fodder

# Configure environment
cp .env.example .env
# Edit .env with your Discord bot token and Qwen API key

# Start the bot
./run-docker.sh
```

### Manual Installation

```bash
# Clone and setup
git clone https://github.com/ruminantia/fodder.git
cd fodder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS: venv\Scripts\activate (Windows)

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg (required for audio processing)
# Ubuntu/Debian: sudo apt install ffmpeg
# macOS: brew install ffmpeg
# Windows: choco install ffmpeg

# Configure and run
cp .env.example .env
# Edit .env with your credentials
mkdir -p downloads fodder temp_chunks
python main.py
```

## 📖 Usage

1. **Invite your bot** to a Discord server with appropriate permissions
2. **Create two dedicated channels**: `#fodder` (for audio uploads) and `#transcriptions` (for results)
3. **Upload audio files** to the #fodder channel
4. **Receive transcriptions** automatically in the #transcriptions channel with status reactions

### Supported Audio Formats
- **WAV** (recommended for best quality)
- **MP3**, **OGG**, **FLAC**, **AAC**, **M4A**, **WMA**

### Status Reactions
The bot provides real-time feedback using emoji reactions:
- **⏳** (Hourglass): Processing started
- **✅** (Checkmark): Transcription completed successfully
- **❌** (Red X): Error occurred during processing

## 🎥 Demonstration

https://github.com/user-attachments/assets/93151d06-2fbd-4a5b-9736-d2a80d086edd



https://github.com/user-attachments/assets/2efad0b4-4481-4aa0-a6e3-22fd8d7f9f11



```
This is a clear, high-quality audio recording of a male speaker. He has a neutral, conversational tone and speaks at a moderate pace.

He states, "I'm just uh demonstrating fodder for my GitHub README." The word "uh" is audible, indicating a slight hesitation in his speech. The content of his statement is specific to the software development community, as a "GitHub README" is a standard file used to describe a project on the GitHub platform. The background is very quiet, with only a faint, low-level hum barely perceptible, suggesting a typical indoor recording environment.
```

## 🏗️ Project Structure

```
fodder/
├── src/                    # Source code
│   ├── discord_bot.py      # Discord bot implementation
│   ├── transcriber.py      # Audio transcription logic
│   └── audio_utils.py      # Audio processing utilities
├── docs/                   # Comprehensive documentation
├── downloads/              # Temporary audio downloads
├── fodder/                 # Completed transcriptions (persistent)
├── temp_chunks/            # Temporary audio chunks
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── run-docker.sh           # Management script
├── test-volume-access.sh   # Volume access testing script
└── requirements.txt        # Python dependencies
```

## ⚙️ Configuration

### Environment Variables
```env
# Required
DISCORD_BOT_TOKEN=your_discord_bot_token_here
QWEN_API_KEY=your_qwen_api_key_here

# Optional
AUDIO_CHUNK_LENGTH=20          # Chunk size in seconds
TRANSCRIPTION_TIMEOUT=60       # API timeout in seconds
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR
```

### Docker Management
```bash
./run-docker.sh           # Start bot (detached mode)
./run-docker.sh logs      # View real-time logs
./run-docker.sh stop      # Stop the bot
./run-docker.sh attach    # Debug mode (attached)
./run-docker.sh status    # Check container status
./run-docker.sh build     # Rebuild Docker image
./run-docker.sh help      # Show all commands
```

### Multi-Container Volume Setup
The bot uses named volumes for persistent storage and multi-container access:

```yaml
# docker-compose.yml volume configuration
volumes:
  downloads:       # Bot-only: temporary audio downloads
  transcriptions:  # Shared: completed transcriptions (read/write for bot, read-only for others)
  temp:            # Bot-only: temporary audio chunks
```

**Access Patterns:**
- **Discord Bot**: Read/write access to all volumes
- **Other Containers**: Read-only access to `transcriptions` volume

### Channel Separation
The bot now uses a dual-channel workflow:
- **#fodder channel**: Upload audio files here
- **#transcriptions channel**: Receive completed transcriptions here
- **Status reactions**: Real-time feedback on processing status

**Testing Volume Access:**
```bash
# Run comprehensive volume access tests
./test-volume-access.sh

# Manual testing
docker-compose up -d
docker exec ruminantia-fodder ls -la /app/fodder
```

**Integrating with Other Services:**
```yaml
# Example: Another container accessing transcriptions
your-service:
  image: your-app:latest
  volumes:
    - transcriptions:/path/to/transcriptions:ro
  networks:
    - fodder-network
```

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](docs/README.md) directory:

- [**Overview**](docs/overview.md) - Project architecture and features
- [**Installation Guide**](docs/installation.md) - Complete setup instructions
- [**Configuration Guide**](docs/configuration.md) - Customization options
- [**Usage Guide**](docs/usage.md) - Operational instructions
- [**Development Guide**](docs/development.md) - Contributing guidelines
- [**Troubleshooting Guide**](docs/troubleshooting.md) - Common issues and solutions
- [**API Reference**](docs/api.md) - Technical API documentation

## 🐛 Troubleshooting

### Common Issues

**Bot won't start:**
```bash
# Check container status
./run-docker.sh status

# View logs for errors
./run-docker.sh logs
```

**Transcription failures:**
- Verify API keys in `.env` file
- Check audio file format and quality
- Review logs for specific error messages

**Permission errors:**
```bash
# Ensure directories exist
mkdir -p downloads fodder temp_chunks

# Set correct permissions
chmod 755 downloads fodder temp_chunks
```

For detailed troubleshooting, see the [Troubleshooting Guide](docs/troubleshooting.md).

## 🤝 Contributing

We welcome contributions! Please see our [Development Guide](docs/development.md) for:

- Code standards and conventions
- Testing procedures
- Pull request guidelines
- Development environment setup

### Development Quick Start
```bash
git clone https://github.com/ruminantia/fodder.git
cd fodder
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## 📊 Performance

- **Processing Speed**: 30-90 seconds per minute of audio
- **Concurrent Processing**: Up to 3 files simultaneously
- **Memory Usage**: ~200-500MB during processing
- **File Size Limit**: 25MB (Discord upload limit)
- **Duration Limit**: 10 minutes (configurable)

## 🔒 Security & Privacy

- **Local Processing**: Audio files processed locally before API calls
- **Temporary Storage**: Files automatically deleted after transcription
- **API Security**: Secure API key management through environment variables
- **Channel Isolation**: Processing confined to designated channel only

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Discord.py** for excellent Discord API integration
- **Qwen3 Omni** for state-of-the-art transcription capabilities
- **pydub/FFmpeg** for robust audio processing
- **Docker** for seamless containerization

---

<div align="center">

**Fodder** - Overkill transcription bot for discord. First stage of building our golden cow.

[📚 Documentation](docs/README.md) • [🐛 Report Issue](https://github.com/ruminantia/fodder/issues) • [💡 Feature Request](https://github.com/ruminantia/fodder/issues)

</div>
