import os
import shutil
from uuid import uuid4

from peewee import CharField, ForeignKeyField

from alkvin.entities.user import User
from alkvin.entities.bot import Bot

from alkvin.db import BaseModel


CHATS_AUDIO_DIR = os.path.join("resources", "audio")


class Chat(BaseModel):
    """Chat model class for chat conversations."""

    title = CharField(default="")
    summary = CharField(default="")

    user = ForeignKeyField(User, backref="chats", null=True)
    bot = ForeignKeyField(Bot, backref="chats", null=True)

    @classmethod
    def create(cls, *args, **kwargs):
        chat = super().create(*args, **kwargs)
        chat_audio_dir = os.path.join(CHATS_AUDIO_DIR, str(chat.id))
        os.makedirs(chat_audio_dir)
        return chat

    @classmethod
    def new(cls):
        new_chat_title = f"NEW CHAT [{uuid4().hex[:8]}]"
        new_chat_summary = (
            "Press the summarization button to get the chat title and summary."
        )
        return cls.create(title=new_chat_title, summary=new_chat_summary)

    def delete_instance(self, *args, **kwargs):
        for user_message in self.user_messages:
            user_message.delete_instance()
        for assistant_message in self.assistant_messages:
            assistant_message.delete_instance()

        chat_audio_dir = os.path.join(CHATS_AUDIO_DIR, str(self.id))
        shutil.rmtree(chat_audio_dir)

        return super().delete_instance(*args, **kwargs)
