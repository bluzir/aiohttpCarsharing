import datetime
from enum import Enum

from peewee import *

from model.base import BaseModel


class RequestType(Enum):
    GET = 1
    POST = 2


class RequestDirection(Enum):
    INCOMING = 1
    OUTCOMING = 2


class SystemName(Enum):
    UNDEFINED = 1
    INPLAT = 2
    STARLINE = 3


class Request(BaseModel):
    request_direction = IntegerField(choices=RequestType)
    request_type = IntegerField(choices=RequestDirection)
    external_system = IntegerField(choices=SystemName, null=True)
    request_url = TextField()
    request_params = TextField(null=True)
    request_headers = TextField(null=True)
    request_data = TextField(null=True)
    response_headers = TextField(null=True)
    response_body = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

