# -*- coding: utf-8 -*-
import datetime

import jwt
from aiohttp import web
from aiohttp_session import get_session
from peewee import *

import base_settings as config
from errors import _error
from lib.external_api.inplat_wrapper import InplatException, InplatClient
from utils.utils import generate_uuid

database = PostgresqlDatabase(config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD)


class BaseModel(Model):
    class Meta:
        database = database


class Tariff(BaseModel):
    name = TextField()
    description = TextField(null=True)


class Problem(BaseModel):
    title = TextField()


class Media(BaseModel):
    path = TextField()


class Car(BaseModel):
    CAR_STATUSES = {
        '0': 'Недоступна',
        '1': 'Доступна',
        '2': 'Забронирована',
        '3': 'В поездке'
    }

    wialon_id = IntegerField(unique=True, null=True)
    car_model = TextField()
    lat = FloatField(default=0)
    long = FloatField(default=0)
    status = IntegerField(choices=CAR_STATUSES)

    def get_fuel(self):
        # request to external API
        return None

    @staticmethod
    def get_available_cars():
        return Car.select().where(Car.status == 1)


class User(BaseModel):
    USER_STATUSES = {
        '0': 'Неподтвержденный',
        '1': 'Администратор',
    }

    first_name = TextField()
    last_name = TextField()
    email = TextField()
    password = TextField()
    phone_number = TextField(null=True)
    status = IntegerField(default=0, choices=USER_STATUSES)
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

    def get_current_ride(self):
        current_rides = self.rides.where(Ride.status == 1)
        if current_rides.__len__() == 1:
            ride = current_rides.get()
            return ride



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


class Payment(BaseModel):
    status = IntegerField()


class Invoice(BaseModel):
    uuid = TextField(unique=True, default=generate_uuid)
    summ = IntegerField()
    payment = ForeignKeyField(Payment, null=True)
    user = ForeignKeyField(User, related_name='invoices')

    def handle_form(self, crypto):
        try:
            if crypto:
                client = InplatClient()
                pay_params = {
                    'cryptogramma': crypto,
                }
                params = {
                    'sum': self.summ,
                    'account': self.id,
                }
                response = client.init(pay_type='card',  pay_params=pay_params, params=params)
                return {'success': True, 'response': response}
            else:
                error = 'Заполните все поля'
            return {'error': error}
        except InplatException as e:
            return {'error': e.message, 'code': e.code}


class Ride(BaseModel):
    RIDE_STATUSES = {
        '0': 'Завершена',
        '1': 'Происходит',
    }

    user = ForeignKeyField(User, related_name='rides')
    car = ForeignKeyField(Car, related_name='rides')
    start_date = DateTimeField(default=datetime.datetime.now)
    end_date = DateTimeField(null=True)
    invoice = ForeignKeyField(Invoice, null=True)
    problem = ForeignKeyField(Problem, null=True)
    status = IntegerField(default=0)


class Damage(BaseModel):
    car = ForeignKeyField(Car)
    applicant = ForeignKeyField(User)
    car_part = IntegerField()
    photos = ForeignKeyField(Media)

