from lib.external_api.inplat_wrapper import InplatClient
from utils.utils import *
import unittest



class TestSmoke(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSmoke, self).__init__(*args, **kwargs)
        self.inplat_client = InplatClient()

    def test_init(self):
        account = generate_uuid()
        print(self.inplat_client.init(
            params={'account': account},
            pay_params={'cryptogramma':'yqzMckvNzouPYboEEBt2CHBiOHDpNVg/BYTkVYxKv643uxC9HtwdOYkaJVed/lTcLtOJbdZ+q5TBC7pNHJ0fyq45VODuXPCOa3hFgmxE+7U='}))


if __name__ == '__main__':
    unittest.main()
