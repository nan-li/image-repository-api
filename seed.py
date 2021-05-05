"""Script to seed database."""
import os
from server import app
from model import connect_to_db, db


os.system('dropdb images')
os.system('createdb images')

connect_to_db(app, echo=False)
db.create_all()