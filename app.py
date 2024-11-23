from flask import Flask
from flask_jwt_extended import JWTManager

from root.auth.auth import auth_bp
from root.challenge.endpoints import challenge_bp
from root.config import Config
from root.friends.endpoints import friend_bp
from root.user_challenges.endpoints import user_challenge_bp

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(challenge_bp)
app.register_blueprint(friend_bp)
app.register_blueprint(user_challenge_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)