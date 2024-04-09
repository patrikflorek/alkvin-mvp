from peewee import CharField, DateTimeField, SQL

from alkvin.db import BaseModel


class Bot(BaseModel):
    """Bot model class for chat bots."""

    name = CharField(unique=True)
    language = CharField()
    instructions = CharField()
    speech_prompt = CharField()
    speech_voice = CharField()

    created_at = DateTimeField(constraints=[SQL("DEFAULT (datetime('now'))")])
    updated_at = DateTimeField()
    deleted_at = DateTimeField(null=True)
