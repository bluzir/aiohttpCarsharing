from peewee import *

from models.base import *


class Media(BaseModel):
    path = TextField()