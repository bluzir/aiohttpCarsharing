from peewee import *

from model.base import *


class Tariff(BaseModel):
    name = TextField()
    description = TextField(null=True)