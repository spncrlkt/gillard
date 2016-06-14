import json
from flask import session

import gillard
import test_utils
from utils import eprint

from models import Playlist, Show

class PlaylistRouteTestCase(test_utils.GillardBaseTestCase):

    def test_playlist_route_exsist(self):
        playlist_display_id = 'FAKEID'
        rv = self.app.get('/playlist/{}'.format(playlist_display_id))
        assert rv.status_code != 404

    def test_playlist_not_exists_message(self):
        playlist_display_id = 'FAKEID'
        rv = self.app.get('/playlist/{}'.format(playlist_display_id))
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'No playlist found for id: FAKEID'

    def test_playlist_exists(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)

        with self.app as app:
            rv = app.get('/playlist/{}'.format(playlist.display_id))
            assert rv.status_code == 200

    def test_playlist_mode_readonly_in_session(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)

        with self.app as app:
            rv = app.get('/playlist/{}'.format(playlist.display_id))
            assert session['playlist_mode'] == 'readonly'

    def test_playlist_mode_edit_exists(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, show_id, password)
            playlist = test_utils.make_playlist(gillard.db.session, show)

        with self.app as app:
            formatted_url = '/playlist/{}?show_id={}&password={}'.\
                format(playlist.display_id, show_id, password)
            rv = app.get(formatted_url)
            assert rv.status_code == 200

    def test_playlist_mode_edit_in_session(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, show_id, password)
            playlist = test_utils.make_playlist(gillard.db.session, show)

        with self.app as app:
            formatted_url = '/playlist/{}?show_id={}&password={}'.\
                format(playlist.display_id, show_id, password)
            rv = app.get(formatted_url)
            assert session['playlist_mode'] == 'edit'

    def test_playlist_mode_edit_associates_to_right_playlist_show_link(self):
        bad_show_id = 'BADID'
        bad_password = 'BADPW'

        show_id = 'TESTID'
        password = 'TESTPW'

        with gillard.app.app_context():
            bad_show = test_utils.make_show(gillard.db.session, bad_show_id, bad_password)
            show = test_utils.make_show(gillard.db.session, show_id, password)
            playlist = test_utils.make_playlist(gillard.db.session, show)

        with self.app as app:
            formatted_url = '/playlist/{}?show_id={}&password={}'.\
                format(playlist.display_id, bad_show_id, bad_password)
            rv = app.get(formatted_url)
            assert session['playlist_mode'] == 'readonly'

    def test_playlist_json_has_song(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)
            playlist_display_id = playlist.display_id
            test_utils.make_song(gillard.db.session, playlist)

        with self.app as app:
            rv = app.get('/playlist/{}'.format(playlist_display_id))
            res_json = json.loads(rv.data.decode("utf-8"))
            assert len(res_json['songs']) == 1

    def test_playlist_json_has_songs(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)
            playlist_display_id = playlist.display_id
            test_utils.make_song(gillard.db.session, playlist)
            test_utils.make_song(gillard.db.session, playlist)

        with self.app as app:
            rv = app.get('/playlist/{}'.format(playlist_display_id))
            res_json = json.loads(rv.data.decode("utf-8"))
            assert len(res_json['songs']) == 2

    def test_playlist_json_has_display_id(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)

        with self.app as app:
            rv = app.get('/playlist/{}'.format(playlist.display_id))
            res_json = json.loads(rv.data.decode("utf-8"))
            assert res_json['display_id'] == playlist.display_id
