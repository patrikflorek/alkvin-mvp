from peewee import CharField, DateTimeField, SQL

from alkvin.db import BaseModel


class User(BaseModel):
    """User model class for chat users."""

    name = CharField(unique=True)
    introduction = CharField(null=True)
