import json
from flask import session

import gillard
import test_utils
from utils import eprint

from models import Playlist, Show

class PlaylistDeleteSongRouteTestCase(test_utils.GillardBaseTestCase):

    def test_playlist_delete_song_route_exists(self):
        playlist_display_id = 'FAKEID'
        rv = self.app.post('/playlist/{}/delete_song'.format(playlist_display_id))
        assert rv.status_code != 404

    def test_playlist_not_exists_message(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)
            playlist_display_id = playlist.display_id
            song = test_utils.make_song(gillard.db.session, playlist)
            song_id = song.id

        playlist_display_id = 'FAKEID'

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post(
                '/playlist/{}/delete_song'.format(playlist_display_id),
                data=json.dumps(dict(
                    song_id= song_id,
                )),
                content_type = 'application/json'
            )

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'No playlist found for id: FAKEID'

    def test_playlist_delete_song_response(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)
            playlist_display_id = playlist.display_id
            song = test_utils.make_song(gillard.db.session, playlist)
            song_id = song.id

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post(
                '/playlist/{}/delete_song'.format(playlist_display_id),
                data=json.dumps(dict(
                    song_id= song_id,
                )),
                content_type = 'application/json'
            )

        assert rv.status_code == 200

    def test_playlist_delete_song_readonly_mode(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)
            playlist_display_id = playlist.display_id
            song = test_utils.make_song(gillard.db.session, playlist)
            song_id = song.id

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'readonly'

            rv = app.post(
                '/playlist/{}/delete_song'.format(playlist_display_id),
                data=json.dumps(dict(
                    song_id= song_id,
                )),
                content_type = 'application/json'
            )

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == "Can't delete songs in readonly mode"

    def test_playlist_delete_invalid_json(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)
            playlist_display_id = playlist.display_id
            song = test_utils.make_song(gillard.db.session, playlist)
            song_id = song.id

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post(
                '/playlist/{}/delete_song'.format(playlist_display_id),
                data='invalid_json{}',
                content_type = 'application/json'
            )

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == "Invalid JSON"

    def test_playlist_delete_non_existent_song(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)
            playlist_display_id = playlist.display_id
            song = test_utils.make_song(gillard.db.session, playlist)
            song_id = song.id + 1

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post(
                '/playlist/{}/delete_song'.format(playlist_display_id),
                data=json.dumps(dict(
                    song_id= song_id,
                )),
                content_type = 'application/json'
            )

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == "No song found for id: {}".format(song_id)

    def test_playlist_delete_song_is_assoc_w_playlist(self):
        with gillard.app.app_context():
            show = test_utils.make_show(gillard.db.session, 'FAKEFAKESHOWID', 'FAKEFAKEPW')
            playlist = test_utils.make_playlist(gillard.db.session, show)
            playlist_display_id = playlist.display_id

            other_playlist = test_utils.make_playlist(gillard.db.session)
            other_playlist_display_id = other_playlist.display_id
            song = test_utils.make_song(gillard.db.session, other_playlist)
            song_id = song.id

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post(
                '/playlist/{}/delete_song'.format(playlist_display_id),
                data=json.dumps(dict(
                    song_id= song_id,
                )),
                content_type = 'application/json'
            )

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == \
            "Song id {} not in playlist id {}".format(song_id, playlist_display_id)

    def test_playlist_delete_song(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)
            playlist_display_id = playlist.display_id
            song = test_utils.make_song(gillard.db.session, playlist)
            song_id = song.id

        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
            songs = playlist.songs
            assert len(songs) == 1

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post(
                '/playlist/{}/delete_song'.format(playlist_display_id),
                data=json.dumps(dict(
                    song_id= song_id,
                )),
                content_type = 'application/json'
            )

        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
            songs = playlist.songs
            assert len(songs) == 0

    def test_playlist_delete_song_2X(self):
        with gillard.app.app_context():
            playlist = test_utils.make_playlist(gillard.db.session)
            playlist_display_id = playlist.display_id
            song_1 = test_utils.make_song(gillard.db.session, playlist)
            song_1_id = song_1.id
            song_2 = test_utils.make_song(gillard.db.session, playlist)
            song_2_id = song_2.id

        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
            songs = playlist.songs
            assert len(songs) == 2

        with self.app as app:
            with app.session_transaction() as sess:
                sess['playlist_mode'] = 'edit'

            rv = app.post(
                '/playlist/{}/delete_song'.format(playlist_display_id),
                data=json.dumps(dict(
                    song_id= song_1_id,
                )),
                content_type = 'application/json'
            )

            rv = app.post(
                '/playlist/{}/delete_song'.format(playlist_display_id),
                data=json.dumps(dict(
                    song_id= song_2_id,
                )),
                content_type = 'application/json'
            )

        with gillard.app.app_context():
            playlist = gillard.db.session.query(Playlist).filter_by(id=1).one()
            songs = playlist.songs
            assert len(songs) == 0
