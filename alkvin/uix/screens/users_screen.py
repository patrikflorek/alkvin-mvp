"""
Users Screen
============

This module defines the UsersScreen class which represents the screen 
for displaing a list of available (virtual) users and provides functionality
for creating new users.
"""

from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, StringProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem

from alkvin.entities.user import User


Builder.load_string(
    """
#:import FAB alkvin.uix.components.fab.FAB


<UsersScreenUserItem>:
    text: root.user_name
    secondary_text: root.user_introduction

    on_release: app.root.switch_screen("user_screen", {"user_id": self.user_id})

    
<UsersScreen>:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Users"
            specific_text_color: app.theme_cls.opposite_text_color
            left_action_items: 
                [
                ["arrow-left", lambda x: app.root.switch_back(), "Back", "Back"]
                ]
        
        MDRecycleView:
            data: root.user_items
            viewclass: "UsersScreenUserItem"

            MDRecycleGridLayout:
                cols: 1
                default_size: None, None
                default_size_hint: 1, None
                adaptive_height: True

    MDAnchorLayout:
        anchor_x: "right"
        anchor_y: "bottom"
        padding: dp(48)
        
        MDFloatingActionButton:
            icon: "account-plus"
            type: "large"
            elevation_normal: 12
            
            on_release: app.root.switch_screen("user_screen", {"user_id": None})

    MDAnchorLayout:
        anchor_x: "right"
        anchor_y: "bottom"
        padding: dp(48)

        FAB:   
            icon: "account-plus"
            
            on_release: app.root.switch_screen("user_screen", {"user_id": None})
"""
)


class UsersScreenUserItem(TwoLineListItem):
    """Custom list item widget for displaying users."""

    user_id = NumericProperty()
    user_name = StringProperty()
    user_introduction = StringProperty()


class UsersScreen(MDScreen):
    """Screen for displaying a list of available users."""

    user_items = ListProperty()

    def on_pre_enter(self):
        if User.select().count() == 0:
            User.create(name="Dummy User")

        users = User.select(User.id, User.name, User.introduction)
        self.user_items = [
            {
                "user_id": user.id,
                "user_name": user.name,
                "secondary_text": user.introduction,
            }
            for user in users
        ]
