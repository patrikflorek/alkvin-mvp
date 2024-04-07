"""
Bot Replica Screen
==================

This module defines the BotReplicaScreen class which represents the screen
for creating a replica of a chat bot.

The BotReplicaScreen class object is a crippled version of the BotScreen class
object lacking the ability to replicate a chat bot.
"""

from kivy.properties import NumericProperty


from alkvin.uix.screens.bot_screen import BotScreen


class BotReplicaScreen(BotScreen):
    """Screen for creating a replica of a chat bot."""

    prototype_bot_id = NumericProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.bot_screen_top_app_bar.title = "Bot replica"

        # Remove replicate functionality
        del self.ids.bot_screen_top_app_bar.right_action_items[0]

    def on_enter(self):
        # Replicate bot
        self.bot_name = "Bot 1 Replica"
        self.bot_stt_language = "en"
        self.bot_text_generation_instructions = "You are a helpful assistant that provides detailed explanations and examples about Python programming."
        self.bot_tts_prompt = "The following is the response from a chat bot which contains a lot of Python code."
        self.bot_tts_voice = "nova"

    # Remove replicate functionality
    def replicate_bot(self):
        pass
