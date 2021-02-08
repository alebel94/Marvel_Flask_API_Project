from marvel_api import app, db
import uuid
from datetime import datetime

#Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique=True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref= 'owner', lazy = True)

    def __init__(self,email,first_name = '', last_name = '', id = '', password = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Character(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    current_alias = db.Column(db.String(150), nullable = False)
    real_name = db.Column(db.String(150), nullable = True, default = '')
    super_power = db.Column(db.String(150), nullable = False)
    affiliation = db.Column(db.String(150), nullable = True, default = '')
    comics_appeared_in = db.Column(db.Integer, nullable = True, default = 0)
    origin_planet = db.Column(db.String(150), nullable = True, default = '')
    description = db.Column(db.String(1000), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, current_alias, super_power, description, date_created, id = '', real_name = '', affiliation = '', comics_appeared_in = '', origin_planet = ''):
        self.id = self.set_id()
        self.current_alias = current_alias
        self.super_power = super_power
        self.description = description
        self.date_created = date_created
        self.real_name = real_name
        self.affiliation = affiliation
        self.comics_appeared_in = comics_appeared_in
        self.origin_planet = origin_planet

    def __repr__(self):
        return f'The following character has been added: {self.current_alias} which belongs tp {self.user_id}'

    def to_dict(self):
        return{
        'current_alias': self.current_alias,
        'real_name': self.real_name,
        'super_power': self.super_power,
        'affiliation': self.affiliation,
        'comics_appeared_in': self.comics_appeared_in,
        'origin_planet': self.origin_planet,
        'description': self.description,
        'date_created': self.date_created 
        }