import static_ffmpeg

static_ffmpeg.add_paths()

from .exceptions import FileExtensionError, InvalidTokenError
from .tts_deepgram import TTS_Deepgram
from .tts_elevenlabs import TTS_ElevenLabs
from .tts_google import TTS_Google
from .tts_openai import TTS_Openai
from .tts_playai import TTS_Playai
from .tts_witai import TTS_Witai
