import json

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
        rv = self.app.get('/playlist/{}'.format(playlist.display_id))
        assert rv.status_code == 200

        """
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id, password)
        rv = self.app.get('/playlist/new?show_id={}&password={}'.format(show_id, password))
        assert rv.status_code == 200
        """
