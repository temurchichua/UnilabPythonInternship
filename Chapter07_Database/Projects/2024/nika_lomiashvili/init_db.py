from app import db, app, Product

with app.app_context():
    db.create_all()