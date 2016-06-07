from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import random
import math

from models import *

app = Flask(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://postgres:postgres@postgres:5432/test',
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('GILLARD_SETTINGS', silent=True)

db = SQLAlchemy(app)

# comments

@app.route('/')
def hello_world():
    return 'Flask in Docker'

@app.route('/create_user')
def create_user():
    rando = math.floor(random() * 100000)
    username = 'buttnutt{}'.format(rando)
    email = 'butt{}@nutt.org'.format(rando)
    user = User(username, email)
    db.session.add(user)
    db.session.commit()
    return 'created: {} {}'.format(username, email)

@app.route('/dump_users')
def dump_users():
    users = User.query.all()
    out = ''
    for user in users:
        out += '{}<br/>'.format(user.username)
    return out

@app.route('/create_db')
def create_db():
    db.create_all()
    return 'created db'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
