from functools import wraps

from flask import request, jsonify 

from marvel_api.models import Character, User
from marvel_api import app

import jwt

import json
from datetime import datetime


def get_jwt(current_user):
    jwt_token = jwt.encode(
        {
            'owner' : current_user.token,
            'access_time' : json.dumps(datetime.utcnow(), indent= 4, sort_keys= 4, default= str)
        },
        app.config['SECRET_KEY'],
        algorithm = 'HS256'
    )
    return jwt_token

    # Create a function to verify a token is present and valid
def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_token = User.query.filter_by(token = data['owner']).first()
            print(token)
            print(data)
            print(current_user_token)
        except:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms = ['HS256'])
            owner = User.query.filter_by(token = data['owner']).first()
            if data['owner'] != owner.token:
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated
    
def verify_owner(current_user_token):
    owner = Character.query.filter_by(user_id = current_user_token.token).first()
    print(current_user_token.token)
    print(owner)
    if owner == None:
        return jsonify({'message': "You don't have any Characters created! Create One!!"})
    if owner.user_id != current_user_token.token:
        return jsonify({'message': "Token is invalid - not authorized to view data"})
    return owner, current_user_token