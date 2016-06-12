import json

import gillard
import test_utils

from models import Playlist

class GillardTestCase(test_utils.GillardBaseTestCase):

    def test_invalid_req(self):
        rv = self.app.get('/bad_url_dont_exist')
        assert rv.status_code == 404

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

    def test_new_playlist_exists(self):
        show_id = 'TESTID'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id)
        rv = self.app.get('/playlist/new/{}'.format(show_id))
        assert rv.status_code == 200

    def _test_new_playlist_returns_disp_pw(self):
        rv = self.app.get('/playlist/new/TESTID')
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['display_id'] is not None
        assert res_json['password'] is not None

    def _test_new_playlist_mks_db_record(self):
        rv = self.app.get('/playlist/new/TESTID')
        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
        assert playlist.display_id is not None
        assert playlist.password is not None

    def _test_new_playlist_returns_db_record_vals(self):
        rv = self.app.get('/playlist/new/TESTID')
        res_json = json.loads(rv.data.decode("utf-8"))
        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
        assert playlist.display_id == res_json['display_id']
        assert playlist.password == res_json['password']

    def test_new_playlist_404s_on_no_show_id(self):
        rv = self.app.get('/playlist/new/')
        assert rv.status_code == 404

    def test_new_playlist_errors_on_no_show_found(self):
        rv = self.app.get('/playlist/new/FAKEID')
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'No show found for id: FAKEID'
