# models/Product.py
from pydantic import BaseModel

# Modelo para crear productos hijos de un componente
class ProductCreate(BaseModel):
    title: str
    component_id: str   # ID del componente padre