"""
User Clone Screen
=================

This module defines the UserCloneScreen class which represents the screen
for creating a "clone" of a virtual user.

The UserCloneScreen class object is a crippled version of the UserScreen class 
object lacking the ability to clone a virtual user.
"""

from kivy.properties import NumericProperty

from alkvin.uix.screens.user_screen import UserScreen


class UserCloneScreen(UserScreen):
    """Screen for creating a clone of a virtual user."""

    original_user_id = NumericProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.user_screen_top_app_bar.title = "User clone"

        # Remove clone functionality
        del self.ids.user_screen_top_app_bar.right_action_items[0]

    def on_enter(self):
        # Clone user

        self.user_name = "Clone of John Doe"
        self.user_introduction = "Hello, I am a clone of John Doe."

    def clone_user(self):
        pass  # Remove clone functionality
