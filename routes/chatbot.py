from flask import Blueprint, render_template

chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/')
def start():
    return render_template('chatbot.html')
