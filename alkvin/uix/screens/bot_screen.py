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
from kivy.properties import NumericProperty, ObjectProperty, StringProperty

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from alkvin.uix.components.invalid_data_error_snackbar import InvalidDataErrorSnackbar

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


class BotScreen(MDScreen):
    """Screen for creating, editing, replicating, and deleting chat bots."""

    bot = ObjectProperty(allownone=True)
    bot_id = NumericProperty(allownone=True)

    bot_name = StringProperty()
    bot_language = StringProperty()
    bot_generation_prompt = StringProperty()
    bot_summarization_prompt = StringProperty()
    bot_speech_prompt = StringProperty()
    bot_speech_voice = StringProperty()

    delete_bot_dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    def set_speech_voice(self, voice):
        self.ids.bot_speech_voice_field.text = voice
        self.speech_voice_menu.dismiss()

    def _create_bot(
        self,
        new_bot_name,
        new_bot_language="",
        new_bot_generation_prompt="",
        new_bot_summarization_prompt="",
        new_bot_speech_prompt="",
        new_bot_speech_voice="alloy",
    ):
        self.bot = Bot.create(
            name=new_bot_name,
            language=new_bot_language,
            generation_prompt=new_bot_generation_prompt,
            summarization_prompt=new_bot_summarization_prompt,
            speech_prompt=new_bot_speech_prompt,
            speech_voice=new_bot_speech_voice,
        )

        self.bot_id = self.bot.id
        self.bot_name = self.bot.name
        self.bot_language = self.bot.language
        self.bot_generation_prompt = self.bot.generation_prompt
        self.bot_summarization_prompt = self.bot.summarization_prompt
        self.bot_speech_prompt = self.bot.speech_prompt
        self.bot_speech_voice = self.bot.speech_voice

    def _load_bot(self):
        self.bot = Bot.get(Bot.id == self.bot_id)

        print("_load_bot", self.bot.language, type(self.bot.language))

        self.bot_name = self.bot.name
        self.bot_language = self.bot.language
        self.bot_generation_prompt = self.bot.generation_prompt
        self.bot_summarization_prompt = self.bot.summarization_prompt
        self.bot_speech_prompt = self.bot.speech_prompt
        self.bot_speech_voice = self.bot.speech_voice

    def _save_bot(self):
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

    def on_pre_enter(self):
        self.ids.bot_screen_top_app_bar.title = (
            "Bot" if self.bot_id is not None else "New bot"
        )

        if self.bot_id is None:
            self._create_bot(
                new_bot_name=Bot.get_new_name(),
                new_bot_language="en",
                new_bot_generation_prompt="You are a useful assistant.",
                new_bot_summarization_prompt="Summarize the chat so far.",
                new_bot_speech_prompt="Following is response from a chat bot.",
                new_bot_speech_voice="alloy",
            )
        else:
            self._load_bot()

        self.taken_bot_names = Bot.get_taken_names(exceptions=[self.bot_name])

    def _can_safely_leave(self):
        try:
            self._save_bot()
        except ValueError as e:
            self.invalid_data_error_snackbar.text = str(e)
            self.invalid_data_error_snackbar.open()

            return False

        return True

    def switch_back(self):
        if not self._can_safely_leave():
            return

        self.bot = None
        self.manager.switch_back()

    def replicate_bot(self):
        if not self._can_safely_leave():
            return

        self.manager.switch_screen(
            "bot_replica_screen", {"prototype_bot_id": self.bot_id}
        )

    def delete_bot(self):
        self.bot.delete_instance()

        self.delete_bot_dialog.dismiss()
        self.manager.switch_back()
