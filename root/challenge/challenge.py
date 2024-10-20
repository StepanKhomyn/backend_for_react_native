from bson import ObjectId
from marshmallow import ValidationError
from pymongo import MongoClient
from root.challenge.models import ChallengeSchema, UpdateChallengeSchema
from root.config import Config
from root.custom_filter import FilterManager

# Ініціалізація MongoDB
client = MongoClient(Config.MONGO_URI)
db = client['my_db']
challenges_collection = db['challenges']

class ChallengeManager:
    # Метод для отримання челенджу
    def get_challenge(self, challenge_id):
        challenge = challenges_collection.find_one({"_id": ObjectId(challenge_id)})
        if challenge:
            challenge['_id'] = str(challenge['_id'])  # Convert ObjectId to string
        return challenge

    # Метод для створення челенджу
    def add_challenge(self, data):
        errors = ChallengeSchema().validate(data)
        if errors:
            return errors, None

        result = challenges_collection.insert_one(data)
        created_challenge = data
        created_challenge['_id'] = str(result.inserted_id)  # Convert ObjectId to string

        return None, created_challenge  # Return the created object

    # Метод для редагування челенджу
    def update_challenge(self, challenge_id, data):
        errors = UpdateChallengeSchema().validate(data)
        if errors:
            return errors, None

        challenges_collection.update_one({"_id": ObjectId(challenge_id)}, {"$set": data})
        updated_challenge = self.get_challenge(challenge_id)
        return None, updated_challenge  # Повертаємо оновлений об'єкт

    # Метод для отримання списку челенджів з фільтрацією
    def get_challenges(self, filters=None, limit=10, offset=0, sort_field='_id', sort_order='desc'):
        try:
            # Get the query and sort criteria from FilterManager
            query, sort_criteria = FilterManager().get_filter_query(filters, sort_field, sort_order)

            # Find the challenges using the query and sort criteria
            challenges = list(challenges_collection.find(query).sort(sort_criteria).skip(offset).limit(limit))

            # Convert ObjectId to string for all challenges
            for challenge in challenges:
                challenge['_id'] = str(challenge['_id'])

            # Count the total number of documents that match the query
            total_count = challenges_collection.count_documents(query)
            return challenges, total_count
        except Exception as e:
            return {"msg": str(e)}, 500
