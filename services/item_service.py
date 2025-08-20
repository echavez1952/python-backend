# services/item_service.py

import shutil, uuid
from pathlib import Path
from bson import ObjectId
from pydantic_core.core_schema import none_schema
from fastapi import HTTPException
from models.Item import ItemCreate
from database.mongo import db

items_collection = db["items"]


# ***********
# Obtener todos los items que hay en la base
def get_items():
    try:
        print("Conectando a MongoDB...")
        results = []
        items = list(items_collection.find())
        for it in items:
            print("Item:", it)
            it["_id"] = str(it["_id"])
            results.append(it)
            print(f"Total items: {len(results)}")
        return results
    except Exception as e:
        print(f"Error al obtener items: {e}")
        return {"error": "No se pudo obtener la lista de items"}


# ***********
# item es un hijo de product
# Crear un item - usando JSON (sin imagen)
# Crear un item - usando FormData (con image)

def create_item(item, product_id: str, file=None):
    image_url = None

    # Si viene un archivo, lo guardamos en /uploads
    if file:
        file_name = f"{uuid.uuid4()}_{file.filename}"
        path_name = Path("uploads")
        path_name.mkdir(parents=True, exist_ok=True)
        destination = path_name / file_name

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        image_url = f"http://localhost:8000/{destination}"

    item_data = {
        "title": item.title,
        "price": item.price,
        "description": item.description,
        "image": image_url,
        "product_id": product_id
    }

    result = items_collection.insert_one(item_data)
    item_data["_id"] = str(result.inserted_id)
    return {
        "message": "Item created successfully",
        "item": item_data
    }


# ***********
# Editar un item usando JSON (sin imagen)
# Editar un item usando FormData (con imagen)

def update_item(item_id: str, item_data: dict, file=None):
    existing_item = items_collection.find_one({"_id": ObjectId(item_id)})
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_fields = {}

    # Si se manda un archivo, guardarlo y actualizar el campo image
    if file:
        file_name = f"{uuid.uuid4()}_{file.filename}"
        path_name = Path("uploads")
        path_name.mkdir(parents=True, exist_ok=True)
        destination = path_name / file_name

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        update_fields["image"] = f"http://localhost:8000/{destination}"

    # Agregar los demás campos del item
    for key, value in item_data.items():
        if value is not None:
            update_fields[key] = value

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    items_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": update_fields}
    )

    updated_item = items_collection.find_one({"_id": ObjectId(item_id)})
    updated_item["_id"] = str(updated_item["_id"])
    return {
        "message": "Item updated successfully",
        "item": updated_item
    }


# ***********
# Eliminar un item
def delete_item(item_id: str):
    result = items_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}


# ***********
# Obtener un item por la ID
def get_item_by_id(item_id: str):
    try:
        item = items_collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            return None

        # Convertir ObjectId a string y normalizar datos
        return {
            "_id": str(item["_id"]),
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "price": item.get("price", 0.0),
            "image": item.get("image", ""),
            "product_id": str(item.get("product_id", "")),
        }
    except Exception as e:
        print(f"Error getting itemt by id: {e}")
        return None


# ***********
# Obtener los items de un producto específico - OK
def list_items_by_product(product_id: str):
    items = list(items_collection.find({"product_id": product_id}))
    if not items:
        raise HTTPException(status_code=404, detail="No se encontraron ítems para este producto")
    for it in items:
        it["_id"] = str(it["_id"])
    return items






