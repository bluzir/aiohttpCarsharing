import json

from inplatpy.utils import create_sign

DEMO_URL = 'https://demo-api2.inplat.ru'
PRODUCTION_URL = 'https://api2.inplat.ru'
API_KEY = 'F5aPOR2Zm3vHFQXVBjLgpnub'
SECRET = 'B1BUnfwEE2mAUK4D'


class InplatAPI:
    def __init__(self):
        self.access_token = API_KEY
        self.method = None
        self.data = None
        self.sign = None
        self.params = None

    def _post_requset(self, params, data):
        pass

    def generate_data(self):
        self.data = {}
        pass

    def generate_sign(self):
        message = json.dumps(self.data).encode('utf-8')
        self.sign = create_sign(SECRET, message)

    def initialize(self):  # Inplat API method init
        self.method = 'init'
        self._generate_data()
        return self._post_requset(data=self.data)







