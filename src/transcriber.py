import os
import base64
import asyncio
from typing import List, Optional
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionChunk


class Transcriber:
    """
    Handles audio transcription using the Qwen3 Omni model with async operations.

    Features:
    - Chunk-aware prompting for multi-part audio files
    - Context passing between consecutive chunks
    - Async/await patterns to prevent blocking
    - Timeout handling for API requests
    - Error recovery for individual chunk failures
    """

    def __init__(self) -> None:
        """
        Initialize the transcriber with API credentials.

        Raises:
            ValueError: If QWEN_API_KEY environment variable is not set
        """
        api_key = os.getenv("QWEN_API_KEY")
        if not api_key:
            raise ValueError("QWEN_API_KEY not found in environment variables")

        # Configure async OpenAI client for Qwen API
        self.client: AsyncOpenAI = AsyncOpenAI(
            api_key=api_key,
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )

    def _encode_audio(self, audio_path: str) -> str:
        """
        Encode audio file to base64 for API transmission.

        Args:
            audio_path: Path to the audio file to encode

        Returns:
            Base64 encoded audio data as string
        """
        with open(audio_path, "rb") as audio_file:
            return base64.b64encode(audio_file.read()).decode("utf-8")

    def _build_chunk_prompt(
        self,
        chunk_index: int,
        total_chunks: int,
        previous_context: Optional[str] = None,
    ) -> str:
        """
        Construct context-aware prompt based on chunk position.

        Prompts are tailored to the chunk's position in the sequence:
        - First chunk: Full description with chunk awareness
        - Middle chunks: Continuation with accumulated context
        - Final chunk: Wrap-up with full context

        Args:
            chunk_index: 0-based index of current chunk
            total_chunks: Total number of chunks in audio
            previous_context: Combined transcription from previous chunks

        Returns:
            Tailored prompt string for the current chunk
        """
        chunk_number = chunk_index + 1

        # Single chunk audio - simple description
        if total_chunks == 1:
            return "Give a thorough description of the audio."

        # First chunk of multi-chunk audio
        if chunk_index == 0:
            return (
                f"Give a thorough description of the chunked audio. "
                f"You are currently listening to part {chunk_number}/{total_chunks} "
                f"meaning it will abruptly end and may lack some context. "
                f"The rest of the audio will be described in a later API request "
                f"and concatenated to this response."
            )

        # Final chunk of multi-chunk audio
        if chunk_index == total_chunks - 1:
            if total_chunks == 2:
                return (
                    f"Give a thorough description of the chunked audio. "
                    f"You are currently listening to the final chunk meaning it will "
                    f"abruptly start and may lack some context. "
                    f"Continue from where the previous request left off and note that "
                    f"certain basic details (like initial audio quality) have already "
                    f"been described. Full context: {previous_context}"
                )
            else:
                return (
                    f"Give a thorough description of the chunked audio. "
                    f"You are currently listening to the final chunk "
                    f"(part {chunk_number}/{total_chunks}) meaning it will abruptly "
                    f"start and may lack some context. Continue from where the previous "
                    f"request left off and note that certain basic details have already "
                    f"been described. Full context: {previous_context}"
                )

        # Middle chunk (not first or last)
        return (
            f"Give a thorough description of the chunked audio. "
            f"You are currently listening to part {chunk_number}/{total_chunks} "
            f"meaning it will abruptly start/end and may lack some context. "
            f"Continue from where the previous request left off and note that "
            f"certain basic details have already been described. "
            f"Full context: {previous_context}"
        )

    async def transcribe(
        self,
        audio_path: str,
        chunk_index: int = 0,
        total_chunks: int = 1,
        previous_context: Optional[str] = None,
        timeout: int = 60,
    ) -> str:
        """
        Transcribe a single audio chunk using Qwen3 Omni model.

        Args:
            audio_path: Path to audio file chunk
            chunk_index: 0-based index of current chunk
            total_chunks: Total number of chunks
            previous_context: Combined transcription from previous chunks
            timeout: Maximum seconds to wait for API response

        Returns:
            Transcribed text for this chunk, or error message on failure
        """
        # Prepare audio data and context-aware prompt
        base64_audio = self._encode_audio(audio_path)
        prompt = self._build_chunk_prompt(chunk_index, total_chunks, previous_context)

        try:
            # Use timeout to prevent indefinite blocking
            async with asyncio.timeout(timeout):
                # Stream transcription from Qwen API
                completion_stream = await self.client.chat.completions.create(
                    model="qwen3-omni-flash",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_audio",
                                    "input_audio": {
                                        "data": f"data:;base64,{base64_audio}",
                                        "format": "wav",
                                    },
                                },
                                {"type": "text", "text": prompt},
                            ],
                        }
                    ],
                    modalities=["text"],
                    extra_body={"enable_thinking": True},
                    stream=True,
                    stream_options={"include_usage": True},
                )

                # Collect streaming response
                transcription = ""
                async for chunk in completion_stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        transcription += chunk.choices[0].delta.content

                return transcription

        except asyncio.TimeoutError:
            print(f"Transcription timeout after {timeout} seconds for {audio_path}")
            return "[Transcription timeout]"
        except Exception as e:
            print(f"Transcription request failed: {e}")
            return ""

    async def transcribe_chunks(self, chunk_paths: List[str]) -> str:
        """
        Transcribe multiple audio chunks with sequential context passing.

        Process flow:
        1. Handle single chunk case directly
        2. For multiple chunks: process sequentially
        3. Pass accumulated context to each subsequent chunk
        4. Combine results with chunk numbering
        5. Continue processing even if individual chunks fail

        Args:
            chunk_paths: List of paths to audio chunk files

        Returns:
            Combined transcription with chunk numbering prefixes
        """
        total_chunks = len(chunk_paths)

        # Single chunk - no context passing needed
        if total_chunks == 1:
            return await self.transcribe(chunk_paths[0], 0, 1)

        # Process chunks sequentially with accumulating context
        chunk_transcriptions = []
        accumulated_context = ""

        for i, chunk_path in enumerate(chunk_paths):
            try:
                # Transcribe current chunk with all previous context
                chunk_transcription = await self.transcribe(
                    chunk_path,
                    chunk_index=i,
                    total_chunks=total_chunks,
                    previous_context=accumulated_context
                    if accumulated_context
                    else None,
                )

                # Store result and update context for next chunk
                if chunk_transcription:
                    chunk_transcriptions.append(chunk_transcription)
                    # Accumulate context for continuity
                    if accumulated_context:
                        accumulated_context += " " + chunk_transcription
                    else:
                        accumulated_context = chunk_transcription
                else:
                    # Handle empty transcription gracefully
                    chunk_transcriptions.append(
                        f"[Empty transcription for chunk {i + 1}]"
                    )

            except Exception as e:
                # Continue processing even if one chunk fails
                print(f"Error transcribing chunk {i}: {e}")
                chunk_transcriptions.append(f"[Error in chunk {i + 1}]")

        # Combine transcriptions with chunk numbering
        full_transcription = ""
        for i, transcription in enumerate(chunk_transcriptions):
            chunk_number = i + 1
            if total_chunks > 1:
                full_transcription += (
                    f"({chunk_number}/{total_chunks}) {transcription} "
                )
            else:
                full_transcription += transcription + " "

        return full_transcription.strip()
