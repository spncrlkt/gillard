import json
from flask import session

import gillard
import test_utils
from utils import eprint

from models import Playlist, Show

class PlaylistAddSongRouteTestCase(test_utils.GillardBaseTestCase):

    def test_playlist_add_song_route_exists(self):
        playlist_display_id = 'FAKEID'
        rv = self.app.post('/playlist/{}/add_song'.format(playlist_display_id))
        assert rv.status_code != 404

    def test_playlist_not_exists_message(self):
        playlist_display_id = 'FAKEID'
        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post('/playlist/{}/add_song'.format(playlist_display_id))

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'No playlist found for id: FAKEID'

    def test_playlist_add_song_response(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, show_id, password)
            playlist = test_utils.make_playlist(gillard.db.session, show)

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post('/playlist/{}/add_song'.format(playlist.display_id), data=json.dumps(dict(
                artist = 'artist',
                title = 'title',
                album = 'album',
                label = 'label',
                release_date = 'release_date',
                notes = 'notes',
                img64px = 'img64px',
                img300px = 'img300px',
                played = True,
            )), content_type = 'application/json')

        assert rv.status_code == 200

    def test_playlist_add_song_invalid_json(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, show_id, password)
            playlist = test_utils.make_playlist(gillard.db.session, show)

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post(
                '/playlist/{}/add_song'.format(playlist.display_id),
                data='not json{}',
                content_type = 'application/json'
            )

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'Invalid JSON'

    def test_playlist_add_song_readonly_mode(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, show_id, password)
            playlist = test_utils.make_playlist(gillard.db.session, show)

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'readonly'

            rv = app.post(
                '/playlist/{}/add_song'.format(playlist.display_id),
                data='not json{}',
                content_type = 'application/json'
            )

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == "Can't add songs in readonly mode"

    def test_playlist_add_song(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, show_id, password)
            playlist = test_utils.make_playlist(gillard.db.session, show)

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post(
                '/playlist/{}/add_song'.format(playlist.display_id),
                data=json.dumps(dict(
                    artist = 'artist',
                    title = 'title',
                    album = 'album',
                    label = 'label',
                    release_date = 'release_date',
                    notes = 'notes',
                    img64px = 'img64px',
                    img300px = 'img300px',
                    played = True,
                )),
                content_type = 'application/json'
            )

        with gillard.app.app_context():
            show = gillard.db.session.query(Show).filter_by(id=1).one()
            songs = show.playlists[0].songs
            assert len(songs) == 1

    def test_playlist_add_song_2X(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, show_id, password)
            playlist = test_utils.make_playlist(gillard.db.session, show)

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post('/playlist/{}/add_song'.format(playlist.display_id), data=json.dumps(dict(
                artist = 'artist',
                title = 'title',
                album = 'album',
                label = 'label',
                release_date = 'release_date',
                notes = 'notes',
                img64px = 'img64px',
                img300px = 'img300px',
                played = True,
            )), content_type = 'application/json')

            rv = app.post('/playlist/{}/add_song'.format(playlist.display_id), data=json.dumps(dict(
                artist = 'artist',
                title = 'title',
                album = 'album',
                label = 'label',
                release_date = 'release_date',
                notes = 'notes',
                img64px = 'img64px',
                img300px = 'img300px',
                played = True,
            )), content_type = 'application/json')

        with gillard.app.app_context():
            show = gillard.db.session.query(Show).filter_by(id=1).one()
            songs = show.playlists[0].songs
            assert len(songs) == 2

    def test_playlist_add_song_has_correct_attrs(self):
        show_id = 'TESTID'
        password = 'TESTPW'
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, show_id, password)
            playlist = test_utils.make_playlist(gillard.db.session, show)

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post('/playlist/{}/add_song'.format(playlist.display_id), data=json.dumps(dict(
                artist = 'artist',
                title = 'title',
                album = 'album',
                label = 'label',
                release_date = 'release_date',
                notes = 'notes',
                img64px = 'img64px',
                img300px = 'img300px',
                played = True,
            )), content_type = 'application/json')

        with gillard.app.app_context():
            show = gillard.db.session.query(Show).filter_by(id=1).one()
            song = show.playlists[0].songs[0]
            assert song.artist == 'artist'
            assert song.title == 'title'
            assert song.album == 'album'
            assert song.label == 'label'
            assert song.release_date == 'release_date'
            assert song.notes == 'notes'
            assert song.img64px == 'img64px'
            assert song.img300px == 'img300px'
            assert song.played == True
