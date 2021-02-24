import re
from sqlalchemy.orm import validates
from .connection import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
  __table__name ='users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  username = db.Column(db.String(100), nullable=False, unique=True, index=True)
  email = db.Column(db.String(100), nullable=False, unique=True)
  password_digest = db.Column(db.String(100), nullable=False)

  def __init__(self, name, username, email, password_digest):
    self.name = name
    self.username = username
    self.email = email
    self.password_digest = User.hashed_password(password_digest)
    

  @staticmethod
  def hashed_password(password):
    if not password:
      raise AssertionError('Password not provided')

    if len(password) < 8 or len(password) > 20:
      raise AssertionError('Password must be between 8 to 20 character')
    
    return generate_password_hash(password)

  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(username=username).first()

  @classmethod
  def find_by_email(cls, email):
    return cls.query.filter_by(email=email).first()
  
  def check_password(self, password):
    return check_password_hash(self.password_digest, password)

  def to_json(self):
    json_obj = {
      "id": self.id,
      "name": self.name,
      "username": self.username,
      "email": self.email,
      "password": self.password_digest
    }
    return json_obj

  @validates('name')
  def validate_name(self, key, name):
    if not name:
      raise AssertionError('Please provide name')

    return name

  @validates('username')
  def validate_username(self, key, username):
    if not username:
      raise AssertionError('Please provide a username')

    if User.query.filter_by(username=username).first():
      raise AssertionError('Username is already in use')

    if len(username) < 5 or len(username) > 20:
      raise AssertionError('Username must be between 6 to 20 characters')

    return username

  @validates('email')
  def validate_email(self, key, email):
    if not email:
      raise AssertionError('Please provide an email address')

    if not re.match("[^@]+@[^@]+\.[^@]+", email):
      raise AssertionError('Email provided is not an email address')

    if User.query.filter_by(email=email).first():
      raise AssertionError('The email provided is already in use')

    return email
