import io
from typing import Any

import requests
from pydub import AudioSegment
from pydub.playback import play

from .audioPlayer import AudioPlayer
from .exceptions import FileExtensionError, InvalidTokenError


class TTS_ElevenLabs:
    """
    The TTS_ElevenLabs class provides text-to-speech synthesis using ElevenLabs API.

    Args:
        apiKey (str): The ElevenLabs API Key for authentication.
    """

    def __init__(self, apiKey: str) -> None:
        # Check if API key is provided
        if not apiKey:
            raise ValueError("API key cannot be empty")

        # Default voice ID, can be changed via set_voice()
        self._voice: str = "UgBBYS2sOqTuMpoF3BR0"
        self._apiKey: str = apiKey

        # Validate provided API key by checking voices endpoint
        if not self._validate_token():
            raise InvalidTokenError("Invalid ElevenLabs API key")

        # AudioPlayer instance (optional, in case you want to play raw bytes)
        self._player: AudioPlayer = AudioPlayer()

    def _validate_token(self) -> bool:
        """
        Validates the ElevenLabs API key by requesting available voices.

        Returns:
            bool: True if API key is valid (status 200), else False.
        """
        headers: dict[str, str] = {"xi-api-key": self._apiKey}
        response = requests.get("https://api.elevenlabs.io/v2/voices", headers=headers)
        return response.status_code == 200

    def get_voice(self) -> str:
        """
        Returns the current voice ID being used.

        Returns:
            str: Current voice ID.
        """
        return self._voice

    def set_voice(self, voice: str) -> None:
        """
        Sets the voice ID for speech synthesis.

        Args:
            voice (str): New voice ID to use.
        """
        self._voice = voice

    def _synthesize_speech(self, text: str) -> bytes:
        """
        Sends a text-to-speech synthesis request to ElevenLabs and returns MP3 audio bytes.

        Args:
            text (str): Text to convert to speech.

        Returns:
            bytes: MP3 audio content received from API.

        Raises:
            Exception: If API responds with an error.
        """
        # API URL with mp3 output format specified
        ELEVENLABS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{self._voice}?output_format=mp3_22050_32"

        headers: dict[str, str] = {
            "xi-api-key": self._apiKey,
            "Content-Type": "application/json",
        }

        # Payload with text and model choice
        payload: dict[str, Any] = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
        }

        # HTTP POST request to synthesize speech
        resp = requests.post(ELEVENLABS_URL, headers=headers, json=payload, stream=True)

        # Raise error if API response is not successful
        if resp.status_code != 200:
            raise Exception(f"API Error: {resp.status_code} - {resp.text}")

        # Return MP3 bytes content
        return resp.content

    def save(self, text: str, filename: str = "output.mp3") -> None:
        """
        Synthesizes speech for the provided text and saves it as an MP3 file.

        Args:
            text (str): Text to synthesize.
            filename (str): Filename to save the MP3 as. Must end with '.mp3'.

        Raises:
            FileExtensionError: if filename does not end with '.mp3'.
        """
        # Ensure filename extension is .mp3 to match audio format
        if not filename.endswith(".mp3"):
            raise FileExtensionError(message="Output file type should be .mp3")

        # Get MP3 audio bytes from API
        audio_bytes = self._synthesize_speech(text)

        # Write bytes to file
        with open(filename, "wb") as f:
            f.write(audio_bytes)

    def speak(self, text: str) -> None:
        """
        Synthesizes speech for the text and plays it directly.

        Args:
            text (str): Text to synthesize and play.
        """
        # Get MP3 bytes from API
        mp3_data = self._synthesize_speech(text)

        # Load bytes as an AudioSegment for playback
        audio_segment = AudioSegment.from_file(io.BytesIO(mp3_data), format="mp3")

        # Play the audio using pydub playback
        play(audio_segment)

    def get_voices(self) -> list[str]:
        """
        Retrieves the list of available voice IDs from ElevenLabs API.

        Returns:
            list[str]: List of voice IDs available.
        """
        url: str = "https://api.elevenlabs.io/v2/voices"
        headers: dict[str, str] = {"xi-api-key": self._apiKey}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data: dict[str, Any] = response.json()

        # Extract voice_id for each voice available
        voices: list[str] = [
            voice.get("voice_id", "")
            for voice in data.get("voices", [])
            if voice.get("voice_id")
        ]
        return voices
