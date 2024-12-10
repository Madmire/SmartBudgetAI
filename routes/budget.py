from flask import Blueprint, request, jsonify
from pymongo import MongoClient

budget_bp = Blueprint("budget", __name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["SmartBudget"]
budget_collection = db["budget"]

@budget_bp.route("/", methods=["POST"])
def create_budget():
    budget_data = request.get_json()
    budget_collection.insert_one(budget_data)
    return jsonify({"message": "Budget ajouté avec succès!"}), 201

@budget_bp.route("/", methods=["GET"])
def get_budgets():
    budgets = list(budget_collection.find({}, {"_id": 0}))
    return jsonify(budgets), 200
