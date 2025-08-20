# services/product_service.py

import shutil
import uuid
from pathlib import Path
from bson import ObjectId
from pydantic_core.core_schema import none_schema

from database.mongo import db

product_collection = db["products"]

def get_products():
    try:
        print("Conectando a MongoDB...")
        results = []
        products = list(product_collection.find())
        for prod in products:
            print("Producto:", prod)
            prod["_id"] = str(prod["_id"])
            results.append(prod)
            print(f"Total products: {len(results)}")
        return results
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return {"error": "No se pudo obtener la lista de productos"}

# Crear producto con imagen
def create_product(title, price, description, note, component_id, file):
    image_url = None
    if file:
        file_name = f"{uuid.uuid4()}_{file.filename}"
        path_name = Path("uploads")
        path_name.mkdir(parents=True, exist_ok=True)
        destination = path_name / file_name

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_url = f"http://localhost:8000/{destination}"

    product_data = {
        "title": title,
        "price": price,
        "description": description,
        "note": note,
        "image": image_url,
        "component_id": component_id
    }
    product_collection.insert_one(product_data)
    return {"message": "Product created successfully"}

# Obtener productos de un componente especifico
def get_products_by_component(component_id: str):
    products = list(product_collection.find({"component_id": component_id}))
    for p in products:
        p["_id"] = str(p["_id"])
    return products

# Editar producto
def update_product(product_id, title, price, description, note, component_id, file):
    product = product_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        return {"message": "Product not found"}

    image_url = product.get("image")
    if file:
        file_name = f"{uuid.uuid4()}_{file.filename}"
        path_name = Path("uploads")
        path_name.mkdir(parents=True, exist_ok=True)
        destination = path_name / file_name
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_url = f"http://localhost:8000/{destination}"

    update_data = {
        "title": title,
        "price": price,
        "description": description,
        "note": note,
        "image": image_url,
        "component_id": component_id
    }

    product_collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    return {"message": "Product updated successfully"}

# Eliminar producto
def delete_product(product_id):
    result = product_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        return {"message": "Product not found"}
    return {"message": "Product deleted successfully"}

# Obtener un producto por la ID
def get_product_by_id(product_id: str):
    try:
        product = product_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            return None

        # Convertir ObjectId a string y normalizar datos
        return {
            "_id": str(product["_id"]),
            "title": product.get("title", ""),
            "description": product.get("description", ""),
            "price": product.get("price", 0.0),
            "note": product.get("note", ""),
            "image": product.get("image", ""),
            "component_id": str(product.get("component_id", "")),
        }
    except Exception as e:
        print(f"Error getting product by id: {e}")
        return None


"""
Este es un modelo valido para Obtener un producto por la ID
# Obtener un producto por la id
def get_product_by_id(id: str):
    result = products.find_one({'_id': ObjectId(id)})
    print("Producto encontrado:", result)
    if not result:
        print("Producto no encontrado")
        raise HTTPException(status_code=404, detail='Producto no encontrado')
    result['_id'] = str(result['_id'])
    return result
"""