import json

import requests


class BaseClient:

    def __init__(self):
        pass

    def get(self, url, params):
        response = requests.get(url=url,
                                params=params)
        return response.json()

    def post(self, url, params, data):
        response = requests.post(url=url,
                                 params=params,
                                 data=json.dumps(data))
        return response.json()

    @staticmethod
    def log_to_database():
        pass
