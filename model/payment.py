from peewee import *

from model.base import *
from model.invoice import Invoice
from model.user import User

class Payment(BaseModel):
    PAYMENT_STATUS = {
        'created': 0,
        'wait_for_redirect': 1,
        'wait_for_callback': 2,
        'success': 3,
        'error': 4
    }

    status = IntegerField(default=0, choices=PAYMENT_STATUS)
    inplat_id = IntegerField()
    order_id = TextField()
    sum = IntegerField()
    invoice = ForeignKeyField(Invoice, null=True)
    user = ForeignKeyField(User, related_name='payments')
