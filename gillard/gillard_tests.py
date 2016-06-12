import json

import gillard
import test_utils

from models import Playlist

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

    def test_new_playlist_mks_db_record(self):
        rv = self.app.get('/playlist/new/TESTID')
        res_json = json.loads(rv.data.decode("utf-8"))
        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
        assert playlist.display_id is not None
        assert playlist.password is not None
