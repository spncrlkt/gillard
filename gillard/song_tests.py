import datetime

import test_utils
import gillard

from models import Song

class SongTestCase(test_utils.GillardBaseTestCase):

    def test_mk_new_song(self):
        with gillard.app.app_context():
            song = Song()
            gillard.db.session.add(song)
            gillard.db.session.commit()
            assert song.id is not None

