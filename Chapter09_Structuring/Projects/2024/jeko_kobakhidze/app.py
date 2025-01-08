from flask import Flask
from src.ext import db
from src.config import Config
from src.views.auth.routes import auth_bp
from src.views.main.routes import main_bp
from src.views.products.routes import products_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(products_bp, url_prefix='/products')

if __name__ == '__main__':
    app.run(debug=True)
