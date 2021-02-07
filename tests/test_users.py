import unittest
from app import create_app, db
from app.models import User, Artist
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

    def test_followed(self):
        u = User(username='bob', email='bob@test.com')
        u.set_password('123')
        a = Artist(name='The Beatles')
        db.session.add_all([u, a])
        db.session.commit()

        self.assertEqual(u.followed.all(), [])
        self.assertEqual(a.followers.all(), [])

        u.follow(a)
        db.session.commit()

        self.assertTrue(u.is_following(a))
        self.assertEqual(u.followed.first().name, 'The Beatles')
        self.assertEqual(u.followed.count(), 1)
        self.assertEqual(a.followers.first().username, 'bob')
        self.assertEqual(a.followers.count(), 1)

        u.unfollow(a)
        db.session.commit()

        self.assertFalse(u.is_following(a))
        self.assertEqual(u.followed.all(), [])
        self.assertEqual(u.followed.count(), 0)
        self.assertEqual(a.followers.all(), [])
        self.assertEqual(a.followers.count(), 0)