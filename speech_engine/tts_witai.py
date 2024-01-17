from .exceptions import InvalidTokenError, FileExtensionError
import winsound
import requests
import os
import json
from time import sleep

class TTS_Witai:
    """
    The TTS_Witai class provides functionality to synthesize text into speech using the wit.ai

    Args:
        authToken (str): The Wit.ai auth token.

    Attributes:
        voice (str): The selected voice for synthesis.

    """
    def __init__(self, authToken):
        self.auth_token = authToken
        self.is_valid_token = self._validate_token()
        if not self.is_valid_token:
            raise InvalidTokenError()
        self.voice = 'Colin'
        self.speed = None
        self.pitch = None

    def _validate_token(self):
        """
        Validate the Wit.ai auth token.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
        }
        response = requests.get('https://api.wit.ai/voices?v=20220622', headers=headers)
        return response.status_code == 200

    def speak(self, text):
        """
        Synthesizes the given text into speech and plays it.

        Args:
            text (str): The text to be synthesized into speech.
        """
        
        data = { 'q': text, 'voice': self.voice }
        if self.speed:
            data['speed'] = self.speed
        
        if self.pitch:
            data['speed'] = self.pitch
        
        audio= requests.post(
        'https://api.wit.ai/synthesize',
        params={
            'v': '20220622',
        },
        headers={
            'Authorization': f'Bearer {self.auth_token}',
        },
        json=data,
        )

        with open("speech.mp3", "wb") as f:
            f.write(audio.content)
        f.close()
        sleep(1)
        winsound.PlaySound("speech.mp3", winsound.SND_FILENAME)
        os.remove("speech.mp3")

    def save(self, text, filename):
        """
        Synthesizes the given text into speech and saves it as an audio file.

        Args:
            text (str): The text to be synthesized into speech.
            filename (str): The filename to save the audio file (should have a .mp3 extension).

        Raises:
            FileExtensionError: If the provided filename doesn't have a .mp3 extension.

        """
        if not filename.endswith('.mp3'):
            raise FileExtensionError()
        audio= requests.post(
        'https://api.wit.ai/synthesize',
        params={
            'v': '20220622',
        },
        headers={
            'Authorization': f'Bearer {self.auth_token}',
        },
        json={ 'q': text, 'voice': self.voice },
        )

        with open("speech.mp3", "wb") as f:
            f.write(audio.content)
        f.close()

    def get_voices(self):
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
        }
        response = requests.get('https://api.wit.ai/voices?v=20220622', headers=headers)
        resp = json.loads(response.content)

        voices = []
        for locale_voices in resp.values():
            for voice in locale_voices:
                voices.append(voice['name'])

        return voices