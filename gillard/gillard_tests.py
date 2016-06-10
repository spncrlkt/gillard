import gillard
import test_utils

class GillardTestCase(test_utils.GillardBaseTestCase):

    def test_index(self):
        rv = self.app.get('/')
        assert b'index' in rv.data

    def test_health(self):
        rv = self.app.get('/health')
        assert b'OK' in rv.data
