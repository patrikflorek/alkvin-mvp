"""
Chats Screen
============

This module defines the ChatScreen class which represents the screen
for displaying a list of previous chats and provides functionality
for creating a new chat.
"""

from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem


Builder.load_string(
    """
#:import FAB alkvin.uix.components.fab.FAB


<ChatsScreenChatItem>:
    on_release: app.root.switch_screen("chat_screen", {"chat_id": self.chat_id})


<ChatsScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Chats"
            specific_text_color: app.theme_cls.opposite_text_color
            left_action_items: 
                [
                ["arrow-left", lambda x: app.root.switch_back(), "Back", "Back"]
                ]
        
        MDRecycleView:
            data: root.chat_items
            viewclass: "ChatsScreenChatItem"

            MDRecycleGridLayout:
                cols: 1
                default_size: None, None
                default_size_hint: 1, None
                adaptive_height: True

    MDAnchorLayout:
        anchor_x: "right"
        anchor_y: "bottom"
        padding: dp(48)

        FAB:
            icon: "message-plus"
            
            on_release: app.root.switch_screen("chat_screen", {"chat_id": None})
"""
)


class ChatsScreenChatItem(TwoLineListItem):
    """Custom list item widget for displaying chat items."""

    chat_id = NumericProperty()


class ChatsScreen(MDScreen):
    """Screen for displaying a list of previous chats."""

    chat_items = ListProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self):
        self.chat_items = [
            {"chat_id": i, "text": f"Chat {i}", "secondary_text": f"Chat {i} summary"}
            for i in range(1, 6)
        ]
