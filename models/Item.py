# models/Item.py
from pydantic import BaseModel
from typing import Optional

# Modelo para crear un ítem (hijo de un product)
# el item puede ser creado con o sin imagen

class ItemCreate(BaseModel):
    title: str
    price: float
    description: Optional[str] = None

"""
# (1) Crear item - Modelo JSON para usar desde POSTMAN, no incluye la imagen
# No se incluye el product_id  porque viene y se coge desde la URL
class ItemCreate(BaseModel):
    title: str
    price: float
    description: Optional[str] = None
    #image: Optional[str] = None   # aquí guardaremos la URL/ruta del archivo
    #product_id: str
"""

"""
class ItemCreate(BaseModel):
    title: str
    price: float
    description: Optional[str] = None
    image: Optional[str] = None   # aquí guardaremos la URL/ruta del archivo
    product_id: str

class ItemResponse(BaseModel):
    _id: str
    title: str
    price: float
    description: Optional[str] = None
    image: Optional[str] = None
    product_id: str
"""
