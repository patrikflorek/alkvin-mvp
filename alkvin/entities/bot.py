from peewee import CharField, DateTimeField, SQL

from alkvin.db import BaseModel


class Bot(BaseModel):
    """Bot model class for chat bots."""

    name = CharField(unique=True)
    language = CharField(null=True)
    instructions = CharField(default="")
    summarization_prompt = CharField(default="")
    speech_prompt = CharField(default="")
    speech_voice = CharField(null=True)
