import unittest
from app import create_app, db
from app.models import User
from config import TestConfig

class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='test', email='test@test.com')
        u.set_password('correct')

        self.assertTrue(u.check_password('correct'))
        self.assertFalse(u.check_password('incorrect'))

    def test_password_salt(self):
        u1 = User(username='bob', email='bob@test.com')
        u1.set_password('correct')

        u2 = User(username='jane', email='jane@test.com')
        u2.set_password('correct')

        self.assertTrue(u1.password != u2.password)