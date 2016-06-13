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

    def _test_playlist_throws_400(self):
        playlist_display_id = 'FAKEID'
        rv = self.app.get('/playlist/{}'.format(playlist_display_id))
        eprint(rv.status_code)
        assert rv.status_code == 400

        """
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            test_utils.make_show(gillard.db.session, show_id, password)
        rv = self.app.get('/playlist/new?show_id={}&password={}'.format(show_id, password))
        assert rv.status_code == 200
        """
