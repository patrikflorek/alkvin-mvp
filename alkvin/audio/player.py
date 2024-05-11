from kivy.clock import Clock

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio


class AudioPlayer:
    def __init__(self, on_playback_finished):
        self._on_playback_finished = on_playback_finished

        self.playback = None
        self.playback_check_timer = None

        self.audio_segment = None

    @property
    def playing_time(self):
        if self.playback is None:
            return 0

        return self.playback.position / 1000

    @property
    def total_time(self):
        if self.playback is None:
            return 0

        return self.playback.duration / 1000

    def _check_playback(self, dt):
        if self.playback is None:
            return

        if (
            not self.playback.is_playing()
            or self.playback.position >= self.playback.duration
        ):
            self.stop()

    def play(self, audio_path):
        audio = AudioSegment.from_file(audio_path, format="mp3")

        self.playback = _play_with_simpleaudio(audio)

        self.playback_check_timer = Clock.schedule_interval(self._check_playback, 0.1)

    def stop(self):
        if self.playback is None:
            return

        self.playback_check_timer.cancel()
        self.playback.stop()
        self.playback = None

        self._on_playback_finished()
