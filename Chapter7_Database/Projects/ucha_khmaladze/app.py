import os
from flask import Flask, render_template, url_for, flash, redirect, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from forms.forms import FormName, FormBook

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ITISHUGESECRET'
db = SQLAlchemy(app)
Migrate(app, db)
serverPort = 8085

pages = (
    ("home", "Home"),
    ("book", "Book now"),
    ("rooms", "Rooms"),
    ("contact", "Contact us"),
)

table_headers = ["#", "Room Type", "Price", "Quantity"]

table_rows = (
    (1, "Double", "80$", 20),
    (2, "Triple", "110$", 5),
    (3, "Quadruple", "130$", 5),
    (4, "Family", "150$", 4)
)

table = {
    "headers": table_headers,
    "rows": table_rows
}

class UserInfo(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, name, last_name, email):
        self.name = name
        self.last_name = last_name
        self.email = email

    @classmethod
    def read(cls,email):
        return cls.query.filter_by(email=email).first()


    def add(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):

        return f'you have done great {self.name} {self.last_name} your email is {self.email}'

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", pages=pages)

@app.route("/book", methods=['GET', 'POST'])
def book():

    name = None
    lastname = None
    date_from = None
    date_to = None
    select_adult = None
    select_child = None
    form = FormBook()

    if form.validate_on_submit():
        session['name'] = form.name.data
        session['lastname'] = form.lastname.data
        session['date_from'] = form.date_from.data
        session['date_to'] = form.date_to.data
        session['select_adult'] = form.select_adult.data
        session['select_child'] = form.select_child.data

        return redirect(url_for("thank_you"))

    return render_template("book_now.html", pages=pages, form=form, name=name, lastname=lastname, date_from=date_from,
                           date_to=date_to, select_adult=select_adult, select_child=select_child)


@app.route("/thank_you")
def thank_you():
    return render_template("thankyou.html")


@app.route("/rooms")
def rooms():
    return render_template("room_info.html", pages=pages, table=table)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    name = None
    lastname = None
    email = None
    form = FormName()

    if form.validate_on_submit():
        name = form.name.data
        lastname = form.lastname.data
        email = form.email.data
        if UserInfo.read(email):
            pass
        else:
            item = UserInfo(name, lastname, email)
            item.add()
        flash(f"Thank you {name} {lastname} you have successfully sent us a message, we will reach you back on {email}")

        return redirect(url_for("contact"))

    return render_template("contact_us.html", pages=pages, form=form, name=name, lastname=lastname, email=email)


if __name__ == "__main__":
    app.run(port=serverPort, debug=True)
