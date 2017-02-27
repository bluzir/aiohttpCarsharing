from lib.external_api.base_wrapper import BaseClient


class StarLineClient(BaseClient):
    DEFAULT_HOST = 'starline.ru'
    DEV_HOST = 'https://dev-id.{}/:4444'.format(DEFAULT_HOST)

    def __init__(self):
        self.slid = None
        self.url = self.DEV_HOST
        super(StarLineClient, self).__init__()

    async def device_sync(self, command, value):  # Temporary naming
        self.data = {
            'id': self.slid,
            'type': command,
            command: value,
        }
        response = await self.post()
        return response

    async def ign_start(self):  # Method that starts the car engine
        response = await self.device_sync(command="ign_start", value=1)
        return response

    async def ign_stop(self):  # Method that stops the car engine
        response = await self.device_sync(command="ign_stop", value=1)
        return response

    



