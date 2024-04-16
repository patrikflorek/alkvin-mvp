"""
Chat Screen
===========

This module defines the ChatScreen class which represents the screen where 
a user can interact with a chat bot.

The ChatScreen class displays the chat messages between the user and 
the chat bot, as well as options to summarize the chat, select a user, select a bot, and delete the chat.
"""

from datetime import datetime

from kivy.lang import Builder
from kivy.properties import (
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

from alkvin.uix.components.select_user_dialog import SelectUserDialog
from alkvin.uix.components.user_message_card import UserMessageCard
from alkvin.uix.components.select_bot_dialog import SelectBotDialog
from alkvin.uix.components.assistant_message_card import AssistantMessageCard

from alkvin.entities.bot import Bot
from alkvin.entities.chat import Chat
from alkvin.entities.user import User


Builder.load_string(
    """
#:import AudioRecorderBox alkvin.uix.components.audio_recorder_box.AudioRecorderBox

        
<ChatScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Chat"
            specific_text_color: app.theme_cls.opposite_text_color
            use_overflow: True
            left_action_items: 
                [
                ["arrow-left", lambda x: app.root.switch_back(), "Back", "Back"]
                ]
            right_action_items: 
                [
                ["file-document", lambda x: root.summarize_chat(), "Summarize", "Summarize"],
                ["account", lambda x: root.select_user(), "User", "User"],
                ["robot", lambda x: root.select_bot(), "Bot", "Bot"],
                ["delete", lambda x: root.delete_chat_dialog.open(), "Delete", "Delete"]
                ]
        
        ScrollView:
            id: chat_screen_scroll
        
            MDGridLayout:
                id: chat_screen_message_container
                cols: 1
                padding: "40dp"
                spacing: "40dp"
                adaptive_height: True
                
                MDCard:
                    orientation: "vertical"
                    padding: "40dp", "40dp", "40dp", "20dp"
                    spacing: "40dp"
                    adaptive_height: True
                    radius: [dp(20)]
                    md_bg_color: "#efefef"
                    elevation: 0.5

                    MDLabel:
                        text: root.chat_title
                        font_style: "H6"
                        theme_text_color: "Primary"
                        adaptive_height: True

                    MDSeparator:
                        height: "1dp"
                
                    MDLabel:
                        text: root.chat_summary if root.chat_summary else "Press summarize button to generate a title and summary."
                        font_style: "Body1" if root.chat_summary else "Subtitle1"
                        theme_text_color: "Primary" if root.chat_summary else "Secondary"
                        adaptive_height: True


                    MDIconButton:
                        icon: "chevron-down"
                        theme_text_color: "Custom"
                        text_color: [0.4, 0.4, 0.4, 0.8]
                        pos_hint: {"center_x": .5}
                        
                        on_release: root.scroll_to_bottom()
                
                MDBoxLayout:
                    id: chat_screen_messages_container
                    
                    orientation: "vertical"
                    padding: 0, 0, 0, "64dp"
                    spacing: "28dp"
                    adaptive_height: True
                
    AudioRecorderBox:
        id: chat_screen_audio_recorder

        pos_hint: {"y": 0}
"""
)


class ChatScreen(MDScreen):
    """Screen for interacting with a chat bot using voice messages."""

    chat = ObjectProperty(allownone=True)
    chat_id = NumericProperty(allownone=True)

    chat_title = StringProperty("A new chat")
    chat_summary = StringProperty("This is a summary of the chat so far.")

    chat_messages = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.select_user_dialog = SelectUserDialog(self._on_select_user_callback)

        self.select_bot_dialog = SelectBotDialog(self._on_select_bot_callback)

        self.delete_chat_dialog = MDDialog(
            title="Delete chat",
            text="Are you sure you want to delete this chat?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.delete_chat_dialog.dismiss(),
                ),
                MDFlatButton(
                    text="DELETE",
                    theme_text_color="Error",
                    on_release=lambda x: self.delete_chat(),
                ),
            ],
        )

        self.ids.chat_screen_audio_recorder.on_recording_finished_callback = (
            self.process_audio_recording
        )

    def process_audio_recording(self, audio_recording_path):
        print("Processing the audio recording:", audio_recording_path)

    def _on_select_user_callback(self, user_id):
        self.chat.user = User.get(User.id == user_id)

        if self.chat.bot is None:
            self.select_bot()

    def _on_select_bot_callback(self, bot_id):
        self.chat.bot = Bot.get(Bot.id == bot_id)

    def _create_chat(self):
        self.chat = Chat.create(
            title=f"NEW CHAT [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
        )

        self.chat_id = self.chat.id
        self.chat_title = self.chat.title
        self.chat_summary = self.chat.summary

    def _load_chat(self):
        self.chat = Chat.get(Chat.id == self.chat_id)

        self.chat_title = self.chat.title
        self.chat_summary = self.chat.summary

    def _message_items_sort_key(self, message_item):
        role, message = message_item["role"], message_item["message"]

        is_unsent_user_message = role == "user" and message.sent_at is None
        in_chat_at = (message == "user" and message.sent_at) or (
            message == "assistant" and message.completion_received_at
        )

        return (is_unsent_user_message, in_chat_at)

    def on_pre_enter(self):
        if self.chat_id is None:
            self._create_chat()
        else:
            self._load_chat()

        user_message_items = [
            {"role": "user", "message": message} for message in self.chat.user_messages
        ]

        assistant_message_items = [
            {"role": "assistant", "message": message}
            for message in self.chat.assistant_messages
        ]

        sorted_message_items = sorted(
            user_message_items + assistant_message_items,
            key=self._message_items_sort_key,
        )

        self.ids.chat_screen_messages_container.clear_widgets()
        for message_item in sorted_message_items:
            sender_role = message_item["role"]
            message = message_item["message"]
            if sender_role == "user":
                self.ids.chat_screen_messages_container.add_widget(
                    UserMessageCard(message)
                )
            elif sender_role == "assistant":
                self.ids.chat_screen_messages_container.add_widget(
                    AssistantMessageCard(message)
                )

        if self.chat.user is None:
            self.select_user()
        elif self.chat.bot is None:
            self.select_bot()

    def scroll_to_bottom(self):
        # If the chat is longer than the screen, scroll to the bottom
        if (
            self.height < self.ids.chat_screen_message_container.height
            and self.ids.chat_screen_scroll.scroll_y != 0
        ):
            self.ids.chat_screen_scroll.scroll_y = 0

    def summarize_chat(self):
        print("Summarizing chat")  # TODO: Implement chat summarization

        self.ids.chat_screen_scroll.scroll_y = 1

    def _create_new_user(self, instance):
        self.select_user_dialog.dismiss()

        self.manager.switch_screen("user_screen")

    def _create_new_bot(self, instance):
        self.select_bot_dialog.dismiss()

        self.manager.switch_screen("bot_screen")

    def select_user(self):
        self.select_user_dialog.update_items(
            [
                {"user_id": user.id, "user_name": user.name}
                for user in User.select(User.id, User.name)
            ]
        )

        self.select_user_dialog.open()

    def select_bot(self):
        self.select_bot_dialog.update_items(
            [
                {"bot_id": bot.id, "bot_name": bot.name}
                for bot in Bot.select(Bot.id, Bot.name)
            ]
        )

        self.select_bot_dialog.open()

    def delete_chat(self):
        self.chat.delete_instance()

        self.delete_chat_dialog.dismiss()
        self.manager.switch_back()
