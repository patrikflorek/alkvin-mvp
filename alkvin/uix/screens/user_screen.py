"""
User Screen
===========

This module defines the UserScreen class which represents the screen
for editing virtual users. The UserScreen class also allows to invoke
"cloning" and deleting the virtual user.

The UserScreen class allows to specify the name and introduction prompt 
for a virtual user.
"""

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen

from alkvin.uix.components.invalid_data_error_snackbar import InvalidDataErrorSnackbar


Builder.load_string(
    """
<UserScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            id: user_screen_top_app_bar

            title: "User"
            specific_text_color: app.theme_cls.opposite_text_color
            use_overflow: True
            left_action_items: 
                [
                ["arrow-left", lambda x: root.switch_back(), "Back", "Back"]
                ]
            right_action_items:
                [
                ["content-copy", lambda x: root.clone_user(), "Clone", "Clone"],
                ["delete", lambda x: root.delete_user_dialog.open(), "Delete", "Delete"]
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


class UserScreen(MDScreen):
    """Screen for creating, editing, replicating, and deleting virtual users."""

    user = ObjectProperty(allownone=True)

    user_name = StringProperty()
    user_introduction = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.invalid_data_error_snackbar = InvalidDataErrorSnackbar()

        self.delete_user_dialog = MDDialog(
            title="Delete user",
            text="Are you sure you want to delete this user?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.delete_user_dialog.dismiss(),
                ),
                MDFlatButton(
                    text="DELETE",
                    theme_text_color="Error",
                    on_release=lambda x: self.delete_user(),
                ),
            ],
        )

    def on_pre_enter(self):
        self.user_name = self.user.name
        self.user_introduction = self.user.introduction

        self.taken_user_names = self.user.get_taken_names()

    def save_user(self):
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

    def clone_user(self):
        if not self.has_valid_data():
            return

        self.manager.switch_screen("user_clone_screen", self.user.clone())

    def delete_user(self):
        self.user.delete_instance()

        self.delete_user_dialog.dismiss()
        self.manager.switch_back()
