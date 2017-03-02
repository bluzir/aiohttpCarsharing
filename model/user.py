import datetime

import jwt
from aiohttp import web
from aiohttp_session import get_session
from peewee import *

from error import _error
from model.base import *
from model.tariff import Tariff


class User(BaseModel):
    USER_STATUS = (
        (0, 'Неподтвержденный'),
        (1, 'Администратор'),
    )

    first_name = TextField(null=True)
    last_name = TextField(null=True)
    email = TextField(unique=True)
    password = TextField()
    phone_number = TextField(unique=True)
    status = IntegerField(default=0, choices=USER_STATUS)
    tariff = ForeignKeyField(Tariff, null=True)

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """

        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': self.id,
        }

        return jwt.encode(
            payload=payload,
            key=config.SECRET_KEY,
            algorithm='HS256')





    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, config.SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    @staticmethod
    def get_user_by_token(auth_token):
        user_id = User.decode_auth_token(auth_token)
        if user_id:
            return User.get(id=user_id)
        else:
            return False

    @staticmethod
    async def handle_registration_form(data, request):
        session = await get_session(request)
        if 'phone' and 'password' in data:
            phone = data['phone']
            password = data['password']
            if 'email' in data:
                email = data['email']
            else:
                email = None

            if phone and password:
                user = User.create(phone_number=phone, email=email, password=password)
                auth_token = user.encode_auth_token().decode("utf-8")
                session['auth_token'] = auth_token
                return web.json_response({'auth_token': auth_token})

        return _error.error_response(_error, _error.EMPTY_FIELD)

    @staticmethod
    async def handle_authorization_form(data, request):
        session = await get_session(request)
        if 'email' in data and 'password' in data:
            email = data['email']
            password = data['password']
            if email and password:
                user = User.select().where(User.email == email, User.password == password)
                if user.__len__() == 1:
                    user = user.get()
                    auth_token = user.encode_auth_token().decode("utf-8")
                    session['auth_token'] = auth_token
                    return web.json_response({'auth_token': auth_token})
                else:
                    return _error.error_response(_error, _error.INVALID_LOGIN)

        return _error.error_response(_error, _error.EMPTY_FIELD)