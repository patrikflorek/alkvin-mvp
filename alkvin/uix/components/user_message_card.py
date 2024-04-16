"""
User Message Card
=================

This module contains the UserMessageCard class, which is a custom card widget
used for displaying in-chat messages from a user.

Example usage:
    card = UserMessageCard(message: UserMessage)
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
    elevation: 1 if self.user_message_sent_at else 0
    opacity: 1 if self.user_message_sent_at else 0.8
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
            height: 0 if root.user_audio_transcript_received_at else self.minimum_height
            opacity: 0 if root.user_audio_transcript_received_at else 1
            disabled: root.user_audio_transcript_received_at
            
            MDIconButton:
                icon: "typewriter"
                icon_size: "24dp"

                on_release: print("STT")  # TODO: Implement STT

        MDBoxLayout:
            size_hint_y: None
            height: self.minimum_height if root.user_audio_transcript_received_at else 0
            opacity: 1 if root.user_audio_transcript_received_at else 0
            
            MDLabel:
                text: root.user_audio_transcript_text
                adaptive_height: True
    
    MDRelativeLayout:
        size_hint_x: None
        width: 0 if root.user_message_sent_at else "48dp"
        disabled: root.user_message_sent_at
        opacity: 0 if root.user_message_sent_at else 1

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

    user_audio_path = StringProperty()
    user_audio_transcript = StringProperty()
    user_audio_transcript_received_at = StringProperty()
    user_message_sent_at = StringProperty()

    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.user_audio_path = message.get_audio_path()
        self.user_audio_transcript = message.audio_transcript
        self.user_audio_transcript_received_at = message.transcript_received_at
        self.user_message_sent_at = message.sent_at
