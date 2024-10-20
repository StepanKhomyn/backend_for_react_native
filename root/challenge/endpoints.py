from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from root.challenge.challenge import ChallengeManager

challenge_bp = Blueprint('challenge_bp', __name__)
challenge_manager = ChallengeManager()

# Отримання списку челенджів
@challenge_bp.route('/challenges', methods=['GET'])
@jwt_required()
def get_challenges_route():
    filters = request.args.to_dict()  # Отримуємо фільтри з параметрів запиту
    limit = request.args.get('limit', 10, type=int)  # Ліміт з параметрів запиту
    offset = request.args.get('offset', 0, type=int)  # Оффсет з параметрів запиту
    sort_field = request.args.get('sort_field', '_id')  # Поле для сортування
    sort_order = request.args.get('sort_order', 'desc')  # Порядок сортування

    # Перевірка параметрів
    if limit <= 0 or offset < 0:
        return jsonify({"msg": "Limit must be greater than 0 and offset cannot be negative."}), 400

    challenges, response_code = challenge_manager.get_challenges(filters, limit, offset, sort_field, sort_order)

    if response_code == 500:
        return jsonify(challenges), 500

    return jsonify({
        'total_count': response_code,
        'challenges': challenges
    }), 200

# Отримання челенджу за ID
@challenge_bp.route('/challenges/<challenge_id>', methods=['GET'])
@jwt_required()
def get_challenge_route(challenge_id):
    challenge = challenge_manager.get_challenge(challenge_id)
    if challenge is None:
        return jsonify({"msg": "Challenge not found"}), 404
    return jsonify(challenge), 200

# Реєстрація челенджу
@challenge_bp.route('/challenges', methods=['POST'])
@jwt_required()
def create_challenge():
    data = request.json
    errors, created_challenge = challenge_manager.add_challenge(data)
    if errors:
        return jsonify(errors), 400

    return jsonify(created_challenge), 201  # This will now return a JSON serializable object

# Редагування челенджу
@challenge_bp.route('/challenges/<challenge_id>', methods=['PUT'])
@jwt_required()
def update_challenge_route(challenge_id):
    data = request.json
    errors, updated_challenge = challenge_manager.update_challenge(challenge_id, data)
    if errors:
        return jsonify(errors), 400

    return jsonify(updated_challenge), 200
