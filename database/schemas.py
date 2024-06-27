from typing import Union
from datetime import datetime

from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str
    price: float
    description: Union[str, None] = None
    img: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()



class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int