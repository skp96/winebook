# package imports
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# module imports
from .config import Configuration
from .routes import users
from .routes import auth
from .models.connection import db
from .models.user import User

app = Flask(__name__)
app.config.from_object(Configuration)
app.register_blueprint(users.bp)
app.register_blueprint(auth.bp)
jwt = JWTManager(app)
db.init_app(app)
Migrate(app, db)

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    print(expired_token)
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401
    


