from peewee import *

from model.base import *
from model.user import User
from model.payment import Payment


class CardLink(BaseModel):
    masked_pan = TextField()
    user = ForeignKeyField(User)
    inplat_link_id = TextField()
    payment = ForeignKeyField(Payment)
