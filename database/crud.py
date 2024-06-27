from sqlalchemy.orm import Session
from . import crud
from . import models
from . import schemas

from icecream import ic
from datetime import datetime


def get_items(db: Session):
    return db.query(models.Item).all()

def get_item(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()

def get_items_with_price(db: Session, price: float):
    return db.query(models.Item).filter(models.Item.price < price).all()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, id: int):
    delete_item = db.query(models.Item).filter(models.Item.id == id).first()
    if delete_item:
        db.delete(delete_item)
        db.commit()
        return delete_item
    return False

def change_item(db: Session, id: int, item: schemas.ItemCreate):
    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    updated_at = datetime.now()

    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db_item.updated_at = updated_at

    db.commit()
    return db_item

 
