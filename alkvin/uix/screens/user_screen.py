"""
User Screen
===========

This module defines the UserScreen class which represents the screen
for creating and editing virtual users. The UserScreen class also allows
"cloning" and deleting a viewed user.

The UserScreen class allows to specify the name and introduction prompt 
for a virtual user.
"""

from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen


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
                ["arrow-left", lambda x: app.root.switch_back(), "Back", "Back"]
                ]
            right_action_items:
                [
                ["content-copy", lambda x: root.clone_user(), "Clone", "Clone"],
                ["delete", lambda x: root.open_delete_user_dialog(), "Delete", "Delete"]
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

    user_id = NumericProperty(allownone=True)

    user_name = StringProperty()
    user_introduction = StringProperty()

    delete_user_dialog = None

    def on_enter(self):
        self.ids.user_screen_top_app_bar.title = (
            "User" if self.user_id is not None else "New user"
        )

        if self.user_id is None:
            # Create new user
            self.user_name = "New user"
            self.user_introduction = "Hi, I am a new user."
        else:
            # Load user
            self.user_name = "John Doe"
            self.user_introduction = "Hello, I am John Doe."

    def clone_user(self):
        print("Cloning user")  # TODO: Implement cloning user

        self.manager.switch_screen(
            "user_clone_screen", {"original_user_id": self.user_id}
        )

    def open_delete_user_dialog(self):
        if self.delete_user_dialog is None:
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

        self.delete_user_dialog.open()

    def delete_user(self):
        print("Deleting user")  # TODO: Implement deleting user

        self.delete_user_dialog.dismiss()
        self.manager.switch_back()
