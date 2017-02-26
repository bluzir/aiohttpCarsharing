from peewee import *

from model.base import *


class Media(BaseModel):
    path = TextField()