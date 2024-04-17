"""
Chats Screen
============

This module defines the ChatScreen class which represents the screen
for displaying a list of previous chats and provides functionality
for creating a new chat.
"""

from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, StringProperty

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem

from alkvin.entities.chat import Chat


Builder.load_string(
    """
#:import FAB alkvin.uix.components.fab.FAB


<ChatsScreenChatItem>:
    text: root.chat_title
    secondary_text: root.chat_summary

    on_release: root.switch_to_chat()


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
            
            on_release: root.switch_to_new_chat()
"""
)


class ChatsScreenChatItem(TwoLineListItem):
    """Custom list item widget for displaying chat items."""

    chat_id = NumericProperty()
    chat_title = StringProperty()
    chat_summary = StringProperty()

    def switch_to_chat(self):
        app = MDApp.get_running_app()
        chat = Chat.get_by_id(self.chat_id)
        app.root.switch_screen("chat_screen", chat)


class ChatsScreen(MDScreen):
    """Screen for displaying a list of previous chats."""

    chats = ListProperty()
    chat_items = ListProperty()

    def on_pre_enter(self):
        self.chat_items = [
            {
                "chat_id": chat.id,
                "chat_title": chat.title,
                "chat_summary": chat.summary,
            }
            for chat in self.chats
        ]

    def switch_to_new_chat(self):
        new_chat = Chat.create()

        self.manager.switch_screen("chat_screen", new_chat)
