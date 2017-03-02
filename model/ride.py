from peewee import *

from model.base import database, BaseModel
from model.car import Car
from model.invoice import Invoice
from model.problem import Problem
from model.user import User


class Ride(BaseModel):
    RIDE_STATUS = (
        (0, 'Завершена'),
        (1, 'Происходит'),
    )

    user = ForeignKeyField(User, related_name='rides')
    car = ForeignKeyField(Car, related_name='rides')
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    invoice = ForeignKeyField(Invoice, null=True)
    problem = ForeignKeyField(Problem, null=True)
    status = IntegerField(default=0)