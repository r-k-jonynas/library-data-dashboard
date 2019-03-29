from app import create_app

import os
import unittest
from app.extensions import db, migrate, login
# import json
# import requests

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = app.test_client(self.app)
        with app.app_context():
            db.init_app(app)
            migrate.init_app(app)
            login.init_app(app)

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # def test_index(self):
    #     pass
    #
    # def test_user(self):
    #     from app.models import User
    #     u = User(username='example', role='Visitor')
    #     self.assertEqual(repr(u), '<User example>')
    #     u.set_password('12345')
    #     self.assertEqual(u.check_password('12345'), True)
    #     u.set_role('User')
    #     self.assertEqual(u.role, 'User')


if __name__ == "__main__":
    unittest.main()
