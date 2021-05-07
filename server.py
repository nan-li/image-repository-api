"""Server for Image Repository app."""

#TODO: Remove unecesary items below

from flask import (Flask, redirect, abort,
                    request, session, jsonify, request)

from model import connect_to_db, User
import cloudinary.uploader
import os
import crud
from flask_jwt_extended import (JWTManager, 
                                create_access_token, 
                                jwt_required, 
                                get_jwt_identity)


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


@app.route('/users/register', methods=['POST'])
def register_user():
    """Create a new user account."""
    if not request.json:
        abort(400, description='Invalid request.')
    username = request.json.get('username').lower()
    password = request.json.get("password")

    if not username or not password:
        abort(400, description='Missing username and/or password.')

    # Check if user with that username already exists
    if crud.get_user_by_username(username):
        abort(400, description='Username already exists.')

    # OK to create a new user account
    user = crud.create_user(username, password)

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
    user = crud.get_user_by_username_and_password(username, password)

    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })

@app.route("/users/logout", methods=["POST"])

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.filter.get(current_user_id)
    
    return jsonify({"id": user.id, "username": user.username }), 200



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
