"""CRUD operations."""

from model import db, User, Image, ImagePermission
from datetime import datetime
from werkzeug.security import generate_password_hash

def create_user(username, password):
    """Create and return a new user."""

    user = User(username=username, password_hash=generate_password_hash(password))
        
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_username(username):
    """Return a user by username."""
    return User.query.filter_by(username=username).first()

def get_user_by_username_and_password(username, password):
    """Return a user by username and password."""
    user = get_user_by_username(username)
    if not user:
        return None

    if user.check_password(password):
        return user


def create_image(image_url, owner, permission="PRIVATE"):
    """Create and return a new image."""

    image = Image(image_url=image_url,
                    owner=owner,
                    permission=permission)
        
    db.session.add(image)
    db.session.commit()
    return image


def get_all_images_for_user(username):
    """Return all images belonging to a user."""

    user = get_user_by_username(username)
    return user.images


def get_public_images_for_user(username):
    """Return all public images belonging to a user."""

    user = get_user_by_username(username)
    images = user.images
    public_images = [img for img in images if img.permission.value == "PUBLIC"]
    return public_images