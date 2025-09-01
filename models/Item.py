# models/Item.py
from pydantic import BaseModel
from typing import Optional

# Modelo para crear un ítem (hijo de un product)
# el item puede ser creado con o sin imagen

class ItemCreate(BaseModel):
    title: str
    price: float
    description: Optional[str] = None

