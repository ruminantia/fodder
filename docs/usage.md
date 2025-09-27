# Usage Guide

## Overview

This guide covers how to effectively use fodder for audio transcription. Learn how to interact with the bot, manage your transcriptions, and optimize your workflow.

## Basic Usage

### Getting Started

1. **Ensure the bot is running**:
   ```bash
   ./run-docker.sh status
   ```
   You should see the bot container running.

2. **Invite the bot to your Discord server** using the OAuth2 URL from the Discord Developer Portal with the following permissions:
   - Read Messages/View Channels
   - Send Messages
   - Attach Files
   - Read Message History

3. **Create a dedicated channel** named `#fodder` where the bot will process audio files.

### Sending Audio for Transcription

1. **Upload an audio file** to the `#fodder` channel
2. **Wait for processing** - the bot will automatically detect and process the audio
3. **Receive transcription** - results will be posted back to the same channel

### Supported Audio Formats

The bot supports the following audio formats:
- **WAV** (recommended for best quality)
- **MP3** (most common format)
- **OGG** (open format)
- **FLAC** (lossless compression)
- **AAC** (Apple devices)
- **M4A** (iOS voice memos)
- **WMA** (Windows Media Audio)

### File Size and Duration Limits

- **Maximum file size**: 25MB (Discord upload limit)
- **Maximum duration**: 10 minutes (configurable)
- **Optimal duration**: 1-5 minutes for best results

## Advanced Usage

### Managing Long Audio Files

For files longer than 20 seconds, the bot automatically:
1. **Splits the audio** into manageable chunks
2. **Processes each chunk** with context awareness
3. **Combines results** with proper chunk numbering

**Example output for a 45-second audio file**:
```
(1/3) [Transcription of first 20 seconds...]
(2/3) [Continuation of next 20 seconds...]
(3/3) [Final 5 seconds and conclusion...]
```

### Understanding Chunk Numbering

The chunk numbering system helps you understand the structure:
- `(1/3)` - First chunk of three total chunks
- `(2/3)` - Middle chunk with context from previous
- `(3/3)` - Final chunk with full context

### Handling Multiple Files

You can process multiple audio files simultaneously:
1. **Upload multiple files** in one message
2. **The bot processes them sequentially**
3. **Each file gets its own transcription thread**

## Bot Commands and Interactions

### Available Commands

While the bot primarily responds to audio attachments, you can use these text commands:

#### `!status`
- **Purpose**: Check bot health and status
- **Response**: Current processing queue and system status

#### `!help`
- **Purpose**: Display usage information
- **Response**: Quick reference guide

#### `!version`
- **Purpose**: Check bot version
- **Response**: Current version and build information

### Response Format

The bot provides transcriptions in code blocks for better readability:

````
```
(1/2) This is the transcription of the first audio chunk...
(2/2) Continuing from the previous chunk, this is the second part...
```
````

## File Management

### Automatic File Handling

The bot manages files automatically:

1. **Downloads** audio files to temporary storage
2. **Processes** the audio through transcription pipeline
3. **Saves** transcriptions to persistent storage
4. **Cleans up** temporary files after processing

### Accessing Saved Transcriptions

Transcriptions are saved locally in the `fodder/` directory with timestamped filenames:

```
fodder/
├── 2024-01-15_14-30-25.txt
├── 2024-01-15_15-45-12.txt
└── 2024-01-16_09-15-33.txt
```

### Manual File Management

#### View Recent Transcriptions
```bash
ls -la fodder/
```

#### Search Transcriptions by Date
```bash
find fodder/ -name "2024-01-15*" -type f
```

#### Backup Transcriptions
```bash
tar -czf transcriptions-backup-$(date +%Y-%m-%d).tar.gz fodder/
```

## Quality Optimization

### Best Practices for Audio Quality

1. **Use WAV format** when possible for highest quality
2. **Ensure clear audio** with minimal background noise
3. **Speak clearly** at a consistent volume
4. **Avoid audio compression** artifacts when possible

### Improving Transcription Accuracy

1. **Single speaker** audio works best
2. **Moderate speaking pace** - not too fast or slow
3. **Good microphone quality** makes a significant difference
4. **Minimize cross-talk** in group recordings

### Troubleshooting Poor Quality

**If transcriptions are inaccurate:**
- Check audio file quality
- Ensure proper microphone placement
- Reduce background noise
- Consider re-recording with better conditions

## Performance Monitoring

### Checking Bot Status

#### Container Status
```bash
./run-docker.sh status
```

#### View Real-time Logs
```bash
./run-docker.sh logs
```

#### System Resources
```bash
docker stats ruminantia-fodder
```

### Monitoring Processing Queue

The bot processes files in the order they're received. You can monitor:
- **Active processing** through Discord status messages
- **Queue length** by counting unprocessed attachments
- **Processing time** typically 2-3x real-time duration

### Performance Metrics

- **Average processing time**: 30-90 seconds per minute of audio
- **Maximum concurrent processes**: 3 files simultaneously
- **Memory usage**: ~200-500MB during processing
- **Disk usage**: Temporary files cleaned automatically

## Advanced Features

### Custom Processing Workflows

#### Batch Processing
For multiple files, upload them sequentially rather than simultaneously to avoid queue congestion.

#### Priority Processing
Files are processed in upload order. For urgent transcriptions, ensure no other files are queued.

### Integration with Other Tools

#### Exporting Transcriptions
```bash
# Convert to different formats
cat fodder/2024-01-15_14-30-25.txt > meeting-notes.txt
```

#### API Integration (Future)
Planned features include REST API endpoints for programmatic access.

## Troubleshooting Common Issues

### "Bot is not responding"
- Check if container is running: `./run-docker.sh status`
- Verify Discord permissions
- Check network connectivity

### "Transcription failed"
- Verify audio file is valid
- Check API key validity
- Review logs for error details: `./run-docker.sh logs`

### "File too large"
- Discord limits files to 25MB
- Compress audio or split into smaller files
- Consider using lower bitrate encoding

### "Processing is slow"
- Check system resource usage
- Monitor API rate limits
- Consider reducing concurrent processing limit

## Best Practices Summary

### Do:
- ✅ Use the dedicated `#fodder` channel
- ✅ Upload one file at a time for optimal processing
- ✅ Use WAV format for best quality
- ✅ Monitor the bot's status regularly
- ✅ Backup important transcriptions

### Don't:
- ❌ Upload files to other channels
- ❌ Send extremely long files (>10 minutes)
- ❌ Interrupt processing once started
- ❌ Modify temporary files during processing

## Getting Help

### Support Resources
1. **Check logs**: `./run-docker.sh logs`
2. **Review documentation**: See other guides in this docs folder
3. **Community support**: Check project repository for issues and discussions

### Reporting Issues
When reporting problems, include:
- Audio file details (format, duration, size)
- Error messages from logs
- Steps to reproduce the issue
- System environment details

This usage guide provides comprehensive instructions for effective operation of Ruminantia Fodder. For configuration options, see the [Configuration Guide](configuration.md). For technical details, refer to the [API Reference](api.md).
