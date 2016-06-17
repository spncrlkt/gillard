import sys
import traceback
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from random import random
import math

from utils import eprint
from database import db

from models import Playlist, Show, Song
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

    # check show exists
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
    # check playlist exists
    try:
        playlist = db.session.query(Playlist).filter_by(display_id=display_id).one()
    except NoResultFound as ex:
        raise InvalidUsage('No playlist found for id: {}'.format(display_id))

    # check for playlist_mode
    show_id = request.args.get('show_id', None)
    password = request.args.get('password', None)

    if show_id is None or password is None:
        session['playlist_mode'] = 'readonly'

    # check show exists and associates to playlist
    try:
        show = db.session.query(Show).filter_by(display_id=show_id, password=password).one()
        if playlist in show.playlists:
            session['playlist_mode'] = 'edit'
        else:
            # TODO log
            session['playlist_mode'] = 'readonly'
    except NoResultFound as ex:
        # TODO log
        session['playlist_mode'] = 'readonly'

    return jsonify(
        display_id=display_id,
        songs=[song.as_dict() for song in playlist.songs]
    )

@app.route('/playlist/<display_id>/add_song', methods=['POST'])
def add_song(display_id):
    # check playlist_mode
    playlist_mode = session.get('playlist_mode')
    if playlist_mode != 'edit':
        raise InvalidUsage("Can't add songs in readonly mode")


    # check playlist exists
    try:
        playlist = db.session.query(Playlist).filter_by(display_id=display_id).one()
    except NoResultFound as ex:
        raise InvalidUsage('No playlist found for id: {}'.format(display_id))

    try:
        song_data = request.get_json()
    except Exception as ex:
        raise InvalidUsage('Invalid JSON')

    song = Song(**song_data)
    playlist.songs.append(song)
    db.session.add(song)
    db.session.commit()

    return 'OK'

@app.route('/playlist/<display_id>/delete_song', methods=['POST'])
def delete_song(display_id):
    # check playlist_mode
    playlist_mode = session.get('playlist_mode')
    if playlist_mode != 'edit':
        raise InvalidUsage("Can't delete songs in readonly mode")

    try:
        request_json = request.get_json()
        song_id = request_json.get('song_id')
    except Exception as ex:
        raise InvalidUsage('Invalid JSON')

    # check song exists
    try:
        song = db.session.query(Song).filter_by(id=song_id).one()
    except NoResultFound as ex:
        raise InvalidUsage('No song found for id: {}'.format(song_id))

    # check playlist exists
    try:
        playlist = db.session.query(Playlist).filter_by(display_id=display_id).one()
    except NoResultFound as ex:
        raise InvalidUsage('No playlist found for id: {}'.format(display_id))

    # check song in playlist
    if song not in playlist.songs:
        raise InvalidUsage("Song id {} not in playlist id {}".format(song.id, playlist.display_id))

    db.session.delete(song)
    db.session.commit()

    return 'OK'

@app.route('/playlists/<show_display_id>', methods=['GET'])
def playlists_by_show_id(show_display_id):
    # check show exists
    try:
        show = db.session.query(Show).filter_by(display_id=show_display_id).one()
    except NoResultFound as ex:
        raise InvalidUsage('No show found for id: {}'.format(show_display_id))

    playlist_disp_ids = [x.display_id for x in show.playlists]

    return jsonify(
        playlists=playlist_disp_ids
    )

@app.route('/song/<song_id>', methods=['POST'])
def song(song_id):
    # check playlist_mode
    playlist_mode = session.get('playlist_mode')
    if playlist_mode != 'edit':
        raise InvalidUsage("Can't edit songs in readonly mode")

    # check song exists
    try:
        song = db.session.query(Song).filter_by(id=song_id).one()
    except NoResultFound as ex:
        raise InvalidUsage('No song found for id: {}'.format(song_id))

    # parse json request
    try:
        song_data = request.get_json()
    except Exception as ex:
        raise InvalidUsage('Invalid JSON')

    for key, value in song_data.items():
        if hasattr(song, key):
            setattr(song, key, value)
        else:
            raise InvalidUsage("Song has no attribute: {}".format(key))

    db.session.add(song)
    db.session.commit()

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
