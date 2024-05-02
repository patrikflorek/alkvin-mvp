"""
Chat Screen
===========

This module defines the ChatScreen class which represents the screen where 
a user can interact with a chat bot.

The ChatScreen class displays the chat messages between the user and 
the chat bot, as well as options to summarize the chat, select a user, select a bot, and delete the chat.
"""

import os
import shutil
from datetime import datetime

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import (
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

from alkvin.uix.recycling import get_recycling_bin

from alkvin.entities.bot import Bot
from alkvin.entities.chat import Chat
from alkvin.entities.user import User
from alkvin.entities.user_message import UserMessage
from alkvin.entities.assistant_message import AssistantMessage


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
                ["arrow-left", lambda x: root.switch_back(), "Back", "Back"]
                ]
            right_action_items: 
                [
                ["file-document", lambda x: root.summarize_chat(), "Summarize", "Summarize"],
                ["account", lambda x: root.select_user_dialog.open(root.chat.user_id), "User", "User"],
                ["robot", lambda x: root.select_bot_dialog.open(root.chat.bot_id), "Bot", "Bot"],
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

                    MDTextField:
                        hint_text: "Title"
                        helper_text_mode: "on_focus"
                        required: True
                        text: root.chat_title
                        on_text: root.chat_title = self.text

                    MDTextField:
                        hint_text: "Summary"
                        helper_text_mode: "on_focus"
                        multiline: True
                        required: True
                        text: root.chat_summary
                        on_text: root.chat_summary = self.text

                    MDIconButton:
                        icon: "chevron-down"
                        theme_text_color: "Custom"
                        text_color: [0.4, 0.4, 0.4, 0.8]
                        pos_hint: {"center_x": .5}
                        
                        on_release: root.scroll_to_bottom()
                
                MDBoxLayout:
                    id: chat_screen_sent_messages_container
                    
                    orientation: "vertical"
                    spacing: "28dp"
                    adaptive_height: True

                MDBoxLayout:
                    id: chat_screen_unsent_messages_container

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

    chat_title = StringProperty()
    chat_summary = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recycling_bin = get_recycling_bin()

        self.select_user_dialog = SelectUserDialog(self.on_user_selected)

        self.select_bot_dialog = SelectBotDialog(self.on_bot_selected)

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
            self.create_user_message
        )

    def create_user_message(self, audio_recording_path):
        new_audio_file_name = f"user_{datetime.now().isoformat()}.wav"
        new_audio_file_path = os.path.join(self.chat.audio_dir, new_audio_file_name)
        shutil.move(audio_recording_path, new_audio_file_path)

        message = UserMessage.create(chat=self.chat, audio_file=new_audio_file_name)

        message_widget = self.recycling_bin.get_message_widget(message)
        message_widget.bind(is_message_sent=self.on_user_message_sent)

        self.ids.chat_screen_unsent_messages_container.add_widget(message_widget)

    def on_user_selected(self, user_id):
        self.chat.user = User.get_by_id(user_id)
        self.chat.save()

        if self.chat.bot is None:
            self.select_bot_dialog.open(self.chat.bot_id)
        elif self.ids.chat_screen_sent_messages_container.children:
            last_sent_message = self.ids.chat_screen_sent_messages_container.children[0]
            if isinstance(last_sent_message, UserMessageCard):
                self.chat.bot.chat_complete(self.chat, self.on_chat_completed)

    def on_bot_selected(self, bot_id):
        self.chat.bot = Bot.get(Bot.id == bot_id)
        self.chat.save()

        if self.ids.chat_screen_sent_messages_container.children:
            last_sent_message = self.ids.chat_screen_sent_messages_container.children[0]
            if isinstance(last_sent_message, UserMessageCard):
                self.chat.bot.chat_complete(self.chat, self.on_chat_completed)

    def on_chat_completed(self, completion):
        message = AssistantMessage.create(chat=self.chat, completion=completion)
        message_widget = self.recycling_bin.get_message_widget(message)
        self.ids.chat_screen_sent_messages_container.add_widget(message_widget)

    def on_user_message_sent(self, message_widget, is_message_sent):
        if not is_message_sent:
            return

        self.ids.chat_screen_unsent_messages_container.remove_widget(message_widget)
        self.ids.chat_screen_sent_messages_container.add_widget(message_widget)

        self.chat.bot.chat_complete(self.chat, self.on_chat_completed)

    def load_chat_messages(self):
        message_widgets = (
            self.ids.chat_screen_sent_messages_container.children
            + self.ids.chat_screen_unsent_messages_container.children
        )
        self.recycling_bin.recycle_message_widgets(message_widgets)

        self.ids.chat_screen_sent_messages_container.clear_widgets()
        self.ids.chat_screen_unsent_messages_container.clear_widgets()

        for message in self.chat.messages:
            if isinstance(message, UserMessage):
                message_widget = self.recycling_bin.get_message_widget(message)
                message_widget.bind(is_message_sent=self.on_user_message_sent)

                if message.sent_at is None:
                    self.ids.chat_screen_unsent_messages_container.add_widget(
                        message_widget
                    )
                    continue
            elif isinstance(message, AssistantMessage):
                message_widget = self.recycling_bin.get_message_widget(message)

            self.ids.chat_screen_sent_messages_container.add_widget(message_widget)

        self.ids.chat_screen_scroll.scroll_y = 1

    def on_pre_enter(self):
        self.chat = Chat.get_by_id(self.chat_id)

        self.chat_title = self.chat.title
        self.chat_summary = self.chat.summary

        self.load_chat_messages()

        if self.chat.user is None:
            self.select_user_dialog.open(self.chat.user_id)
            # if both and user and bot are not selected, the select bot dialog will be opened after the the user is selected
        elif self.chat.bot is None:
            self.select_bot_dialog.open(self.chat.bot_id)
        elif self.ids.chat_screen_sent_messages_container.children:
            # If both user and bot are selected and if the last message in the sent messages is a user message, then request a response from the bot
            last_sent_message = self.ids.chat_screen_sent_messages_container.children[0]
            if isinstance(last_sent_message, UserMessageCard):
                self.chat.bot.chat_complete(self.chat, self.on_chat_completed)

    def save_chat(self):
        self.chat_title = self.chat_title.strip()

        if self.chat_title == "":
            raise ValueError("Chat title cannot be empty")

        self.chat.title = self.chat_title
        self.chat.summary = self.chat_summary

        self.chat.save()

    def has_valid_data(self):
        try:
            self.save_chat()
        except ValueError as e:
            self.invalid_data_error_snackbar.text = str(e)
            self.invalid_data_error_snackbar.open()

            return False

        return True

    def switch_back(self):
        if not self.has_valid_data():
            return

        self.manager.switch_back()

    def scroll_to_bottom(self):
        if self.height >= self.ids.chat_screen_message_container.height:
            return

        anim = Animation(
            scroll_y=self.ids.chat_screen_message_container.y
            / self.ids.chat_screen_message_container.height,
            d=0.5,
            t="out_quad",
        )
        anim.start(self.ids.chat_screen_scroll)

    def summarize_chat(self):
        print("Summarizing chat")  # TODO: Implement chat summarization

        self.ids.chat_screen_scroll.scroll_y = 1

    def delete_chat(self):
        self.chat.delete_instance()

        self.delete_chat_dialog.dismiss()
        self.manager.switch_back()
