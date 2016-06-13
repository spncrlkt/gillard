import unittest

import gillard
from models import Show

def save_and_refresh(session, record):
    session.add(record)
    gillard.db.session.commit()
    record_id = record.id
    session.expunge_all()
    return session.query(type(record)).filter_by(id=record_id).one()

def make_show(session, show_display_id, password):
    show = Show(show_display_id)
    show.password = password
    return save_and_refresh(session, show)

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
