from peewee import SqliteDatabase, Model

db = SqliteDatabase("resources/alkvin.db")


class BaseModel(Model):
    class Meta:
        database = db
        legacy_table_names = False
