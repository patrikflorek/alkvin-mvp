from .recorder import AudioRecorder
from .player import AudioPlayer


class AudioBus:
    def __init__(self):
        self._state = "idle"

        self._active_audio_widget = None

        self._audio_recorder = AudioRecorder(
            on_recording_finished=self._on_recording_finished
        )
        self._audio_player = AudioPlayer(
            on_playback_finished=self._on_playback_finished
        )

    @property
    def state(self):
        return self._state

    @property
    def audio_passed_time(self):
        if self._state == "idle":
            return 0

        if self._state == "recording":
            return self._audio_recorder.recording_time

        if self._state == "playing":
            return self._audio_player.playing_time

    @property
    def audio_total_time(self):
        if self._state == "idle":
            return 0

        if self._state == "recording":
            return self._audio_recorder.recording_time

        if self._state == "playing":
            return self._audio_player.total_time

    def record(self, audio_recorder_widget, recording_path):
        if self._state == "playing":
            self._audio_player.stop()
            self._active_audio_widget.state = "stopped"

        self._active_audio_widget = audio_recorder_widget

        self._audio_recorder.record(recording_path)

        self._state = "recording"

    def play(self, audio_player_widget, audio_path):
        if self._state == "recording":
            return

        if self._state == "playing":
            self._active_audio_widget.state = "stopped"
            self._audio_player.stop()

        self._active_audio_widget = audio_player_widget
        self._audio_player.play(audio_path)
        self._active_audio_widget.state = "playing"

        self._state = "playing"

    def stop(self, audio_widget=None):
        if self._state == "recording" and audio_widget is self._active_audio_widget:
            self._audio_recorder.stop()

        if self._state == "playing":
            self._audio_player.stop()

    def _on_recording_finished(self, recording_path):
        if self._active_audio_widget is None:
            return

        self._active_audio_widget.recording_path = recording_path

        self._active_audio_widget = None
        self._state = "idle"

    def _on_playback_finished(self):
        if self._active_audio_widget is None:
            return

        self._active_audio_widget.state = "stopped"
        self._active_audio_widget = None
        self._state = "idle"
