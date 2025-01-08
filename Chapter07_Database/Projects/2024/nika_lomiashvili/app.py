from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import ProductForm, RegisterField
from os import path, remove
from uuid import  uuid4

BASE_DIRECTORY = path.abspath(path.dirname(__file__))
UPLOAD_PATH = path.join(BASE_DIRECTORY, "static")

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdasdasdasd"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path.join(BASE_DIRECTORY, "database.db")

db = SQLAlchemy(app)




class Product(db.Model):

    __tablename__ = "product"
    id = db.Column(db.Integer(), primary_key= True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    description = db.Column(db.String())
    img = db.Column(db.String())



@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", product_list= products)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterField()
    if form.validate_on_submit():
        print(form.data)
    return render_template('register.html', form=form)

@app.route("/product/<int:product_id>")
def view_product(product_id):
    product = Product.query.get(product_id)
    return render_template("product.html", product=product)

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():

        file = form.img.data
        filename , ext = path.splitext(file.filename)
        filename = f"{uuid4()}{ext}"

        directory = path.join(UPLOAD_PATH, filename)
        file.save(directory)

        new_product = Product(name=form.name.data,
                              price=form.price.data,
                              description=form.description.data,
                              img=filename)
        db.session.add(new_product)
        db.session.commit()

        print('Validated')
        return redirect(url_for("index"))
    else:
        print(form.errors)
    return render_template("add_product.html" , form=form)


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price, description=product.description)

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data

        if form.img.data:
            file = form.img.data
            filename, ext = path.splitext(file.filename)
            filename = f"{uuid4()}{ext}"
            directory = path.join(UPLOAD_PATH, filename)
            file.save(directory)
            product["img"] = filename
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("add_product.html", form=form, product=product)  


@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    product = Product.query.get(product_id)

    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("index"))
if __name__ == "__main__":
    app.run(debug=True)

