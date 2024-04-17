"""
New Bot Screen
===============

This module defines the NewBotScreen class which represents the screen
for modification of a new bot.

The NewBotScreen class object is a crippled version of the BotScreen class 
object lacking the ability to replicate the new bot. 
"""

from alkvin.uix.screens.bot_screen import BotScreen


class BotCreateScreen(BotScreen):
    """Screen for creating a replica of a bot."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.bot_screen_top_app_bar.title = "New bot"

        # Remove bot replicate functionality
        del self.ids.bot_screen_top_app_bar.right_action_items[0]

    def replicate_bot(self):
        pass  # Remove bot replicate functionality
