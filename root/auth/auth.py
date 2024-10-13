from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies
)

from root.auth.users import add_user, get_user, update_user
from root.auth.models import UserSchema, TokenSchema, UserLoginSchema
from root.config import Config

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    email = data['email']
    password = data['password']

    if get_user(email):
        return jsonify({"msg": "User already exists"}), 400

    add_user(data)
    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(msg="Welcome to the protected route!")


@auth_bp.route('/jwt/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()

    # Перевірка наявності рефреш токена (використовуючи словник Config.refresh_tokens)
    if current_user not in Config.refresh_tokens:
        return jsonify({"msg": "Refresh token not found"}), 401

    # Створення нового доступного токена
    new_access_token = create_access_token(identity=current_user)

    # Можна також створити новий рефреш токен
    new_refresh_token = create_refresh_token(identity=current_user)
    Config.refresh_tokens[current_user] = new_refresh_token  # Оновлюємо словник

    return jsonify(access_token=new_access_token, refresh_token=new_refresh_token)


@auth_bp.route('/update_user', methods=['PUT'])
@jwt_required()
def update_user_route():
    data = request.json
    errors = user_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    email = data['email']
    password = data['password']

    if not get_user(email):
        return jsonify({"msg": "User not found"}), 404

    update_user(data)
    return jsonify({"msg": "User updated successfully"})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    errors = UserLoginSchema().validate(data)

    if errors:
        return jsonify(errors), 400

    email = data['email']
    password = data['password']

    user = get_user(email)
    if user is None or user['password'] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)
    Config.refresh_tokens[email] = refresh_token  # Зберігаємо токен у класі Config

    return jsonify(access_token=access_token, refresh_token=refresh_token)

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    Config.refresh_tokens.pop(current_user, None)  # Видаляємо токен з класу Config
    response = jsonify(msg="Logout successful")
    unset_jwt_cookies(response)
    return response
