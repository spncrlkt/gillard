import json
from flask import session

import gillard
import test_utils
from utils import eprint

from models import Playlist, Show

class PlaylistsByShowIDTestCase(test_utils.GillardBaseTestCase):

    def test_playlists_route_exists(self):
        show_display_id = 'FAKEID'
        rv = self.app.get('/playlists/{}'.format(show_display_id))
        assert rv.status_code != 404

    def test_show_not_exists_message(self):
        show_display_id = 'FAKEID'
        rv = self.app.get('/playlists/{}'.format(show_display_id))
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'No show found for id: FAKEID'

    def test_200(self):
        show_display_id = 'TESTID'
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, show_display_id)
            playlist = test_utils.make_playlist(gillard.db.session, show)
        rv = self.app.get('/playlists/{}'.format(show_display_id))
        assert rv.status_code == 200

    def test_has_show(self):
        show_display_id = 'TESTID'
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, show_display_id)
            playlist = test_utils.make_playlist(gillard.db.session, show)
        rv = self.app.get('/playlists/{}'.format(show_display_id))
        res_json = json.loads(rv.data.decode("utf-8"))
        assert len(res_json['playlists']) == 1

    def test_has_shows(self):
        show_display_id = 'TESTID'
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, show_display_id)
            playlist_1 = test_utils.make_playlist_no_expunge(gillard.db.session, show)
            playlist_2 = test_utils.make_playlist_no_expunge(gillard.db.session, show)
        rv = self.app.get('/playlists/{}'.format(show_display_id))
        res_json = json.loads(rv.data.decode("utf-8"))
        assert len(res_json['playlists']) == 2

    def test_has_correct_show(self):
        show_display_id = 'TESTID'
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, show_display_id)
            playlist = test_utils.make_playlist(gillard.db.session, show)
            playlist_disp_id = playlist.display_id

        rv = self.app.get('/playlists/{}'.format(show_display_id))
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['playlists'][0] == playlist_disp_id

