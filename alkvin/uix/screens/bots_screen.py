"""
Bots Screen
===========

This module defines the BotsScreen class which represents the screen 
for displaying a list of available chat bots and provides functionality
for creating new bots.
"""

from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, StringProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem

from alkvin.entities.bot import Bot


Builder.load_string(
    """
#:import FAB alkvin.uix.components.fab.FAB

<BotsScreenBotItem>:
    text: root.bot_name
    secondary_text: root.bot_instructions

    on_release: app.root.switch_screen("bot_screen", {"bot_id": self.bot_id})

<BotsScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Bots"
            specific_text_color: app.theme_cls.opposite_text_color
            left_action_items: 
                [
                ["arrow-left", lambda x: app.root.switch_back(), "Back", "Back"]
                ]
        
        MDRecycleView:
            data: root.bot_items
            viewclass: "BotsScreenBotItem"

            MDRecycleGridLayout:
                cols: 1
                default_size: None, None
                default_size_hint: 1, None
                adaptive_height: True

    MDAnchorLayout:
        anchor_x: "right"
        anchor_y: "bottom"
        padding: dp(48)    

        FAB:
            icon: "robot-love"
            
            on_release: app.root.switch_screen("bot_screen", {"bot_id": None})
"""
)


class BotsScreenBotItem(TwoLineListItem):
    """Custom list item for displaying a chat bot."""

    bot_id = NumericProperty()
    bot_name = StringProperty()
    bot_instructions = StringProperty()


class BotsScreen(MDScreen):
    """Screen for displaying a list of available chat bots."""

    bot_items = ListProperty()

    def on_pre_enter(self):
        if Bot.select().count() == 0:
            Bot.create(name="Dummy Bot")

        bots = Bot.select(Bot.id, Bot.name, Bot.generation_prompt)
        self.bot_items = [
            {
                "bot_id": bot.id,
                "bot_name": bot.name,
                "bot_instructions": bot.generation_prompt,
            }
            for bot in bots
        ]
