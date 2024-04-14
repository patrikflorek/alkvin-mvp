from peewee import CharField, DateTimeField, SQL

from alkvin.db import BaseModel


class User(BaseModel):
    """User model class for chat users."""

    name = CharField(unique=True)
    introduction = CharField(default="")

    def get_new_name():
        """Get a new user name."""
        return f"NEW USER [{User.select().count() + 1}]"

    def get_clone_name(original_user_name):
        """Get a clone user name."""
        return f"CLONE OF {original_user_name} [{User.select().count() + 1}]"

    def get_taken_names(exceptions=[]):
        """Get taken user names."""
        return [user.name for user in User.select().where(User.name.not_in(exceptions))]
