from flask import Blueprint, request, jsonify
from pymongo import MongoClient,User

user_routes = Blueprint("user", __name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["SmartBudget"]
users_collection = db["Users"]

@user_routes.route("/", methods=["POST"])
def create_user():
    user_data = request.get_json()
    users_collection.insert_one(user_data)
    return jsonify({"message": "Utilisateur ajouté avec succès!"}), 201

@user_routes.route("/", methods=["GET"])
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))
    return jsonify(users), 200


@user_routes.route('/profile')
def profile():
    user = User.query.first()  # Exemple : récupérer le premier utilisateur
    return render_template('profile.html', user=user)

@user_routes.route('/update', methods=['POST'])
def update_balance():
    new_balance = request.form['balance']
    user = User.query.first()
    user.balance = new_balance
    db.session.commit()
    return redirect(url_for('user_routes.profile'))