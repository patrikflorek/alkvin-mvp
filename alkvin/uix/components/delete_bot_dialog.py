"""
Delete Bot Dialog
=================

This module contains the DeleteBotDialog class, which is a custom dialog widget
used to prompt the user to confirm the deletion of a chat bot.

Example usage:
    dialog = DeleteBotDialog()
    dialog.open(bot_name="My Bot", on_delete_bot_callback=lambda: print("Bot deleted!"))
"""

from kivy.properties import StringProperty

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class DeleteBotDialog(MDDialog):
    bot_name = StringProperty()

    def __init__(self, **kwargs):
        self.title = "Delete bot"
        self.text = "Are you sure you want to delete this bot?"
        self.buttons = [
            MDFlatButton(
                text="CANCEL",
                on_release=lambda x: self.dismiss(),
            ),
            MDFlatButton(
                text="DELETE",
                theme_text_color="Error",
                on_release=lambda x: self.on_delete_bot_callback(),
            ),
        ]
        super().__init__(**kwargs)

    def on_delete_bot_callback(self):
        # This method is called when the user confirms the deletion of the bot.
        pass

    def open(self, bot_name, on_delete_bot_callback):
        self.text = f"Are you sure you want to delete bot \n[b]{bot_name}[/b]?"
        self.on_delete_bot_callback = on_delete_bot_callback

        super().open()
