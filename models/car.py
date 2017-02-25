from peewee import *

from models.base import *


class Car(BaseModel):
    CAR_STATUSES = {
        '0': 'Недоступна',
        '1': 'Доступна',
        '2': 'Забронирована',
        '3': 'В поездке'
    }

    wialon_id = IntegerField(unique=True, null=True)
    car_model = TextField()
    lat = FloatField(default=0)
    long = FloatField(default=0)
    status = IntegerField(choices=CAR_STATUSES)

    def get_fuel(self):
        # request to external API
        return None

    @staticmethod
    def get_available_cars():
        return Car.select().where(Car.status == 1)