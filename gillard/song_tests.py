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

    def test_song_attrs(self):
        with gillard.app.app_context():
            song = Song()

            song.artist = 'artist'
            song.title = 'title'
            song.album = 'album'
            song.label = 'label'
            song.release_date = 'release_date'
            song.notes = 'notes'
            song.img64px = 'img64px'
            song.img300px = 'img300px'
            song.played = True

            gillard.db.session.add(song)
            gillard.db.session.commit()

            song = test_utils.save_and_refresh(gillard.db.session, song)

            assert song.artist == 'artist'
            assert song.title == 'title'
            assert song.album == 'album'
            assert song.label == 'label'
            assert song.release_date == 'release_date'
            assert song.notes == 'notes'
            assert song.img64px == 'img64px'
            assert song.img300px == 'img300px'
            assert song.played is True

