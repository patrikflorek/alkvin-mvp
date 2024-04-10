from peewee import CharField, DateTimeField, ForeignKeyField, SQL

from alkvin.db import BaseModel

from alkvin.entities.chat import Chat


class UserMessage(BaseModel):
    """UserMessage model class for chat user messages."""

    chat = ForeignKeyField(Chat, backref="user_messages")

    audio_file = CharField()
    audio_created_at = DateTimeField(constraints=[SQL("DEFAULT (datetime('now'))")])

    transcript = CharField(null=True)
    transcript_received_at = DateTimeField(null=True)

    sent_at = DateTimeField(null=True)
    updated_at = DateTimeField()
    deleted_at = DateTimeField(null=True)
