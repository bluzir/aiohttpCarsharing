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

Users.create(login='test', password='test')

database.close()

objects = peewee_async.Manager(database)
database.set_allow_sync(False)

async def handler():
    await objects.create(Users, text="Not bad. Watch this, I'm async!")
    all_objects = await objects.execute(Users.select())
    for obj in all_objects:
        print(obj.login, obj.password)



loop = asyncio.get_event_loop()
loop.run_until_complete(handler())
loop.close()





