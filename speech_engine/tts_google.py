from gtts import gTTS
from playsound import playsound
import os
from .exceptions import FileExtensionError
from time import sleep

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

        if self.tld:
            gtts = gTTS(text=text, tld=self.tld, lang=self.lang, slow=self.slow)
        else:
            gtts = gTTS(text=text, lang=self.lang, slow=self.slow)

        gtts.save(filename)