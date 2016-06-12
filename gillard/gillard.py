from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from random import random
import math

from database import db

from models import Playlist

app = Flask(__name__)

db_uri = 'postgresql+psycopg2://postgres:postgres@postgres:5432'

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='{}/dev'.format(db_uri),
    DEBUG=True,
    SECRET_KEY='development key',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
))
app.config.from_envvar('GILLARD_SETTINGS', silent=True)

db.init_app(app)

# comments

@app.route('/')
def hello_world():
    return 'index'

@app.route('/health')
def health():
    return 'OK'

@app.route('/playlist/new/<show_id>')
def new_playlist(show_id):
    playlist = Playlist()
    db.session.add(playlist)
    db.session.commit()

    return jsonify(
        display_id=playlist.display_id,
        password=playlist.password,
    )

def create_tables():
    db.create_all()
    return 'created db tables'

def drop_tables():
    db.drop_all()
    return 'dropped db tables'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
