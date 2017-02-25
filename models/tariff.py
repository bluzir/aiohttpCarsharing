from peewee import *

from models.base import *


class Tariff(BaseModel):
    name = TextField()
    description = TextField(null=True)