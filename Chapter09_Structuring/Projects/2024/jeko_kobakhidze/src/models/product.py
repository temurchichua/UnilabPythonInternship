from src.ext import db
from src.models.base import BaseModel

class Product(BaseModel):
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
