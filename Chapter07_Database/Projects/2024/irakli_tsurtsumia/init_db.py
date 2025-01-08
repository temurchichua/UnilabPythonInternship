from app import db, app, User

with app.app_context():
    db.create_all()
