import json
import logging

import requests


class BaseClient:

    def __init__(self):
        pass

    def get(self, url, params=None):
        response = requests.get(url=url,
                                params=params)
        return response.json()

    def post(self, url, data, params=None):
        response = requests.post(url=url,
                                 params=params,
                                 data=json.dumps(data))
        logging.debug(params)
        logging.debug(data)
        logging.debug(response.json())
        return response.json()

    @staticmethod
    def log_to_database():
        pass
