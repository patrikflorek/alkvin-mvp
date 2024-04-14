from datetime import datetime

from peewee import CharField, DateTimeField, ForeignKeyField

from alkvin.db import BaseModel

from alkvin.entities.chat import Chat


class AssistantMessage(BaseModel):
    """AssistantMessage model class for chat assistant messages."""

    chat = ForeignKeyField(Chat, backref="assistant_messages")

    completion = CharField()
    completion_received_at = DateTimeField(default=datetime.now)

    speech_file = CharField(null=True)
    speech_received_at = DateTimeField(null=True)
