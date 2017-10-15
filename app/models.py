# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
    """
    Create an User table
    """
    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    weather_xz = db.relationship('Weathers_xz', backref='user', lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Weathers_xz(db.Model):

    __tablename__ = 'weather_xz'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(60))
    weather = db.Column(db.String(60))
    temperature = db.Column(db.String(60))
    day = db.Column(db.String(80))
#    code = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def __init__(self, location, weather, temperature, day, user_id):
        self.location = location
        self.weather = weather
        self.temperature = temperature
        self.day = day

    def __repr__(self):
        return '<Weathers_xz: {}>'.format(self.location)
