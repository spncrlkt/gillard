import json

import gillard
import test_utils

class GillardTestCase(test_utils.GillardBaseTestCase):

    def test_index_exists(self):
        rv = self.app.get('/')
        assert rv.status_code == 200
        assert b'index' in rv.data

    def test_health(self):
        rv = self.app.get('/health')
        assert rv.status_code == 200
        assert b'OK' in rv.data

    def test_new_playlist_exists(self):
        rv = self.app.get('/playlist/new/TESTID')
        assert rv.status_code == 200

    def test_new_playlist_returns_disp_pw(self):
        rv = self.app.get('/playlist/new/TESTID')
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['display_id'] is not None
        assert res_json['password'] is not None
