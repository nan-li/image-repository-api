"""CRUD operations."""

from model import db, User, Image
from datetime import datetime


def create_user(username, password):
    """Create and return a new user."""

    # When I create a new user, I don't pass password in:
    user = User(username=username)
    
    # Here I set the password_hash with password
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_username(username):
    """Return a user by username."""
    return User.query.filter_by(username=username).first()


"""Send a friend request from sender to recipient."""

"""Accept a friend request."""
