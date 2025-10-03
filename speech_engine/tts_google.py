import io

from gtts import gTTS
from pydub import AudioSegment

from .audioPlayer import AudioPlayer
from .exceptions import FileExtensionError


class TTS_Google:
    """
    The TTS_Google class provides functionality to synthesize text into speech using the gTTS library.
    """

    def __init__(self):
        self._lang = "en"
        self._tld = ""
        self._slow = False
        self._player = AudioPlayer()

    def get_language(self) -> str:
        """
        Returns the current language.

        Returns:
            str: The current language.
        """
        return self._lang

    def set_language(self, lang: str):
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

    def set_tld(self, tld: str):
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

    def set_slow(self, slow: bool):
        """
        Set the speech speed.

        Args:
            slow (bool): True to enable slow speech, False otherwise.

        """
        self._slow = slow

    def _synthesize_speech(self, text: str) -> gTTS:
        """
        Generates a gTTS audio object.

        Args:
            text (str): The text to be synthesized.

        Returns:
            gTTS: gTTS object.
        """
        if self._tld:
            return gTTS(text=text, lang=self._lang, tld=self._tld, slow=self._slow)

        return gTTS(text=text, lang=self._lang, slow=self._slow)

    def speak(self, text: str):
        """
        Synthesizes the given text into speech and plays it.

        Args:
            text (str): The text to be synthesized into speech.
        """
        gtts = self._synthesize_speech(text)

        mp3_buffer = io.BytesIO()
        gtts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)

        audio = AudioSegment.from_mp3(mp3_buffer)
        audio = audio.set_frame_rate(44100).set_sample_width(2).set_channels(2)

        self._player.play_bytes(
            audio.raw_data, channels=2, sample_width=2, frame_rate=44100
        )

    def save(self, text: str, filename: str = "output.mp3"):
        """
        Synthesizes the given text into speech and saves it as an audio file.

        Args:
            text (str): The text to be synthesized into speech.
            filename (str): The filename to save the audio file (should have a .mp3 extension).

        Raises:
            FileExtensionError: If the provided filename doesn't have a .mp3 extension.

        """
        if not filename.endswith(".mp3"):
            raise FileExtensionError()

        self._synthesize_speech(text).save(filename)
