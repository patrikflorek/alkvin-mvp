from peewee import CharField, DateTimeField, SQL

from alkvin.db import BaseModel


class User(BaseModel):
    """User model class for chat users."""

    name = CharField(unique=True)
    introduction = CharField()

    created_at = DateTimeField(constraints=[SQL("DEFAULT (datetime('now'))")])
    updated_at = DateTimeField()
    deleted_at = DateTimeField(null=True)
