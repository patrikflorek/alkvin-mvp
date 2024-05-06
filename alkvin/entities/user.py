"""
User
====

This module defines the User model class, which is used to store virtual chat 
users in the database.

Example usage:
    user = User.create(name="My User")
"""

from uuid import uuid4

from peewee import CharField

from alkvin.db import BaseModel


class User(BaseModel):
    """User model class for chat users."""

    name = CharField(unique=True)
    introduction = CharField(default="")

    def new():
        return User.create(name=f"NEW USER [{uuid4().hex[:8]}]")

    def clone(self):
        """Get a clone of the virtual user."""

        return User.create(
            name=f"{self.name} CLONE [{uuid4().hex[:8]}]",
            introduction=self.introduction,
        )

    def get_taken_names(self):
        return [user.name for user in User.select().where(User.name != self.name)]
