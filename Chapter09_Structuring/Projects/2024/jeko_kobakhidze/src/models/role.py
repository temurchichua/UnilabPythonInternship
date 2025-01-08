from src.ext import db
from src.models.base import BaseModel

class Role(BaseModel):
    name = db.Column(db.String(50), unique=True, nullable=False)
