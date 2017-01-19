import requests

from inplatpy import settings


class InplatAPICLient:
    _demo_url = 'https://demo-api2.inplat.ru'
    _production_url = 'https://api2.inplat.ru'


    def __init__(self, conformation, **kwargs):
        self.confirmation = None
        self.client_id = None
        self.pay_type = None
        self.client_id = None
        self.case = None
        self.pay_params = None
        self.params = None
        self.data = None


    def create_data(self):
        data = {
            "method": "form",
            "pay_type": self.pay_type,
            "case": self.case,
        }

        if self.client_id:
            data.update({'client_id': self.client_id})
        pass


    def post(self, method, sign, data=None, **kwargs):
        params = {
            'apikey': settings.API_KEY,
            'sign': sign,
        }
        response = requests.get(self._demo_url, params=params, data=data)
        pass






new_user = InplatAPICLient()
