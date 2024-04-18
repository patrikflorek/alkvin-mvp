"""
Alkvin MVP App
==============

Alkvin MVP is a kivy/kivymd-based app designed for voice-based communication 
with LLM chat bots.
"""

from dotenv import get_key

from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager

from alkvin.uix.screens.home_screen import HomeScreen
from alkvin.uix.screens.chats_screen import ChatsScreen
from alkvin.uix.screens.chat_screen import ChatScreen
from alkvin.uix.screens.users_screen import UsersScreen
from alkvin.uix.screens.user_screen import UserScreen
from alkvin.uix.screens.user_create_screen import UserCreateScreen
from alkvin.uix.screens.user_clone_screen import UserCloneScreen
from alkvin.uix.screens.bots_screen import BotsScreen
from alkvin.uix.screens.bot_screen import BotScreen
from alkvin.uix.screens.bot_create_screen import BotCreateScreen
from alkvin.uix.screens.bot_replicate_screen import BotReplicateScreen
from alkvin.uix.screens.settings_screen import SettingsScreen

from alkvin.db import db

from alkvin.entities.chat import Chat
from alkvin.entities.user import User
from alkvin.entities.bot import Bot
from alkvin.entities.user_message import UserMessage
from alkvin.entities.assistant_message import AssistantMessage


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
        self.add_widget(UserCreateScreen(name="user_create_screen"))
        self.add_widget(UserCloneScreen(name="user_clone_screen"))
        self.add_widget(BotsScreen(name="bots_screen"))
        self.add_widget(BotScreen(name="bot_screen"))
        self.add_widget(BotCreateScreen(name="bot_create_screen"))
        self.add_widget(BotReplicateScreen(name="bot_replicate_screen"))
        self.add_widget(SettingsScreen(name="settings_screen"))

    def push_to_history(self, screen_name, screen_entity_id):
        screen_history_item = (screen_name, screen_entity_id)
        if screen_history_item in self.screen_history:
            self.screen_history.remove(screen_history_item)
        self.screen_history.append(screen_history_item)

    def switch_screen(self, screen_name, screen_entity_id=None, direction="forward"):
        self.push_to_history(screen_name, screen_entity_id)
        self.transition.direction = "right" if direction == "back" else "left"

        screen = self.get_screen(screen_name)
        screen_entity_id_attribute = screen_name.split("_")[0] + "_id"
        if hasattr(screen, screen_entity_id_attribute):
            setattr(screen, screen_entity_id_attribute, screen_entity_id)

        self.current = screen_name

    def pop_from_history(self):
        current_screen_name, current_screen_entity_id = self.screen_history.pop()

        # Remove original/prototype screen from the history when switching back from user clone screen and robot replica screen, respectively.
        if current_screen_name in ["user_clone_screen", "bot_replica_screen"]:
            self.screen_history.pop()

        return self.screen_history[-1]  # screen_name, screen_entity_id

    def switch_back(self):
        if len(self.screen_history) > 1:
            screen_name, screen_entity_id = self.pop_from_history()
            self.switch_screen(screen_name, screen_entity_id, direction="back")


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "LightBlue"
        self.theme_cls.accent_palette = "Orange"

        return AppRoot()

    def on_start(self):
        db.connect()
        db.create_tables([Chat, User, Bot, UserMessage, AssistantMessage])

        if get_key(".env", "OPENAI_API_KEY") is None:
            Clock.schedule_once(
                lambda dt: self.root.switch_screen("settings_screen"), 2
            )
