import json
from flask import session

import gillard
import test_utils
from utils import eprint

from models import Playlist, Show

class PlaylistPostRoutesTestCase(test_utils.GillardBaseTestCase):

    def test_playlist_add_song_route_exists(self):
        playlist_display_id = 'FAKEID'
        rv = self.app.post('/playlist/{}/add_song'.format(playlist_display_id))
        assert rv.status_code != 404

    def test_playlist_not_exists_message(self):
        playlist_display_id = 'FAKEID'
        rv = self.app.post('/playlist/{}/add_song'.format(playlist_display_id))
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'No playlist found for id: FAKEID'
