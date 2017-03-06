from enum import Enum

import datetime
from peewee import *

from model.base import database, BaseModel
from model.car import Car
from model.invoice import Invoice
from model.problem import Problem
from model.user import User


class RideStatus(Enum):
    ENDED = 1
    OCCURS = 2  # происходит


class Ride(BaseModel):
    user = ForeignKeyField(User, related_name='rides')
    car = ForeignKeyField(Car, related_name='rides')
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    invoice = ForeignKeyField(Invoice, null=True)
    problem = ForeignKeyField(Problem, null=True)
    status = IntegerField(default=0, choices=RideStatus)
    created_at = DateTimeField(default=datetime.datetime.now)