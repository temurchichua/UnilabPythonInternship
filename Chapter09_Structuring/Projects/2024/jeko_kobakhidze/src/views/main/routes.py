from flask import render_template, Blueprint

main_bp = Blueprint('main', __name__, template_folder='../../templates/main')

@main_bp.route('/')
def home():
    return render_template('home.html')
