from peewee import *

from inplat_wrapper.api import InplatException

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

    def encode_auth_token(self, user_id):
        pass

    @staticmethod
    def decode_auth_token(auth_token):
        pass


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
            print(user_id, card_number, year, month, cvv, card_holder )
            return {'success': True}
        except InplatException as e:
            return {'error': e.code, 'message': e.message}


class Order(BaseModel):
    user = ForeignKeyField(User)
    car = ForeignKeyField(Car)
    invoice = ForeignKeyField(Invoice)






