import peewee
import peewee_async

# database = peewee_async.PostgresqlDatabase()


class Car(peewee.Model):
    id = peewee.IntegerField(
        primary_key=True,
    )
    car_model = peewee.TextField(
        verbose_name='Модель машины',
    )

    def get_fuel(self):
        pass

    class Meta:
        database = ''


class User(peewee.Model):
    USER_STATUSES = {
        '0': 'Неподтвержденный',
        '1': 'Администратор',
    }

    id = peewee.IntegerField(
        primary_key=True,
    )
    first_name = peewee.TextField(
        verbose_name='Имя',
    )
    last_name = peewee.TextField(
        verbose_name='Фамилия',
    )
    email = peewee.TextField(
        verbose_name='Email',
    )
    password = peewee.TextField(
        verbose_name='Пароль',
    )
    phone_number = peewee.TextField(
        verbose_name='Номер телефона',
    )
    status = peewee.IntegerField(
        default=0,
        choices=USER_STATUSES,
        verbose_name='Статус'
    )