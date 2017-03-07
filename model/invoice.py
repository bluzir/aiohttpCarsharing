import datetime

from peewee import *

from model.base import *
from model.payment import Payment
from model.user import User
from utils import generate_uuid


class Invoice(BaseModel):
    uuid = TextField(unique=True, default=generate_uuid)
    summ = IntegerField()
    payment = ForeignKeyField(Payment, null=True)
    user = ForeignKeyField(User, related_name='invoices')
    created_at = DateTimeField(default=datetime.datetime.now)

    def handle_form(self, crypto):
        return {}