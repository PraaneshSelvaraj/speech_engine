# Speech Engine

Speech Engine is a Python package that provides a simple interface for synthesizing text into speech using different TTS engines, including Google Text-to-Speech (gTTS), Wit.ai Text-to-Speech (Wit TTS), OpenAI TTS, Deepgram TTS, ElevenLabs TTS, and PlayAI TTS.

## Installation

You can install `speech-engine` using pip:

```bash
pip install speech-engine
```

## Usage

### TTS_GOOGLE

```python
from speech_engine import TTS_Google, FileExtensionError

# Instantiate TTS_Google
tts = TTS_Google()

# Set the language and other options
tts.set_language('en')
tts.set_slow(False)

# Synthesize and play speech
tts.speak("Hello, world!")

# Synthesize and save speech as an audio file
try:
    tts.save("Hello, world!", "output.mp3")
except FileExtensionError as e:
    print(e.message)
```

### TTS_Witai

```python
from speech_engine import TTS_Witai

# Instantiate TTS_Witai with the Wit.ai auth token
tts = TTS_Witai(your_authtoken)

# Set the voice
tts.set_voice('Colin')

# Synthesize and play speech
tts.speak("Hello, world!")

# Synthesize and save speech as an audio file
tts.save("Hello, world!", "output.wav")


# Get available voices
voices = tts.get_voices()
print(voices)
```

### TTS_Openai

```python
from speech_engine import TTS_Openai

# Instantiate TTS_Openai with the Openai Api key
tts = TTS_Openai(your_apikey)

# Set the voice
tts.set_voice('alloy')

# Synthesize and play speech
tts.speak("Hello, world!")

# Synthesize and save speech as an audio file
tts.save("Hello, world!", "output.mp3")

# Get available voices
voices = tts.get_voices()
print(voices)
```

### TTS_Deepgram

```python
from speech_engine import TTS_Deepgram

# Instantiate TTS_Deepgram with the Deepgram Api key
tts = TTS_Deepgram(your_apikey)

# Set the voice
tts.set_voice('aura-angus-en')

# Synthesize and play speech
tts.speak("Hello, world!")

# Synthesize and save speech as an audio file
tts.save("Hello, world!", "output.wav")

# Get available voices
voices = tts.get_voices()
print(voices)
```

### TTS_ElevenLabs

```python
from speech_engine import TTS_ElevenLabs

# Instantiate TTS_ElevenLabs with the ElevenLabs API key
tts = TTS_ElevenLabs(your_apikey)

# Set the voice (voice ID)
tts.set_voice('UgBBYS2sOqTuMpoF3BR0')

# Synthesize and play speech
tts.speak("Hello, world!")

# Synthesize and save speech as an audio file
tts.save("Hello, world!", "output.mp3")

# Get available voices
voices = tts.get_voices()
print(voices)
```

### TTS_Playai

```python
from speech_engine import TTS_Playai

# Instantiate TTS_Playai with the Groq API key
tts = TTS_Playai(your_apikey)

# Set the voice
tts.set_voice('Arista-PlayAI')

# Synthesize and play speech
tts.speak("Hello, world!")

# Synthesize and save speech as an audio file
tts.save("Hello, world!", "output.wav")

# Get available voices
voices = tts.get_voices()
print(voices)
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/PraaneshSelvaraj/speech_engine/blob/main/LICENSE) file for details.

## Contributions

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.
