from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        connect_bank = request.form['connect_bank']
        user = User(username, email, password)
        user.save()

        if connect_bank == 'yes':
            return redirect(url_for('budget.connect_bank'))
        return redirect(url_for('chatbot.start'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Logique pour la connexion de l'utilisateur
    return render_template('login.html')
