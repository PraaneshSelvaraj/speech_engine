from __future__ import annotations

import io
import wave
import os
import subprocess
import requests
from typing import List

from .audioPlayer import AudioPlayer
from .exceptions import FileExtensionError, InvalidTokenError


class TTS_Playai:
    """
    The TTS_Playai class provides functionality to synthesize text into speech using Playai.

    Args:
        apiKey (str): The GROQ API Key.
    """

    _voice: str
    _apiKey: str
    _player: AudioPlayer

    def __init__(self, apiKey: str) -> None:
        if not apiKey:
            raise ValueError("API key cannot be empty")

        self._voice = "Arista-PlayAI"
        self._apiKey = apiKey
        if not self._validate_token():
            raise InvalidTokenError()
        self._player = AudioPlayer()

    def _validate_token(self) -> bool:
        """
        Validate the Groq API auth token.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        headers: dict[str, str] = {"Authorization": f"Bearer {self._apiKey}"}
        response = requests.get(
            "https://api.groq.com/openai/v1/models", headers=headers
        )
        return response.status_code == 200

    def get_voice(self) -> str:
        """
        Returns the current voice.

        Returns:
            str: The current voice.
        """
        return self._voice

    def set_voice(self, voice: str) -> None:
        """
        Sets the voice to be used for synthesis.

        Args:
            voice (str): The voice to be set.
        """
        self._voice = voice

    def _synthesize_speech(self, text: str) -> bytes:
        """Fetch TTS audio bytes from the Playai API."""
        GROQ_URL = "https://api.groq.com/openai/v1/audio/speech"
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self._apiKey}",
            "Content-Type": "application/json",
        }
        payload: dict[str, str] = {
            "model": "playai-tts",
            "input": text,
            "voice": self._voice,
            "response_format": "wav",
        }

        resp = requests.post(GROQ_URL, headers=headers, json=payload, stream=True)

        if resp.status_code != 200:
            raise Exception(f"API Error: {resp.status_code} - {resp.text}")

        return resp.content

    def save(self, text: str, filename: str = "output.wav") -> None:
        """
        Synthesizes the given text into speech and saves it as an audio file.

        Args:
            text (str): The text to be synthesized into speech.
            filename (str): The filename to save the audio file (must have a .wav extension).

        Raises:
            FileExtensionError: If the filename doesn't have a .wav extension.
        """
        if not filename.endswith(".wav"):
            raise FileExtensionError(message="Output file type should be .wav")

        with open(filename, "wb") as f:
            f.write(self._synthesize_speech(text))

    def speak(self, text: str) -> None:
        """
        Synthesizes the given text into speech and plays it.

        Args:
            text (str): The text to be synthesized into speech.
        """
        audio = io.BytesIO(self._synthesize_speech(text))

        with wave.open(audio, "rb") as wav_file:
            channels: int = wav_file.getnchannels()
            sample_width: int = wav_file.getsampwidth()
            frame_rate: int = wav_file.getframerate()
            raw_audio: bytes = wav_file.readframes(wav_file.getnframes())

        self._player.play_bytes(raw_audio, channels, sample_width, frame_rate)

    def get_voices(self) -> List[str]:
        """
        Fetches available voices from the Groq PlayAI API.

        Returns:
            list[str]: A list of available voice names.
        """
        voices: List[str] = [
            "Arista-PlayAI",
            "Atlas-PlayAI",
            "Basil-PlayAI",
            "Briggs-PlayAI",
            "Calum-PlayAI",
            "Celeste-PlayAI",
            "Cheyenne-PlayAI",
            "Chip-PlayAI",
            "Cillian-PlayAI",
            "Deedee-PlayAI",
            "Fritz-PlayAI",
            "Gail-PlayAI",
            "Indigo-PlayAI",
            "Mamaw-PlayAI",
            "Mason-PlayAI",
            "Mikail-PlayAI",
            "Mitch-PlayAI",
            "Quinn-PlayAI",
            "Thunder-PlayAI",
        ]
        return voices
