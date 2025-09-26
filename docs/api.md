# API Reference

## Overview

This document provides comprehensive technical reference for fodder's API interfaces, classes, methods, and configuration options. This is intended for developers extending or integrating with the bot.

## Table of Contents

- [Core Classes](#core-classes)
- [Discord Bot API](#discord-bot-api)
- [Transcriber API](#transcriber-api)
- [Audio Utilities API](#audio-utilities-api)
- [Configuration API](#configuration-api)
- [Error Handling](#error-handling)
- [Event System](#event-system)

## Core Classes

### Transcriber Class

The main class responsible for audio transcription using Qwen3 Omni model.

#### Constructor
```python
Transcriber() -> Transcriber
```
Initializes the transcriber with API credentials from environment variables.

**Raises:**
- `ValueError`: If QWEN_API_KEY environment variable is not set

#### Methods

##### `transcribe(audio_path, chunk_index=0, total_chunks=1, previous_context=None, timeout=60)`
```python
async transcribe(
    audio_path: str,
    chunk_index: int = 0,
    total_chunks: int = 1,
    previous_context: Optional[str] = None,
    timeout: int = 60
) -> str
```
Transcribes a single audio chunk using context-aware prompts.

**Parameters:**
- `audio_path` (str): Path to audio file
- `chunk_index` (int): 0-based index of current chunk
- `total_chunks` (int): Total number of chunks
- `previous_context` (Optional[str]): Transcription from previous chunks
- `timeout` (int): Maximum seconds to wait for API response

**Returns:**
- `str`: Transcribed text or error message

**Raises:**
- `asyncio.TimeoutError`: If transcription exceeds timeout
- `Exception`: For other transcription failures

##### `transcribe_chunks(chunk_paths)`
```python
async transcribe_chunks(chunk_paths: List[str]) -> str
```
Transcribes multiple audio chunks with sequential context passing.

**Parameters:**
- `chunk_paths` (List[str]): List of paths to audio chunk files

**Returns:**
- `str`: Combined transcription with chunk numbering

#### Internal Methods

##### `_encode_audio(audio_path)`
```python
_encode_audio(audio_path: str) -> str
```
Encodes audio file to base64 for API transmission.

##### `_build_chunk_prompt(chunk_index, total_chunks, previous_context)`
```python
_build_chunk_prompt(
    chunk_index: int,
    total_chunks: int,
    previous_context: Optional[str] = None
) -> str
```
Constructs context-aware prompt based on chunk position.

## Discord Bot API

### Client Configuration
```python
client = discord.Client(intents=discord.Intents.default())
```
Discord client with message content intent enabled.

### Event Handlers

#### `on_ready()`
```python
@client.event
async def on_ready()
```
Called when bot successfully connects to Discord. Prints login confirmation.

#### `on_message(message)`
```python
@client.event
async def on_message(message: discord.Message)
```
Main message handler that processes audio attachments in #fodder channel.

**Processing Flow:**
1. Validates message is in #fodder channel
2. Checks for audio attachments
3. Downloads and processes audio files
4. Sends transcriptions back to channel
5. Cleans up temporary files

## Audio Utilities API

### `get_audio_format(filename)`
```python
get_audio_format(filename: str) -> str
```
Detects audio format based on file extension.

**Supported Formats:**
- `wav`, `mp3`, `ogg`, `flac`, `aac`, `m4a`, `wma`

**Parameters:**
- `filename` (str): Audio filename with extension

**Returns:**
- `str`: Format string recognized by pydub

### `chunk_audio(audio_path, chunk_length_s=20)`
```python
chunk_audio(audio_path: str, chunk_length_s: int = 20) -> List[str]
```
Splits audio file into smaller chunks if longer than specified duration.

**Parameters:**
- `audio_path` (str): Path to audio file
- `chunk_length_s` (int): Maximum chunk length in seconds (default: 20)

**Returns:**
- `List[str]`: List of paths to audio chunk files

**Behavior:**
- Returns single-element list if audio is shorter than chunk length
- Splits into multiple chunks for longer audio
- All chunks exported as WAV format for API compatibility

## Configuration API

### Environment Variables

#### Required Variables

##### `DISCORD_BOT_TOKEN`
- **Type**: `str`
- **Description**: Discord bot authentication token
- **Source**: Discord Developer Portal

##### `QWEN_API_KEY`
- **Type**: `str`
- **Description**: Qwen3 Omni API key
- **Source**: DashScope or other Qwen provider

#### Optional Variables

##### `AUDIO_CHUNK_LENGTH`
- **Type**: `int`
- **Default**: `20`
- **Range**: `10` - `60`
- **Description**: Maximum audio chunk length in seconds

##### `TRANSCRIPTION_TIMEOUT`
- **Type**: `int`
- **Default**: `60`
- **Range**: `30` - `300`
- **Description**: API response timeout in seconds

##### `LOG_LEVEL`
- **Type**: `str`
- **Default**: `"INFO"`
- **Options**: `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`
- **Description**: Logging verbosity level

### Docker Configuration

#### Volume Mounts
- `./downloads:/app/downloads` - Temporary audio storage
- `./transcriptions:/app/transcriptions` - Completed transcriptions
- `./temp_chunks:/app/temp_chunks` - Audio chunks during processing
- `./.env:/app/.env:ro` - Read-only environment configuration

#### Network Configuration
- Custom `fodder-network` with bridge driver
- Isolated network for security

## Error Handling

### Custom Exceptions

#### `AudioProcessingError`
```python
class AudioProcessingError(Exception):
    """Base exception for audio processing failures."""
```
Raised when audio files cannot be processed.

#### `TranscriptionError`
```python
class TranscriptionError(Exception):
    """Exception for transcription API failures."""
```
Raised when transcription API calls fail.

### Error Recovery

#### Graceful Degradation
- Individual chunk failures don't stop entire processing
- Error messages included in final transcription
- Processing continues with remaining chunks

#### Timeout Handling
- Configurable timeout prevents indefinite blocking
- Timeout errors logged with specific chunk information
- Bot remains responsive during long processing

## Event System

### Processing Events

#### Audio Download Event
- Triggered when audio file is received
- Includes file metadata and user information
- Opportunity for pre-processing validation

#### Chunk Processing Event
- Triggered for each audio chunk
- Includes chunk index and total chunks
- Allows custom chunk processing logic

#### Transcription Complete Event
- Triggered when transcription is finished
- Includes final transcription text
- Opportunity for post-processing

### Custom Event Handlers

#### Adding Custom Handlers
```python
@client.event
async def on_audio_processed(audio_file, transcription):
    """Custom handler for processed audio."""
    # Custom logic here
    pass
```

## Data Structures

### Audio Chunk Object
```python
@dataclass
class AudioChunk:
    path: str
    index: int
    total_chunks: int
    duration: float
    format: str
```
Represents a single audio chunk during processing.

### Transcription Result
```python
@dataclass
class TranscriptionResult:
    text: str
    confidence: float
    processing_time: float
    chunk_info: Optional[AudioChunk]
```
Contains transcription results with metadata.

## Performance Metrics

### Available Metrics

#### Processing Time
- Individual chunk processing duration
- Total transcription time
- API response time

#### Resource Usage
- Memory consumption during processing
- CPU utilization
- Disk I/O operations

#### Quality Metrics
- Transcription accuracy (if ground truth available)
- Chunk processing success rate
- Error frequency and types

### Monitoring Endpoints

#### Health Check
```python
async def get_health_status() -> Dict[str, Any]:
    """Returns system health information."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "uptime": get_uptime(),
        "queue_length": get_queue_length()
    }
```

#### Metrics Endpoint
```python
async def get_metrics() -> Dict[str, Any]:
    """Returns performance metrics."""
    return {
        "transcriptions_processed": get_processed_count(),
        "average_processing_time": get_avg_processing_time(),
        "error_rate": get_error_rate()
    }
```

## Extension Points

### Custom Transcription Providers

#### Implementing Custom Provider
```python
class CustomTranscriber:
    async def transcribe(self, audio_path: str) -> str:
        """Custom transcription implementation."""
        # Implementation here
        pass
```

### Audio Processing Plugins

#### Custom Audio Processor
```python
def custom_audio_processor(audio_path: str) -> AudioSegment:
    """Custom audio processing logic."""
    # Implementation here
    pass
```

This API reference provides comprehensive technical documentation for developers working with Ruminantia Fodder. For usage instructions, see the [Usage Guide](usage.md). For configuration details, refer to the [Configuration Guide](configuration.md).
