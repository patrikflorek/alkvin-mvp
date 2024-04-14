"""
User Clone Screen
=================

This module defines the UserCloneScreen class which represents the screen
for creating a "clone" of a virtual user.

The UserCloneScreen class object is a crippled version of the UserScreen class 
object lacking the ability to clone a virtual user.
"""

from kivy.properties import NumericProperty, ObjectProperty

from alkvin.uix.screens.user_screen import UserScreen

from alkvin.entities.user import User


class UserCloneScreen(UserScreen):
    """Screen for creating a clone of a virtual user."""

    original_user = ObjectProperty(allownone=True)
    original_user_id = NumericProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.user_screen_top_app_bar.title = "User clone"

        # Remove clone functionality
        del self.ids.user_screen_top_app_bar.right_action_items[0]

    def _clone_original_user(self):
        user_clone_name = User.get_clone_name(self.original_user.name)
        self.user = User.create(
            name=user_clone_name,
            introduction=self.original_user.introduction,
        )

        self.user_id = self.user.id
        self.user_name = self.user.name
        self.user_introduction = self.user.introduction

    def on_pre_enter(self):
        self.original_user = User.get(self.original_user_id)

        self._clone_original_user()

        self.taken_user_names = User.get_taken_names(exceptions=[self.user_name])

    def clone_user(self):
        pass  # Remove clone functionality
