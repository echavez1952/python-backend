# routes/item.py

import uuid
from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from models.Item import ItemCreate
from services.item_service import (
    get_items,
    create_item,
    update_item,
    delete_item,
    list_items_by_product,
    get_item_by_id
)

router = APIRouter(prefix="/item", tags=["item"])


# Obtener todos los items que hay en la base
@router.get('/')
def get_items_route():
    return get_items()


# ***********
# Crear item - usando JSON (sin imagen)
@router.post('/{product_id}')
def create_item_json(product_id: str, item: ItemCreate):
    return create_item(item, product_id)


# ***********
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


# ***********
# Editar un item usando JSON (sin imagen)
@router.put("/{item_id}")
def update_item_json(item_id: str, item: ItemCreate):
    return update_item(item_id, item.dict())

# Editar un item usando FormData (con imagen)
@router.put("/form/{item_id}")
def update_item_form(
    item_id: str,
    title: str = Form(None),
    price: float = Form(None),
    description: str = Form(None),
    file: UploadFile = File(None)
):
    item_data = {
        "title": title,
        "price": price,
        "description": description
    }
    return update_item(item_id, item_data, file)


# ***********
# Eliminar un item
@router.delete("/{item_id}")
def remove_item(item_id: str):
    return delete_item(item_id)


# ***********
# Obtener un item por la ID
@router.get("/{item_id}")
def get_item_route(item_id: str):
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# ***********
# Obtener los items de un producto específico - POSTMAN ok
@router.get("/product/{product_id}")
def list_items_by_product_route(product_id: str):
    return list_items_by_product(product_id)








