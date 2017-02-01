import peewee
import peewee_async

# database = peewee_async.PostgresqlDatabase()
from inplat_wrapper.api import InplatClient, InplatException


class Car(peewee.Model):
    id = peewee.IntegerField(primary_key=True,)
    car_model = peewee.TextField(verbose_name='Модель машины',)

    def get_fuel(self):
        pass


class User(peewee.Model):
    USER_STATUSES = {
        '0': 'Неподтвержденный',
        '1': 'Администратор',
    }

    id = peewee.IntegerField(primary_key=True,)
    first_name = peewee.TextField(verbose_name='Имя')
    last_name = peewee.TextField(verbose_name='Фамилия')
    email = peewee.TextField(verbose_name='Email')
    password = peewee.TextField(verbose_name='Пароль')
    phone_number = peewee.TextField(verbose_name='Номер телефона')
    status = peewee.IntegerField(default=0, choices=USER_STATUSES, verbose_name='Статус')


class Payment(peewee.Model):
    id = peewee.IntegerField(primary_key=True)

    def handle_form(self, data):
        try:
            card_number = data['card-number']
            year = data['year']
            month = data['month']
            cvv = data['cvv']
            card_holder = data['card-holder']
            try:
                payment_sum = int(data['payment-sum'])
            except Exception as e:
                payment_sum = data['payment-sum']
                return {'error': e}
            if card_number and year and month and cvv and card_holder:
                client = InplatClient()
                pay_params = {
                    'pan': card_number,
                    'expire_month': month,
                    'expire_year': year,
                    'cvv': cvv,
                    'cardholder_name': card_holder,
                }
                params = {
                    'sum': payment_sum,
                    'account': data['payment_id'],
                }
                response = client.init(pay_type='card',
                                       client_id=data['user-id'],
                                       pay_params=pay_params,
                                       params=params)
                return {'success': True, 'id': response['id'], 'url': response['id']}
            else:
                return {'user_id': data['user-id'], 'account': data['account'], 'sum': payment_sum,
                        'error': 'Заполните все поля'}
        except InplatException as e:
            return {'error': e.message, 'status': e.code}