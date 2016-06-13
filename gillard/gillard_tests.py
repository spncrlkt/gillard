import json

import gillard
import test_utils

from models import Playlist, Show

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

    def test_new_playlist_returns_disp_pw(self):
        show_id = 'TESTID'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id)
        rv = self.app.get('/playlist/new/{}'.format(show_id))
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['display_id'] is not None

    def test_new_playlist_mks_db_record(self):
        show_id = 'TESTID'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id)
        rv = self.app.get('/playlist/new/{}'.format(show_id))
        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
        assert playlist.display_id is not None

    def test_new_playlist_returns_db_record_vals(self):
        show_id = 'TESTID'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id)
        rv = self.app.get('/playlist/new/{}'.format(show_id))
        res_json = json.loads(rv.data.decode("utf-8"))
        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
        assert playlist.display_id == res_json['display_id']

    def test_new_playlist_associates_to_show(self):
        show_id = 'TESTID'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id)
        rv = self.app.get('/playlist/new/{}'.format(show_id))
        res_json = json.loads(rv.data.decode("utf-8"))

        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
            show = gillard.db.session.query(Show).filter_by(id=1).one()
            show_playlists = show.playlists

        assert len(show_playlists) == 1

        show_playlist = show_playlists[0]

        assert playlist.id == show_playlist.id

    def test_new_playlist_associates_to_show_2X(self):
        show_id = 'TESTID'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id)
        rv = self.app.get('/playlist/new/{}'.format(show_id))
        res_json = json.loads(rv.data.decode("utf-8"))

        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
            show = gillard.db.session.query(Show).filter_by(id=1).one()
            show_playlists = show.playlists

        assert len(show_playlists) == 1

        first_show_playlist = show_playlists[0]

        assert playlist.id == first_show_playlist.id

        rv = self.app.get('/playlist/new/{}'.format(show_id))
        res_json = json.loads(rv.data.decode("utf-8"))

        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=2).one()
            show = gillard.db.session.query(Show).filter_by(id=1).one()
            show_playlists = show.playlists

        assert len(show_playlists) == 2

        second_show_playlist = show_playlists[1]

        assert playlist.id == second_show_playlist.id
        assert first_show_playlist.id != second_show_playlist.id

    def test_new_playlist_404s_on_no_show_id(self):
        rv = self.app.get('/playlist/new/')
        assert rv.status_code == 404

    def test_new_playlist_errors_on_no_show_found(self):
        rv = self.app.get('/playlist/new/FAKEID')
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'No show found for id: FAKEID'
