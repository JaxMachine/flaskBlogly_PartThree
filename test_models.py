from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    db.drop_all()
    db.create_all()

class UserModelTestCase(TestCase):
    """Tests for model for User"""

    def setUp(self):
        """Cleans up any current users"""
        with app.app_context():
            User.query.delete()
    
    def tearDown(self):
        """Clean up any issues"""
        with app.app_context():
            db.session.rollback()

    def test_full_name(self):
        user=User(user_name="TestMon2", first_name="Test",last_name="Mon2",user_email="Test.Mon2@something.com")
        self.assertEqual(user.get_full_name, "Test Mon2")