"""
Bot Replica Screen
==================

This module defines the BotReplicaScreen class which represents the screen
for creating a replica of a chat bot.

The BotReplicaScreen class object is a crippled version of the BotScreen class
object lacking the ability to replicate a chat bot.
"""

from kivy.properties import NumericProperty, ObjectProperty

from alkvin.uix.screens.bot_screen import BotScreen

from alkvin.entities.bot import Bot


class BotReplicaScreen(BotScreen):
    """Screen for creating a replica of a chat bot."""

    prototype_bot = ObjectProperty(allownone=True)
    prototype_bot_id = NumericProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.bot_screen_top_app_bar.title = "Bot replica"

        # Remove replicate functionality
        del self.ids.bot_screen_top_app_bar.right_action_items[0]

    def _replicate_prototype_bot(self):
        bot_replica_name = Bot.get_replica_name(self.prototype_bot.name)
        self.bot = Bot.create(
            name=bot_replica_name,
            language=self.prototype_bot.language,
            generation_prompt=self.prototype_bot.generation_prompt,
            summarization_prompt=self.prototype_bot.summarization_prompt,
            speech_prompt=self.prototype_bot.speech_prompt,
            speech_voice=self.prototype_bot.speech_voice,
        )

        self.bot_id = self.bot.id
        self.bot_name = self.bot.name
        self.bot_stt_language = self.bot.language
        self.bot_text_generation_instructions = self.bot.generation_prompt
        self.bot_tts_prompt = self.bot.speech_prompt
        self.bot_tts_voice = self.bot.speech_voice

    def on_pre_enter(self):
        self.prototype_bot = Bot.get(self.prototype_bot_id)

        self._replicate_prototype_bot()

        self.taken_bot_names = Bot.get_taken_names(exceptions=[self.bot_name])

    def replicate_bot(self):
        pass  # Remove replicate functionality
