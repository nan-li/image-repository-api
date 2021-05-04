"""Server for Image Repository app."""

#TODO: Remove unecesary items below

from flask import (Flask, render_template, redirect, abort,
                    flash, request, session, jsonify, request)

from model import connect_to_db, User
import cloudinary.uploader
import os
import crud

cloudinary.config(
    cloud_name = os.environ['CLOUDINARY_CLOUD_NAME'],  
    api_key = os.environ['CLOUDINARY_API_KEY'],  
    api_secret = os.environ['CLOUDINARY_API_SECRET'] 
)

app = Flask(__name__)
app.secret_key = 'dev'

"""Routes"""

@app.route('/api/users/signup', methods=['POST'])
def register_user():
    """Create a new user account."""
    username = request.json.get('username').lower()
    password = request.json.get('password')

    if not username or not password:
        abort(400, description='Missing username and/or password.')
    
    # Check if user with that username already exists
    if crud.get_user_by_username(username):
        abort(400, description='Username already exists.')

    # OK to create a new user account
    user = crud.create_user(username, password)

    session['user_id'] = user.id

    return jsonify({
                'status': 'success',
                'message': 'Account successfully created.',
                'user': username
    })

@app.route('/api/users/login', methods=['POST'])
def login_user():
    pass



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
