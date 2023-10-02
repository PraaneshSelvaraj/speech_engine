from gtts import gTTS
from playsound import playsound
import os
import winsound
import json

class FileExtensionError(Exception):
    def __init__(self, message="Output file type should be .mp3"):
        self.message = message
        super().__init__(self.message)

class InvalidTokenError(Exception):
    def __init__(self, message="Invalid AuthToken"):
        self.message = message
        super().__init__(self.message)

class TTS_Google:
    """
    The TTS_Google class provides functionality to synthesize text into speech using the gTTS library.

    Attributes:
        lang (str): The language code for the synthesized speech (e.g., 'en' for English).
        tld (str): The top-level domain for the gTTS service.
        slow (bool): Whether to generate speech at a slower speed.

    """

    def __init__(self):
        self.lang = 'en'
        self.tld = ''
        self.slow = False

    def speak(self, text):
        """
        Synthesizes the given text into speech and plays it.

        Args:
            text (str): The text to be synthesized into speech.
        """
        if self.tld:
            gtts = gTTS(text=text, tld=self.tld, lang=self.lang, slow=self.slow)
        else:
            gtts = gTTS(text=text, lang=self.lang, slow=self.slow)

        gtts.save("speech.mp3")
        playsound("speech.mp3")
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

        if self.tld:
            gtts = gTTS(text=text, tld=self.tld, lang=self.lang, slow=self.slow)
        else:
            gtts = gTTS(text=text, lang=self.lang, slow=self.slow)

        gtts.save(filename)

import requests

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

        with open("speech.mp3","wb") as f:
            f.writelines(audio)
        f.close()
        
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

        with open(filename,"wb") as f:
            f.writelines(audio)
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