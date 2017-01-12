import hashlib

import peewee
import peewee_async

import settings


USER_STATUS_CHOICES = (
    ('0', 'Новый'),
    ('1', 'Подтвержденный'),
    ('2', 'Заблокирован'),
)

class Users(peewee.Model):
    email = peewee.CharField(
        max_length=30,
        unique=True,
    )
    password = peewee.CharField(
        max_length=30,
    )


    @classmethod
    def encrypt_password(cls, password):
        return hashlib.sha256(password).hexdigest()

    class Meta:
        database = peewee_async.PostgresqlDatabase(settings.DB_NAME, user=settings.DB_USER)








