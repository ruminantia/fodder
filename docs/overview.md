# Project Overview

## What is fodder?

Fodder is a sophisticated Discord bot designed for high-quality audio transcription using Qwen3 omni. The bot automatically processes audio files sent to a dedicated Discord channel.

## Key Features

### 🎯 Intelligent Audio Processing
- **Automatic Chunking**: Splits long audio files (>20 seconds) into manageable chunks
- **Context-Aware Transcription**: Maintains narrative continuity across multiple chunks
- **Multi-Format Support**: Handles WAV, MP3, OGG, FLAC, AAC, M4A, and WMA formats
- **Quality Preservation**: All audio is processed as WAV for optimal transcription quality

### 🤖 Smart Discord Integration
- **Channel-Specific Processing**: Only responds to audio in the dedicated #fodder channel
- **Message Splitting**: Automatically handles Discord's 2000-character message limit
- **Async Operations**: Non-blocking design prevents Discord heartbeat issues
- **Error Resilience**: Continues processing even if individual chunks fail

### 🐳 Production-Ready Deployment
- **Docker Containerization**: Full container support with Docker and Docker Compose
- **Persistent Storage**: Data preservation across container restarts
- **Auto-Restart**: Automatic recovery from failures

## Architecture Overview

### Core Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Discord Bot   │───▶│   Transcriber    │───▶│  Qwen3 Omni API │
│   (discord.py)  │    │  (AsyncOpenAI)   │    │   (DashScope)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│  Audio Utils    │    │  File Management │
│   (pydub/FFmpeg)│    │  (Local Storage) │
└─────────────────┘    └──────────────────┘
```

### Data Flow

1. **Audio Reception**: User uploads audio file to #fodder channel
2. **File Download**: Bot downloads audio to temporary storage
3. **Chunk Processing**: Long files are split into 20-second chunks
4. **Sequential Transcription**: Chunks are processed with context passing
5. **Result Assembly**: Transcripts are combined with chunk numbering
6. **Delivery**: Results sent back to Discord channel and saved locally

## Technology Stack

### Core Technologies
- **Python 3.13**: Primary programming language
- **discord.py**: Discord API integration
- **Qwen3 Omni**: AI transcription model via Alibaba DashScope API
- **pydub/FFmpeg**: Audio processing and format conversion

### Infrastructure
- **Docker**: Containerization and deployment
- **Docker Compose**: Container orchestration
- **Volume Mounts**: Persistent data storage

### Development Tools
- **Async/Await**: Non-blocking programming patterns
- **Type Hints**: Improved code readability and maintenance
- **Environment Variables**: Secure configuration management

## Performance Characteristics

### Processing Capabilities
- **Audio Length**: Handles files of any duration through intelligent chunking
- **Concurrency**: Supports multiple users simultaneously
- **Throughput**: Processes audio in real-time with minimal delay
- **Accuracy**: Leverages Qwen3 Omni's advanced transcription capabilities

### Resource Requirements
- **Memory**: Efficient memory usage through streaming processing
- **Storage**: Temporary files automatically cleaned up after processing
- **Network**: Optimized API calls with timeout handling

## Security & Privacy

### Data Handling
- **Local Processing**: Audio files processed locally before API calls
- **Temporary Storage**: Files automatically deleted after transcription
- **API Security**: Secure API key management through environment variables
- **Channel Isolation**: Processing confined to designated channel only

### Privacy Features
- **No Data Retention**: Transcripts only stored if explicitly saved by user
- **User Control**: Users control what audio gets processed
- **Transparent Operation**: Clear feedback on processing status

## Why fodder?

### Unique Advantages
- **Context Preservation**: Unlike simple transcription services, maintains narrative flow across chunks
- **Discord Integration**: Seamless workflow within existing Discord communities
- **Open Architecture**: Self-hosted solution with full control over data
- **Cost Effective**: No per-minute transcription fees after initial setup

### Comparison to Alternatives
- **vs. Cloud Services**: Full data control and no recurring costs
- **vs. Simple Bots**: Advanced chunking and context preservation
- **vs. Manual Processing**: Automated, consistent, and scalable

## Future Roadmap

### Planned Enhancements
- **Real-time Processing**: Live audio stream transcription
- **Advanced Format Support**: Video file audio extraction

### Community Contribution Ideas
- **Plugin System**: Extensible architecture for custom features
- **API Endpoints**: REST API for programmatic access
- **Web Interface**: Browser-based management dashboard

---
