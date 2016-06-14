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
            song = Song(
                artist = 'artist',
                title = 'title',
                album = 'album',
                label = 'label',
                release_date = 'release_date',
                notes = 'notes',
                img64px = 'img64px',
                img300px = 'img300px',
                played = True,
            )

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

    def test_new_song_has_created_at(self):
        with gillard.app.app_context():
            song = Song()

            song = test_utils.save_and_refresh(
                gillard.db.session, song
            )

            assert \
                (datetime.datetime.now() - song.created_at).\
                total_seconds() < 2

    def test_new_song_has_updated_at(self):
        with gillard.app.app_context():
            song = Song()

            song = test_utils.save_and_refresh(
                gillard.db.session, song
            )

            # updated_at starts empty
            assert song.updated_at is None

            song.artist = 'fake_ass_bullshit'

            song = test_utils.save_and_refresh(
                gillard.db.session, song
            )

            # on update, updated_at gets set to now-ish
            assert (datetime.datetime.now() - song.updated_at).\
                total_seconds() < 2

    def test_new_song_has_played_at(self):
        with gillard.app.app_context():
            song = Song()

            song = test_utils.save_and_refresh(
                gillard.db.session, song
            )

            # played_at starts empty
            assert song.played_at is None

            song.artist = 'fake_ass_bullshit'

            song = test_utils.save_and_refresh(
                gillard.db.session, song
            )

            # played_at doesn't update unless 'played' changes
            assert song.played_at is None

            song.played = True

            song = test_utils.save_and_refresh(
                gillard.db.session, song
            )

            # on update played field, played_at gets set to now-ish
            assert (datetime.datetime.now() - song.played_at).\
                total_seconds() < 2
