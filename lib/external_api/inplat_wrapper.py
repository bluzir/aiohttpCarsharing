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
    API_ID = 1
    DEFAULT_HOST = 'https://demo-api2.inplat.ru/'
    API_KEY = 'EVrAuGGEjgN020MmMdwV0dqp'
    SECRET_WORD = b'a3NchcP7P2145qTE'  # TODO: Hide into non-versioned file

    def __init__(self):
        self.sign = None
        self.data = None

        self.params = {
            'api_key': self.API_KEY,
        }

        self.pay_type = None
        self.client_id = None
        super(InplatClient, self).__init__()

    def _post(self):
        self.generate_sign()
        super().post(url=self.DEFAULT_HOST,
                         params=self.params,
                         data=self.data)

    # Initialize payment
    def init(self, pay_type='card', pay_params={}, params={}, merc_data=''):
        self.data = {
            'method': 'init',
            'pay_type': pay_type,
            'pay_params': pay_params,
            'params': params,
            'merc_data': merc_data,
        }

        return self._post()

    # Check payment status in Inplat system
    def check(self, payment_id):
        self.data = {
            'method': 'check',
            'id': payment_id,
        }
        return self._post()

    # Payment by linked card
    def pay(self, client_id, link_id, params):
        self.data = {
            'method': 'pay',
            'client_id': client_id,
            'link_id': link_id,
            'params': params,
            'merc_data': 'Random information',
        }
        return self._post()

    # Refund payment
    def refund(self, payment_id, amount, params):
        self.data = {
            'method': 'refund',
            'id': payment_id,
            'amount': amount,
        }
        return self._post()

    # Link a card
    def link(self, client_id, cryptogramma):
        self.data = {
            'method': 'link',
            'pay_type': 'card',
            'client_id': client_id,
            'pay_params': {
                'cryptogramma': cryptogramma
            },
        }
        return self._post()

    # Link a card
    def pay_and_link(self, client_id, cryptogramma):
        '''
                        "params": {
                    "account": "test",
                    "sum": 1023,
                    "email": "pay@example.com",
                    "details": "Some data",
                    "address": " Some data"
                },
                "merc_data": "Random information"
        '''

        self.data = {
            'method': 'init',
            'pay_type': 'card',
            'client_id': client_id,
            'case': 'link',
            'pay_params': {
                'cryptogramma': cryptogramma
            },
        }

        return self._post()

    # Unlink a card
    def unlink(self, link_id, params):
        self.data = {
            'method': 'unlink',
            'link_id': link_id,
        }
        return self._post()

    # List of linked cards by id
    def links(self, client_id, params):
        self.data = {
            'method': 'links',
            'client_id': client_id,
        }
        return self._post()

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


