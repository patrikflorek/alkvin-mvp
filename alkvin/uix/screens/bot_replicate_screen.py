"""
Bot Replicate Screen
====================

This module defines the BotReplicateScreen class which represents the screen
for modification of a replica of a chat bot.

The BotReplicaScreen class code originates from code of the BotScreen class
lacking the ability to replicate the newly created bot replica.
"""

from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, StringProperty

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from alkvin.uix.components.invalid_data_error_snackbar import InvalidDataErrorSnackbar
from alkvin.uix.components.delete_bot_dialog import DeleteBotDialog

from alkvin.entities.bot import Bot


Builder.load_string(
    """
<BotReplicateScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            id: bot_screen_top_app_bar
            title: "Bot replica"
            specific_text_color: app.theme_cls.opposite_text_color
            use_overflow: True
            left_action_items: 
                [
                ["arrow-left", lambda x: root.switch_back(), "Back", "Back"]
                ]
            right_action_items: 
                [
                ["delete", lambda x: root.delete_bot_dialog.open(root.bot_name, root.delete_bot), "Delete", "Delete"]
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
                    id: bot_language_field
                    text: root.bot_language
                    on_text: root.bot_language = self.text
                    hint_text: "Language"

                MDTextField:
                    id: bot_generation_prompt_field
                    text: root.bot_generation_prompt
                    on_text: root.bot_generation_prompt = self.text
                    hint_text: "Text generation instructions"
                    multiline: True

                MDTextField:
                    id: bot_summarization_prompt_field
                    text: root.bot_summarization_prompt
                    on_text: root.bot_summarization_prompt = self.text
                    hint_text: "Summarization instructions"
                    multiline: True

                MDTextField:
                    id: bot_speech_prompt_field
                    text: root.bot_speech_prompt
                    on_text: root.bot_speech_prompt = self.text
                    hint_text: "Text-to-speech instructions"
                    multiline: True

                MDTextField:
                    id: bot_speech_voice_field
                    text: root.bot_speech_voice
                    hint_text: "Text-to-speech voice"
                    on_focus: if self.focus: root.speech_voice_menu.open()
"""
)


class BotReplicateScreen(MDScreen):
    """Screen for replicating a chat bot."""

    bot = ObjectProperty(allownone=True)
    bot_id = NumericProperty(allownone=True)

    bot_name = StringProperty()
    bot_language = StringProperty()
    bot_generation_prompt = StringProperty()
    bot_summarization_prompt = StringProperty()
    bot_speech_prompt = StringProperty()
    bot_speech_voice = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.invalid_data_error_snackbar = InvalidDataErrorSnackbar()

        speech_voices = Bot.get_speech_voices()
        self.speech_voice_menu = MDDropdownMenu(
            caller=self.ids.bot_speech_voice_field,
            position="center",
            items=[
                {
                    "viewclass": "OneLineListItem",
                    "text": voice.capitalize(),
                    "on_release": lambda x=voice: self.set_speech_voice(x),
                }
                for voice in speech_voices
            ],
        )

        self.delete_bot_dialog = DeleteBotDialog()

    def on_bot_speech_voice(self, instance, value):
        self.ids.bot_speech_voice_field.text = value

    def set_speech_voice(self, voice):
        self.bot_speech_voice = voice
        self.speech_voice_menu.dismiss()

    def on_pre_enter(self):
        self.bot = Bot.get_by_id(self.bot_id)

        self.bot_name = self.bot.name
        self.bot_language = self.bot.language
        self.bot_generation_prompt = self.bot.generation_prompt
        self.bot_summarization_prompt = self.bot.summarization_prompt
        self.bot_speech_prompt = self.bot.speech_prompt
        self.bot_speech_voice = self.bot.speech_voice

        self.taken_bot_names = self.bot.get_taken_names()

    def save_bot(self):
        self.bot_name = self.bot_name.strip()

        if self.bot_name == "":
            raise ValueError("Bot name cannot be empty")

        if self.bot_name in self.taken_bot_names:
            raise ValueError(f"Bot name '{self.bot_name}' is already taken")

        self.bot.name = self.bot_name
        self.bot.language = self.bot_language
        self.bot.generation_prompt = self.bot_generation_prompt
        self.bot.summarization_prompt = self.bot_summarization_prompt
        self.bot.speech_prompt = self.bot_speech_prompt
        self.bot.speech_voice = self.bot_speech_voice

        self.bot.save()

    def has_valid_data(self):
        try:
            self.save_bot()
        except ValueError as e:
            self.invalid_data_error_snackbar.text = str(e)
            self.invalid_data_error_snackbar.open()

            return False

        return True

    def switch_back(self):
        if not self.has_valid_data():
            return

        self.manager.switch_back()

    def delete_bot(self):
        self.bot.delete_instance()

        self.delete_bot_dialog.dismiss()
        self.manager.switch_back()
