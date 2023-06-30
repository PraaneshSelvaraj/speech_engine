# speech-engine

speech_engine is a Python package that provides a simple interface for synthesizing text into speech using multiple .

## Installation

You can install `speech-engine` using pip:

```python
pip install speech-engine
```

## Usage

### Basic Usage

```python
from speech_engine import TTS_Google, FileExtensionError

# Instantiate TTS_Google
tts = TTS_Google()

# Set the language and other options
tts.lang = 'en'
tts.slow = False

# Synthesize and play speech
tts.speak("Hello, world!")

# Synthesize and save speech as an audio file
try:
    tts.save("Hello, world!", "output.mp3")
except FileExtensionError as e:
    print(e.message)
```


### Customizing Options
You can customize various options of the TTS_Google class:


```python
# Set the language
tts.lang = 'en'

# Set the top-level domain (optional)
tts.tld = 'com'

# Set the speech speed
tts.slow = False
```

### Handling File Extension Errors
When using the save() method, if the provided filename does not have a .mp3 extension, a FileExtensionError will be raised. You can handle this exception as follows:

```python
try:
    tts.save("Hello, world!", "output.wav")
except FileExtensionError as e:
    print(e.message)
```

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/PraaneshSelvaraj/speech_engine/blob/main/LICENSE) file for details.

## Contributions
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.
