from flask import Blueprint, render_template
from src.models.product import Product

products_bp = Blueprint('products', __name__, template_folder='../../templates/products')

@products_bp.route('/')
def products():
    product_list = Product.query.all()
    return render_template('products.html', products=product_list)
