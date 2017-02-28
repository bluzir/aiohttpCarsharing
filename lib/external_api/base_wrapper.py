import json
import logging

import aiohttp
import requests


class BaseClient:

    def __init__(self):
        self.data = {}
        self.params = {}
        self.cookies = None
        self.url = None

    @staticmethod
    async def _decode(resp):
        try:
            logging.debug(await resp.text())
            logging.debug(resp.headers)
            decoded = await resp.json()
            return decoded
        except Exception as e:
           pass


    async def get(self):
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.get(self.url, params=self.params) as resp:
                decoded = await self._decode(resp)


        logging.debug(self.params)
        logging.debug(decoded)
        return decoded

    async def post(self):
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.post(self.url, data=json.dumps(self.data).encode("utf-8"),
                                    params=self.params) as resp:
                decoded = await self._decode(resp)

        logging.debug(self.params)
        logging.debug(self.data)
        logging.debug(decoded)
        return decoded

    @staticmethod
    def log_to_database():
        pass
