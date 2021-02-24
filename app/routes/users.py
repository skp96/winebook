# Route to sign user up
from flask import Blueprint, jsonify, request
from ..models.user import User
from ..models.connection import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('users', __name__, url_prefix='/user')

@bp.route("/", methods=["GET"])
@jwt_required
def get_user():
  current_user = get_jwt_identity()
  return jsonify(logged_in_as=current_user),200

@bp.route('/register', methods=["POST"])
def signup():
  user_data = request.get_json()
  name, username, email, password = user_data.values()
  
  try:
    user = User(
    name = name,
    username = username,
    email = email,
    password_digest = password
    )
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=user.id, expires_delta=False, fresh=True)
    return jsonify(access_token=access_token), 200
  except AssertionError as exception_message:
    return jsonify(error='{}. '.format(exception_message)), 400
  


