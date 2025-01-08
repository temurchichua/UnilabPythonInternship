from src.models.product import Product
from src.ext import db
def seed_products():
    products = [
        Product(name="python course", description="you learn how to create web app", price=10),
        Product(name="marketing", description="sfgsrge3", price=20.0),
    ]
    db.session.add_all(products)
    db.session.commit()
