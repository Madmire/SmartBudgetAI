  from flask import Flask
from flask_cors import CORS
from routes.user import user_bp
from routes.budget import budget_bp
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Configuration de la base de données MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/SmartBudget"
client = MongoClient(app.config["MONGO_URI"])
db = client["Smartbudget"]

# Enregistrement des Blueprints
app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(budget_bp, url_prefix="/api/budget")

@app.route("/")
def home():
    return "Bienvenue sur SmartBudgetAI !"

if __name__ == "__main__":
    app.run(debug=True)

