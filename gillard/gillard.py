import sys
import traceback
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from random import random
import math

from utils import eprint
from database import db

from models import Playlist, Show
from invalid_usage import InvalidUsage

app = Flask(__name__)

db_uri = 'postgresql+psycopg2://postgres:postgres@postgres:5432'

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='{}/dev'.format(db_uri),
    DEBUG=True,
    SECRET_KEY="w!\x1c\xcd\xc5\x82\xdc'\xdd>\x1b,\xaf(\x9b\xc8\x80|k\x10<\x8fo\xaf",
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

@app.route('/playlist/new', methods=['GET'])
def new_playlist():
    show_id = request.args.get('show_id')
    password = request.args.get('password')
    try:
        show = db.session.query(Show).filter_by(display_id=show_id, password=password).one()
    except NoResultFound as ex:
        raise InvalidUsage('No show found for id: {}'.format(show_id))

    playlist = Playlist()
    show.playlists.append(playlist)
    db.session.add(playlist)
    db.session.commit()

    return jsonify(display_id=playlist.display_id)

@app.route('/playlist/<display_id>', methods=['GET'])
def playlist(display_id):
    try:
        playlist = db.session.query(Playlist).filter_by(display_id=display_id).one()
    except NoResultFound as ex:
        raise InvalidUsage('No playlist found for id: {}'.format(display_id))

    session['playlist_mode'] = 'readonly'

    return 'OK'

def create_tables():
    db.create_all()
    return 'created db tables'

def drop_tables():
    db.drop_all()
    return 'dropped db tables'

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(Exception)
def all_error_handler(error):
    eprint('\n**********')
    eprint('\nUnhandled Exception')
    traceback.print_exc(file=sys.stderr)
    eprint('\n**********')
    return 'Error', 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
