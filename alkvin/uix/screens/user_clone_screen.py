"""
User Clone Screen
=================

This module defines the UserCloneScreen class which represents the screen
for modification a "clone" of a virtual user.

The UserCloneScreen class code originates from code of UserScreen class 
lacking the ability to clone the newly created virtual user clone.
"""

from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, StringProperty

from kivymd.uix.screen import MDScreen

from alkvin.uix.components.invalid_data_error_snackbar import InvalidDataErrorSnackbar
from alkvin.uix.components.delete_user_dialog import DeleteUserDialog

from alkvin.entities.user import User


Builder.load_string(
    """
<UserCloneScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            id: user_screen_top_app_bar

            title: "User clone"
            specific_text_color: app.theme_cls.opposite_text_color
            use_overflow: True
            left_action_items: 
                [
                ["arrow-left", lambda x: root.switch_back(), "Back", "Back"]
                ]
            right_action_items:
                [
                ["delete", lambda x: root.delete_user_dialog.open(root.user_name, root.delete_user), "Delete", "Delete"]
                ]

        ScrollView:
            id: user_screen_scroll
        
            MDGridLayout:
                cols: 1
                padding: "40dp"
                spacing: "40dp"
                adaptive_height: True
                
                MDTextField:
                    id: user_name_field
                    text: root.user_name
                    on_text: root.user_name = self.text
                    hint_text: "Name"

                MDTextField:
                    id: user_introduction_field
                    text: root.user_introduction
                    on_text: root.user_introduction = self.text
                    hint_text: "Introduction"
                    multiline: True
"""
)


class UserCloneScreen(MDScreen):
    """Screen for "cloning" a virtual user."""

    user = ObjectProperty(allownone=True)
    user_id = NumericProperty(allownone=True)

    user_name = StringProperty()
    user_introduction = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.invalid_data_error_snackbar = InvalidDataErrorSnackbar()

        self.delete_user_dialog = DeleteUserDialog()

    def on_pre_enter(self):
        self.user = User.get_by_id(self.user_id)

        self.user_name = self.user.name
        self.user_introduction = self.user.introduction

        self.taken_user_names = self.user.get_taken_names()

    def save_user(self):
        self.user_name = self.user_name.strip()

        if self.user_name == "":
            raise ValueError("User name cannot be empty")

        if self.user_name in self.taken_user_names:
            raise ValueError(f"User name '{self.user_name}' is already taken")

        self.user.name = self.user_name
        self.user.introduction = self.user_introduction

        self.user.save()

    def has_valid_data(self):
        try:
            self.save_user()
        except ValueError as e:
            self.invalid_data_error_snackbar.text = str(e)
            self.invalid_data_error_snackbar.open()

            return False

        return True

    def switch_back(self):
        if not self.has_valid_data():
            return

        self.manager.switch_back()

    def delete_user(self):
        self.user.delete_instance()

        self.delete_user_dialog.dismiss()
        self.manager.switch_back()
