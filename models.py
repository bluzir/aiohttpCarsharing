import peewee
import peewee_async

import settings

DATABASE = peewee_async.PostgresqlDatabase(settings.DB_NAME, user=settings.DB_USER)


class Users(peewee.Model):
    email = peewee.CharField(
        max_length=30,
        unique=True,
    )
    password = peewee.CharField(
        max_length=30,
    )

    class Meta:
        database = DATABASE








