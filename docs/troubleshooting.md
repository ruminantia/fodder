# Troubleshooting Guide

## Overview

This guide provides solutions to common issues encountered when using fodder. Follow the steps below to diagnose and resolve problems with the bot's operation.

## Quick Diagnosis

### First Steps for Any Issue

1. **Check bot status**:
   ```bash
   ./run-docker.sh status
   ```

2. **View recent logs**:
   ```bash
   ./run-docker.sh logs --tail=50
   ```

3. **Verify configuration**:
   ```bash
   # Check environment file exists
   ls -la .env

   # Verify required variables are set
   grep -E "(DISCORD_BOT_TOKEN|QWEN_API_KEY)" .env
   ```

## Common Issues and Solutions

### Bot Won't Start

#### Symptoms
- Container fails to start
- Bot doesn't appear online in Discord
- Error messages during startup

#### Solutions

**Issue: Missing .env file**
```
Error: .env file not found!
```
**Fix**:
```bash
cp .env.example .env
# Edit .env with your actual credentials
nano .env
```

**Issue: Invalid API credentials**
```
discord.errors.LoginFailure: Improper token has been passed.
```
**Fix**:
1. Verify Discord bot token is correct
2. Check Qwen API key validity
3. Ensure tokens are not expired

**Issue: Port conflicts**
```
Error: port 80 is already in use
```
**Fix**:
Modify `docker-compose.yml` to use different ports or stop conflicting services.

### Bot Starts But Doesn't Respond

#### Symptoms
- Bot appears online but ignores messages
- No response to audio files in #fodder channel
- No error messages in logs

#### Solutions

**Issue: Incorrect channel permissions**
**Fix**:
1. Ensure bot has "Read Messages" permission in #fodder channel
2. Verify bot can send messages in the channel
3. Check channel-specific permission overrides

**Issue: Message intent not enabled**
**Fix**:
1. Go to Discord Developer Portal
2. Select your application
3. Enable "Message Content Intent" in Bot settings
4. Re-invite bot to server with new permissions

**Issue: Bot not in correct channel**
**Fix**:
- Ensure you're using the dedicated #fodder channel
- The bot only processes messages in this specific channel

### Audio Processing Failures

#### Symptoms
- Audio files are ignored
- "Error processing audio attachment" messages
- Partial transcriptions or timeouts

#### Solutions

**Issue: Unsupported audio format**
```
Error: Could not decode audio file
```
**Fix**:
- Convert audio to supported format (WAV, MP3, OGG, FLAC, AAC, M4A, WMA)
- Use recommended WAV format for best results

**Issue: File too large**
```
Error: File exceeds 25MB limit
```
**Fix**:
- Compress audio file
- Split into smaller segments
- Reduce audio quality settings

**Issue: FFmpeg not available**
```
Error: ffmpeg/avconv not found
```
**Fix**:
```bash
# Install FFmpeg
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
choco install ffmpeg     # Windows
```

### Transcription Quality Issues

#### Symptoms
- Poor transcription accuracy
- Missing or garbled text
- Incomplete transcriptions

#### Solutions

**Issue: Poor audio quality**
**Fix**:
- Use better microphone
- Reduce background noise
- Ensure clear speaking voice
- Use WAV format instead of compressed formats

**Issue: Audio too long**
**Fix**:
- Break long audio into smaller segments
- Use optimal 2-5 minute segments
- Consider manual segmentation for very long content

**Issue: Multiple speakers**
**Fix**:
- The bot works best with single speakers
- For multiple speakers, ensure clear separation
- Consider post-processing to identify speakers

### Performance Issues

#### Symptoms
- Slow processing times
- High memory or CPU usage
- Bot becoming unresponsive

#### Solutions

**Issue: Too many concurrent processes**
**Fix**:
- Reduce `MAX_CONCURRENT_TRANSCRIPTIONS` in .env
- Process files sequentially instead of simultaneously
- Increase system resources if available

**Issue: Large audio files**
**Fix**:
- Use smaller audio segments
- Increase `AUDIO_CHUNK_LENGTH` for fewer API calls
- Optimize audio quality settings

**Issue: API rate limiting**
**Fix**:
- Increase `TRANSCRIPTION_TIMEOUT` in .env
- Implement delays between processing
- Contact API provider for higher limits

### Docker-Specific Issues

#### Symptoms
- Container crashes or restarts
- Volume mount errors
- Permission denied errors

#### Solutions

**Issue: Volume permission errors**
```
Error: permission denied for volume mount
```
**Fix**:
```bash
# Ensure directories exist and have correct permissions
mkdir -p downloads fodder temp_chunks
chmod 755 downloads fodder temp_chunks
```

**Issue: Container resource limits**
```
Error: container killed due to memory exhaustion
```
**Fix**:
Modify `docker-compose.yml` to increase resource limits:
```yaml
services:
  discord-bot:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
```

**Issue: Docker daemon not running**
```
Error: Cannot connect to the Docker daemon
```
**Fix**:
```bash
# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Network and API Issues

#### Symptoms
- API timeout errors
- Network connection failures
- SSL certificate errors

#### Solutions

**Issue: API authentication failures**
```
HTTP 401: Unauthorized
```
**Fix**:
- Verify API keys are correct and not expired
- Check API provider status page
- Ensure proper API endpoint configuration

**Issue: Network timeouts**
```
asyncio.TimeoutError
```
**Fix**:
- Increase `TRANSCRIPTION_TIMEOUT` in .env
- Check network connectivity to API endpoints
- Verify firewall settings

**Issue: SSL certificate problems**
```
SSL: CERTIFICATE_VERIFY_FAILED
```
**Fix**:
- Update system certificates
- Check system time and date settings
- Temporarily disable SSL verification for testing (not recommended for production)

## Diagnostic Commands

### System Health Check
```bash
# Check Docker system status
docker system df
docker stats ruminantia-fodder

# Check disk space
df -h
du -sh downloads/ fodder/ temp_chunks/

# Check memory usage
free -h
```

### Log Analysis
```bash
# View real-time logs
./run-docker.sh logs -f

# Search for specific errors
docker compose logs | grep -i error
docker compose logs | grep -i timeout

# Export logs for analysis
docker compose logs > bot_logs.txt
```

### Configuration Verification
```bash
# Check environment variables
docker compose exec discord-bot env | grep -E "(TOKEN|KEY|API)"

# Verify file permissions
docker compose exec discord-bot ls -la /app/

# Test API connectivity
docker compose exec discord-bot python -c "
import os
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key=os.getenv('QWEN_API_KEY'))
print('API connection test passed')
"
```

## Advanced Troubleshooting

### Debug Mode
Enable detailed logging for complex issues:

```bash
# Set debug mode in .env
echo "DEBUG=true" >> .env
echo "LOG_LEVEL=DEBUG" >> .env

# Restart bot with debug settings
./run-docker.sh restart
```

### Network Diagnostics
```bash
# Test API endpoint connectivity
curl -I https://dashscope-intl.aliyuncs.com/

# Check DNS resolution
nslookup dashscope-intl.aliyuncs.com

# Test network latency
ping dashscope-intl.aliyuncs.com
```

### Performance Profiling
```python
# Add to discord.py for performance analysis
import time
import logging

async def on_message(message):
    start_time = time.time()
    # Processing code
    processing_time = time.time() - start_time
    logging.info(f"Message processed in {processing_time:.2f}s")
```

## Prevention Best Practices

### Regular Maintenance
- **Update dependencies** regularly
- **Monitor disk space** and clean old files
- **Backup configuration** before changes
- **Test changes** in development environment first

### Monitoring Setup
```bash
# Create monitoring script
cat > monitor_bot.sh << 'EOF'
#!/bin/bash
while true; do
    ./run-docker.sh status
    docker compose logs --tail=5
    sleep 60
done
EOF
chmod +x monitor_bot.sh
```

### Disaster Recovery
```bash
# Backup important data
tar -czf backup-$(date +%Y-%m-%d).tar.gz fodder/ .env

# Restore from backup
tar -xzf backup-2024-01-15.tar.gz
```

## Getting Additional Help

If you cannot resolve an issue using this guide:

1. **Check the logs** for specific error messages
2. **Search existing issues** in the project repository
3. **Create a detailed bug report** including:
   - Error messages and logs
   - Steps to reproduce
   - System environment details
   - Audio file information (if applicable)

### Support Resources
- Project documentation in `/docs/` folder
- GitHub issues page
- Community Discord server (if available)

This troubleshooting guide covers the most common issues and solutions. For specific configuration options, see the [Configuration Guide](configuration.md). For usage instructions, refer to the [Usage Guide](usage.md).
