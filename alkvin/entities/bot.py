from peewee import CharField

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

    def get_replica_name(self):
        """Get a replica bot name."""
        return f"{self.name} REPLICA [{Bot.select().count() + 1}]"

    def get_taken_names(self):
        """Get taken bot names."""
        return [bot.name for bot in Bot.select().where(Bot.name != self.name)]
