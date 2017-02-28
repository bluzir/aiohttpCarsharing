from lib.external_api.base_wrapper import BaseClient


class StarLineClient(BaseClient):
    DEFAULT_HOST = 'starline.ru'
    DEV_HOST = 'https://dev-id.{}/:4444'.format(DEFAULT_HOST)

    def __init__(self):
        super(StarLineClient, self).__init__()
        self.slid = None
        self.url = self.DEV_HOST

    async def authorize(self):  # Placeholder for authorization method
        self.cookies = ''
        return True

    async def get_device_state(self):  # Get current state of device sensors
        method_url = '/json/v1/device/{}/state'.format(self.slid)
        self.url = '{}{}'.format(self.DEV_HOST, method_url)
        response = await self.get()
        return response

    async def device_sync(self, command, value):  # Temporary naming
        method_url = '/json/v1/device/{}/set_param'.format(self.slid)
        self.url = '{}{}'.format(self.DEV_HOST, method_url)
        self.data = {
            'id': self.slid,
            'type': command,
            command: value,
        }
        response = await self.post()
        return response

    



