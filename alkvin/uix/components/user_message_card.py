"""
User Message Card
=================

This module contains the UserMessageCard class, which is a custom card widget
used for displaying in-chat messages from a user.

Example usage:
    card = UserMessageCard(message: UserMessage)
"""

from datetime import datetime

from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty

from kivymd.uix.card import MDCard


Builder.load_string(
    """
#:import AudioPlayerBox alkvin.uix.components.audio_player_box.AudioPlayerBox


<UserMessageCard>:
    orientation: "horizontal"
    md_bg_color: app.theme_cls.accent_light
    radius: "25dp", "25dp", "25dp", 0
    elevation: 1 if self.is_message_sent else 0
    opacity: 1 if self.is_message_sent else 0.8
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
            height: 0 if root.user_transcript else self.minimum_height
            opacity: 0 if root.user_transcript else 1
            disabled: bool(root.user_transcript)
            
            MDIconButton:
                icon: "typewriter"
                icon_size: "24dp"

                on_release: print("STT")  # TODO: Implement STT

        MDBoxLayout:
            size_hint_y: None
            height: self.minimum_height if root.user_transcript else 0
            opacity: 1 if root.user_transcript else 0
            
            MDLabel:
                text: root.user_transcript
                adaptive_height: True
    
    MDRelativeLayout:
        size_hint_x: None
        width: 0 if root.is_message_sent else "48dp"
        disabled: root.is_message_sent
        opacity: 0. if root.is_message_sent else 1.

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
                
                on_release: root.send_message()    
"""
)


class UserMessageCard(MDCard):
    """Custom card widget for displaying messages from a user."""

    message = ObjectProperty()

    user_audio_path = StringProperty()
    user_transcript = StringProperty()

    is_message_sent = BooleanProperty(False)

    on_message_sent_callback = None

    def __init__(self, message, on_message_sent_callback, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.on_message_sent_callback = on_message_sent_callback

        self.user_audio_path = message.audio_path
        self.user_transcript = message.transcript

        self.is_message_sent = message.sent_at is not None

    def send_message(self):
        self.message.sent_at = datetime.now()
        self.message.save()

        self.is_message_sent = True

        if self.on_message_sent_callback is not None:
            self.on_message_sent_callback(self)
