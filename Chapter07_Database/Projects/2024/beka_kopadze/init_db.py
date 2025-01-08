from app import db, app, Personal

with app.app_context():
    db.create_all()