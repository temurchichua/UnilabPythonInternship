from flask import Flask, render_template, url_for, request, redirect
from forms import PersonalForm
from flask_sqlalchemy import SQLAlchemy

from os import path
from uuid import uuid4

import sqlite3

app = Flask(__name__)
BASE_DIRECTORY = path.abspath(path.dirname(__file__))
UPLOAD_PATH = path.join(app.root_path, "static")

app.config["SECRET_KEY"] = "thisiskey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path.join(BASE_DIRECTORY, "database.db")


db = SQLAlchemy(app)

###Model###
class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    image = db.Column(db.String)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    personal = Personal.query.all()
    return render_template('about.html', personal=personal)\

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/add_person', methods=['GET', 'POST'])
def add_personal():
    form = PersonalForm()
    if form.validate_on_submit():
        file = form.image.data
        filename, file_extension = path.splitext(file.filename)
        filename = f"{uuid4()}{file_extension}"

        directory = path.join(UPLOAD_PATH, filename)
        file.save(directory)
        new_personal = Personal(name=form.name.data, surname=form.surname.data, image=filename)

        db.session.add(new_personal)
        db.session.commit()
        print("validated")
        return redirect(url_for('index'))
    else:
        print(form.errors)
    return render_template('add_personal.html', form = form)

@app.route('/edit_person/<int:personal_id>', methods=['GET', 'POST'])
def edit_personal(personal_id):
    person = Personal.query.get(personal_id)
    form = PersonalForm(name = person.name, surname = person.surname)

    #see 55 minutes on lecture
    if form.validate_on_submit():
        person.name = form.name.data
        person.surname = form.surname.data
        db.session.commit()
        print("validated")
        return redirect(url_for('index'))
    else:
        print(form.errors)
    return render_template('add_personal.html', form = form)

@app.route('/delete_person/<int:personal_id>', methods=['GET', 'POST'])
def delete_personal(personal_id):
    person = Personal.query.get(personal_id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('about'))

if __name__ == '__main__':
    app.run(debug=True)

print(__name__)