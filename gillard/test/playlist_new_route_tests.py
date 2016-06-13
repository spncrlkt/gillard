import json

import gillard
import test_utils
from utils import eprint

from models import Playlist, Show

class PlaylistNewRouteTestCase(test_utils.GillardBaseTestCase):

    def test_new_playlist_exists_with_show(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id, password)
        rv = self.app.get('/playlist/new?show_id={}&password={}'.format(show_id, password))
        assert rv.status_code == 200

    def test_new_playlist_returns_disp(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id, password)
        rv = self.app.get('/playlist/new?show_id={}&password={}'.format(show_id, password))
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['display_id'] is not None

    def test_new_playlist_mks_db_record(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id, password)
        rv = self.app.get('/playlist/new?show_id={}&password={}'.format(show_id, password))
        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
        assert playlist.display_id is not None

    def test_new_playlist_returns_db_record_vals(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id, password)
        rv = self.app.get('/playlist/new?show_id={}&password={}'.format(show_id, password))
        res_json = json.loads(rv.data.decode("utf-8"))
        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
        assert playlist.display_id == res_json['display_id']

    def test_new_playlist_associates_to_show(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id, password)
        rv = self.app.get('/playlist/new?show_id={}&password={}'.format(show_id, password))
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
        password = 'TESTPW'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id, password)
        rv = self.app.get('/playlist/new?show_id={}&password={}'.format(show_id, password))
        res_json = json.loads(rv.data.decode("utf-8"))

        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
            show = gillard.db.session.query(Show).filter_by(id=1).one()
            show_playlists = show.playlists

        assert len(show_playlists) == 1

        first_show_playlist = show_playlists[0]

        assert playlist.id == first_show_playlist.id

        rv = self.app.get('/playlist/new?show_id={}&password={}'.format(show_id, password))
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
        rv = self.app.get('/playlist/new?show_id={}&password={}'.format('FAKEID', 'FAKEPW'))
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'No show found for id: FAKEID'

    def test_new_playlist_errors_on_bad_pw(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id, password)
        rv = self.app.get('/playlist/new?show_id={}&password={}'.format(show_id, 'FAKEPW'))
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json.get('message') == 'No show found for id: TESTID'
