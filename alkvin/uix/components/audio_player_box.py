"""
Audio Player Box
================

This model defines the AudioPlayerBox class, which is a custom box layout
widget used for playing audio files.
"""

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty

from kivymd.uix.boxlayout import MDBoxLayout

from alkvin.audio import get_audio_bus


Builder.load_string(
    """
<AudioPlayerBox>:
    orientation: "horizontal"
    size_hint_y: None
    height: "48dp"
    canvas:
        Color:
            rgba: (.5, .5, .5, .5)
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: (dp(24),)

    MDIconButton:
        id: play_button
        icon: "play" if root.state == "stopped" else "stop"
        theme_icon_color: "Custom"
        icon_color: (0.2, 0.2, 0.2, 0.6)
        
        on_release: root.toggle_playing()

    MDBoxLayout:
        padding: dp(10), dp(20), dp(30), dp(20)
        MDProgressBar:
            id: progress_bar
            min: 0.1
            max: 100
            value: .1
            color: root.progress_bar_color
"""
)


class AudioPlayerBox(MDBoxLayout):
    """Custom box layout widget used for playing audio files."""

    state = StringProperty("stopped")

    audio_path = StringProperty()
    progress_bar_color = ListProperty([0.2, 0.2, 0.2, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.audio_bus = get_audio_bus()
        self.progress_bar_update_schedule = None

    def _update_progress_bar(self, dt):

        progress = (
            self.ids.progress_bar.max
            if self.audio_bus.audio_total_time == 0
            else (self.audio_bus.audio_passed_time / self.audio_bus.audio_total_time)
        )

        self.ids.progress_bar.value = progress * (
            self.ids.progress_bar.max - self.ids.progress_bar.min
        )

    def on_state(self, instance, value):
        if value == "playing":
            self.ids.play_button.icon = "stop"
            self.progress_bar_update_schedule = Clock.schedule_interval(
                self._update_progress_bar, 0.2
            )
        elif value == "stopped":
            self.ids.play_button.icon = "play"
            self.progress_bar_update_schedule.cancel()
            self.progress_bar_update_schedule = None
            self.ids.progress_bar.value = self.ids.progress_bar.min

    def toggle_playing(self):
        if self.state == "stopped" and self.audio_bus.state != "recording":
            self.audio_bus.play(self, self.audio_path)
        elif self.state == "playing":
            self.audio_bus.stop(self)
