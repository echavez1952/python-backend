# routes/item.py

import uuid
from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from models.Item import ItemCreate
from services.item_service import (
    create_item,
    get_items)

router = APIRouter(prefix="/item", tags=["item"])

# Crear item - usando JSON (sin imagen)
@router.post('/{product_id}')
def create_item_json(product_id: str, item: ItemCreate):
    return create_item(item, product_id)

# Crear item - usando FormData (con imagen)
@router.post('/form/{product_id}')
def create_item_form(
    product_id: str,
    title: str = Form(...),
    price: float = Form(...),
    description: str = Form(None),
    file: UploadFile = File(None)
):
    item = ItemCreate(title=title, price=price, description=description)
    return create_item(item, product_id, file)






