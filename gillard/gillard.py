from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from random import random
import math

from models import *

app = Flask(__name__)

db_uri = 'postgresql+psycopg2://postgres:postgres@postgres:5432'

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='{}/dev'.format(db_uri),
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

@app.route('/create_tables')
def create_tables_route():
    return create_tables()

def create_tables():
    db.create_all()
    return 'created db tables'

@app.route('/create_dbs')
def create_dbs_route():
    return create_dbs()

def create_dbs():
    create_db_if_not_exists('test')
    create_db_if_not_exists('dev')
    return 'created dbs'

def create_db_if_not_exists(db_name):
    result = db.engine.execute(
            "SELECT 1 FROM pg_database WHERE datname = '{}'".format(db_name))
    res = []
    for row in result:
        res.append(row[0])
    if not res:
        create_db(db_name)

def create_db(db_name):
    engine = create_engine(db_uri+'/template1')
    session = sessionmaker(bind=engine)()
    session.connection().connection.set_isolation_level(0)
    session.execute('CREATE DATABASE {}'.format(db_name))
    session.connection().connection.set_isolation_level(1)
    session.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
