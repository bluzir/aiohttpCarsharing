import datetime
from peewee import *

from model.base import *


class Tariff(BaseModel):
    name = TextField()
    description = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)