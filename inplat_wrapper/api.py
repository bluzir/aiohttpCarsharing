import hashlib
import hmac

import requests


class InplatClient:
    API_KEY = 'F5aPOR2Zm3vHFQXVBjLgpnub'
    DEFAULT_HOST = 'https://demo-api2.inplat.ru/{}'
    SECRET_WORD = 'B1BUnfwEE2mAUK4D'

    def __init__(self):
        self.sign = None
        self.data = None

        self.params = {
            'api_key': self.API_KEY,
            'sign': self.sign,
        }

    def init(self, pay_type, client_id, ):
        self.data = {
            'method': 'init',
            'pay_type': pay_type,
            'client_id': client_id,
            'case': 'link',
            'pay_params': {},
            'params': {},
            'merc_data': 'Random information',
        }
        self.request()

    def request(self):
        if self.generate_sign():
            return requests.post(url=self.DEFAULT_HOST,
                                 params=self.params,
                                 data=self.data)
        else:
            print('Problem with generating sign')
            return False

    def generate_sign(self):
        try:
            self.sign = hmac.new(self.SECRET_WORD,
                                 msg=self.data,
                                 digestmod=hashlib.sha256).hexdigest()
        except Exception as e:
            print(e)
            return False



