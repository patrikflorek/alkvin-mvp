"""
Audio Recorder Box
==================

This module defines the AudioRecorderBox class, which is a custom box layout
widget used for recording audio.
"""

import os
from uuid import uuid4

from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import CommonElevationBehavior

from alkvin.audio import get_audio_bus

from alkvin.config import AUDIO_RECORDING_DIR


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
            
            on_release: root.state = "stopped" if root.state == "recording" else "recording"

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

    recording_path = StringProperty(allownone=True)

    def __init__(self, **kwargs):
        super(AudioRecorderBox, self).__init__(**kwargs)
        self._audio_bus = get_audio_bus()

    def on_state(self, instance, value):
        if value == "recording":
            self.recording_path = None

            os.makedirs(AUDIO_RECORDING_DIR, exist_ok=True)
            recording_path = os.path.join(
                AUDIO_RECORDING_DIR, f"user_{uuid4().hex[:8]}.mp3"
            )
            self._audio_bus.record(self, recording_path)

        elif value == "stopped":
            self._audio_bus.stop()
