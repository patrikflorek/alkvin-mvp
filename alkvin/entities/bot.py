from peewee import CharField, DateTimeField, SQL

from alkvin.db import BaseModel


class Bot(BaseModel):
    """Bot model class for chat bots."""

    name = CharField(unique=True)
    language = CharField(default="")
    generation_prompt = CharField(default="")
    summarization_prompt = CharField(default="")
    speech_prompt = CharField(default="")
    speech_voice = CharField(default="")

    def get_speech_voices():
        return ("alloy", "echo", "fable", "onyx", "nova", "shimmer")

    def get_new_name():
        """Get a new bot name."""
        return f"NEW BOT [{Bot.select().count() + 1}]"

    def get_replica_name(prototype_bot_name):
        """Get a replica bot name."""
        return f"{prototype_bot_name} REPLICA [{Bot.select().count() + 1}]"

    def get_taken_names(exceptions=[]):
        """Get taken bot names."""
        return [bot.name for bot in Bot.select().where(Bot.name.not_in(exceptions))]
