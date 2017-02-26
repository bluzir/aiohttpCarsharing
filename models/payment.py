from peewee import *

from models.base import *


class Payment(BaseModel):
    status = IntegerField(default=0)