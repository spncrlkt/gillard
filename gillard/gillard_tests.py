import os
import gillard
import unittest

class GillardTestCase(unittest.TestCase):

    def setUp(self):
        gillard.app.config['TESTING'] = True
        self.app = gillard.app.test_client()
        with gillard.app.app_context():
            gillard.create_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
