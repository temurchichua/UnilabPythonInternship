from flask import Flask, render_template, redirect, url_for, flash
from models import db, User
from forms import RegistrationForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data

        new_user = User(username=username, email=email)

        db.session.add(new_user)
        db.session.commit()

        flash(f"User {username} has been successfully registered!", 'success')
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('index.html', form=form, users=users)


if __name__ == "__main__":
    app.run(debug=True)
