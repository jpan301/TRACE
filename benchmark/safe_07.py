from flask import request
from sqlalchemy.orm import Session
from myapp.models import Product

def get_product(request, db: Session):
    pid = request.args.get("pid")
    return db.query(Product).filter(Product.id == pid).first()
