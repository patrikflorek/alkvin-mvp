from peewee import CharField, DateTimeField, ForeignKeyField, SQL

from alkvin.db import BaseModel

from alkvin.entities.chat import Chat


class BotMessage(BaseModel):
    """BotMessage model class for chat bot messages."""

    chat = ForeignKeyField(Chat, backref="bot_messages")

    completion = CharField()
    completion_received_at = DateTimeField(
        constraints=[SQL("DEFAULT (datetime('now'))")]
    )

    speech_file = CharField(null=True)
    speech_received_at = DateTimeField(null=True)
