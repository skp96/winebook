# Routes for login and logout
import datetime
from flask import Blueprint, jsonify, request
from ..models.user import User
from ..models.connection import db
from flask_jwt_extended import create_access_token, get_jwt_identity, decode_token, get_raw_jwt, jwt_required

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=["POST"])
def login():
    login_data = request.get_json()
    email, password = login_data.values()

    if not email:
      return jsonify({"error": 'Please provide an email'}), 400
  
    if not password:
      return jsonify({"error": "Please provide your password"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
      return jsonify({"error": "User cannot be found. Please try again or sign up"})

    if not user.check_password(password):
      return jsonify({"error": "Incorrect password, please try again"})

    access_token = create_access_token(identity=user.id, expires_delta=False, fresh=True)
    decoded = decode_token(access_token)
    return jsonify(access_token=access_token, decoded=decoded), 200

@bp.route('/logout', methods=['DELETE'])
def logout():
  jti = get_raw_jwt()['jti']
  blacklist.add(jti)
  return jsonify({"msg": 'Successfully logged out'}), 200

  