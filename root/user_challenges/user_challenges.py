from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient
from root.config import Config
from root.challenge.models import ChallengeSchema

# Ініціалізація MongoDB
client = MongoClient(Config.MONGO_URI)
db = client['my_db']
user_challenges_collection = db['user_challenges']  # Нова колекція для вибраних челенджів

class UserChallengeManager:
    def __init__(self):
        self.db = db

    # Додавання челенджу до вибраних челенджів користувача
    def add_user_challenge(self, user_email, challenge_id):
        existing_challenge = user_challenges_collection.find_one({"user_email": user_email, "challenge_id": ObjectId(challenge_id)})
        if existing_challenge:
            return {"msg": "Challenge already added to the user's list."}, None

        # Додаємо челендж користувачу
        user_challenges_collection.insert_one({
            "user_email": user_email,
            "challenge_id": ObjectId(challenge_id),
            "status": "in_progress",  # Статус "in_progress" за замовчуванням
            "date_added": datetime.datetime.now()
        })

        return {"msg": "Challenge added successfully."}, None

    # Завершення челенджу
    def complete_challenge(self, user_email, challenge_id):
        result = user_challenges_collection.update_one(
            {"user_email": user_email, "challenge_id": ObjectId(challenge_id)},
            {"$set": {"status": "completed"}}
        )

        if result.matched_count == 0:
            return {"msg": "Challenge not found for this user."}, None

        return {"msg": "Challenge completed successfully."}, None

    # Видалення челенджу з вибраних челенджів
    def remove_challenge(self, user_email, challenge_id):
        result = user_challenges_collection.delete_one(
            {"user_email": user_email, "challenge_id": ObjectId(challenge_id)}
        )

        if result.deleted_count == 0:
            return {"msg": "Challenge not found for this user."}, None

        return {"msg": "Challenge removed successfully."}, None

    # Отримання всіх челенджів для користувача
    def get_user_challenges(self, user_email):
        user_challenges = user_challenges_collection.find({"user_email": user_email})
        challenges = []

        for user_challenge in user_challenges:
            challenge = self.get_challenge(user_challenge["challenge_id"])
            if challenge:
                user_challenge["_id"] = str(user_challenge["_id"])
                user_challenge["challenge"] = challenge
                challenges.append(user_challenge)

        return challenges

    # Отримання челенджу за ID
    def get_challenge(self, challenge_id):
        challenge = user_challenges_collection.find_one({"_id": ObjectId(challenge_id)})
        if challenge:
            challenge['_id'] = str(challenge['_id'])  # Перетворенн
