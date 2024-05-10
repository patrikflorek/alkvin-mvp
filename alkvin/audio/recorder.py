import pyaudio

from pydub import AudioSegment


class AudioRecorder:
    # PyAudio parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    def __init__(self, on_recording_finished):
        self.on_recording_finished = on_recording_finished

        self._p = pyaudio.PyAudio()
        self._stream = None
        self._frames = []
        self._frame_count = 0
        self._recording_path = None

    @property
    def recording_time(self):
        if self._stream is None or not self._stream.is_active():
            return 0

        return self._frame_count / self.RATE

    def record(self, recording_path):
        self._recording_path = recording_path
        self._frames = []
        self._frame_count = 0

        self._stream = self._p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self._stream_callback,
        )

    def _stream_callback(self, in_data, frame_count, time_info, status):
        self._frames.append(in_data)
        self._frame_count += frame_count

        return in_data, pyaudio.paContinue

    def stop(self):
        audio_segment = AudioSegment(
            b"".join(self._frames), sample_width=2, frame_rate=44100, channels=1
        )
        audio_segment.export("test.mp3", format="mp3")
        self.on_recording_finished(self._recording_path)
