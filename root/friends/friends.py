from pymongo import MongoClient
from root.config import Config

# Ініціалізація MongoDB
client = MongoClient(Config.MONGO_URI)
db = client["my_db"]
friends_collection = db["friends"]

class FriendManager:
    def __init__(self):
        self.db = db

    def add_friend(self, user_email, friend_email):
        # Перевірка, чи вже є зв'язок між користувачами
        existing_friendship = friends_collection.find_one({"email": user_email})
        if existing_friendship and friend_email in existing_friendship.get("friends", []):
            return {"error": "This user is already a friend."}

        # Додавання друга для користувача
        friends_collection.update_one(
            {"email": user_email},
            {"$push": {"friends": friend_email}},
            upsert=True
        )

        # Додавання користувача до списку друзів іншого користувача
        friends_collection.update_one(
            {"email": friend_email},
            {"$push": {"friends": user_email}},
            upsert=True
        )

        return {"msg": "Friend added successfully."}

    def get_friends(self, user_email):
        user_friends = friends_collection.find_one({"email": user_email})
        if user_friends:
            return user_friends.get("friends", [])
        return None
