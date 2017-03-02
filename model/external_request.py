import datetime
from peewee import *

from model.base import BaseModel


class ExternalRequest(BaseModel):
    EXTERNAL_SYSTEM = (
        (0, 'Undefined'),
        (1, 'Inplat'),
        (2, 'Starline'),
    )

    external_system = IntegerField(choices=EXTERNAL_SYSTEM)
    request_url = TextField()
    request_params = TextField(null=True)
    request_headers = TextField(null=True)
    request_data = TextField(null=True)
    response_headers = TextField(null=True)
    response_body = TextField(null=True)
    created_at = FloatField(default=datetime.datetime.now().timestamp())

