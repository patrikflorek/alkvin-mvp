class AudioPlayer:
    def __init__(self, on_playback_finished):
        self._on_playback_finished_callback = on_playback_finished
