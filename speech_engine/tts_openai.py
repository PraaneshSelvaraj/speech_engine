import os
from openai import OpenAI
from playsound import playsound
from .exceptions import FileExtensionError

class TTS_Openai:
    """
    The TTS_Openai class provides functionality to synthesize text into speech using the OpenAI

    Args:
        apiKey (str): The Open AI API Key.
    """

    def __init__(self, apiKey : str):
        if not apiKey:
            raise ValueError("API key cannot be empty")
        
        self._apiKey = apiKey
        self._voice = "alloy"
        self._client = OpenAI(api_key=apiKey)

        return
    
    def get_voice(self) -> str:
        """
        Returns the current voice.

        Returns:
            str: The current voice.
        """
        return self._voice

    def set_voice(self, voice : str):
        """
        Sets the voice to be used for synthesis.

        Args:
            voice (str): The voice to be set.
        """
        self._voice = voice

    def speak(self, text : str):
        """
        Synthesizes the given text into speech and plays it.

        Args:
            text (str): The text to be synthesized into speech.
        """
        response = self._client.audio.speech.create(
        model="tts-1",
        voice=self._voice,
        input=text
        )
        
        response.stream_to_file("speech.mp3")
        playsound("speech.mp3")
        os.remove("speech.mp3")

    def save(self, text : str, filename : str):
        """
        Synthesizes the given text into speech and saves it as an audio file.

        Args:
            text (str): The text to be synthesized into speech.
            filename (str): The filename to save the audio file (should have a .mp3 extension).

        Raises:
            FileExtensionError: If the provided filename doesn't have a .mp3 extension.

        """
        if filename.split(".")[-1] != "mp3": raise FileExtensionError

        response = self._client.audio.speech.create(
        model="tts-1",
        voice=self._voice,
        input=text
        )
        
        response.stream_to_file(filename)

    def get_voices(self) -> list:
        """
        Returns available voices

        Returns:
            list : A list of available voices
        """
        voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        return voices