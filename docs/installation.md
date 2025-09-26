# Installation Guide

## Overview

This guide provides comprehensive installation instructions for fodder. You can choose between Docker-based installation (recommended) or manual Python installation.

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows
- **Docker** (for containerized installation): Docker Engine 20.10+ and Docker Compose 2.0+
- **Python** (for manual installation): Python 3.13+
- **Disk Space**: Minimum 2GB free space
- **Memory**: 2GB RAM recommended
- **Network**: Stable internet connection for API calls

### Required Accounts
- **Discord Developer Account**: [Create here](https://discord.com/developers/applications)
- **Qwen API Access**: [DashScope](https://dashscope.aliyuncs.com/) or other Qwen provider

## Method 1: Docker Installation (Recommended)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd ruminantia/fodder
```

### Step 2: Set Up Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit the configuration with your credentials
nano .env  # or your preferred editor
```

Edit the `.env` file with your actual credentials:
```env
DISCORD_BOT_TOKEN=your_actual_discord_bot_token_here
QWEN_API_KEY=your_actual_qwen_api_key_here
```

### Step 3: Start the Bot
```bash
# Make the management script executable
chmod +x run-docker.sh

# Start the bot (detached mode)
./run-docker.sh
```

### Step 4: Verify Installation
```bash
# Check container status
./run-docker.sh status

# View logs to confirm successful startup
./run-docker.sh logs
```

## Method 2: Manual Python Installation

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd ruminantia/fodder
```

### Step 2: Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### Step 3: Install System Dependencies

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg python3-pip
```

#### macOS (with Homebrew):
```bash
brew install ffmpeg
```

#### Windows (with Chocolatey):
```bash
choco install ffmpeg
```

### Step 4: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment
```bash
# Copy and edit environment file
cp .env.example .env
nano .env  # add your credentials
```

### Step 6: Create Necessary Directories
```bash
mkdir -p downloads transcriptions temp_chunks
```

### Step 7: Start the Bot
```bash
python main.py
```

## Docker-Specific Configuration

### Customizing Docker Setup

#### Modify Resource Limits
Edit `docker-compose.yml` to add resource constraints:
```yaml
services:
  discord-bot:
    # ... existing configuration ...
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
```

#### Change Volume Mounts
Modify volume paths for different storage locations:
```yaml
services:
  discord-bot:
    # ... existing configuration ...
    volumes:
      - /custom/path/downloads:/app/downloads
      - /custom/path/transcriptions:/app/transcriptions
```

### Advanced Docker Commands

#### Build Custom Image
```bash
./run-docker.sh build
```

#### Start in Debug Mode
```bash
./run-docker.sh attach
```

#### View Real-time Logs
```bash
./run-docker.sh logs
```

## Manual Installation Customization

### Virtual Environment Management

#### Using direnv (Optional)
Create `.envrc` file:
```bash
cp .envrc.example .envrc
direnv allow
```

#### Python Path Configuration
Add to your shell profile for easier access:
```bash
echo 'export PYTHONPATH=$PWD/src:$PYTHONPATH' >> ~/.bashrc
```

### Service Management

#### Systemd Service (Linux)
Create `/etc/systemd/system/ruminantia-fodder.service`:
```ini
[Unit]
Description=Ruminantia Fodder Discord Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/fodder
ExecStart=/path/to/fodder/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable ruminantia-fodder
sudo systemctl start ruminantia-fodder
```

## Platform-Specific Instructions

### Windows Installation

#### Using Windows Subsystem for Linux (WSL)
```bash
# Install WSL and Ubuntu
wsl --install

# Follow Linux instructions within WSL
```

#### Native Windows
1. Install Python 3.13 from [python.org](https://python.org)
2. Install FFmpeg and add to PATH
3. Use Command Prompt or PowerShell for commands

### macOS Installation

#### Using Homebrew
```bash
# Install Python and dependencies
brew install python@3.13 ffmpeg

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
```

### Linux Server Installation

#### Ubuntu Server 22.04+
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install docker.io docker-compose ffmpeg git

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

## Verification Steps

### Test Basic Functionality

1. **Check Bot Status**:
   ```bash
   ./run-docker.sh status  # or check Python process
   ```

2. **Verify API Connectivity**:
   - Bot should appear online in Discord
   - No authentication errors in logs

3. **Test Audio Processing**:
   - Send a short audio file to #fodder channel
   - Verify transcription is returned

### Common Verification Commands

```bash
# Check Docker container health
docker compose ps

# View recent logs
docker compose logs --tail=50

# Check Python installation
python --version
pip list | grep -E "(discord|openai|pydub)"

# Verify FFmpeg installation
ffmpeg -version
```

## Troubleshooting Installation

### Common Issues and Solutions

#### Docker Issues
- **Permission denied**: Add user to docker group: `sudo usermod -aG docker $USER`
- **Port conflicts**: Modify docker-compose.yml to use different ports
- **Volume mount errors**: Ensure directory permissions are correct

#### Python Issues
- **Module not found**: Verify virtual environment is activated
- **FFmpeg errors**: Ensure FFmpeg is installed and in PATH
- **Permission errors**: Run with appropriate user permissions

#### API Issues
- **Authentication failures**: Verify API keys in .env file
- **Rate limiting**: Check API provider limits and adjust timeouts

## Next Steps

After successful installation:

1. **Configure Discord**: Invite bot to your server and set up #fodder channel
2. **Test Functionality**: Send test audio files to verify transcription
3. **Monitor Performance**: Check logs for any issues or optimizations
4. **Customize Settings**: Adjust chunk sizes, timeouts, or other parameters

See the [Configuration Guide](configuration.md) for detailed customization options and the [Usage Guide](usage.md) for operational instructions.
