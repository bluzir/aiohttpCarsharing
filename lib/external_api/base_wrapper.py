import json
import logging

import aiohttp
import requests

from model.external_request import ExternalRequest


class BaseClient:

    def __init__(self):
        self.external_system = 0
        self.data = {}
        self.params = {}
        self.cookies = None
        self.url = None
        self.response = None
        self.decoded = None
        self.text = None

    @staticmethod
    async def _decode(resp):
        try:
            logging.debug(await resp.text())
            logging.debug(resp.headers)
            logging.debug(resp.status)
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
                self.response = resp
                self.text = await resp.text()
                self.decoded = await self._decode(resp)

        logging.debug(self.params)
        logging.debug(self.data)
        logging.debug(self.decoded)

        log = self.log_to_database()

        return self.decoded

    def log_to_database(self):
        ExternalRequest.create(request_url=self.url, external_system=self.external_system,
                               response_headers=self.response.raw_headers, response_body=self.text)



