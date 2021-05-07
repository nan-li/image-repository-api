"""Models for Image Repository app."""

from datetime import datetime
from enum import Enum, auto

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class ImageStatus(Enum):
    """Statuses that images can have."""
    ACTIVE = auto()
    IN_TRASH = auto()

class ImagePermission(Enum):
    """Permissions that images can have."""
    PRIVATE = auto()
    FRIENDS_ONLY = auto()
    PUBLIC = auto()

class FriendStatus(Enum):
    """Statuses that friends can have."""
    REQUESTED = auto()
    ACCEPTED = auto()
    DENIED = auto()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'
    
    # TODO: come back and make nullable=False

    id = db.Column(db.Integer,
                    autoincrement=True, 
                    primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String)

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

class Friend(db.Model):
    """A friendship relationship between two users."""
    __tablename__ = 'friends'

    id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.Enum(FriendStatus), default='REQUESTED')

    def __repr__(self):
        return f'<Friend relationship from User {self.sender_id} to {self.recipient_id} | Status {self.status}>.'


class Image(db.Model):
    """An image."""
    __tablename__ = 'images'

    id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    title = db.Column(db.String)
    url = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    permission = db.Column(db.Enum(ImagePermission), default='PRIVATE')
    status = db.Column(db.Enum(ImageStatus), default='ACTIVE')
    # trashed_at timestamp resets if trashed image is restored and re-trashed
    trashed_at = db.Column(db.DateTime)
    # owner = user who uploaded this image

    def __repr__(self):
        return f'<Image from {self.ownder}>.'

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'url': self.url,
        }
        return data


def example_data():
    """Create some sample data for testing."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Image.query.delete()
    Friend.query.delete()

    # Add sample users and images
    user1 = User(username='user1')
    user1.set_password('test1')
    user2 = User(username='user2')
    user2.set_password('test2')

    user1image1 = Image(url='url/for/user1image1', owner=user1)
    user2image1 = Image(url='url/for/user2image1', owner=user2)
    user1image2_private = Image(url='url/for/user1image2_private', 
                                owner=user1)

    db.session.add_all([user1, 
                        user2, 
                        user1image1, 
                        user2image1, 
                        user1image2_private])
    db.session.commit()

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