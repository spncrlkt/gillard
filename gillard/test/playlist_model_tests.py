import datetime

import test_utils
import gillard
from models import Playlist, Song

class PlaylistTestCase(test_utils.GillardBaseTestCase):

    def test_mk_new_playlist(self):
        with gillard.app.app_context():
            playlist = Playlist()

            playlist = test_utils.save_and_refresh(
                gillard.db.session, playlist
            )

            assert playlist.id is not None

    def test_new_playlist_has_display_id(self):
        with gillard.app.app_context():
            playlist = Playlist()

            playlist = test_utils.save_and_refresh(
                gillard.db.session, playlist
            )

            assert playlist.display_id is not None

    def test_new_playlist_has_created_at(self):
        with gillard.app.app_context():
            playlist = Playlist()

            playlist = test_utils.save_and_refresh(
                gillard.db.session, playlist
            )

            assert \
                (datetime.datetime.now() - playlist.created_at).\
                total_seconds() < 2

    def test_playlist_updated_at(self):
        with gillard.app.app_context():
            playlist = Playlist()

            playlist = test_utils.save_and_refresh(
                gillard.db.session, playlist
            )

            # updated_at starts empty
            assert playlist.updated_at is None

            playlist.display_id = 'NEWTESTDISPID'

            playlist = test_utils.save_and_refresh(
                gillard.db.session, playlist
            )

            # on update, updated_at gets set to now-ish
            assert (datetime.datetime.now() - playlist.updated_at).\
                total_seconds() < 2

    def test_new_playlist_has_no_songs(self):
        with gillard.app.app_context():
            playlist = Playlist()

            playlist = test_utils.save_and_refresh(gillard.db.session, playlist)

            assert len(playlist.songs) == 0

    def test_add_song_to_playlist(self):
        with gillard.app.app_context():
            song = Song()
            playlist = Playlist()

            playlist.songs = [song]

            playlist = test_utils.save_and_refresh(gillard.db.session, playlist)

            assert len(playlist.songs) == 1

            # cascading add
            assert playlist.songs[0].id is not None
