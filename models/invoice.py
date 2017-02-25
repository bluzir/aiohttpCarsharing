from peewee import *

from models.base import *
from models.payment import Payment
from models.user import User
from utils.utils import generate_uuid


class Invoice(BaseModel):
    uuid = TextField(unique=True, default=generate_uuid)
    summ = IntegerField()
    payment = ForeignKeyField(Payment, null=True)
    user = ForeignKeyField(User, related_name='invoices')

    def handle_form(self, crypto):
        return {}