import os
from pydub import AudioSegment


def get_audio_format(filename: str) -> str:
    """
    Detect audio file format based on file extension.

    Maps common audio file extensions to pydub-compatible format strings.
    Falls back to 'wav' format for unknown extensions.

    Args:
        filename: Name of the audio file with extension

    Returns:
        Format string recognized by pydub (e.g., 'wav', 'mp3', 'ogg')
    """
    ext = filename.lower().split(".")[-1]
    format_map = {
        "wav": "wav",
        "mp3": "mp3",
        "ogg": "ogg",
        "flac": "flac",
        "aac": "aac",
        "m4a": "mp4",
        "wma": "wma",
    }
    return format_map.get(ext, "wav")  # Default to wav for unknown formats


def chunk_audio(audio_path: str, chunk_length_s: int = 20) -> list[str]:
    """
    Split audio file into smaller chunks if it exceeds the specified duration.

    For audio files longer than chunk_length_s, splits into multiple chunks
    of approximately equal length. Files shorter than chunk_length_s are
    returned as a single chunk. All chunks are exported as WAV format for
    consistent transcription API compatibility.

    Args:
        audio_path: Path to the audio file to process
        chunk_length_s: Maximum chunk length in seconds (default: 20)

    Returns:
        List of paths to audio chunk files. Returns single-element list
        with original path if audio is shorter than chunk_length_s.

    Raises:
        Various audio processing exceptions, but falls back to returning
        original file path on error to maintain processing flow.
    """
    try:
        # Detect format and load audio using appropriate pydub method
        audio_format = get_audio_format(audio_path)

        # Load audio using format-specific method for better reliability
        if audio_format == "wav":
            audio = AudioSegment.from_wav(audio_path)
        elif audio_format == "mp3":
            audio = AudioSegment.from_mp3(audio_path)
        elif audio_format == "ogg":
            audio = AudioSegment.from_ogg(audio_path)
        elif audio_format == "flac":
            audio = AudioSegment.from_flac(audio_path)
        elif audio_format == "mp4":
            audio = AudioSegment.from_file(audio_path, format="mp4")
        else:
            # Fallback to auto-detection for unsupported formats
            audio = AudioSegment.from_file(audio_path)

        # Calculate audio duration in seconds
        duration_s = len(audio) / 1000  # pydub uses milliseconds

        # Return original file if it's short enough
        if duration_s <= chunk_length_s:
            return [audio_path]

        # Prepare for chunking
        chunk_length_ms = chunk_length_s * 1000
        chunks = []
        output_dir = "temp_chunks"

        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Split audio into chunks of specified length
        for i, start_ms in enumerate(range(0, len(audio), chunk_length_ms)):
            # Extract chunk segment
            chunk = audio[start_ms : start_ms + chunk_length_ms]

            # Generate unique chunk filename
            chunk_path = os.path.join(output_dir, f"chunk_{i}.wav")

            # Export as WAV for transcription API compatibility
            chunk.export(chunk_path, format="wav")
            chunks.append(chunk_path)

        return chunks

    except Exception as e:
        # Log error but return original file to allow processing to continue
        print(f"Error processing audio file {audio_path}: {e}")

        # Fallback: return original file path to maintain processing flow
        return [audio_path]
