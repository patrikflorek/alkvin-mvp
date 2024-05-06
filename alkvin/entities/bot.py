"""
Bot
===

This module defines the Bot model class, which is used to store chat bots data 
in the database.

Example usage:
    bot = Bot.create(name="My Bot")
"""

from datetime import datetime
from uuid import uuid4

from peewee import CharField, FloatField

from alkvin.db import BaseModel


SPEECH_VOICES = ("alloy", "echo", "fable", "onyx", "nova", "shimmer")


class Bot(BaseModel):
    """Bot model class for chat bots."""

    name = CharField(unique=True)

    transcription_language = CharField(default="en")  # ISO-639-1 format
    transcription_prompt = CharField(default="")
    transcription_temperature = FloatField(default=0.0)

    completion_prompt = CharField(default="")
    completion_temperature = FloatField(default=1.0)

    summarization_prompt = CharField(default="")

    speech_voice = CharField(default=SPEECH_VOICES[0])

    def get_speech_voices():
        return SPEECH_VOICES

    def new():
        return Bot.create(name=f"NEW BOT [{uuid4().hex[:8]}]")

    def replicate(self):
        """Get a replica of the bot."""

        return Bot.create(
            name=f"{self.name} REPLICA [{uuid4().hex[:8]}]",
            transcription_language=self.transcription_language,
            transcription_prompt=self.transcription_prompt,
            transcription_temperature=self.transcription_temperature,
            completion_prompt=self.completion_prompt,
            completion_temperature=self.completion_temperature,
            summarization_prompt=self.summarization_prompt,
            speech_voice=self.speech_voice,
        )

    def get_taken_names(self):
        return [bot.name for bot in Bot.select().where(Bot.name != self.name)]

    def transcribe_audio(self, audio_path):
        from random import choice

        transcript = choice(
            [
                "This is a transcription.",
                "This is another transcription.",
                "This is yet another transcription.",
                "This is the final transcription.",
            ]
        )
        return transcript

    def chat_complete(self, chat, on_completion_callback):
        """Create a completion based on the bot's prompts and
        the previous chat messages."""

        messages = chat.messages_to_complete

        from random import choice

        completion = choice(
            [
                "This is a completion.",
                "This is another completion.",
                "This is yet another completion.",
                "This is the final completion.",
            ]
        )

        on_completion_callback(completion)

    def synthesize_speech(self, completion):
        return f"user_{datetime.now().isoformat()}.opus"
