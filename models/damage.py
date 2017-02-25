from peewee import *

from models.base import *
from models.car import Car
from models.user import User


class Damage(BaseModel):
    car = ForeignKeyField(Car)
    applicant = ForeignKeyField(User)
    car_part = IntegerField()
    photos = ForeignKeyField(Media)