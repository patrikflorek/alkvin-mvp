"""
Audio Recorder Box
==================

This module defines the AudioRecorderBox class, which is a custom box layout
widget used for recording audio.
"""

from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import CommonElevationBehavior


Builder.load_string(
    """
#:import FAB alkvin.uix.components.fab.FAB


<AudioRecorderBox>:
    size_hint_y: None
    height: "64dp"
    md_bg_color: app.theme_cls.accent_dark
    elevation: 2

    MDAnchorLayout:
        anchor_x: "left"
        anchor_y: "center"
        padding: "48dp", 0, 0, "96dp"
        
        FAB:
            icon: "microphone"
            md_bg_color: app.theme_cls.accent_dark
            icon_color: 
                (app.theme_cls.colors["LightGreen"]["A400"] 
                if root.state == "recording" 
                else app.theme_cls.colors["Gray"]["300"])
            
            on_release: root.toggle_recording()  # TODO: Implement record audio

    MDAnchorLayout:
        anchor_x: "right"
        anchor_y: "center"
        padding: 0, 0, "24dp", 0

        MDLabel:
            id: audio_recorder_timer

            padding: "24dp", 0
            text: "00:00"
            halign: "right"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: 
                (app.theme_cls.colors["LightGreen"]["A400"] 
                if root.state == "recording" 
                else app.theme_cls.colors["Gray"]["300"])
"""
)


class AudioRecorderBox(MDBoxLayout, CommonElevationBehavior):
    """Custom box layout and associated floating action button widget used for
    recording audio.
    """

    state = StringProperty("stopped")

    def toggle_recording(self):
        if self.state == "stopped":
            self.state = "recording"
            print("Start recording audio")
        else:
            self.state = "stopped"
            print("Stop recording audio")
