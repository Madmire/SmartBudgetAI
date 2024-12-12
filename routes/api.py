from flask import Blueprint, request, jsonify
from models.user import create_user

user_routes = Blueprint('user_routes', __name__)

@user_routes.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    user_id = create_user(mongo, data)
    return jsonify({"message": "Utilisateur enregistré avec succès", "user_id": str(user_id)}), 201
