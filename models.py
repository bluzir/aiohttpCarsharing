import peewee
import settings


class Users(peewee.Model):
    login = peewee.CharField(
        max_length=30,
    )
    password = peewee.CharField(
        max_length=30,
    )

    class Meta:
        database = settings.DATABASE








