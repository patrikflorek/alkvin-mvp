import os
from datetime import datetime

from peewee import CharField, DateTimeField, ForeignKeyField

from alkvin.db import BaseModel

from alkvin.entities.chat import Chat

from alkvin.config import CHATS_AUDIO_DIR


class UserMessage(BaseModel):
    """UserMessage model class for chat user messages."""

    chat = ForeignKeyField(Chat, backref="user_messages")

    audio_file = CharField()
    audio_created_at = DateTimeField(default=datetime.now)

    transcript = CharField(default="")
    transcript_received_at = DateTimeField(null=True)

    sent_at = DateTimeField(null=True)

    def get_audio_path(self):
        return os.path.join(CHATS_AUDIO_DIR, str(self.chat.id), self.audio_file)
