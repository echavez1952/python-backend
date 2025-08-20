# routes/product.py

from fastapi import APIRouter, Form, HTTPException
from models.Product import ProductCreate
from services.product_service import (
    get_products,
    create_product,
    get_products_by_component,
    get_product_by_id,
    update_product,
    delete_product
)

router = APIRouter(prefix="/product", tags=["product"])

# Obtener todos los products que hay en la base - funciona okq
@router.get('/')
def get_products_route():
    return get_products()

"""
# Crear un producto, desde una forma
@router.post('/')
def create_product_route(
    title: str = Form(...),
    component_id: str = Form(...),
):
    return create_product(title, component_id)
"""

# Crear un producto - POSTMAN funciona ok
@router.post('/')
def create_product_route(product: ProductCreate):
    return create_product(product.title, product.component_id)

# Obtener los products de un componente específico - funciona ok
@router.get("/component/{component_id}")
def get_products_by_component_route(component_id: str):
    return get_products_by_component(component_id)
# Explicacion del uso de la ruta /product/component/
# /product/component/{component_id} → todos los productos que pertenecen a ese componente.
# /product/component/68a134f4e6ed840f0149eeef
# significa “dame todos los productos del componente con id X”.


# Obtener un producto por la ID - funciona ok
@router.get("/{product_id}")
def get_product_route(product_id: str):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



"""
# Editar un producto
@router.put("/{product_id}")
def update_product_route(
    product_id: str,
    title: str = Form(...),
    component_id: str = Form(...),
):
    return update_product(product_id, title, component_id)
"""
"""
@router.put("/{product_id}/form")
def update_product_title_route(product_id: str, title: str = Form(...)):
    return update_product_title(product_id, title)
"""

# Editar un producto (NO funciona)
@router.put("/{product_id}")
def update_product_route(product_id: str, title: str, component_id: str):
    return update_product(product_id, title, component_id)


# Eliminar producto - funciona ok
@router.delete("/{product_id}")
def delete_product_route(product_id: str):
    return delete_product(product_id)
