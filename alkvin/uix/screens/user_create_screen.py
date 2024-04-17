"""
New User Screen
===============

This module defines the NewUserScreen class which represents the screen
for modification of a new virtual user.

The NewUserScreen class object is a crippled version of the UserScreen class 
object lacking the ability to clone the new virtual user. 
"""

from alkvin.uix.screens.user_screen import UserScreen


class UserCreateScreen(UserScreen):
    """Screen for creating a clone of a virtual user."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.user_screen_top_app_bar.title = "New user"

        # Remove clone functionality
        del self.ids.user_screen_top_app_bar.right_action_items[0]

    def clone_user(self):
        pass  # Remove clone functionality
