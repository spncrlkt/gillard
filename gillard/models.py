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
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    display_id = db.Column(db.Text)
    password = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
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

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
