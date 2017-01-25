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