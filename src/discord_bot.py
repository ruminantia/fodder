import os
import discord
from datetime import datetime
import re

from src.transcriber import Transcriber
from src.audio_utils import chunk_audio

# Discord bot token loaded from environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Configure Discord intents to allow message content access
intents = discord.Intents.default()
intents.message_content = True

# Initialize Discord client with configured intents
client = discord.Client(intents=intents)

# Initialize the audio transcriber
transcriber = Transcriber()


@client.event
async def on_ready():
    """Handler for when the bot successfully connects to Discord."""
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    """
    Handler for incoming Discord messages.

    Processes audio attachments in the #fodder channel by:
    1. Downloading the audio file
    2. Chunking long audio files
    3. Transcribing with context-aware prompts
    4. Saving transcriptions locally
    5. Sending results back to the channel
    6. Cleaning up temporary files
    """
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Only process messages in the dedicated #fodder channel
    if message.channel.name != "fodder":
        return

    # Process any audio attachments in the message
    if message.attachments:
        for attachment in message.attachments:
            # Verify this is an audio file before processing
            if attachment.content_type and attachment.content_type.startswith("audio/"):
                try:
                    # Download the audio file to local storage
                    audio_path = f"downloads/{attachment.filename}"
                    if not os.path.exists("downloads"):
                        os.makedirs("downloads")
                    await attachment.save(audio_path)

                    # Split audio into manageable chunks if it's too long
                    chunks = chunk_audio(audio_path)

                    # Transcribe all chunks with context passing between them
                    full_transcription = await transcriber.transcribe_chunks(chunks)

                    # Save transcription to file with timestamp
                    output_dir = "fodder"
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    now = datetime.now()
                    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
                    output_filename = f"{output_dir}/{timestamp}.txt"

                    with open(output_filename, "w") as f:
                        f.write(full_transcription)

                    # Clean up temporary files to prevent disk space accumulation
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                    if os.path.exists("temp_chunks"):
                        for chunk_path in chunks:
                            if os.path.exists(chunk_path):
                                os.remove(chunk_path)

                    # Handle Discord's 2000-character message limit
                    if len(full_transcription) > 2000:
                        # Smart splitting that preserves chunk numbering structure
                        max_content_length = 2000  # Full Discord character limit

                        messages = []
                        current_message = ""

                        # Split by chunk boundaries to maintain numbering context
                        chunk_pattern = r"(?=\(\d+/\d+\))"
                        text_chunks = re.split(chunk_pattern, full_transcription)
                        text_chunks = [
                            chunk.strip() for chunk in text_chunks if chunk.strip()
                        ]

                        if text_chunks:
                            # Group chunks together when they fit within the limit
                            for chunk in text_chunks:
                                if (
                                    len(current_message) + len(chunk) + 1
                                    <= max_content_length
                                ):
                                    if current_message:
                                        current_message += " " + chunk
                                    else:
                                        current_message = chunk
                                else:
                                    # Start new message when current one would exceed limit
                                    if current_message:
                                        messages.append(current_message)
                                    current_message = chunk

                                    # Handle individual chunks that are too large
                                    if len(current_message) > max_content_length:
                                        # Split oversized chunk across multiple messages
                                        chunk_messages = [
                                            current_message[i : i + max_content_length]
                                            for i in range(
                                                0,
                                                len(current_message),
                                                max_content_length,
                                            )
                                        ]
                                        messages.extend(chunk_messages[:-1])
                                        current_message = chunk_messages[-1]

                            # Don't forget the last message
                            if current_message:
                                messages.append(current_message)
                        else:
                            # Fallback: simple character-based splitting
                            messages = [
                                full_transcription[i : i + max_content_length]
                                for i in range(
                                    0, len(full_transcription), max_content_length
                                )
                            ]

                        # Send all message parts to Discord
                        for msg_content in messages:
                            await message.channel.send(f"```\n{msg_content}\n```")
                    else:
                        # Single message fits within Discord's limit
                        await message.channel.send(f"```\n{full_transcription}\n```")

                except Exception as e:
                    # Handle any errors during audio processing
                    print(f"Error processing audio attachment: {e}")
                    await message.channel.send(
                        "Sorry, there was an error processing the audio file."
                    )
