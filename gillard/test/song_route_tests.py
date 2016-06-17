import json
from flask import session

import gillard
import test_utils
from utils import eprint

from models import Playlist, Show

class SongRouteTestCase(test_utils.GillardBaseTestCase):

    def test_song_route_exists(self):
        song_id = 69
        rv = self.app.post('/song/{}'.format(song_id))
        assert rv.status_code != 404

    def test_song_not_exists_message(self):
        song_id = 69
        rv = self.app.post('/song/{}'.format(song_id))
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'No song found for id: 69'

