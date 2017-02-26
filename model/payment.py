from peewee import *

from model.base import *


class Payment(BaseModel):
    status = IntegerField(default=0)