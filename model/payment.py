from enum import Enum

import datetime
from peewee import *

from model.base import *
from model.user import User


class PaymentStatus(Enum):
    CREATED = 1
    WAIT_FOR_REDIRECT = 2
    WAIT_FOR_CALLBACK = 3
    SUCCESS = 4
    ERROR = 5


class Payment(BaseModel):
    status = IntegerField(default=0, choices=PaymentStatus)
    error_code = IntegerField(default=0)
    inplat_id = TextField(null=True, unique=True)
    order_id = TextField(null=True, unique=True)
    sum = IntegerField()
    # 0 - links, 1 - checkout
    case = IntegerField()
    user = ForeignKeyField(User, related_name='payments')
    created_at = DateTimeField(default=datetime.datetime.now)
    paid_at = DateTimeField(null=True)
