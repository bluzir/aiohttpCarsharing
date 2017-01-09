import asyncio
import peewee
import peewee_async


database = peewee_async.PostgresqlDatabase('test_db', user='test_user')


class Users(peewee.Model):
    login = peewee.CharField(
        max_length=30,
    )
    password = peewee.CharField(
        max_length=30,
    )

    class Meta:
        database=database








