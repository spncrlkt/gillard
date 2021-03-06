from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.orm import relationship
import uuid
import datetime

from database import db
from utils import eprint

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_id = db.Column(db.Text, index=True, unique=True)
    playlists = relationship("Playlist")
    password = db.Column(db.Text)
    title = db.Column(db.Text)
    startDay = db.Column(db.Integer)
    startHour = db.Column(db.Integer)
    endDay = db.Column(db.Integer)
    endHour = db.Column(db.Integer)

    def __init__(self, display_id, password, **kwargs):
        # auto-generate password && display_id hashes
        super(Show, self).__init__(**kwargs)
        self.display_id = display_id
        self.password = password
        for key, value in kwargs.items():
            self.key = value

    def missing_columns(self):
        nullable_columns = ['playlists','id']
        missing_columns = []
        mapper = inspect(Show)
        for column in mapper.attrs:
            key = column.key
            val = getattr(self,key)
            if key not in nullable_columns and not val:
                missing_columns.append(key)

        return missing_columns



class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    songs = relationship("Song", cascade="all, delete, delete-orphan")
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    display_id = db.Column(db.Text, index=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    def __init__(self, **kwargs):
        # auto-generate display_id hash
        super(Playlist, self).__init__(**kwargs)
        self.display_id = uuid.uuid4().hex


def update_played_at(context):
    if context.current_parameters.get('played', False):
        return datetime.datetime.now()
    else:
        return None

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    artist = db.Column(db.Text)
    title = db.Column(db.Text)
    album = db.Column(db.Text)
    label = db.Column(db.Text)
    release_date = db.Column(db.Text)
    notes = db.Column(db.Text)
    img64px = db.Column(db.Text)
    img300px = db.Column(db.Text)
    played = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now)
    played_at = db.Column(db.DateTime, onupdate=update_played_at)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, **kwargs):
        # init w/ song data
        super(Song, self).__init__(**kwargs)
        for key, value in kwargs.items():
            self.key = value
