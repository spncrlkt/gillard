import unittest

import gillard
from models import Show, Playlist, Song

def save_and_refresh(session, record):
    session.add(record)
    gillard.db.session.commit()
    record_id = record.id
    session.expunge_all()
    return session.query(type(record)).filter_by(id=record_id).one()

def save(session, record):
    session.add(record)
    gillard.db.session.commit()
    return record

def make_show(session, show_display_id='TESTID', password='TESTPW'):
    show = Show(show_display_id)
    show.password = password
    return save_and_refresh(session, show)

def make_playlist(session, show=None, ):
    if show is None:
        show = make_show(session)
    playlist = Playlist()
    show.playlists.append(playlist)
    return save_and_refresh(session, playlist)

def make_playlist_no_expunge(session, show=None, ):
    if show is None:
        show = make_show(session)
    playlist = Playlist()
    show.playlists.append(playlist)
    return save(session, playlist)

def make_song(session, playlist=None):
    if playlist is None:
        playlist = make_playlist(session)
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
    playlist.songs.append(song)

    session.add(song)
    gillard.db.session.commit()
    return song

class GillardBaseTestCase(unittest.TestCase):

    def setUp(self):
        gillard.app.config['TESTING'] = True
        gillard.app.config['SQLALCHEMY_DATABASE_URI']=\
            '{}/test'.format(gillard.db_uri)
        self.app = gillard.app.test_client()
        with gillard.app.app_context():
            gillard.create_tables()

    def tearDown(self):
        with gillard.app.app_context():
            gillard.drop_tables()
