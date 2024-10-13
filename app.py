from flask import Flask
from flask_jwt_extended import JWTManager

from root.auth.auth import auth_bp
from root.config import Config

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)