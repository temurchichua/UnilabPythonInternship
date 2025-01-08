from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import User
from src.ext import db
from src.views.auth.forms import RegisterForm, LoginForm

auth_bp = Blueprint('auth', __name__, template_folder='../../templates/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password.data, form.password.data):
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)
