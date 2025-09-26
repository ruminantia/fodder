import sys
import os
from dotenv import load_dotenv

# Add src directory to Python path to enable module imports
# This allows importing from the src package without installation
sys.path.append("src")

# Load environment variables from .env file
# This must happen before importing discord_bot to ensure variables are available
load_dotenv()

# Import the Discord bot module after environment is loaded
# This ensures DISCORD_BOT_TOKEN is available when the module is imported
from src import discord_bot


def main():
    """
    Main entry point for the Ruminantia Fodder Discord bot.

    This function:
    1. Validates that required environment variables are set
    2. Starts the Discord bot with the provided token
    3. Handles any startup errors gracefully

    The bot will run until stopped by external signal (Ctrl+C) or error.
    """
    # Validate that Discord bot token is available
    if not discord_bot.DISCORD_BOT_TOKEN:
        raise ValueError(
            "DISCORD_BOT_TOKEN not found in environment variables.\n"
            "Please ensure your .env file contains a valid Discord bot token."
        )

    # Start the Discord bot
    # This begins the event loop and connects to Discord's gateway
    discord_bot.client.run(discord_bot.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    """
    Standard Python idiom to ensure main() only runs when script is executed directly.

    This prevents the bot from starting if the file is imported as a module,
    which is important for testing and other integration scenarios.
    """
    main()
