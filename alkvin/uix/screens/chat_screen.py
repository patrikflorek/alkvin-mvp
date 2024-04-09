"""
Chat Screen
===========

This module defines the ChatScreen class which represents the screen where 
a user can interact with a chat bot.

The ChatScreen class displays the chat messages between the user and 
the chat bot, as well as options to summarize the chat, select a user, select a bot, and delete the chat.
"""

from kivy.lang import Builder
from kivy.properties import DictProperty, NumericProperty, StringProperty

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

from alkvin.uix.components.select_user_dialog import SelectUserDialog
from alkvin.uix.components.user_message_card import UserMessageCard
from alkvin.uix.components.select_bot_dialog import SelectBotDialog
from alkvin.uix.components.assistant_message_card import AssistantMessageCard


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
        pos_hint: {"y": 0}
"""
)


class ChatScreen(MDScreen):
    """Screen for interacting with a chat bot using voice messages."""

    chat_id = NumericProperty(allownone=True)

    chat_title = StringProperty("A new chat")
    chat_summary = StringProperty("This is a summary of the chat so far.")
    chat_user = DictProperty(None)
    chat_bot = DictProperty(None)

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

    def _on_select_user_callback(self, user_id):
        # TODO: Retrieve user data

        self.chat_user = {
            "user_id": user_id,
            "user_name": "John Doe",
            "user_introduction": "Hello, I am John Doe.",
        }

    def _on_select_bot_callback(self, bot_id):
        # TODO: Retrieve bot data

        self.chat_bot = {
            "bot_id": bot_id,
            "bot_name": "Bot 1",
            "bot_introduction": "Hello, I am Bot 1.",
        }

    def on_enter(self):
        if self.chat_id is None:
            # Create new chat
            self.chat_title = "A new chat"
            self.chat_summary = ""
            self.chat_messages = []
        else:
            # Load chat
            self.chat_title = "Chat 1"
            self.chat_summary = "This is a summary of Chat 1."

            self.chat_messages = [
                {
                    "role": "user",
                    "user_audio_file": "adstfswrrf.wav",
                    "user_audio_created_at": "2020-07-01T12:01:00",
                    "user_message_sent_at": "2020-07-01T12:01:02",
                    "user_audio_transcript": "Hello, I'm a human. I'm here to help you with any questions you may have about the product. How can I help you today?",
                    "user_transcript_received_at": "2020-07-01T12:02:00",
                },
                {
                    "role": "assistant",
                    "completion_text": "Hello, I'm a bot. I'm here to help you with any questions you may have about the product. How can I help you today?",
                    "completion_received_at": "2020-07-01T12:05:00",
                    "speech_audio_file": "weqdstrwer.wav",
                    "speech_audio_received_at": "2020-07-01T12:08:00",
                },
                {
                    "role": "user",
                    "user_audio_file": "kdqwservfy.wav",
                    "user_audio_created_at": "2020-07-01T12:08:30",
                    "user_message_sent_at": "2020-07-01T12:08:32",
                    "user_audio_transcript": "I have a question about the product. Can you tell me more about the features?",
                    "user_transcript_received_at": "2020-07-01T12:09:00",
                },
                {
                    "role": "assistant",
                    "completion_text": "Sure! The product has a lot of features. It has a built-in camera, a microphone, and a speaker. It also has a touch screen display and a battery that can last for up to 12 hours. It's a great product for people who are always on the go.",
                    "completion_received_at": "2020-07-01T12:10:00",
                    "speech_audio_file": "",
                    "speech_audio_received_at": "",
                },
                {
                    "role": "user",
                    "user_audio_file": "deasdfdpacvx.wav",
                    "user_audio_created_at": "2020-07-01T12:12:30",
                    "user_message_sent_at": "",
                    "user_audio_transcript": "Thank you for the information. I'm interested in purchasing the product. Can you tell me how I can place an order?",
                    "user_audio_transcript_received_at": "2020-07-01T12:12:32",
                },
                {
                    "role": "user",
                    "user_audio_file": "rgsonnksqeib.wav",
                    "user_audio_created_at": "2020-07-01T12:12:34",
                    "user_message_sent_at": "",
                    "user_audio_transcript": "",
                    "user_audio_transcript_received_at": "",
                },
            ]

        self.ids.chat_screen_messages_container.clear_widgets()
        for message in self.chat_messages:
            if message["role"] == "user":
                self.ids.chat_screen_messages_container.add_widget(
                    UserMessageCard(
                        user_audio_file=message.get("user_audio_file", ""),
                        user_audio_created_at=message.get("user_audio_created_at", ""),
                        user_audio_transcript=message.get("transcript_text", ""),
                        user_audio_transcript_received_at=message.get(
                            "transcript_received_at", ""
                        ),
                        user_message_sent_at=message.get("message_sent_at", ""),
                    )
                )
            elif message["role"] == "assistant":
                self.ids.chat_screen_messages_container.add_widget(
                    AssistantMessageCard(
                        completion_text=message.get("completion_text", ""),
                        completion_received_at=message.get(
                            "completion_received_at", ""
                        ),
                        speech_audio_file=message.get("speech_audio_file", ""),
                        speech_audio_received_at=message.get(
                            "speech_audio_received_at", ""
                        ),
                    )
                )

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
                {
                    "user_id": 1,
                    "user_name": "John Doe",
                },
                {
                    "user_id": 2,
                    "user_name": "Jane Doe",
                },
                {
                    "user_id": 3,
                    "user_name": "Alice Doe",
                },
            ]
        )

        self.select_user_dialog.open()

    def select_bot(self):
        self.select_bot_dialog.update_items(
            [
                {
                    "bot_id": 1,
                    "bot_name": "Bot 1",
                },
                {
                    "bot_id": 2,
                    "bot_name": "Bot 2",
                },
                {
                    "bot_id": 3,
                    "bot_name": "Bot 3",
                },
            ]
        )

        self.select_bot_dialog.open()

    def delete_chat(self):
        print("Deleting chat")  # TODO: Implement chat deletion

        self.delete_chat_dialog.dismiss()
        self.manager.switch_back()
