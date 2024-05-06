"""
User Message
============

This module contains the UserMessage model class, which is used to store chat user messages in the database.

Example usage:
    message = UserMessage.create(chat=chat, audio_file="audio.wav")
"""

import os
from datetime import datetime

from peewee import CharField, DateTimeField, ForeignKeyField

from alkvin.db import BaseModel

from alkvin.entities.chat import Chat


class UserMessage(BaseModel):
    """UserMessage model class for chat user messages."""

    chat = ForeignKeyField(Chat, backref="user_messages")

    audio_file = CharField()
    audio_created_at = DateTimeField(default=datetime.now)

    transcript = CharField(default="")
    transcript_received_at = DateTimeField(null=True)

    sent_at = DateTimeField(null=True)

    @property
    def audio_path(self):
        return os.path.join(self.chat.audio_dir, self.audio_file)
