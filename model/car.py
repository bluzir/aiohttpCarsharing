from enum import Enum

import datetime
from peewee import *

from model.base import *


class CarStatus(Enum):
    UNAVAILABLE = 1
    AVAILABLE = 2
    BOOKED = 3
    RIDING = 4


class Car(BaseModel):
    wialon_id = IntegerField(unique=True, null=True)
    car_model = TextField()
    lat = FloatField(default=0)
    long = FloatField(default=0)
    status = IntegerField(choices=CarStatus)
    created_at = DateTimeField(default=datetime.datetime.now)

    def get_fuel(self):
        # request to external API
        return None

    @staticmethod
    def get_available_cars():
        return Car.select().where(Car.status == 1)