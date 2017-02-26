from lib.external_api.base_wrapper import BaseClient


class StarLineClient(BaseClient):
    DEFAULT_HOST = 'starline.ru'
    DEV_HOST = 'https://dev-id.{}/:4444'.format(DEFAULT_HOST)

    def __init__(self, data, cookie):
        self.data = data
        self.cookies = None

    def device_sync(self, id, type, command):  # Temporary naming
        data =  {
            'id': id,
            'type': type,
            command['name']: command['value'],
        }
        response = self.post(url=self.DEV_HOST,
                             data=data,
                             cookies=self.cookies)

        return response



