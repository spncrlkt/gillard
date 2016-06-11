from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import uuid
import datetime

from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    songs = relationship("Song")
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    display_id = db.Column(db.Text, index=True, unique=True)
    password = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    def __init__(self, **kwargs):
        # auto-generate password && display_id hashes
        super(Playlist, self).__init__(**kwargs)
        self.password = uuid.uuid4().hex
        self.display_id = uuid.uuid4().hex


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlists = relationship("Playlist")
    startDay = db.Column(db.Integer)
    startHour = db.Column(db.Integer)
    endDay = db.Column(db.Integer)
    endHour = db.Column(db.Integer)

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
