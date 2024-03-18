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
    """

    def __init__(self, authToken : str):
        if not authToken:
            raise ValueError("Auth Token cannot be empty")
        
        self._auth_token = authToken
        self.is_valid_token = self._validate_token()

        if not self.is_valid_token:
            raise InvalidTokenError()
        
        self._voice = 'Colin'
        self._speed = None
        self._pitch = None

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

    def get_speed(self) -> int:
        """
        Returns the current speed.

        Returns:
            int: The current speed.
        """
        return self._speed

    def set_speed(self, speed : int):
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

    def set_pitch(self, pitch : int):
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
            'Authorization': f'Bearer {self._auth_token}',
        }
        response = requests.get('https://api.wit.ai/voices?v=20220622', headers=headers)
        return response.status_code == 200

    def speak(self, text : str):
        """
        Synthesizes the given text into speech and plays it.

        Args:
            text (str): The text to be synthesized into speech.
        """
        
        data = { 'q': text, 'voice': self._voice }
        if self._speed:
            data['speed'] = self._speed
        
        if self._pitch:
            data['speed'] = self._pitch
        
        audio= requests.post(
        'https://api.wit.ai/synthesize',
        params={
            'v': '20220622',
        },
        headers={
            'Authorization': f'Bearer {self._auth_token}',
        },
        json=data,
        )

        with open("speech.mp3", "wb") as f:
            f.write(audio.content)
        f.close()
        sleep(0.3)
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
        if filename.split(".")[-1] != "mp3": raise FileExtensionError

        data = { 'q': text, 'voice': self._voice }
        if self._speed:
            data['speed'] = self._speed
        
        if self._pitch:
            data['speed'] = self._pitch
        
        audio= requests.post(
        'https://api.wit.ai/synthesize',
        params={
            'v': '20220622',
        },
        headers={
            'Authorization': f'Bearer {self._auth_token}',
        },
        json=data,
        )

        with open(filename, "wb") as f:
            f.write(audio.content)
        f.close()


    def get_voices(self):
        """
        Fetches available voices from the Wit.ai API.

        Returns:
            list: A list of available voices.
        """ 
        headers = {
            'Authorization': f'Bearer {self._auth_token}',
        }
        response = requests.get('https://api.wit.ai/voices?v=20220622', headers=headers)
        resp = json.loads(response.content)

        voices = []
        for locale_voices in resp.values():
            for voice in locale_voices:
                voices.append(voice['name'].replace("wit$", ""))

        return voices