"""
Bot Screen
==========

This module defines the BotScreen class which represents the screen
for viewing and editing a chat. The BotScreen class also provides navigation
to replication and deletion of a viewed chat bot. 

The BotScreen class allows to specify the Bot model data.
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
                ["arrow-left", lambda x: root.switch_back(), "Back", "Back"]
                ]
            right_action_items: 
                [
                ["content-copy", lambda x: root.replicate_bot(), "Replicate", "Replicate"],
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
                    required: True
                    on_text: root.bot_name = self.text
                    hint_text: "Name"
                    helper_text_mode: "on_error"
                    helper_text: "Cannot be empty"
                    error: True if root.bot_name == "" else False

                MDTextField:
                    id: bot_transcription_language_field
                    text: root.bot_transcription_language
                    on_text: root.bot_language = self.text
                    hint_text: "Transcription language"

                MDTextField:
                    id: bot_transcription_prompt_field
                    text: root.bot_transcription_prompt
                    on_text: root.bot_transcription_prompt = self.text
                    hint_text: "Transcription instructions"

                MDTextField:
                    id: bot_transcription_temperature_field
                    text: root.bot_transcription_temperature
                    on_text: root.validate_transcription_temperature(self)
                    hint_text: "Transcription temperature"
                    helper_tex_mode: "on_error"
                    helper_text: "Must be a decimal number between 0.0 and 1.0"
                
                MDTextField:
                    id: bot_completion_prompt_field
                    text: root.bot_completion_prompt
                    on_text: root.bot_completion_prompt = self.text
                    hint_text: "Text generation instructions"
                    multiline: True

                MDTextField:
                    id: bot_completion_temperature_field
                    text: root.bot_completion_temperature
                    on_text: root.validate_completion_temperature(self)
                    hint_text: "Text generation temperature"
                    helper_tex_mode: "on_error"
                    helper_text: "Must be a decimal number between 0.0 and 2.0"

                MDTextField:
                    id: bot_summarization_prompt_field
                    text: root.bot_summarization_prompt
                    on_text: root.bot_summarization_prompt = self.text
                    hint_text: "Summarization instructions"
                    multiline: True

                MDTextField:
                    id: bot_speech_voice_field
                    text: root.bot_speech_voice
                    hint_text: "Text-to-speech voice"
                    on_focus: if self.focus: root.speech_voice_menu.open()
"""
)


class BotScreen(MDScreen):
    """Screen for viewing and editing a chat bot."""

    bot = ObjectProperty(allownone=True)
    bot_id = NumericProperty(allownone=True)

    bot_name = StringProperty()
    bot_transcription_language = StringProperty()
    bot_transcription_prompt = StringProperty()
    bot_transcription_temperature = StringProperty()
    bot_completion_prompt = StringProperty()
    bot_completion_temperature = StringProperty()
    bot_summarization_prompt = StringProperty()
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

    def validate_transcription_temperature(self, transcription_temperature_field):
        self.bot_transcription_temperature = transcription_temperature_field.text

        try:
            temperature = float(self.bot_transcription_temperature)
        except ValueError:
            transcription_temperature_field.error = True
        else:
            transcription_temperature_field.error = not (0.0 <= temperature <= 1.0)

    def validate_completion_temperature(self, completion_temperature_field):
        self.bot_completion_temperature = completion_temperature_field.text

        try:
            temperature = float(self.bot_completion_temperature)
        except ValueError:
            completion_temperature_field.error = True
        else:
            completion_temperature_field.error = not (0.0 <= temperature <= 2.0)

    def on_bot_speech_voice(self, instance, value):
        self.ids.bot_speech_voice_field.text = value

    def set_speech_voice(self, voice):
        self.bot_speech_voice = voice
        self.speech_voice_menu.dismiss()

    def on_pre_enter(self):
        self.bot = Bot.get_by_id(self.bot_id)

        self.bot_name = self.bot.name
        self.bot_transcription_language = self.bot.transcription_language
        self.bot_transcription_prompt = self.bot.transcription_prompt
        self.bot_transcription_temperature = str(self.bot.transcription_temperature)
        self.bot_completion_prompt = self.bot.completion_prompt
        self.bot_completion_temperature = str(self.bot.completion_temperature)
        self.bot_summarization_prompt = self.bot.summarization_prompt
        self.bot_speech_voice = self.bot.speech_voice

        self.taken_bot_names = self.bot.get_taken_names()

    def save_bot(self):
        self.bot_name = self.bot_name.strip()

        if self.bot_name == "":
            raise ValueError("Bot name cannot be empty")

        if self.bot_name in self.taken_bot_names:
            raise ValueError(f"Bot name '{self.bot_name}' is already taken")

        self.bot.name = self.bot_name

        self.bot.transcription_language = self.bot_transcription_language
        self.bot.transcription_prompt = self.bot_transcription_prompt

        try:
            self.bot.transcription_temperature = float(
                self.bot_transcription_temperature
            )
        except ValueError:
            raise ValueError("Transcription temperature must be a number")
        else:
            if not (0.0 < self.bot.transcription_temperature < 1.0):
                raise ValueError(
                    "Transcription temperature must be between 0.0 and 1.0"
                )

        self.bot.completion_prompt = self.bot_completion_prompt
        try:
            self.bot.completion_temperature = float(self.bot_completion_temperature)
        except ValueError:
            raise ValueError("Text generation temperature must be a number")
        else:
            if not (0.0 < self.bot.completion_temperature < 2.0):
                raise ValueError(
                    "Text generation temperature must be between 0.0 and 2.0"
                )

        self.bot.summarization_prompt = self.bot_summarization_prompt

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

    def replicate_bot(self):
        if not self.has_valid_data():
            return

        bot_replica = self.bot.replicate()

        self.manager.switch_screen("bot_replicate_screen", bot_replica.id)

    def delete_bot(self):
        self.bot.delete_instance()

        self.delete_bot_dialog.dismiss()
        self.manager.switch_back()
