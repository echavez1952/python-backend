# models/Product.py
from pydantic import BaseModel
from typing import Optional

# Modelo para crear un producto (hijos de un componente)
class Product(BaseModel):
    title: str
    price: float
    description: Optional[str] = None
    note: Optional[str] = None
    image_url: Optional[str] = None
    component_id: str  # ID del componente padre