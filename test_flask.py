from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
    db.drop_all()
    db.create_all()

class UserViewsTestCase(TestCase):
    """Test Views for Users"""

    def setUp(self):
        """Add sample user"""
        with app.app_context():
            User.query.delete()
            user=User(user_name="TestMon2", first_name="Test",last_name="Mon2",user_email="Test.Mon2@something.com")
            db.session.add(user)
            db.session.commit()
            self.user_id=user.id

    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp= client.get("/", follow_redirects=True)
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestMon2", html)

    def test_show_user(self):
        with app.test_client() as client:
            resp= client.get(f"/user/{self.user_id}")
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestMon2</p>", html)

    def test_add_user(self):
        with app.test_client() as client:
            user = {"user_name" :"TestMon3", "first_name": "Test","last_name" : "Mon3", "user_email" : "Test.Mon3@something.com"}
            resp = client.post("/users/new", data=user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<li>TestMon3</li>", html)