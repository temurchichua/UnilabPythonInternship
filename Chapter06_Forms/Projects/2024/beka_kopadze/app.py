from flask import Flask, render_template, url_for, request, redirect
from forms import PersonalForm

from os import path
from uuid import uuid4

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisiskey"
UPLOAD_PATH = path.join(app.root_path, "static")
READ_PATH = path.join("static")

personal = [
    {"name": "ბექა", "surname": "კოპაძე", "image": "static/avicuga.png", "id": 0}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html', personal = personal)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/add_personal', methods=['GET', 'POST'])
def add_personal():
    form = PersonalForm()
    if form.validate_on_submit():
        file = form.image.data
        filename, file_extension = path.splitext(file.filename)
        filename = f"{uuid4()}{file_extension}"

        directory = path.join(UPLOAD_PATH, filename)
        file.save(directory)
        new_personal = {
            "name": form.name.data,
            "surname": form.surname.data,
            "image": path.join(READ_PATH,filename),
            "id": len(personal)
        }

        personal.append(new_personal)
        print("validated")
        return redirect(url_for('index'))
    else:
        print(form.errors)
    return render_template('add_personal.html', form = form)

@app.route('/edit_personal/<int:personal_id>', methods=['GET', 'POST'])
def edit_personal(personal_id):
    person = personal[personal_id]
    form = PersonalForm(name = person["name"], surname = person["surname"], image = person["image"])


    #see 55 minutes on lecture
    if form.validate_on_submit():
        person["name"] = form.name.data
        person["surname"] = form.surname.data
        person["image"] = form.image.data

        print("validated")
        return redirect(url_for('index'))
    else:
        print(form.errors)
    return render_template('add_personal.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)

print(__name__)