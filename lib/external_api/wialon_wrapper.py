import requests


class WialonException(Exception):
    """
    Exception raised when an Wialon Remote API call fails due to a network
    related error or for a Wialon specific reason.
    """

    # Errors codes
    errors = {
        1: 'Invalid session',
        2: 'Invalid service',
        3: 'Invalid result',
        4: 'Invalid input',
        5: 'Error performing request',
        6: 'Unknow error',
        7: 'Access denied',
        8: 'Invalid user name or password',
        9: 'Authorization server is unavailable, please try again later',
        1001: 'No message for selected interval',
        1002: 'Item with such unique property already exists',
        1003: 'Only one request of given time is allowed at the moment'
    }

    def __init__(self, code):
        self.code = code

        try:
            self.text = self.errors[code]
        except Exception as e:
            self.text = 'Unexpected error'


class WialonClient:
    # Token settings
    TOKEN = '2fe8024e0ab91aa6c8ed82717b71bddcECDC362358DF7D90986F5173D405CD0D42DE7B38'

    # Default host settings
    DEFAULT_HOST = 'https://hst-api.wialon.com/{}'
    API_URL_POSTFIX = 'wialon/ajax.html'

    def __init__(self, token=None):
        self.token = self.TOKEN
        self.authenticated = False

        if not token:
            raise Exception

    def login(self):
        login_params = {"token": self.token}

        return self.request(
            method='token/login',
            params=login_params,)

    def get_profile_info(self, detail=False):
        profile_params = {"type": 1 if not detail else 2}

        return self.request(
            method='core/get_account_data',
            params=profile_params,
        )

    def get_fuel_consumption(self, unit_id):
        fuel_params = {"itemId": unit_id}

        return self.request(
            method='unit/get_fuel_settings',
            params=fuel_params,
        )

    def get_sensors_values_by_id(self, unit_id):
        unit_params = {
            'source': '',
            'indexFrom': '',
            'indexTo': '',
            'unitId': unit_id,
            'sensorId': '',
            'width': ''
        }

        return self.request(
            method='unit/calc_sensors',
            params=unit_params,
        )

    def request(self, method, params, **kwargs):
        url = self.DEFAULT_HOST.format(self.API_URL_POSTFIX)
        par = {
            'svc': method,
            'params': params
        }

        response = requests.get(
            url=url,
            params=par,
        )

        decoded = response.json()

        if 'error' not in decoded:
            return decoded
        else:
            raise WialonException(code=decoded['error'])


class Command(WialonClient):
    def __init__(self, id, name):
        super(Command, self).__init__()
        self.id = id
        self.name = name
        self.link_type = ''
        self.param = {}
        self.timeout = 0

    def modify(self, callmode, command_type=None):
        modify_params = {
            'itemId': '',
            'id': self.id,
            'callMode': callmode,
            'n': self.name,
            'c': command_type,
            'l': self.link_type,
            'p': '',
            'a': '',
        }

        return self.request(
            method='unit/update_command_definition',
            params=modify_params,
        )

    def execute(self):
        execute_params = {
            'itemId': self.id,
            'commandName': self.name,
            'linkType': self.link_type,
            'param': self.param,
            'timeout': self.timeout
        }

        return self.request(
            method='unit/exec_cmd',
            params=execute_params,
        )


client = WialonClient()

if client.login():
    print('Login successful')
    client.authenticated = True