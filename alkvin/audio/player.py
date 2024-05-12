from kivy.clock import Clock

from pydub import AudioSegment
from pydub.playback import play


class AudioPlayer:
    def __init__(self, on_playback_finished):
        self._on_playback_finished = on_playback_finished

        self.audio = None
        self.playback = None
        self.position = 0  # in milliseconds
        self.is_playing = False

    @property
    def playing_time(self):
        if self.playback is None:
            return 0

        return self.position / 1000

    @property
    def total_time(self):
        if self.playback is None:
            return 0

        return len(self.audio) / 1000

    def _play_and_check(self, dt):
        chunk_size = dt * 100  # in milliseconds
        chunk = self.audio[self.position : self.position + chunk_size]
        play(chunk)
        self.position += chunk_size

        if not self.is_playing or self.position >= len(self.audio):
            self.stop()

    def play(self, audio_path):
        self.audio = AudioSegment.from_file(audio_path, format="mp3")
        self.position = 0
        self.is_playing = True
        # play(self.audio)

        self.playback = Clock.schedule_interval(self._play_and_check, 0.5)

    def stop(self):
        self.is_playing = False
        if self.playback is not None:
            self.playback.unschedule(self.playback)

        self.playback = None
        self.audio = None
        self.position = 0

        self._on_playback_finished()
