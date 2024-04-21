import os
from datetime import datetime

from peewee import CharField, DateTimeField, ForeignKeyField

from alkvin.db import BaseModel

from alkvin.entities.chat import Chat


class AssistantMessage(BaseModel):
    """AssistantMessage model class for chat assistant messages."""

    chat = ForeignKeyField(Chat, backref="assistant_messages")

    completion = CharField(default="")
    completion_received_at = DateTimeField(null=True)

    speech_file = CharField(null=True)
    speech_received_at = DateTimeField(null=True)

    @property
    def speech_path(self):
        return os.path.join(self.chat.audio_dir, self.speech_file)

    @classmethod
    def create(cls, *args, **kwargs):
        super().create(*args, completion_received_at=datetime.now(), **kwargs)
