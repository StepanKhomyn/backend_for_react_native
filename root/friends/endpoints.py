from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from root.friends.friends import FriendManager

friend_bp = Blueprint('friend_bp', __name__)
friend_manager = FriendManager()  # Клас для роботи з друзями


# Додавання друга
@friend_bp.route('/friends', methods=['POST'])
@jwt_required()
def add_friend():
    data = request.json
    user_email = data.get('user_email')
    friend_email = data.get('friend_email')

    if not user_email or not friend_email:
        return jsonify({"msg": "Both user_email and friend_email are required."}), 400

    result = friend_manager.add_friend(user_email, friend_email)

    if 'error' in result:
        return jsonify(result), 400

    return jsonify({"msg": "Friend added successfully."}), 201


# Отримання списку друзів користувача
@friend_bp.route('/friends', methods=['GET'])
@jwt_required()
def get_friends():
    user_email = request.args.get('user_email')

    if not user_email:
        return jsonify({"msg": "user_email is required."}), 400

    friends = friend_manager.get_friends(user_email)

    if friends is None:
        return jsonify({"msg": "User not found."}), 404

    return jsonify({"friends": friends}), 200
