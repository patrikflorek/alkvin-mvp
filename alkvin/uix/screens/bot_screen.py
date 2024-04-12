"""
Bot Screen
==========

This module defines the BotScreen class which represents the screen
for creating and editing chat bots. The BotScreen class also allows 
replication and deletion a viewed chat bot.

The BotScreen class allows to specify the name, speech-to-text language,
text generation instructions, and text-to-speech settings for a chat bot.
"""

from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


Builder.load_string(
    """
<BotScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            id: bot_screen_top_app_bar
            title: "Bot"
            specific_text_color: app.theme_cls.opposite_text_color
            use_overflow: True
            left_action_items: 
                [
                ["arrow-left", lambda x: app.root.switch_back(), "Back", "Back"]
                ]
            right_action_items: 
                [
                ["content-copy", lambda x: root.replicate_bot(), "Replicate", "Replicate"],
                ["delete", lambda x: root.delete_bot_dialog.open(), "Delete", "Delete"]
                ]
        
        ScrollView:
            id: bot_screen_scroll
        
            MDGridLayout:
                cols: 1
                padding: "40dp"
                spacing: "40dp"
                adaptive_height: True
                
                MDTextField:
                    id: bot_name_field
                    text: root.bot_name
                    on_text: root.bot_name = self.text
                    hint_text: "Name"

                MDTextField:
                    id: bot_stt_language_field
                    text: root.bot_stt_language
                    on_text: root.bot_stt_language = self.text
                    hint_text: "Speech-to-text language"

                MDTextField:
                    id: bot_instructions_field
                    text: root.bot_text_generation_instructions
                    on_text: root.bot_text_generation_instructions = self.text
                    hint_text: "Text generation instructions"
                    multiline: True

                MDTextField:
                    id: bot_summarization_instructions_field
                    text: root.bot_summarization_instructions
                    on_text: root.bot_summarization_instructions = self.text
                    hint_text: "Summarization instructions"
                    multiline: True

                MDTextField:
                    id: bot_tts_prompt_field
                    text: root.bot_tts_prompt
                    on_text: root.bot_tts_prompt = self.text
                    hint_text: "Text-to-speech prompt"
                    multiline: True

                MDTextField:
                    id: bot_tts_voice_field
                    text: root.bot_tts_voice
                    hint_text: "Text-to-speech voice"
                    on_focus: if self.focus: root.tts_voice_menu.open()
"""
)


class BotScreen(MDScreen):
    """Screen for creating, editing, replicating, and deleting chat bots."""

    bot_id = NumericProperty(allownone=True)

    bot_name = StringProperty()
    bot_stt_language = StringProperty()
    bot_text_generation_instructions = StringProperty()
    bot_summarization_instructions = StringProperty()
    bot_tts_prompt = StringProperty()
    bot_tts_voice = StringProperty()

    delete_bot_dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        tts_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

        self.tts_voice_menu = MDDropdownMenu(
            caller=self.ids.bot_tts_voice_field,
            position="center",
            items=[
                {
                    "viewclass": "OneLineListItem",
                    "text": voice.capitalize(),
                    "on_release": lambda x=voice: self.set_tts_voice(x),
                }
                for voice in tts_voices
            ],
        )

        self.delete_bot_dialog = MDDialog(
            title="Delete bot",
            text="Are you sure you want to delete this bot?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.delete_bot_dialog.dismiss(),
                ),
                MDFlatButton(
                    text="DELETE",
                    theme_text_color="Error",
                    on_release=lambda x: self.delete_bot(),
                ),
            ],
        )

    def set_tts_voice(self, voice):
        self.ids.bot_tts_voice_field.text = voice
        self.tts_voice_menu.dismiss()

    def on_enter(self):
        self.ids.bot_screen_top_app_bar.title = (
            "Bot" if self.bot_id is not None else "New bot"
        )

        if self.bot_id is None:
            # Create new bot
            self.bot_name = "New bot"
            self.bot_stt_language = "en"
            self.bot_text_generation_instructions = "You are a useful assistant."
            self.bot_summarization_instructions = "Summarize the chat so far."
            self.bot_tts_prompt = "Following is response from a chat bot."
            self.bot_tts_voice = "alloy"
        else:
            # Load bot
            self.chat_name = "Bot 1"
            self.bot_stt_language = "en"
            self.bot_text_generation_instructions = "You are a helpful assistant that provides detailed explanations and examples about Python programming."
            self.bot_summarization_instructions = "Summarize the chat so far and provide a brief explanation of the Python code."
            self.bot_tts_prompt = "The following is the response from a chat bot which contains a lot of Python code."
            self.bot_tts_voice = "nova"

    def replicate_bot(self):
        print("Replicating bot")  # TODO: Implement bot replication

        self.manager.switch_screen(
            "bot_replica_screen", {"prototype_bot_id": self.bot_id}
        )

    def delete_bot(self):
        print("Deleting bot")  # TODO: Implement bot deletion

        self.delete_bot_dialog.dismiss()
        self.manager.switch_back()
