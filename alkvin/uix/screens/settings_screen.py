"""
Settings Screen
===============

This module defines the SettingsScreen class which represents the screen for configuring the application settings.

The SettingsScreen class allows users to set the OpenAI API key required to run OpenAI models.
"""

from dotenv import get_key, set_key

from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.screen import MDScreen


Builder.load_string(
    """
<SettingsScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Settings"
            specific_text_color: app.theme_cls.opposite_text_color
            left_action_items: 
                [
                ["arrow-left", lambda x: app.root.switch_back(), "Back", "Back"]
                ]

        ScrollView:
            id: settings_screen_scroll

            MDBoxLayout:
                orientation: "vertical"
                padding: "40dp"
                spacing: "40dp"
                adaptive_height: True

                MDBoxLayout:
                    orientation: "horizontal"
                    adaptive_height: True
                    spacing: "20dp"

                    MDTextField:
                        id: open_api_key_field
                        text: root.openai_api_key
                        on_text: root.openai_api_key = self.text
                        hint_text: "OpenAI API Key"
                        helper_text: "Required to run OpenAI models"
                        helper_text_mode: "on_focus"
                        icon_left: "key-variant"
                        required: True
"""
)


class SettingsScreen(MDScreen):
    """Screen for configuring the application settings."""

    openai_api_key = StringProperty()

    def on_enter(self):
        openai_api_key = get_key(".env", "OPENAI_API_KEY")
        if openai_api_key is not None:
            self.openai_api_key = openai_api_key

    def on_pre_leave(self):
        set_key(".env", "OPENAI_API_KEY", self.openai_api_key)
