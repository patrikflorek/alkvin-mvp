"""
Audio Player Box
================

This model defines the AudioPlayerBox class, which is a custom box layout
widget used for playing audio files.
"""

from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty

from kivymd.uix.boxlayout import MDBoxLayout


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
        icon: "play" if root.state == "stopped" else "stop"
        theme_icon_color: "Custom"
        icon_color: (0.2, 0.2, 0.2, 0.6)
        
        on_release: root.toggle_playing()  # TODO: Implement play audio

    MDBoxLayout:
        padding: dp(10), dp(20), dp(30), dp(20)
        MDProgressBar:
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

    def toggle_playing(self):
        if self.state == "stopped":
            self.state = "playing"
            print("Start playing audio")
        else:
            self.state = "stopped"
            print("Stop playing audio")
