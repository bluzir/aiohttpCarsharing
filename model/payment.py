from peewee import *

from model.base import *
from model.user import User


class Payment(BaseModel):
    PAYMENT_STATUS = (
        (0, 'created'),
        (1, 'wait_for_redirect'),
        (2, 'wait_for_callback'),
        (3, 'success'),
        (4, 'error')
    )

    status = IntegerField(default=0)
    error_code = IntegerField(default=0)
    inplat_id = TextField(null=True, unique=True)
    order_id = TextField(null=True, unique=True)
    sum = IntegerField()
    # 0 - links, 1 - checkout
    case = IntegerField()
    user = ForeignKeyField(User, related_name='payments')
