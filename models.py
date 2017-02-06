# -*- coding: utf-8 -*-
import datetime

import jwt
from peewee import *

import settings as config
from lib.external_api.inplat_wrapper import InplatException, InplatClient

database = PostgresqlDatabase(config.DB_NAME, user=config.DB_USER)


class BaseModel(Model):
    class Meta:
        database = database


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
            return {'user_id': payload['sub']}
        except jwt.ExpiredSignatureError:
            return {'error': 'Signature expired. Please log in again.'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token. Please log in again.'}


class Payment(BaseModel):
    status = IntegerField()


class Invoice(BaseModel):
    summ = DecimalField()
    payment = ForeignKeyField(Payment, null=True)
    user = ForeignKeyField(User)

    def handle_form(self, data):
        try:
            user_id = self.user.id
            card_number = data['card-number']
            year = data['year']
            month = data['month']
            cvv = data['cvv']
            card_holder = data['card-holder']
            payment_sum = self.summ
            if card_holder and card_number and month and year and cvv:
                client = InplatClient()
                pay_params = {
                    'pan': card_number,
                    'expire_month': month,
                    'expire_year': year,
                    'cvv': cvv,
                    'cardholder_name': card_holder,
                }
                params = {
                    'sum': int(self.summ),
                    'account': self.id,
                }
                response = client.init(pay_type='card',  client_id=user_id,  pay_params=pay_params, params=params)
                return {'success': True, 'response': response}
            else:
                error = 'Заполните все поля'
            return {'error': error}
        except InplatException as e:
            return {'error': e.message, 'code': e.code}


class Order(BaseModel):
    user = ForeignKeyField(User)
    car = ForeignKeyField(Car)
    invoice = ForeignKeyField(Invoice, null=True)






