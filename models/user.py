from pymongo import MongoClient

class UserModel:
    def __init__(self, db):
        self.collection = db["users"]

    def create_user(self, user_data):
        return self.collection.insert_one(user_data)

    def get_all_users(self):
        return list(self.collection.find({}, {"_id": 0}))

