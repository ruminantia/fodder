# Configuration Guide

## Overview

This guide covers all configuration options available for fodder. The bot uses environment variables for configuration, making it easy to customize for different environments and use cases.

## Quick Start Configuration

### Basic Setup

1. **Copy the example configuration file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file with your credentials:**
   ```env
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   QWEN_API_KEY=your_qwen_api_key_here
   ```

3. **Start the bot:**
   ```bash
   ./run-docker.sh
   ```

## Environment Variables Reference

### Required Variables

#### `DISCORD_BOT_TOKEN`
- **Description**: Your Discord bot's authentication token
- **Format**: String (alphanumeric)
- **How to get**: From [Discord Developer Portal](https://discord.com/developers/applications)
- **Example**: `DISCORD_BOT_TOKEN=1234`

#### `QWEN_API_KEY`
- **Description**: API key for Qwen3 Omni transcription service
- **Format**: String (alphanumeric)
- **How to get**: From [DashScope](https://dashscope.aliyuncs.com/) or other Qwen provider
- **Example**: `QWEN_API_KEY=sk-whatever`

### Optional Configuration Variables

#### Audio Processing Settings

##### `AUDIO_CHUNK_LENGTH`
- **Description**: Maximum length of audio chunks in seconds
- **Default**: `20`
- **Range**: `10` to `60` seconds
- **Purpose**: Controls how long audio files are split for processing
- **Example**: `AUDIO_CHUNK_LENGTH=30`

##### `MAX_AUDIO_DURATION`
- **Description**: Maximum total audio duration to process (in seconds)
- **Default**: `600` (10 minutes)
- **Purpose**: Prevents processing extremely long files
- **Example**: `MAX_AUDIO_DURATION=1200`

#### API and Performance Settings

##### `TRANSCRIPTION_TIMEOUT`
- **Description**: Maximum time to wait for transcription API response (seconds)
- **Default**: `60`
- **Range**: `30` to `300` seconds
- **Purpose**: Prevents hanging on slow API responses
- **Example**: `TRANSCRIPTION_TIMEOUT=120`

##### `MAX_CONCURRENT_TRANSCRIPTIONS`
- **Description**: Maximum number of simultaneous transcription requests
- **Default**: `3`
- **Range**: `1` to `10`
- **Purpose**: Controls API rate limiting and resource usage
- **Example**: `MAX_CONCURRENT_TRANSCRIPTIONS=5`

#### Logging and Debugging

##### `LOG_LEVEL`
- **Description**: Controls the verbosity of logging output
- **Default**: `INFO`
- **Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`
- **Purpose**: Debugging and monitoring
- **Example**: `LOG_LEVEL=DEBUG`

##### `DEBUG`
- **Description**: Enable debug mode for detailed output
- **Default**: `false`
- **Options**: `true`, `false`
- **Purpose**: Extended logging and error details
- **Example**: `DEBUG=true`

#### File Management

##### `CLEANUP_INTERVAL`
- **Description**: How often to clean temporary files (minutes)
- **Default**: `60`
- **Purpose**: Prevents disk space accumulation
- **Example**: `CLEANUP_INTERVAL=30`

##### `KEEP_TRANSCRIPTIONS_DAYS`
- **Description**: How long to keep transcription files (days)
- **Default**: `30`
- **Purpose**: Automatic cleanup of old transcriptions
- **Example**: `KEEP_TRANSCRIPTIONS_DAYS=7`

## Advanced Configuration

### Docker Compose Customization

#### Resource Limits
Modify `docker-compose.yml` to set resource constraints:

```yaml
services:
  discord-bot:
    # ... existing configuration ...
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
```

#### Network Configuration
```yaml
services:
  discord-bot:
    # ... existing configuration ...
    networks:
      - fodder-network

networks:
  fodder-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

#### Volume Configuration
```yaml
services:
  discord-bot:
    # ... existing configuration ...
    volumes:
      - ./downloads:/app/downloads:rw
      - ./transcriptions:/app/transcriptions:rw
      - ./temp_chunks:/app/temp_chunks:rw
      - ./.env:/app/.env:ro
```

### Source Code Configuration

#### Audio Processing Parameters
Modify `src/audio_utils.py` for advanced audio handling:

```python
# Change default chunk length
def chunk_audio(audio_path: str, chunk_length_s: int = 30) -> list[str]:
    # Custom implementation
    pass

# Add custom format support
format_map = {
    "wav": "wav",
    "mp3": "mp3",
    "ogg": "ogg",
    "flac": "flac",
    "aac": "aac",
    "m4a": "mp4",
    "wma": "wma",
    "webm": "webm",  # Custom addition
}
```

#### Transcription Prompts
Customize prompts in `src/transcriber.py`:

```python
def _build_chunk_prompt(self, chunk_index: int, total_chunks: int, previous_context: Optional[str] = None) -> str:
    # Custom prompt templates
    if total_chunks == 1:
        return "Transcribe this audio with timestamps and speaker identification."
    # ... additional customizations
```

## Environment-Specific Configurations

### Development Environment

#### `.env.development`
```env
DISCORD_BOT_TOKEN=your_development_bot_token
QWEN_API_KEY=your_development_api_key
LOG_LEVEL=DEBUG
DEBUG=true
AUDIO_CHUNK_LENGTH=15
TRANSCRIPTION_TIMEOUT=90
```

### Production Environment

#### `.env.production`
```env
DISCORD_BOT_TOKEN=your_production_bot_token
QWEN_API_KEY=your_production_api_key
LOG_LEVEL=WARNING
DEBUG=false
AUDIO_CHUNK_LENGTH=20
TRANSCRIPTION_TIMEOUT=60
MAX_CONCURRENT_TRANSCRIPTIONS=2
```

### Testing Environment

#### `.env.testing`
```env
DISCORD_BOT_TOKEN=test_token
QWEN_API_KEY=test_api_key
LOG_LEVEL=ERROR
DEBUG=false
AUDIO_CHUNK_LENGTH=10
```

## Configuration Validation

### Validation Script
Create a validation script to check configuration:

```bash
#!/bin/bash
# config-validate.sh

echo "Validating configuration..."

# Check required variables
if [ -z "$DISCORD_BOT_TOKEN" ]; then
    echo "❌ DISCORD_BOT_TOKEN is missing"
    exit 1
fi

if [ -z "$QWEN_API_KEY" ]; then
    echo "❌ QWEN_API_KEY is missing"
    exit 1
fi

# Validate numeric values
if [ "$AUDIO_CHUNK_LENGTH" -lt 10 ] || [ "$AUDIO_CHUNK_LENGTH" -gt 60 ]; then
    echo "❌ AUDIO_CHUNK_LENGTH must be between 10 and 60"
    exit 1
fi

echo "✅ Configuration validated successfully"
```

### Health Check Endpoint
Add a health check to verify configuration:

```python
# In discord_bot.py
@client.event
async def on_message(message):
    if message.content == "!health":
        # Check configuration and system status
        health_status = check_health()
        await message.channel.send(f"Health status: {health_status}")
```

## Security Configuration

### Secure Credential Management

#### Using Docker Secrets
```yaml
services:
  discord-bot:
    # ... existing configuration ...
    secrets:
      - discord_bot_token
      - qwen_api_key

secrets:
  discord_bot_token:
    file: ./secrets/discord_token.txt
  qwen_api_key:
    file: ./secrets/qwen_key.txt
```

#### Environment File Permissions
```bash
# Set secure permissions on .env file
chmod 600 .env
chown $USER:www-data .env
```

### Network Security

#### Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
# Deny all other incoming traffic
sudo ufw default deny incoming
```

## Performance Tuning

### Memory Optimization

#### Docker Memory Settings
```yaml
services:
  discord-bot:
    # ... existing configuration ...
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

#### Python Garbage Collection
```python
# In main.py
import gc

# Configure garbage collection
gc.set_threshold(700, 10, 10)
```

### API Rate Limiting

#### Custom Rate Limiter
```python
# In transcriber.py
import asyncio
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_calls: int, period: int):
        self.max_calls = max_calls
        self.period = timedelta(seconds=period)
        self.calls = []

    async def acquire(self):
        now = datetime.now()
        # Remove old calls
        self.calls = [call for call in self.calls if now - call < self.period]

        if len(self.calls) >= self.max_calls:
            sleep_time = (self.calls[0] + self.period - now).total_seconds()
            await asyncio.sleep(max(0, sleep_time))
            self.calls.pop(0)

        self.calls.append(now)
```

## Monitoring Configuration

### Logging Setup

#### Structured Logging
```python
import logging
import json

# Configure JSON logging for better analysis
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        return json.dumps(log_entry)

# Apply formatter
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

### Metrics Collection

#### Custom Metrics
```python
# In discord_bot.py
import time

class Metrics:
    def __init__(self):
        self.transcriptions_started = 0
        self.transcriptions_completed = 0
        self.transcriptions_failed = 0
        self.average_processing_time = 0

    def record_transcription_start(self):
        self.transcriptions_started += 1
        self.start_time = time.time()

    def record_transcription_complete(self):
        self.transcriptions_completed += 1
        processing_time = time.time() - self.start_time
        # Update average
        self.average_processing_time = (
            (self.average_processing_time * (self.transcriptions_completed - 1) + processing_time)
            / self.transcriptions_completed
        )
```

## Troubleshooting Configuration Issues

### Common Problems and Solutions

#### "Module not found" Errors
- **Cause**: Incorrect Python path or missing dependencies
- **Solution**: Verify virtual environment activation and requirements installation

#### API Authentication Failures
- **Cause**: Invalid or expired API keys
- **Solution**: Check key validity and regenerate if necessary

#### File Permission Errors
- **Cause**: Incorrect directory permissions
- **Solution**: Ensure write permissions on data directories

#### Memory Exhaustion
- **Cause**: Processing very large files
- **Solution**: Reduce `AUDIO_CHUNK_LENGTH` or increase memory limits

### Diagnostic Commands

```bash
# Check environment variables
echo $DISCORD_BOT_TOKEN
echo $QWEN_API_KEY

# Verify file permissions
ls -la .env
ls -la downloads/ transcriptions/ temp_chunks/

# Check Docker container status
docker compose ps
docker compose logs
```

## Configuration Best Practices

1. **Use different tokens** for development and production
2. **Regularly rotate API keys** for security
3. **Monitor resource usage** and adjust limits accordingly
4. **Keep backups** of important configuration files
5. **Use version control** for configuration changes (excluding secrets)
6. **Test configuration changes** in a staging environment first

This configuration guide provides comprehensive coverage of all customization options. For operational guidance, see the [Usage Guide](usage.md). For troubleshooting specific issues, refer to the [Troubleshooting Guide](troubleshooting.md).
