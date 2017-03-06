import datetime
from enum import IntEnum

from peewee import *

from model.base import BaseModel


class RequestMethod(IntEnum):
    GET = 1
    POST = 2
    OTHER = 3


class RequestType(IntEnum):
    INCOMING = 1
    OUTCOMING = 2


class SystemName(IntEnum):
    UNDEFINED = 1
    INPLAT = 2
    STARLINE = 3


class Request(BaseModel):
    external_system = IntegerField(choices=SystemName, null=True)
    # request fields
    request_type = IntegerField(choices=RequestType)
    request_method = IntegerField(choices=RequestMethod, null=True)
    request_url = TextField()
    request_params = TextField(null=True)
    request_headers = TextField(null=True)
    request_data = TextField(null=True)
    # response fields
    response_headers = TextField(null=True)
    response_body = TextField(null=True)
    # date
    created_at = DateTimeField(default=datetime.datetime.now)

