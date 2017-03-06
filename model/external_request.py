import datetime
from enum import Enum

from peewee import *

from model.base import BaseModel


class ExternalSystemName(Enum):
    UNDEFINED = 1
    INPLAT = 2
    STARLINE = 3


class ExternalRequest(BaseModel):
    external_system = IntegerField(choices=ExternalSystemName)
    request_url = TextField()
    request_params = TextField(null=True)
    request_headers = TextField(null=True)
    request_data = TextField(null=True)
    response_headers = TextField(null=True)
    response_body = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

