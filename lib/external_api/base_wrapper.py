import requests


class BaseClient:
    def __init__(self):
        pass

    def get(self, url, params):
        response = requests.get(url=url,
                                params=params)
        return response

    def post(self, url, params, data):
        response = requests.post(url=url,
                                 params=params,
                                 data=data)
        return response

