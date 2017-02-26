import json
import logging

import aiohttp
import requests


class BaseClient:

    def __init__(self):
        pass

    async def get(self, url, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                decoded = await resp.json()

        logging.debug(params)
        logging.debug(decoded)
        return decoded

    async def post(self, url, data, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, params=params) as resp:
                decoded = await resp.json()

        logging.debug(params)
        logging.debug(data)
        logging.debug(decoded)

        return decoded

    @staticmethod
    def log_to_database():
        pass
