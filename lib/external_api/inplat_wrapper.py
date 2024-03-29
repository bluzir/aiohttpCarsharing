import hashlib
import hmac
import json

import requests

from lib.external_api.base_wrapper import BaseClient, SystemName


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
        super(InplatClient, self).__init__()
        self.sign = None
        self.url = self.DEFAULT_HOST
        self.external_system = SystemName.INPLAT

        self.params = {
            'api_key': self.API_KEY,
        }

        self.pay_type = None
        self.client_id = None

    async def _post(self):
        self.generate_sign()
        return await super().post()

    # Initialize payment
    async def init(self, pay_type='card', pay_params={}, params={}, merc_data=''):
        self.data = {
            'method': 'init',
            'pay_type': pay_type,
            'pay_params': pay_params,
            'params': params,
            'merc_data': merc_data,
        }

        return await self._post()

    # Check payment status in Inplat system
    async def check(self, payment_id):
        self.data = {
            'method': 'check',
            'id': payment_id,
        }
        return await self._post()

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

    async def pay_by_link(self, client_id, link_id, summ, account):
        self.data = {
            'method': 'pay',
            'client_id': self._md5(client_id),
            'link_id': link_id,
            'params': {
                'account': account, # fuck inplat
                'sum': summ,
                'client_id': self._md5(client_id),
                },
            'merc_data': 'Random information',
        }
        return await self._post()

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
            'client_id': self._md5(client_id),
            'pay_params': {
                'cryptogramma': cryptogramma
            },
        }
        return self._post()

    async def pay_and_link(self, client_id, cryptogramma, account, summ):

        self.data = {
            'method': 'init',
            'pay_type': 'card',
            'case': 'link',
            'client_id': self._md5(client_id),
            'redirect_url': 'https://stage.2car.spb.ru/api/inplat/redirect/',
            'pay_params': {
                'cryptogramma': cryptogramma
            },
            'params': {
                'account': account, # fuck inplat
                'sum': summ,
                },
            # only for test
            #'redirect_url': 'http://127.0.0.1:9999/api/inplat/redirect/'
        }

        return await self._post()

    # Unlink a card
    def unlink(self, link_id):
        self.data = {
            'method': 'unlink',
            'link_id': link_id,
        }
        return self._post()

    # List of linked cards by id
    def links(self, client_id):
        self.data = {
            'method': 'links',
            'client_id': self._md5(client_id), # fuck inplat [2]
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

    @staticmethod
    def _md5(s):
        return hashlib.md5(str(s).encode('utf-8')).hexdigest()

