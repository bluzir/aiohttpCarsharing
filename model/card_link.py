from peewee import *

from model.base import *
from model.user import User


class CardLink(BaseModel):
    masked_pan = TextField()
    user = ForeignKeyField(User)
    create_date = DateTimeField(null=True)