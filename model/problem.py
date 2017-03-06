import datetime
from peewee import *

from model.base import *


class Problem(BaseModel):
    title = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)