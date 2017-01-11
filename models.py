import peewee
import peewee_async

import settings

DATABASE = peewee_async.PostgresqlDatabase(settings.DB_NAME, user=settings.DB_USER)


class Users(peewee.Model):
    login = peewee.CharField(
        max_length=30,
    )
    password = peewee.CharField(
        max_length=30,
    )

    class Meta:
        database = DATABASE








