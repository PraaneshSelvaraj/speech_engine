import io

import pyaudio


class AudioPlayer:
    def __init__(self, chunk_size: int = 512) -> None:
        """
        Initializes the AudioPlayer with a given chunk size.

        Args:
            chunk_size (int): The size of the audio buffer for playback.
        """
        self.chunk_size = chunk_size
        self.p = pyaudio.PyAudio()

    def play_bytes(
        self, audio_data: bytes, channels: int, sample_width: int, frame_rate: int
    ) -> None:
        """
        Plays audio data directly from bytes or a BytesIO object.

        Args:
            audio_data (bytes or io.BytesIO): The raw audio data.
            channels (int): Number of audio channels (1 for mono, 2 for stereo).
            sample_width (int): Sample width in bytes (e.g., 2 for 16-bit audio).
            frame_rate (int): Frame rate (sampling rate in Hz).
        """

        audio = io.BytesIO(audio_data)
        stream = self.p.open(
            format=self.p.get_format_from_width(sample_width),
            channels=channels,
            rate=frame_rate,
            output=True,
        )

        data = audio.read(self.chunk_size)

        while data:
            stream.write(data)
            data = audio.read(self.chunk_size)

        stream.stop_stream()
        stream.close()
