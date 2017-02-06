import hashlib
import hmac
import json

import requests

from lib.external_api.base_wrapper import BaseClient


class InplatException(BaseException):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class InplatClient(BaseClient):
    DEFAULT_HOST = 'https://demo-api2.inplat.ru/'
    API_KEY = 'F5aPOR2Zm3vHFQXVBjLgpnub'
    SECRET_WORD = b'B1BUnfwEE2mAUK4D'

    def __init__(self):
        self.sign = None
        self.data = None

        self.params = {
            'api_key': self.API_KEY,
        }

        self.pay_type = None
        self.client_id = None
        super(InplatClient, self).__init__()

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
            'redirect_url': 'http://127.0.0.1:8080'
        }
        self.generate_sign()
        return self.post(url=self.DEFAULT_HOST,
                         params=self.params,
                         data=self.data)

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
            print(self.params)
            response = requests.post(url=self.DEFAULT_HOST,
                                     params=self.params,
                                     data=json.dumps(self.data))
            decoded = response.json()
            if 'code' in decoded:
                if decoded['code'] != 0:
                    raise InplatException(decoded['code'], decoded['message'])
                else:
                    return decoded
            else:
                print(decoded)
                raise InplatException(500, 'Problem with request')
        else:
            raise InplatException(-1, 'Problem with generating sign')

    def generate_sign(self):
        try:
            json_data = json.dumps(self.data).encode('utf-8')
            generated = hmac.new(self.SECRET_WORD,
                                 msg=json_data,
                                 digestmod=hashlib.sha256).hexdigest()
            self.sign = generated
            self.params.update({'sign': self.sign})
            return True
        except Exception as e:
            print(e)
            return False

def main():
    client = InplatClient()
    init = client.init(
        pay_type='mc',
        client_id='hp1L18kmOWVegdka30',
        pay_params={"msisdn": 79265327068},
        params={
            "account": "test",
            "sum": 1023,
            "email": "pay@example.com",
            "details": "Оплата благотворительности",
            "address": "ул. Пролетарская 23",
        }
    )
    print(init.json())


if __name__ == '__main__':
    main()
