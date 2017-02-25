from peewee import *

from models.base import *
from models.car import Car
from models.invoice import Invoice
from models.problem import Problem
from models.user import User


class Ride(BaseModel):
    RIDE_STATUSES = {
        '0': 'Завершена',
        '1': 'Происходит',
    }

    user = ForeignKeyField(User, related_name='rides')
    car = ForeignKeyField(Car, related_name='rides')
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    invoice = ForeignKeyField(Invoice, null=True)
    problem = ForeignKeyField(Problem, null=True)
    status = IntegerField(default=0)