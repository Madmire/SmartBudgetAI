from flask import Blueprint, request, render_template
from models.user import User

budget = Blueprint('budget', __name__)

@budget.route('/update', methods=['POST'])
def update_budget():
    # Logique pour mettre à jour le budget et générer des statistiques
    return render_template('dashboard.html', statistics=statistics)
