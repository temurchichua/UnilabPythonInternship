from os import path

from flask import Flask, render_template, request, redirect

from forms import UserForm
from flask_sqlalchemy import SQLAlchemy

BASE_DIRECTORY = path.abspath(path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path.join(BASE_DIRECTORY, "db.sqlite")
db = SQLAlchemy(app)


##MODELS##
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50))


###########################
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def get_users():
    users = User.query.all()
    return render_template('users.html', users_list=users)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/user/<int:id>')
def get_user(id):
    user = User.query.get(id)
    return render_template("user.html", user=user)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = UserForm()

    if form.validate_on_submit():
        new_user = User(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        username=form.username.data)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/")

    else:
        print("error:", form.errors)

    return render_template("sign_in.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
