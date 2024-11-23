from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from root.user_challenges.user_challenges import UserChallengeManager

user_challenge_bp = Blueprint('user_challenge_bp', __name__)
user_challenge_manager = UserChallengeManager()

# Додавання челенджу в список вибраних користувачем
@user_challenge_bp.route('/user_challenges', methods=['POST'])
@jwt_required()
def add_user_challenge():
    data = request.json
    user_email = data.get('user_email')
    challenge_id = data.get('challenge_id')

    if not user_email or not challenge_id:
        return jsonify({"msg": "user_email and challenge_id are required."}), 400

    response, _ = user_challenge_manager.add_user_challenge(user_email, challenge_id)
    return jsonify(response), 201

# Завершення челенджу для користувача
@user_challenge_bp.route('/user_challenges/complete', methods=['POST'])
@jwt_required()
def complete_user_challenge():
    data = request.json
    user_email = data.get('user_email')
    challenge_id = data.get('challenge_id')

    if not user_email or not challenge_id:
        return jsonify({"msg": "user_email and challenge_id are required."}), 400

    response, _ = user_challenge_manager.complete_challenge(user_email, challenge_id)
    return jsonify(response), 200

# Видалення челенджу з вибраних челенджів користувача
@user_challenge_bp.route('/user_challenges/remove', methods=['DELETE'])
@jwt_required()
def remove_user_challenge():
    data = request.json
    user_email = data.get('user_email')
    challenge_id = data.get('challenge_id')

    if not user_email or not challenge_id:
        return jsonify({"msg": "user_email and challenge_id are required."}), 400

    response, _ = user_challenge_manager.remove_challenge(user_email, challenge_id)
    return jsonify(response), 200

# Отримання всіх челенджів користувача
@user_challenge_bp.route('/user_challenges', methods=['GET'])
@jwt_required()
def get_user_challenges():
    user_email = request.args.get('user_email')

    if not user_email:
        return jsonify({"msg": "user_email is required."}), 400

    challenges = user_challenge_manager.get_user_challenges(user_email)
    return jsonify({"challenges": challenges}), 200
