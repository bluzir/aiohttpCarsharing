from peewee import *

from model.base import *
from model.car import Car
from model.user import User


class Damage(BaseModel):
    car = ForeignKeyField(Car)
    applicant = ForeignKeyField(User)
    car_part = IntegerField()
    photos = ForeignKeyField(Media)