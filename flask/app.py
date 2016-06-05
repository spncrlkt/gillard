from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import random
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@postgres:5432/test'
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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
