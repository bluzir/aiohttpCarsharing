from peewee import *

from models.base import *


class Problem(BaseModel):
    title = TextField()