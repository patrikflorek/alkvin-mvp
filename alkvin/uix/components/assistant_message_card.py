"""
Assistant Message Card
======================

This module defines the AssistantMessageCard class, which is a custom card
widget used for displaying in-chat messages from an AI assistant.

Example usage:
    card = AssistantMessageCard(
        completion_text="Hello, how can I assist you?",
        completion_received_at="2022-01-01 10:00:00",
        speech_audio_file="tts_audio.wav",
        speech_audio_received_at="2022-01-01 10:01:00"
    )
"""

from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.card import MDCard


Builder.load_string(
    """
#:import AudioPlayerBox alkvin.uix.components.audio_player_box.AudioPlayerBox


<AssistantMessageCard>:
    orientation: "vertical"
    padding: "24dp"
    spacing: "12dp"
    md_bg_color: app.theme_cls.primary_light
    radius: "25dp", 0, "25dp", "25dp"
    elevation: 1 if self.speech_audio_received_at else 0
    opacity: 1 if self.speech_audio_received_at else 0.8
    adaptive_height: True

    MDLabel:
        text: root.completion_text
        font_style: "H6"
        adaptive_height: True

    MDBoxLayout:
        size_hint_y: None
        height: 0 if root.speech_audio_received_at else self.minimum_height
        opacity: 0 if root.speech_audio_received_at else 1
        disabled: root.speech_audio_received_at
        
        MDIconButton:
            icon: "account-voice"
            icon_size: "24dp"

            on_release: print("TTS")  # TODO: Implement TTS

    AudioPlayerBox:
        audio_path: root.speech_audio_file
        progress_bar_color: app.theme_cls.primary_color

        height: "48dp" if root.speech_audio_received_at else 0
        opacity: 1 if root.speech_audio_received_at else 0
        disabled: not root.speech_audio_received_at       
"""
)


class AssistantMessageCard(MDCard):
    """Custom card widget for displaying messages from an AI assistant."""

    completion_text = StringProperty()
    completion_received_at = StringProperty()
    speech_audio_file = StringProperty()
    speech_audio_received_at = StringProperty()

    def __init__(
        self,
        completion_text,
        completion_received_at,
        speech_audio_file,
        speech_audio_received_at,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.completion_text = completion_text
        self.completion_received_at = completion_received_at
        self.speech_audio_file = speech_audio_file
        self.speech_audio_received_at = speech_audio_received_at
