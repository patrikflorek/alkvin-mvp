from peewee import CharField, DateTimeField, SQL

from alkvin.db import BaseModel


class Bot(BaseModel):
    """Bot model class for chat bots."""

    name = CharField(unique=True)
    language = CharField(null=True)
    instructions = CharField(null=True)
    summarization_prompt = CharField(null=True)
    speech_prompt = CharField(null=True)
    speech_voice = CharField(null=True)
