import os
from datetime import datetime

from peewee import CharField, DateTimeField, ForeignKeyField

from alkvin.db import BaseModel

from alkvin.entities.chat import Chat

from alkvin.config import CHATS_AUDIO_DIR


class AssistantMessage(BaseModel):
    """AssistantMessage model class for chat assistant messages."""

    chat = ForeignKeyField(Chat, backref="assistant_messages")

    completion = CharField()
    completion_received_at = DateTimeField(default=datetime.now)

    speech_file = CharField(null=True)
    speech_received_at = DateTimeField(null=True)

    def get_speech_path(self):
        return os.path.join(CHATS_AUDIO_DIR, str(self.chat.id), self.speech_file)
