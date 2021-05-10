"""Server for Image Repository app."""

#TODO: Remove unecesary items below

from flask import (Flask, redirect,
                    request, session, jsonify, request)

from model import connect_to_db, User
import cloudinary.uploader
import os
import crud
from flask_jwt_extended import (JWTManager, 
                                create_access_token, 
                                jwt_required, 
                                current_user)
import json

cloudinary.config(
    cloud_name = os.environ['CLOUDINARY_CLOUD_NAME'],  
    api_key = os.environ['CLOUDINARY_API_KEY'],  
    api_secret = os.environ['CLOUDINARY_API_SECRET'] 
)

app = Flask(__name__)
app.secret_key = 'dev'

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ['JWT_SECRET_KEY']  
jwt = JWTManager(app)


# Register a callback function that loades a user from your database whenever
# a protected route is accessed. Return None if the lookup failed.
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Generic Internal Server Error message
error_msg = {'status': 'fail',
            "message": 'Internal Server Error occur.'}

@app.route('/users/register', methods=['POST'])
def register_user():
    """Create a new user account."""

    if not request.json:
        return jsonify({
            'status': 'fail',
            "message": 'Invalid request.'}), 400

    username = request.json.get('username').lower()
    password = request.json.get("password")

    if not username or not password:
        return jsonify({
            'status': 'fail',
            "message": 'Missing username and/or password.'}), 400

    # Check if user with that username already exists
    try:
        if crud.get_user_by_username(username):
            return jsonify({
                'status': 'fail',
                "message": 'Username already exists.'}), 400
    except:
        return jsonify(error_msg), 500

    # OK to create a new user account
    try:
        user = crud.create_user(username, password)
    except:
        return jsonify({
            'status': 'fail',
            "message": 'Error occured while registering user.'}), 500

    return jsonify({
                'status': 'success',
                'message': 'Account successfully created.',
                'username': username,
                'user_id': user.id
    })

@app.route("/users/login", methods=["POST"])
def login():
    """Authenticate the user and return JWT."""

    username = request.json.get('username').lower()
    password = request.json.get('password')

    # Query database for username and password
    try:
        user = crud.get_user_by_username_and_password(username, password)
    except:
        return jsonify(error_msg), 500

    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user)
    return jsonify({ "token": access_token, "user_id": user.id })


@app.route("/users/<username>/upload", methods=["POST"])
@jwt_required()
def upload_image(username):
    """Upload an image."""

    # Cannot upload an image to another user's account
    if username != current_user.username:
        return jsonify({
            'status': 'fail',
            'message': 'Access denied.'}), 401

    image_file = request.files.get('image')
    cloudinary_upload = cloudinary.uploader.upload(image_file)
    image_url = cloudinary_upload['url']

    # Check if request wants to set permissions
    permission = None
    if request.form.get('permission'):
        permission = request.form.get('permission')

    # Create Image and catch errors such as providing incorrect 
    # permission values other than PRVIATE or PUBLIC
    try:
        user = crud.get_user_by_username(current_user.username)
        image = crud.create_image(image_url, user, permission)
    except:
        return jsonify(error_msg), 500

    return jsonify({ 
        'status': 'success',
        'message': 'Image successfully uploaded.',
        'permission': image.permission.name,
        "image_url": image_url })

@app.route("/users/<username>/images")
@jwt_required()
def get_image(username):
    """
    Return a user's images.
    Returns all images if the user is requesting own images.
    Returns public images of another user.
    """
    images = []

    if username == current_user.username:
        try:
            images = crud.get_all_images_for_user(username)
        except:
            return jsonify(error_msg), 500
    else:
        try:
            images = crud.get_public_images_for_user(username)
        except:
            return jsonify(error_msg), 500

    images_info = [image.to_dict() for image in images]

    return jsonify({
        'status': 'success',
        'total': len(images_info),
        'images': images_info
    })


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
