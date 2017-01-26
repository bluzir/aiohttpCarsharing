import hashlib
import hmac
import json

import requests


class InplatException:
    def __init__(self):
        self.error = None
        self.text = None


class InplatClient:
    API_KEY = 'F5aPOR2Zm3vHFQXVBjLgpnub'
    DEFAULT_HOST = 'https://demo-api2.inplat.ru/'
    SECRET_WORD = b'B1BUnfwEE2mAUK4D'

    def __init__(self):
        self.sign = None
        self.data = None

        self.params = {
            'api_key': self.API_KEY,
        }

        self.pay_type = None
        self.client_id = None

    # Initialize payment
    def init(self, pay_type, client_id, pay_params, params):
        self.data = {
            'method': 'init',
            'pay_type': pay_type,
            'client_id': client_id,
            'case': 'link',
            'pay_params': pay_params,
            'params': params,
            'merc_data': 'Random information',
        }
        return self.request()

    # Check payment status in Inplat system
    def check(self, payment_id):
        self.data = {
            'method': 'check',
            'id': payment_id,
        }
        return self.request()

    # Payment by linked card
    def pay(self, client_id, link_id, params):
        self.data = {
            'method': 'pay',
            'client_id': client_id,
            'link_id': link_id,
            'params': params,
            'merc_data': 'Random information',
        }
        return self.request()

    # Refund payment
    def refund(self, payment_id, amount):
        self.data = {
            'method': 'refund',
            'id': payment_id,
            'amount': amount,
        }
        return self.request()

    # Link a card
    def link(self, client_id, pay_params):
        self.data = {
            'method': 'link',
            'pay_type': 'card',
            'client_id': client_id,
            'pay_params': pay_params,
        }
        return self.request()

    # Unlink a card
    def unlink(self, link_id):
        self.data = {
            'method': 'unlink',
            'link_id': link_id,
        }
        return self.request()

    # List of linked cards by id
    def links(self, client_id):
        self.data = {
            'method': 'links',
            'client_id': client_id,
        }
        return self.request()

    # Basic request with self.data
    def request(self):
        if self.generate_sign():
            self.params.update({'sign': self.sign})
            response = requests.post(url=self.DEFAULT_HOST,
                                     params=self.params,
                                     data=self.data)
            if response.status_code == 200:
                return response
            else:
                print(response.status_code)
                print(response.text)
                return False
        else:
            print('Problem with generating sign')
            return False

    def generate_sign(self):
        try:
            json_data = json.dumps(self.data).encode('utf-8')
            generated = hmac.new(self.SECRET_WORD,
                                 msg=json_data,
                                 digestmod=hashlib.sha256).hexdigest()
            print(generated)
            self.sign = generated
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    client = InplatClient()
    init = client.init(
        pay_type='mc',
        client_id='hp1L18kmOWVegdka30',
        pay_params={"msisdn":79265327068},
        params={
            "account": "test",
            "sum": 1023,
            "email": "pay@example.com",
            "details": "Оплата благотворительности",
            "address": "ул. Пролетарская 23",
        }
    )
    print(init.json())