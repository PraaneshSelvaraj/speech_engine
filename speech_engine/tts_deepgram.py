import io
import wave

import os
import subprocess
import requests
from .audioPlayer import AudioPlayer
from .exceptions import FileExtensionError, InvalidTokenError


class TTS_Deepgram:
    """
    The TTS_Deepgram class provides functionality to synthesize text into speech using the Deepgram

    Args:
        apiKey (str): The Open AI API Key.

    """
    def __init__(self, apiKey : str):
        if not apiKey:
            raise ValueError("API key cannot be empty")

        self._voice = 'aura-asteria-en'
        self._apiKey = apiKey
        if not self._validate_token():
            raise InvalidTokenError()
        self._player = AudioPlayer()

    def _validate_token(self):
        """
        Validate the Deepgram API auth token.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        headers = {
            "Authorization": f"Bearer {self._apiKey}",
        }
        return (
            requests.get(
                "https://api.deepgram.com/v1/models", headers=headers
            ).status_code
            == 200
        )

    def get_voice(self) -> str:
        """
        Returns the current voice.

        Returns:
            str: The current voice.
        """
        return self._voice

    def set_voice(self, voice: str):
        """
        Sets the voice to be used for synthesis.

        Args:
            voice (str): The voice to be set.
        """
        self._voice = voice

    def _synthesize_speech(self, text: str) -> bytes:
        """Fetch TTS audio bytes from the Deepgram API."""
        DEEPGRAM_URL = (
            "https://api.deepgram.com/v1/speak"
            f"?model={self._voice}"
            "&encoding=linear16"
            "&sample_rate=24000"
        )
        headers = {
            "Authorization": f"Token {self._apiKey}",
            "Content-Type": "application/json",
        }
        payload = {"text": text}

        resp = requests.post(DEEPGRAM_URL, headers=headers, json=payload, stream=True)

        if resp.status_code != 200:
            raise Exception(f"API Error: {resp.status_code} - {resp.text}")

        return resp.content
    
    def save(self, text: str, filename: str = "output.wav"):
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
    
    def speak(self, text: str):
        """
        Synthesizes the given text into speech and plays it.

        Args:
            text (str): The text to be synthesized into speech.
        """
        audio = io.BytesIO(self._synthesize_speech(text))

        with wave.open(audio, "rb") as wav_file:
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            frame_rate = wav_file.getframerate()
            raw_audio = wav_file.readframes(wav_file.getnframes())

        self._player.play_bytes(raw_audio, channels, sample_width, frame_rate)
    
    def get_voices(self):
        """
        Fetches available voices from the Deepgram API.

        Returns:
            list: A list of available voices.
        """
        url = "https://api.deepgram.com/v1/models"
        headers = {
            "Authorization": f"Token {self._apiKey}"
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        
        voices = []
        for model in data.get("tts", []):
            voice_name = model.get("canonical_name")
            if voice_name:
                voices.append(voice_name)
        return voices

