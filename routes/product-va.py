# routes/product-va.py

import uuid
from fastapi import APIRouter, Form, HTTPException
from services.product_service import (
    create_product,
    get_products,
    get_products_by_component,
    get_product_by_id,
    update_product,
    delete_product
)

router = APIRouter(prefix="/product", tags=["product"])

# Obtener todos los productos que hay en la db
@router.get('/')
def get_products_route():
    return get_products()

# Obtener productos de un componente específico
@router.get("/component/{component_id}")
def get_products_by_component_route(component_id: str):
    return get_products_by_component(component_id)

# Obtener un producto por la ID
@router.get("/{product_id}")
def get_product_route(product_id: str):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Crear un producto
@router.post('/')
def create_product_route(
    title: str = Form(...),
    component_id: str = Form(...),
):
    return create_product(title, component_id)

"""
# Listar productos de un componente
@router.get("/{component_id}")
def get_products_by_component_route(component_id: str):
    return get_products_by_component(component_id)
"""

# Editar producto
@router.put("/{product_id}")
def update_product_route(
    product_id: str,
    title: str = Form(...),
    price: float = Form(...),
    description: str = Form(None),
    note: str = Form(None),
    component_id: str = Form(...),
    file: UploadFile = File(None)
):
    return update_product(product_id, title, price, description, note, component_id, file)

# Eliminar producto
@router.delete("/{product_id}")
def delete_product_route(product_id: str):
    return delete_product(product_id)
