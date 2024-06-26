"""
Assistant Message Card
======================

This module defines the AssistantMessageCard class, which is a custom card
widget used for displaying in-chat messages from an AI assistant.

Example usage:
    card = AssistantMessageCard(message: AssistantMessage)
"""

import os

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty

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
    elevation: 1
    adaptive_height: True

    MDLabel:
        text: root.assistant_completion
        font_style: "H6"
        adaptive_height: True

    MDBoxLayout:
        size_hint_y: None
        height: 0 if root.assistant_speech_path is not None else self.minimum_height
        opacity: 0 if root.assistant_speech_path is not None else 1
        disabled: root.assistant_speech_path is not None
        
        MDIconButton:
            icon: "account-voice"
            icon_size: "24dp"

            on_release: root.synthesize_speech()

    AudioPlayerBox:
        audio_path: root.assistant_speech_path if root.assistant_speech_path else ""
        progress_bar_color: app.theme_cls.primary_color

        height: "48dp" if root.assistant_speech_path is not None else 0
        opacity: 1 if root.assistant_speech_path is not None else 0
        disabled: root.assistant_speech_path is None       
"""
)


class AssistantMessageCard(MDCard):
    """Custom card widget for displaying messages from an AI assistant."""

    message = ObjectProperty()
    chat = ObjectProperty()

    assistant_completion = StringProperty()
    assistant_speech_path = StringProperty(allownone=True)

    def __init__(self, message, chat, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.chat = chat

    def on_message(self, instance, message):
        """Update content of the recycled message widget."""

        self.assistant_completion = message.completion
        self.assistant_speech_path = message.speech_path

    def synthesize_speech(self):
        speech_file = self.chat.bot.synthesize_speech(self.message.completion)
        self.assistant_speech_path = os.path.join(self.chat.audio_dir, speech_file)

        # TODO: Move generated speech file to chat audio directory

        self.message.speech_file = speech_file
        self.message.save()
