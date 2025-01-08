from flask import Flask, render_template, url_for, request, redirect

from forms import ProductForm, RegisterField
from os import path, remove
from uuid import  uuid4

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdasdasdasd"
UPLOAD_PATH = path.join(app.root_path, "static")

products = [
    {"name": "Service One" , "description" : "A brief description of our first amazing service.", "img": "img-1.jpg",  "price": 300, "id": 0 },
    {"name": "Service Two", "description": "Discover how we can help with this incredible offering.", "img": "img-2.jpg","price": 350, "id": 1 },
    {"name": "Service Three", "description": "Learn more about our third unique service.", "img": "img-3.jpg", "price" : 400, "id": 2},
    {"name": "Service Three", "description": "Learn more about our third unique service.", "img": "img-3.jpg", "price": 500, "id": 3},
    {"name": "Service Three", "description": "Learn more about our third unique service.", "img": "img-3.jpg", "price": 600, "id": 4},
]


@app.route("/")
def index():
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
    return render_template("product.html", product=products[product_id])

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():

        file = form.img.data
        filename , ext = path.splitext(file.filename)
        filename = f"{uuid4()}{ext}"

        directory = path.join(UPLOAD_PATH, filename)
        file.save(directory)

        new_product ={
            "id": len(products),
            "name" : form.name.data,
            "price": form.price.data,
            "description": form.description.data,
            "img" : file.filename
        }
        print('Validated')
        products.append(new_product)
        return redirect(url_for("index"))
    else:
        print(form.errors)
    return render_template("add_product.html" , form=form)


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = products[product_id]
    form = ProductForm(name=product["name"], price=product["price"], description=product["description"])

    if form.validate_on_submit():
        product["name"] = form.name.data
        product["price"] = form.price.data
        product["description"] = form.description.data

        if form.img.data:
            file = form.img.data
            filename, ext = path.splitext(file.filename)
            filename = f"{uuid4()}{ext}"
            directory = path.join(UPLOAD_PATH, filename)
            file.save(directory)
            product["img"] = filename

        return redirect(url_for("index"))

    return render_template("add_product.html", form=form, product=product)  # Pass product for editing


@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    product_to_delete = next((product for product in products if product['id'] == product_id), None)

    if product_to_delete:
        products.remove(product_to_delete)

        image_path = path.join(UPLOAD_PATH, product_to_delete["img"])
        if path.exists(image_path):
            remove(image_path)

        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))
if __name__ == "__main__":
    app.run(debug=True)

