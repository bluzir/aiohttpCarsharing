from peewee import *

from models.base import *
from models.user import User


class CardLink(BaseModel):
    masked_pan = TextField()
    user = ForeignKeyField(User)
    create_date = DateTimeField(null=True)