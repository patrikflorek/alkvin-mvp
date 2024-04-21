from uuid import uuid4

from peewee import CharField

from alkvin.db import BaseModel

SPEECH_VOICES = ("alloy", "echo", "fable", "onyx", "nova", "shimmer")


class Bot(BaseModel):
    """Bot model class for chat bots."""

    name = CharField(unique=True)
    language = CharField(default="")
    generation_prompt = CharField(default="")
    summarization_prompt = CharField(default="")
    speech_prompt = CharField(default="")
    speech_voice = CharField(default=SPEECH_VOICES[0])

    def get_speech_voices():
        return SPEECH_VOICES

    def new():
        """Get a new bot."""
        return Bot.create(name=f"NEW BOT [{uuid4().hex[:8]}]")

    def replicate(self):
        """Get a replica of the bot."""
        return Bot.create(
            name=f"{self.name} REPLICA [{uuid4().hex[:8]}]",
            language=self.language,
            generation_prompt=self.generation_prompt,
            summarization_prompt=self.summarization_prompt,
            speech_prompt=self.speech_prompt,
            speech_voice=self.speech_voice,
        )

    def get_taken_names(self):
        """Get taken bot names."""
        return [bot.name for bot in Bot.select().where(Bot.name != self.name)]

    def complete_chat(self, messages_to_complete, on_completion_callback):
        completion = "This is a completion."
        on_completion_callback(completion)
