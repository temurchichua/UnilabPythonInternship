from flask import Flask, render_template


app = Flask(__name__)

products = [
    {"name": "Service One" , "description" : "A brief description of our first amazing service.", "img": "img-1.jpg",  "price": 300, "id": 0 },
    {"name": "Service Two", "description": "Discover how we can help with this incredible offering.", "img": "img-2.jpg","price": 350, "id": 1 },
    {"name": "Service Three", "description": "Learn more about our third unique service.", "img": "img-3.jpg", "price" : 400, "id": 2},
    {"name": "Service Three", "description": "Learn more about our third unique service.", "img": "img-3.jpg", "price": 400, "id": 3},
    {"name": "Service Three", "description": "Learn more about our third unique service.", "img": "img-3.jpg", "price": 400, "id": 4},
]


@app.route("/")
def index():
    return render_template("index.html", product_list= products)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/product/<int:product_id>")
def view_product(product_id):
    return render_template("product.html", product=products[product_id])

if __name__ == "__main__":
    app.run(debug=True)
