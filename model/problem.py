from peewee import *

from model.base import *


class Problem(BaseModel):
    title = TextField()