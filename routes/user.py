from flask import Blueprint, request, jsonify
from pymongo import MongoClient

user_bp = Blueprint("user", __name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["SmartBudget"]
users_collection = db["Users"]

@user_bp.route("/", methods=["POST"])
def create_user():
    user_data = request.get_json()
    users_collection.insert_one(user_data)
    return jsonify({"message": "Utilisateur ajouté avec succès!"}), 201

@user_bp.route("/", methods=["GET"])
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))
    return jsonify(users), 200
