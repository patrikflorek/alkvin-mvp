"""
Floating Action Button (FAB)
============================

This module contains a custom floating action button (FAB) widget with fixed
elevation defect.

Example usage:
    fab = FAB()
"""

from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton


class FAB(MDFloatingActionButton):
    """Custom floating action button (FAB) widget with fixed elevation defect."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "large"
        self.theme_icon_color = "Custom"
        app = MDApp.get_running_app()
        self.icon_color = app.theme_cls.opposite_text_color

        Clock.schedule_once(
            self.set_elevation
        )  # This is a hack to set the elevation after rendering of a FAB

    def set_elevation(self, dt):
        self.elevation = 2
