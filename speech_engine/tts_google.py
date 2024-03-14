from gtts import gTTS
from playsound import playsound
import os
from .exceptions import FileExtensionError
from time import sleep

class TTS_Google:
    """
    The TTS_Google class provides functionality to synthesize text into speech using the gTTS library.
    """

    def __init__(self):
        self._lang = 'en'
        self._tld = ''
        self._slow = False

    def get_language(self) -> str:
        """
        Returns the current language.

        Returns:
            str: The current language.
        """
        return self._lang

    def set_language(self, lang : str):
        """
        Set the language for text synthesis.

        Args:
            lang (str): The language code.

        """
        self._lang = lang

    def get_tld(self) -> str:
        """
        Returns the current top-level domain (TLD).

        Returns:
            str: The current top-level domain (TLD).
        """
        return self._tld

    def set_tld(self, tld : str):
        """
        Set the top-level domain (TLD) for regional language accents.

        Args:
            tld (str): The top-level domain (TLD) code.

        """
        self._tld = tld

    def get_slow(self) -> bool:
        """
        Returns the current speech speed setting.

        Returns:
            bool: The current speech speed setting.
        """
        return self._slow

    def set_slow(self, slow : bool):
        """
        Set the speech speed.

        Args:
            slow (bool): True to enable slow speech, False otherwise.

        """
        self._slow = slow
        
    def speak(self, text):
        """
        Synthesizes the given text into speech and plays it.

        Args:
            text (str): The text to be synthesized into speech.
        """
        if self._tld:
            gtts = gTTS(text=text, tld=self._tld, lang=self._lang, slow=self._slow)
        else:
            gtts = gTTS(text=text, lang=self._lang, slow=self._slow)

        gtts.save("speech.mp3")
        sleep(0.5)
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

        if self._tld:
            gtts = gTTS(text=text, tld=self._tld, lang=self._lang, slow=self._slow)
        else:
            gtts = gTTS(text=text, lang=self._lang, slow=self._slow)

        gtts.save(filename)