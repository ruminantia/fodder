#!/bin/bash

# =============================================================================
# Ruminantia Fodder - Docker Container Management Script
#
# This script provides a convenient command-line interface for managing the
# Discord audio transcription bot using Docker Compose. It handles environment
# validation, container lifecycle management, and user-friendly error messages.
# =============================================================================

# Exit immediately if any command fails
set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# =============================================================================
# COLOR DEFINITIONS FOR USER-FRIENDLY OUTPUT
# =============================================================================
RED='\033[0;31m'      # Error messages
GREEN='\033[0;32m'    # Success messages
YELLOW='\033[1;33m'   # Warning messages
NC='\033[0m'          # No Color (reset)

# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

# Print informational status messages
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Print warning messages for non-critical issues
print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Print error messages and exit if necessary
print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# =============================================================================
# ENVIRONMENT VALIDATION FUNCTIONS
# =============================================================================

check_env_file() {
    # Validate that the .env file exists and contains required configuration.
    #
    # This function:
    # 1. Checks for the existence of the .env file
    # 2. Verifies that required environment variables are present
    # 3. Creates necessary data directories if they don't exist
    # 4. Provides helpful guidance if configuration is missing
    #
    # Exits with error code 1 if .env file is missing.
    # Check if .env file exists
    if [ ! -f .env ]; then
        print_error ".env file not found!"
        echo ""
        echo "Configuration file is required for the bot to function."
        echo ""
        echo "Setup instructions:"
        echo "1. Copy the example file: cp .env.example .env"
        echo "2. Edit .env with your actual credentials:"
        echo "   - DISCORD_BOT_TOKEN: Get from https://discord.com/developers/applications"
        echo "   - QWEN_API_KEY: Get from your Qwen API provider"
        echo ""
        echo "Example .env file structure:"
        echo "DISCORD_BOT_TOKEN=your_actual_discord_bot_token_here"
        echo "QWEN_API_KEY=your_actual_qwen_api_key_here"
        exit 1
    fi

    # Verify required environment variables are present
    if ! grep -q "DISCORD_BOT_TOKEN" .env || ! grep -q "QWEN_API_KEY" .env; then
        print_warning ".env file exists but may be missing required variables"
        echo "Required variables: DISCORD_BOT_TOKEN, QWEN_API_KEY"
        echo ""
        echo "Ensure your .env file contains:"
        echo "DISCORD_BOT_TOKEN=your_actual_discord_bot_token"
        echo "QWEN_API_KEY=your_actual_qwen_api_key"
    fi

    # Ensure necessary data directories exist
    for dir in downloads fodder temp_chunks; do
        if [ ! -d "$dir" ]; then
            print_warning "Creating missing directory: $dir"
            mkdir -p "$dir"
        fi
    done
}

# =============================================================================
# CONTAINER MANAGEMENT FUNCTIONS
# =============================================================================

start_bot() {
    # Start the Discord bot in detached mode (background).
    #
    # This runs the container as a background service, freeing up the terminal.
    # The bot will automatically restart on failure unless manually stopped.
    print_status "Starting Ruminantia Fodder bot in detached mode..."
    docker compose up -d
    print_status "Bot started successfully!"
    echo "To view logs: ./run-docker.sh logs"
    echo "To stop the bot: ./run-docker.sh stop"
}

stop_bot() {
    # Stop the running bot container and clean up resources.
    #
    # This stops the container and removes the associated Docker network.
    # All data in mounted volumes (transcriptions, etc.) is preserved.
    print_status "Stopping Ruminantia Fodder bot..."
    docker compose down
    print_status "Bot stopped successfully!"
}

restart_bot() {
    # Restart the bot container with current configuration.
    #
    # Useful for applying configuration changes or recovering from issues.
    # The container is stopped and started with the same settings.
    print_status "Restarting Ruminantia Fodder bot..."
    docker compose restart
    print_status "Bot restarted successfully!"
}

view_logs() {
    # Display real-time container logs in follow mode.
    #
    # Shows the bot's output stream. Useful for debugging and monitoring.
    # Press Ctrl+C to exit log viewing mode.
    print_status "Showing bot logs (Ctrl+C to exit)..."
    docker compose logs -f
}

build_image() {
    # Rebuild the Docker image from scratch.
    #
    # Useful when Dockerfile changes are made or to ensure a clean build.
    # Uses --no-cache to force complete rebuild of all layers.
    print_status "Building Docker image (clean rebuild)..."
    docker compose build --no-cache
    print_status "Image built successfully!"
}

show_status() {
    # Display the current status of Docker containers.
    #
    # Shows running/stopped status, container names, and other details.
    # Useful for verifying the bot's operational state.
    print_status "Container status:"
    docker compose ps
}

start_attached() {
    # Start the bot in attached mode for debugging.
    #
    # Runs the container in the foreground, showing real-time output.
    # The terminal will be occupied until the bot is stopped with Ctrl+C.
    check_env_file
    print_status "Starting Ruminantia Fodder bot in attached mode..."
    print_warning "Press Ctrl+C to stop the bot"
    print_warning "Terminal will be occupied until bot is stopped"
    docker compose up
}

show_help() {
    # Display comprehensive help information for the management script.
    #
    # Provides usage instructions, available commands, and examples.
    # This is the default help message shown when users need assistance.
    echo "Ruminantia Fodder - Discord Bot Management Script"
    echo "=================================================="
    echo ""
    echo "A convenient interface for managing the audio transcription bot."
    echo ""
    echo "Usage: ./run-docker.sh [command]"
    echo ""
    echo "Available Commands:"
    echo "  start     - Start the bot in detached mode (recommended)"
    echo "  stop      - Stop the running bot container"
    echo "  restart   - Restart the bot with current configuration"
    echo "  logs      - View real-time bot logs (follow mode)"
    echo "  build     - Rebuild the Docker image from scratch"
    echo "  status    - Show container status information"
    echo "  attach    - Start in attached mode for debugging"
    echo "  help      - Display this help message"
    echo ""
    echo "Default Behavior:"
    echo "  If no command is provided, the bot starts in detached mode."
    echo ""
    echo "Operational Notes:"
    echo "  - Detached mode runs the bot in the background"
    echo "  - Attached mode is useful for debugging but occupies the terminal"
    echo "  - Logs can be viewed anytime with the 'logs' command"
    echo "  - Data is preserved in mounted volumes across restarts"
    echo ""
    echo "Examples:"
    echo "  ./run-docker.sh           # Start bot (detached mode)"
    echo "  ./run-docker.sh logs      # View real-time logs"
    echo "  ./run-docker.sh stop      # Stop the bot"
    echo "  ./run-docker.sh attach    # Debug mode (attached)"
    echo ""
    echo "For more information, see the project README.md file."
}

# =============================================================================
# MAIN SCRIPT LOGIC - COMMAND DISPATCHER
# =============================================================================

case "${1:-}" in
    "start")
        # Start the bot in detached mode (background)
        check_env_file
        start_bot
        ;;
    "stop")
        # Stop the running bot container
        stop_bot
        ;;
    "restart")
        # Restart the bot with current configuration
        check_env_file
        restart_bot
        ;;
    "logs")
        # Display real-time container logs
        view_logs
        ;;
    "build")
        # Rebuild the Docker image
        build_image
        ;;
    "status")
        # Show container status information
        show_status
        ;;
    "attach")
        # Start bot in attached mode for debugging
        start_attached
        ;;
    "help"|"-h"|"--help")
        # Display comprehensive help information
        show_help
        ;;
    "")
        # Default behavior: start in detached mode
        check_env_file
        print_status "Starting Ruminantia Fodder bot in detached mode..."
        docker compose up -d
        print_status "Bot started successfully!"
        echo "To view logs: ./run-docker.sh logs"
        echo "To stop: ./run-docker.sh stop"
        ;;
    *)
        # Handle unknown commands with helpful error message
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
