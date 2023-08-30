from unittest import TestCase
from app import app
from models import db, Blog

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO']= False
db.drop.all()
db.create_all()

class BlogModelTestCase(TestCase):
    
    def setUp(self):

        Blog.query.delete()

    def tearDown(self):

        db.session.rollback()

    def test_greet(self):
        blogger = Blog(first_name='Adam', last_name='Adams', img_url='http://')
