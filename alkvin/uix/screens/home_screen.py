"""
Home Screen
===========

This module defines the HomeScreen class and related components for the Alkvin MVP application.

The HomeScreen class represents the main screen of the application, which displays a menu directing users to different
sections of the app, such as chats, users, bots, and settings.
"""

from kivy.lang import Builder

from kivymd.uix.screen import MDScreen

from alkvin.entities.chat import Chat
from alkvin.entities.user import User
from alkvin.entities.bot import Bot


Builder.load_string(
    """
<HomeScreenMenuItem@MDCard>:
    icon: ""
    text: ""

    orientation: "vertical"
    size_hint: None, None
    size: "200dp", "200dp"
    md_bg_color: app.theme_cls.primary_color
    elevation: 0.5
    ripple_behavior: True

    MDAnchorLayout:
        anchor_x: "center"
        anchor_y: "bottom"

        MDIcon:
            icon: root.icon
            font_size: "60sp"
            theme_text_color: "Custom"
            text_color: app.theme_cls.opposite_text_color

    MDLabel:
        text: root.text
        halign: "center"
        theme_text_color: "Custom"
        text_color: app.theme_cls.opposite_text_color
        font_style: "H6"


<HomeScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Alkvin MVP"
            theme_text_color: "Custom"
            specific_text_color: app.theme_cls.opposite_text_color

        MDScrollView:
            id: home_screen_scroll

            MDGridLayout:
                cols: max(1, int(home_screen_scroll.width / dp(240)))
                adaptive_height: True
                padding: "40dp"
                spacing: "40dp"

                MDAnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"
                    size_hint_y: None
                    height: self.width

                    HomeScreenMenuItem:
                        id: chats_menu_item

                        icon: "forum"
                        text: "Chats"
                        
                        on_release: app.root.switch_to_chats()

                MDAnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"
                    size_hint_y: None
                    height: self.width

                    HomeScreenMenuItem:
                        id: users_menu_item

                        icon: "account-group"
                        text: "Users"
                        
                        on_release: root.switch_to_users()

                MDAnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"
                    size_hint_y: None
                    height: self.width

                    HomeScreenMenuItem:
                        id: bots_menu_item

                        icon: "robot"
                        text: "Bots"
                        
                        on_release: root.switch_to_bots()

                MDAnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"
                    size_hint_y: None
                    height: self.width

                    HomeScreenMenuItem:
                        id: settings_menu_item

                        icon: "cogs"
                        text: "Settings"
                        
                        on_release: root.switch_to_settings()
"""
)


class HomeScreen(MDScreen):
    """Main screen of the Alkvin MVP application."""

    def switch_to_chats(self):
        """Switch to the chats screen."""
        chats = Chat.select().order_by(Chat.updated_at.desc())

        self.manager.switch_screen("chats_screen", chats)

    def switch_to_users(self):
        """Switch to the users screen."""
        if User.select().count() == 0:
            User.create(name="Dummy User")

        users = User.select().order_by(User.name)

        self.manager.switch_screen("users_screen", users)

    def switch_to_bots(self):
        """Switch to the bots screen."""
        if Bot.select().count() == 0:
            Bot.create(name="Dummy Bot")

        bots = Bot.select().order_by(Bot.name)

        self.manager.switch_screen("bots_screen", bots)

    def switch_to_settings(self):
        """Switch to the settings screen."""
        self.manager.switch_screen("settings_screen")
