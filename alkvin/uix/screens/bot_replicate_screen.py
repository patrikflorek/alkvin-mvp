"""
Bot Replica Screen
==================

This module defines the BotReplicaScreen class which represents the screen
for creating a replica of a chat bot.

The BotReplicaScreen class object is a crippled version of the BotScreen class
object lacking the ability to replicate a chat bot.
"""

from alkvin.uix.screens.bot_screen import BotScreen


class BotReplicateScreen(BotScreen):
    """Screen for creating a replica of a chat bot."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.bot_screen_top_app_bar.title = "Bot replica"

        # Remove replicate functionality
        del self.ids.bot_screen_top_app_bar.right_action_items[0]

    def replicate_bot(self):
        pass  # Remove replicate functionality
