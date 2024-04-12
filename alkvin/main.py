"""
Alkvin MVP App
==============

Alkvin MVP is a kivy/kivymd-based app designed for voice-based communication 
with LLM chat bots.
"""

from dotenv import get_key

from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager

from alkvin.uix.screens.home_screen import HomeScreen
from alkvin.uix.screens.chats_screen import ChatsScreen
from alkvin.uix.screens.chat_screen import ChatScreen
from alkvin.uix.screens.users_screen import UsersScreen
from alkvin.uix.screens.user_screen import UserScreen
from alkvin.uix.screens.user_clone_screen import UserCloneScreen
from alkvin.uix.screens.bots_screen import BotsScreen
from alkvin.uix.screens.bot_screen import BotScreen
from alkvin.uix.screens.bot_replica_screen import BotReplicaScreen
from alkvin.uix.screens.settings_screen import SettingsScreen

from alkvin.db import db

from alkvin.entities.chat import Chat
from alkvin.entities.user import User
from alkvin.entities.bot import Bot
from alkvin.entities.user_message import UserMessage
from alkvin.entities.bot_message import BotMessage


from kivy.clock import Clock


class AppRoot(ScreenManager):
    screen_history = [("home_screen", None)]

    missing_api_key_snackbar = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HomeScreen(name="home_screen"))
        self.add_widget(ChatsScreen(name="chats_screen"))
        self.add_widget(ChatScreen(name="chat_screen"))
        self.add_widget(UsersScreen(name="users_screen"))
        self.add_widget(UserScreen(name="user_screen"))
        self.add_widget(UserCloneScreen(name="user_clone_screen"))
        self.add_widget(BotsScreen(name="bots_screen"))
        self.add_widget(BotScreen(name="bot_screen"))
        self.add_widget(BotReplicaScreen(name="bot_replica_screen"))
        self.add_widget(SettingsScreen(name="settings_screen"))

        if get_key(".env", "OPENAI_API_KEY") is None:
            Clock.schedule_once(lambda dt: self.switch_screen("settings_screen"), 3)

    def switch_screen(self, screen_name, screen_data=None, direction="forward"):
        screen_history_item = (screen_name, screen_data)
        if screen_history_item in self.screen_history:
            self.screen_history.remove(screen_history_item)
        self.screen_history.append((screen_name, screen_data))

        self.transition.direction = "right" if direction == "back" else "left"

        screen = self.get_screen(screen_name)
        if screen_data is not None:
            for key, value in screen_data.items():
                setattr(screen, key, value)
        else:
            # If no screen data is provided, check if the screen has an attribute ending with "_id".
            id_attribute = next(
                (attr for attr in dir(screen) if attr.endswith("_id")), None
            )
            if id_attribute is not None and hasattr(screen, id_attribute):
                setattr(screen, id_attribute, None)

        self.current = screen_name

    def switch_back(self):
        if len(self.screen_history) > 1:
            current_screen, current_screen_data = self.screen_history.pop()
            # Remove original/prototype screen from the history when switching back from user clone screen and robot replica screen, respectively.
            if current_screen in ["user_clone_screen", "bot_replica_screen"]:
                self.screen_history.pop()

            screen_name, screen_data = self.screen_history[-1]
            self.switch_screen(screen_name, screen_data, direction="back")


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "LightBlue"
        self.theme_cls.accent_palette = "Orange"

        return AppRoot()

    def on_start(self):
        db.connect()
        db.create_tables([Chat, User, Bot, UserMessage, BotMessage])
