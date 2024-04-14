from peewee import CharField

from alkvin.db import BaseModel


class User(BaseModel):
    """User model class for chat users."""

    name = CharField(unique=True)
    introduction = CharField(default="")

    def get_new_name():
        """Get a new user name."""
        return f"NEW USER [{User.select().count() + 1}]"

    def get_clone_name(self):
        """Get a clone user name."""
        return f"{self.name} CLONE [{User.select().count() + 1}]"

    def taken_names(self):
        """Get taken user names."""
        return [user.name for user in User.select().where(User.name != self.name)]
