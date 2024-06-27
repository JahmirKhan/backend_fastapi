from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder

import sqlalchemy
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List

from database import models
from database import schemas
from database import crud
from database.database import SessionLocal, engine

from icecream import ic

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

IMAGEDIR = './images/'

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






@app.get("/items/", response_model=List[schemas.Item])
async def read_items(db: Session = Depends(get_db)):
    items = crud.get_items(db=db)
    if items is None:
        raise HTTPException(status_code=404, detail='There is not items')
    return items


@app.get('/items/filter', response_model=List[schemas.Item])
async def read_items_price(price: float = 0, db: Session = Depends(get_db)):
    items = crud.get_items_with_price(db=db, price=price)
    if items is None:
        raise HTTPException(status_code=404, detail='no items under this price')

    return items


@app.get('/items/{id}', response_model=schemas.Item)
async def read_item(id: int, db: Session = Depends(get_db)):
    item = crud.get_item(id=id, db=db)
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
      
    return item


@app.post('/items/', response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = crud.create_item(item=item,db=db)
    return item

@app.delete('/items/{id}', response_model=schemas.Item)
async def delete_item(id: int, db: Session = Depends(get_db)):
    deleted_item = crud.delete_item(id=id, db=db)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return deleted

@app.put('/items/{id}', response_model=schemas.Item)
async def change_item(id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    changed_item = crud.change_item(id=id, db=db, item=item)
    if changed_item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return changed_item        


"""Это все хуйня от которой нужно избавиться, но жалко("""
# @app.get("/items/{id}", response_model=ItemResponse)
# async def read_item(id: int, db: Session = Depends(get_db)):
#     db_item = db.query(Item).filter(Item.id == id).first()
#     if db_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return db_item

# @app.post("/items/", response_model=list[schemas.Item])
# async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
#     db_item = Item(**item.model_dump()) 
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# @app.delete("/items/{id}")
# async def delete_user(id: int, db: Session = Depends(get_db)):
#     print(id)
#     user_to_delete = db.query(Item).filter(Item.id == id).first()
#     if user_to_delete:
#         db.delete(user_to_delete)
#         db.commit()
#         return True
#     else:
#         return {'User not found'}


# @app.put('/items/{id}', response_model=ItemResponse)
# async def update_item(id: int, item: ItemCreate, db: Session = Depends(get_db)):
#     ic(id, item)
#     db_item = db.query(Item).get(id)

#     for key, value in item.dict().items():
#         setattr(db_item, key, value)

#     db.commit()

#     return db_item

# # API endpoint to get image

# @app.get("/imgs/{img}")
# async def read_random_file(img: str):

#     # get random file from the image directory
#     files = os.listdir(IMAGEDIR)

#     path = f"{IMAGEDIR}{img}"
#     return FileResponse(path)