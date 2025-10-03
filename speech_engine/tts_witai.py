import io
import wave

import requests

from .audioPlayer import AudioPlayer
from .exceptions import FileExtensionError, InvalidTokenError


class TTS_Witai:
    """
    The TTS_Witai class provides functionality to synthesize text into speech using the wit.ai

    Args:
        authToken (str): The Wit.ai auth token.
    """

    def __init__(self, authToken: str):
        if not authToken:
            raise ValueError("Auth Token cannot be empty")

        self._auth_token = authToken
        self._api_version = "20220622"
        self._request_headers = {"Authorization": f"Bearer {self._auth_token}"}

        if not self._validate_token():
            raise InvalidTokenError()

        self._voice = "Colin"
        self._speed = None
        self._pitch = None
        self._player = AudioPlayer()

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

    def get_speed(self) -> int:
        """
        Returns the current speed.

        Returns:
            int: The current speed.
        """
        return self._speed

    def set_speed(self, speed: int):
        """
        Sets the speed of speech synthesis.

        Args:
            speed (int): The speed to be set.
        """
        self._speed = speed

    def get_pitch(self) -> int:
        """
        Returns the current pitch.

        Returns:
            int: The current pitch.
        """
        return self._pitch

    def set_pitch(self, pitch: int):
        """
        Sets the pitch of speech synthesis.

        Args:
            pitch (int): The pitch to be set.
        """
        self._pitch = pitch

    def _validate_token(self):
        """
        Validate the Wit.ai auth token.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        headers = {
            "Authorization": f"Bearer {self._auth_token}",
        }
        return (
            requests.get(
                "https://api.wit.ai/voices?v=20220622", headers=headers
            ).status_code
            == 200
        )

    def _prepare_payload(self, text: str) -> dict:
        """Prepares the request payload for text-to-speech synthesis."""
        payload = {"q": text, "voice": self._voice}
        if self._speed:
            payload["speed"] = self._speed
        if self._pitch:
            payload["pitch"] = self._pitch
        return payload

    def _synthesize_speech(self, text: str) -> bytes:
        """Calls Wit.ai API to synthesize speech and returns the raw audio content."""
        resp = requests.post(
            "https://api.wit.ai/synthesize",
            params={"v": self._api_version},
            headers=self._request_headers,
            json=self._prepare_payload(text),
        )

        if resp.status_code != 200:
            raise Exception(f"API Error: {resp.status_code} - {resp.text}")

        return resp.content

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

    def get_voices(self):
        """
        Fetches available voices from the Wit.ai API.

        Returns:
            list: A list of available voices.
        """
        response = requests.get(
            f"https://api.wit.ai/voices?v={self._api_version}",
            headers=self._request_headers,
        )
        resp = response.json()

        voices = []
        for locale_voices in resp.values():
            for voice in locale_voices:
                voices.append(voice["name"].replace("wit$", ""))

        return voices
