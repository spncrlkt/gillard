import json
from flask import session

import gillard
import test_utils
from utils import eprint

from models import Playlist, Show, Song

class SongRouteTestCase(test_utils.GillardBaseTestCase):

    def test_song_route_not_404(self):
        song_id = 69
        rv = self.app.post('/song/{}'.format(song_id))
        assert rv.status_code != 404

    def test_song_not_exists_message(self):
        song_id = 69
        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'
            rv = app.post('/song/{}'.format(song_id))
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'No song found for id: 69'

    def test_song_route_200(self):
        with gillard.app.app_context():
            song = test_utils.make_song(gillard.db.session)
            song_id = song.id

        artist = 'NEW ARTIST'
        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'
            rv = app.post(
                '/song/{}'.format(song_id),
                data=json.dumps(dict(
                    artist=artist,
                )),
                content_type = 'application/json'
            )
        assert rv.status_code == 200

    def test_song_route_invalid_json(self):
        with gillard.app.app_context():
            song = test_utils.make_song(gillard.db.session)
            song_id = song.id

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'
            rv = app.post(
                '/song/{}'.format(song_id),
                data='invalid_JSON{}',
                content_type = 'application/json'
            )
        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == "Invalid JSON"

    def test_song_route_readonly_mode(self):
        with gillard.app.app_context():
            song = test_utils.make_song(gillard.db.session)
            song_id = song.id

        artist = 'NEW ARTIST'
        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'readonly'
            rv = app.post(
                '/song/{}'.format(song_id),
                data=json.dumps(dict(
                    artist=artist,
                )),
                content_type = 'application/json'
            )

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == "Can't edit songs in readonly mode"

    def test_song_route_changes_record(self):
        with gillard.app.app_context():
            song = test_utils.make_song(gillard.db.session)
            song_id = song.id

        artist = 'NEW ARTIST'
        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'
            rv = app.post(
                '/song/{}'.format(song_id),
                data=json.dumps(dict(
                    artist=artist,
                )),
                content_type = 'application/json'
            )

        with gillard.app.app_context():
            song = gillard.db.session.query(Song).filter_by(id=song_id).one()
            new_artist = song.artist

        assert new_artist == artist

    def test_song_route_invalid_song_attr(self):
        with gillard.app.app_context():
            song = test_utils.make_song(gillard.db.session)
            song_id = song.id

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'
            rv = app.post(
                '/song/{}'.format(song_id),
                data=json.dumps(dict(
                    fartist='fartist',
                )),
                content_type = 'application/json'
            )

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == "Song has no attribute: fartist"
