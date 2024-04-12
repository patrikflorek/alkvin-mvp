from datetime import datetime

from peewee import DateTimeField, Model, SqliteDatabase


db = SqliteDatabase("resources/alkvin.db")


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    deleted_at = DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        database = db
        legacy_table_names = False
