"""
Home Screen
===========

This module defines the HomeScreen class and related components for 
the Alkvin MVP application.

The HomeScreen class represents the main screen of the application, which 
displays a menu directing users to differentsections of the app, such as chats, 
users, bots, and settings.
"""

from kivy.lang import Builder

from kivymd.uix.screen import MDScreen


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
                        
                        on_release: app.root.switch_screen("chats_screen")

                MDAnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"
                    size_hint_y: None
                    height: self.width

                    HomeScreenMenuItem:
                        id: users_menu_item

                        icon: "account-group"
                        text: "Users"
                        
                        on_release: app.root.switch_screen("users_screen")

                MDAnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"
                    size_hint_y: None
                    height: self.width

                    HomeScreenMenuItem:
                        id: bots_menu_item

                        icon: "robot"
                        text: "Bots"
                        
                        on_release: app.root.switch_screen("bots_screen")

                MDAnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"
                    size_hint_y: None
                    height: self.width

                    HomeScreenMenuItem:
                        id: settings_menu_item

                        icon: "cogs"
                        text: "Settings"
                        
                        on_release: app.root.switch_screen("settings_screen")
"""
)


class HomeScreen(MDScreen):
    """Main screen of the Alkvin MVP application."""
