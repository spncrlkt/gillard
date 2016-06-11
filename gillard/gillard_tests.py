import gillard
import test_utils

class GillardTestCase(test_utils.GillardBaseTestCase):

    def test_index(self):
        rv = self.app.get('/')
        assert rv.status_code == 200
        assert b'index' in rv.data

    def test_health(self):
        rv = self.app.get('/health')
        assert rv.status_code == 200
        assert b'OK' in rv.data

    def test_new_playlist(self):
        rv = self.app.get('/playlist/new/TESTID')
        assert rv.status_code == 200
