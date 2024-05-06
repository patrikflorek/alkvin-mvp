"""
Chat
====

This module defines the Chat model class, which is used to store chat 
conversations in the database.

Example usage:
    chat = Chat.create(title="My Chat")
"""

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

    @property
    def messages(self):
        """Get all messages in the chat, sorted by sent time."""

        def messages_sorting_key(message):
            from .user_message import UserMessage
            from .assistant_message import AssistantMessage

            is_sent_message = (
                isinstance(message, UserMessage) and message.sent_at is not None
            ) or isinstance(message, AssistantMessage)

            if isinstance(message, UserMessage):
                sorting_time = (
                    message.sent_at
                    if message.sent_at is not None
                    else message.audio_created_at
                )
            elif isinstance(message, AssistantMessage):
                sorting_time = message.completion_received_at

            return (is_sent_message, sorting_time)

        return sorted(
            list(self.user_messages) + list(self.assistant_messages),
            key=messages_sorting_key,
        )

    @property
    def audio_dir(self):
        return os.path.join(CHATS_AUDIO_DIR, str(self.id))

    @property
    def messages_to_complete(self):
        """Conversation messages and prompts packed in the API format."""

        from .user_message import UserMessage
        from .assistant_message import AssistantMessage

        messages = [{"role": "system", "content": self.bot.completion_prompt}]

        if self.user.introduction:
            messages.append({"role": "user", "content": self.user.introduction})

        for message in self.messages:
            if isinstance(message, UserMessage) and message.sent_at is not None:
                messages.append({"role": "user", "content": message.transcript})
            elif isinstance(message, AssistantMessage):
                messages.append({"role": "assistant", "content": message.completion})

        return messages

    @classmethod
    def create(cls, *args, **kwargs):
        chat = super().create(*args, **kwargs)
        os.makedirs(chat.audio_dir)
        return chat

    @classmethod
    def new(cls):
        new_chat_title = f"NEW CHAT [{uuid4().hex[:8]}]"
        new_chat_summary = (
            "Press the summarization button to get the chat title and summary."
        )
        return cls.create(title=new_chat_title, summary=new_chat_summary)

    def delete_instance(self, *args, **kwargs):
        """Delete the chat instance and all its messages and audio files."""

        for user_message in self.user_messages:
            user_message.delete_instance()
        for assistant_message in self.assistant_messages:
            assistant_message.delete_instance()

        chat_audio_dir = os.path.join(CHATS_AUDIO_DIR, str(self.id))
        shutil.rmtree(chat_audio_dir)

        return super().delete_instance(*args, **kwargs)
