"""Models for Image Repository app."""

from datetime import datetime
from enum import Enum

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class ImagePermission(Enum):
    """Permissions that images can have."""
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"


class User(db.Model):
    """A user."""

    __tablename__ = 'users'
    
    # TODO: come back and make nullable=False

    id = db.Column(db.Integer,
                    autoincrement=True, 
                    primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    images = db.relationship('Image', 
                    foreign_keys='Image.owner_id',
                    backref='owner')

    def __repr__(self):
        return f'<User {self.username}>.'

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
        }
        return data

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Image(db.Model):
    """An image."""
    __tablename__ = 'images'

    id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    image_url = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    permission = db.Column(db.Enum(ImagePermission), default='PRIVATE')
    # owner = user who uploaded this image

    def __repr__(self):
        return f'<Image from {self.ownder}>.'

    def to_dict(self):
        data = {
            'id': self.id,
            'image_url': self.image_url,
            'permission': self.permission.value
        }
        return data






def connect_to_db(flask_app, db_uri='postgresql:///images', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app
    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)