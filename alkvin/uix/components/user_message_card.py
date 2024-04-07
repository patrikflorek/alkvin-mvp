"""
User Message Card
=================

This module contains the UserMessageCard class, which is a custom card widget
used for displaying in-chat messages from a user.

Example usage:
    card = UserMessageCard(
        user_audio_file="user_voice_audio.wav",
        user_audio_created_at="2022-01-02 09:00:00",
        message_sent_at="2022-01-02 09:01:00",
        transcript_text="Hello, I need your help.",
        transcript_received_at="2022-01-02 09:02:00"
    )
"""

from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.card import MDCard


Builder.load_string(
    """
#:import AudioPlayerBox alkvin.uix.components.audio_player_box.AudioPlayerBox


<UserMessageCard>:
    orientation: "horizontal"
    md_bg_color: app.theme_cls.accent_light
    radius: "25dp", "25dp", "25dp", 0
    elevation: 1 if self.message_sent_at else 0
    opacity: 1 if self.message_sent_at else 0.8
    adaptive_height: True

    MDBoxLayout:
        orientation: "vertical"
        padding: "24dp"
        spacing: "12dp"
        adaptive_height: True

        AudioPlayerBox:
            audio_path: root.user_audio_path
            progress_bar_color: app.theme_cls.accent_color

        MDBoxLayout:
            size_hint_y: None
            height: 0 if root.transcript_received_at else self.minimum_height
            opacity: 0 if root.transcript_received_at else 1
            disabled: root.transcript_received_at
            
            MDIconButton:
                icon: "typewriter"
                icon_size: "24dp"

                on_release: print("STT")  # TODO: Implement STT

        MDBoxLayout:
            size_hint_y: None
            height: self.minimum_height if root.transcript_received_at else 0
            opacity: 1 if root.transcript_received_at else 0
            
            MDLabel:
                text: root.transcript_text
                adaptive_height: True
    
    MDRelativeLayout:
        size_hint_x: None
        width: 0 if root.message_sent_at else "48dp"
        disabled: root.message_sent_at
        opacity: 0 if root.message_sent_at else 1

        MDAnchorLayout:
            anchor_x: "right"
            anchor_y: "top"
            padding: "16dp"

            MDIconButton:
                icon: "close"
                icon_size: "18dp"
                
                on_release: print("Remove message")  # TODO: Implement message removal

        MDAnchorLayout:
            anchor_x: "right"
            anchor_y: "bottom"
            padding: "16dp"

            MDIconButton:
                icon: "send"
                icon_size: "24dp"
                
                on_release: print("Send message")  # TODO: Implement message sending    
"""
)


class UserMessageCard(MDCard):
    """Custom card widget for displaying messages from a user."""

    user_audio_file = StringProperty()
    user_audio_path = StringProperty()
    user_audio_created_at = StringProperty()
    message_sent_at = StringProperty()
    transcript_text = StringProperty()
    transcript_received_at = StringProperty()

    def __init__(
        self,
        user_audio_file,
        user_audio_created_at,
        message_sent_at,
        transcript_text,
        transcript_received_at,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.user_audio_file = user_audio_file
        self.user_audio_created_at = user_audio_created_at
        self.message_sent_at = message_sent_at
        self.transcript_text = transcript_text
        self.transcript_received_at = transcript_received_at
