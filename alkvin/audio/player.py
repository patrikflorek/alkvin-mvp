from kivy.core.audio import SoundLoader


class AudioPlayer:
    def __init__(self, on_playback_finished):
        self._on_playback_finished = on_playback_finished

        self.audio = None

    @property
    def playing_time(self):
        return self.audio.get_pos()

    @property
    def total_time(self):
        return self.audio.length

    def play(self, audio_path):
        self.audio = SoundLoader.load(audio_path)
        self.audio.bind(on_stop=lambda dt: self._on_playback_finished())
        self.audio.volume = 0.5
        self.audio.play()

    def stop(self):
        self.audio.stop()
        self.audio = None
        self._on_playback_finished()
