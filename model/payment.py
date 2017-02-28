from peewee import *

from model.base import *
from model.user import User

class Payment(BaseModel):
    PAYMENT_STATUS = {
        'created': 0,
        'wait_for_redirect': 1,
        'wait_for_callback': 2,
        'success': 3,
        'error': 4
    }

    status = IntegerField(default=0)
    error_code = IntegerField(default=0)
    inplat_id = TextField(null=True, unique=True)
    order_id = TextField(null=True, unique=True)
    sum = IntegerField()
    # 0 - links, 1 - checkout
    case = IntegerField(default=0)
    user = ForeignKeyField(User, related_name='payments')
