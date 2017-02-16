import requests
import unittest

WEB_ROOT = 'https://stage.2car.spb.ru/'

class TestSmoke(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSmoke, self).__init__(*args, **kwargs)
        self.s = requests.session()

    def _make_get_request(self, url):
        return self.s.get(WEB_ROOT + url, verify=False)  # TODO: fix cert

    def _make_post_request(self, url, data):
        return self.s.post(WEB_ROOT + url, data, verify=False)  # TODO: fix cert

    def _index(self):
        r = self._make_get_request('')
        self.assertAlmostEqual(r.status_code, 200)

    def _login(self):
        r = self._make_post_request('login/', {'email': 'bluzir@bluzir.me', 'password':'qweqwe'})
        self.assertAlmostEqual(r.status_code, 200)

    def _profile(self):
        r = self._make_get_request('profile/')
        # TODO: проверить существование на странице инфы о пользователе
        self.assertAlmostEqual(r.status_code, 200)

    def _logout(self):
        r = self._make_get_request('logout/')
        self.assertAlmostEqual(r.status_code, 200)

    def test_main(self):
        self._index()
        self._login()
        self._profile()
        self._logout()
