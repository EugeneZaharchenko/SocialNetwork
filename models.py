from peewee import (Model, SqliteDatabase, DoubleField, CharField, IntegerField, DateTimeField,
                    datetime as peewee_datetime)
from config import DB_NAME


network_db = SqliteDatabase(DB_NAME)


class User(Model):
    class Meta:
        db = network_db

    created = DateTimeField(default=peewee_datetime.datetime.now)
    visit = DateTimeField(default=peewee_datetime.datetime.now)
    user_name = CharField(max_length=100)
    user_email = CharField(max_length=100)

    def to_dict(self):
        return self._data


User.create_table(True)
