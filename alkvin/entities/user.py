from peewee import CharField

from alkvin.db import BaseModel


class User(BaseModel):
    """User model class for chat users."""

    name = CharField(unique=True)
    introduction = CharField(default="")

    def new():
        """Get a new user."""
        return User.create(name=f"NEW USER [{User.select().count() + 1}]")

    def clone(self):
        """Get a clone of the user."""
        return User.create(
            name=f"{self.name} CLONE [{User.select().count() + 1}]",
            introduction=self.introduction,
        )

    def get_taken_names(self):
        """Get taken user names."""
        return [user.name for user in User.select().where(User.name != self.name)]
