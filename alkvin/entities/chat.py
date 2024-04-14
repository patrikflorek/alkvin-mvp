import os
import shutil

from peewee import CharField, ForeignKeyField

from alkvin.entities.user import User
from alkvin.entities.bot import Bot

from alkvin.db import BaseModel


CHATS_AUDIO_DIR = os.path.join("alkvin", "resources", "audio")


class Chat(BaseModel):
    """Chat model class for chat conversations."""

    title = CharField()
    summary = CharField()
    user = ForeignKeyField(User, backref="chats", null=True)
    bot = ForeignKeyField(Bot, backref="chats", null=True)

    def create(*args, **kwargs):
        chat = super().create(*args, **kwargs)
        chat_audio_dir = os.path.join(CHATS_AUDIO_DIR, str(chat.id))
        os.makedirs(chat_audio_dir)
        return chat

    def delete_instance(self, *args, **kwargs):
        for user_message in self.user_messages:
            user_message.delete_instance()
        for assistant_message in self.assistant_messages:
            assistant_message.delete_instance()

        chat_audio_dir = os.path.join(CHATS_AUDIO_DIR, str(self.id))
        shutil.rmtree(chat_audio_dir)

        return super().delete_instance(*args, **kwargs)
