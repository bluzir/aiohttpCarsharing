import datetime

import jwt
from peewee import *

from inplat_wrapper.api import InplatException, InplatClient
import settings as config

database = SqliteDatabase('carsharing.db')  # Temporary database


class BaseModel(Model):
    class Meta:
        database = database


class Car(BaseModel):
    car_model = TextField()


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

    def encode_auth_token(self, user_id, jwt=None):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256')
        except Exception as e:
            return e

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
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


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
            client = InplatClient()
            return {'success': True}
        except InplatException as e:
            return {'error': e.code, 'message': e.message}


class Order(BaseModel):
    user = ForeignKeyField(User)
    car = ForeignKeyField(Car)
    invoice = ForeignKeyField(Invoice, null=True)






