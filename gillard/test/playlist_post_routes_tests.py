import json
from flask import session

import gillard
import test_utils
from utils import eprint

from models import Playlist, Show

class PlaylistPostRoutesTestCase(test_utils.GillardBaseTestCase):

    def test_playlist_add_song_exists(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)

        with self.app as app:
            rv = app.post('/playlist/{}/add_song'.format(playlist.display_id))
            assert rv.status_code != 404
