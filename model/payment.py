from enum import IntEnum

import datetime
from playhouse.postgres_ext import *

from model.base import *
from model.user import User


class PaymentStatus(IntEnum):
    CREATED = 1
    WAIT_FOR_REDIRECT = 2
    WAIT_FOR_CALLBACK = 3
    BLOCKED = 4
    PAID = 5
    REVERSED = 6
    REFUND = 7
    ERROR = 10


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
    credentials = JSONField(null=True)
    pstamp = DateTimeField(null=True)
    astamp = DateTimeField(null=True)
    inplat_link_id = TextField(null=True)

