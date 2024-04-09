from peewee import CharField, DateTimeField, ForeignKeyField, SQL

from alkvin.entities.user import User
from alkvin.entities.bot import Bot

from alkvin.db import BaseModel


class Chat(BaseModel):
    """Chat model class for chat conversations."""

    title = CharField()
    summary = CharField()
    user = ForeignKeyField(User, backref="chats")
    bot = ForeignKeyField(Bot, backref="chats")

    created_at = DateTimeField(constraints=[SQL("DEFAULT (datetime('now'))")])
    updated_at = DateTimeField()
    deleted_at = DateTimeField(null=True)
