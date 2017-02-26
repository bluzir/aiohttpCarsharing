from lib.external_api.inplat_wrapper import InplatClient
from utils.utils import *
import unittest



class TestInplat(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInplat, self).__init__(*args, **kwargs)
        self.inplat_client = InplatClient()

    def test_init(self):
        account = generate_uuid()
        print(self.inplat_client.init(
            params={
                'account': account,
                'sum': 123
            },
            pay_params={'cryptogramma':'0dUZK7Iy0I4S9xggWJXH9Y+QUGUn/6cARcnH4B8jZUhDD/A9dyKq9PlBKhyjDHVDWdWYtNSZuDNa4YTLFzt+5O7xzh5dyGP9eZitzws8/ag='}))


if __name__ == '__main__':
    unittest.main()
