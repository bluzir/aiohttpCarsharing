import json
import logging

import aiohttp
import requests


class BaseClient:

    def __init__(self):
        pass

    async def get(self, url, cookies=None, params=None):
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(url, params=params) as resp:
                decoded = await resp.json()

        logging.debug(params)
        logging.debug(decoded)
        return decoded

    async def post(self, url, cookies=None, data=None, params=None):
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.post(url, data=data, params=params) as resp:
                decoded = await resp.json()

        logging.debug(params)
        logging.debug(data)
        logging.debug(decoded)

        return decoded

    @staticmethod
    def log_to_database():
        pass
