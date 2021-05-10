"""Script to seed database."""
import os
from server import app
from model import User, Image, connect_to_db, db
from werkzeug.security import generate_password_hash

os.system('dropdb images')
os.system('createdb images')

connect_to_db(app, echo=False)
db.create_all()

# Add sample users and images
user1 = User(username='user1', password_hash=generate_password_hash('test1'))
user2 = User(username='user2', password_hash=generate_password_hash('test2'))

user1image1 = Image(image_url='url/for/user1image1', owner=user1)
user2image1 = Image(image_url='url/for/user2image1', owner=user2)
user1image2_public = Image(image_url='url/for/user1image2_private', 
                            owner=user1, permission='PUBLIC')

db.session.add_all([user1, 
                    user2, 
                    user1image1, 
                    user2image1, 
                    user1image2_public])
db.session.commit()