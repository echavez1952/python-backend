import shutil
import uuid
from pathlib import Path
from bson import ObjectId
from fastapi import HTTPException
from database.mongo import db

product_collection = db["products"]

def get_products():
    results = []
    products = list(product_collection.find())
    for prod in products:
        prod["_id"] = str(prod["_id"])
        results.append(prod)
    return results

def get_products_by_component(component_id: str):
    try:
        products = list(product_collection.find({"component_id": component_id}))
        for prod in products:
            prod["_id"] = str(prod["_id"])
        return products
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid component ID")

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

def update_product(product_id: str, title, price, description, note, component_id, file):
    try:
        update_data = {
            "title": title,
            "price": price,
            "description": description,
            "note": note,
            "component_id": component_id
        }

        if file:
            file_name = f"{uuid.uuid4()}_{file.filename}"
            path_name = Path("uploads")
            path_name.mkdir(parents=True, exist_ok=True)
            destination = path_name / file_name
            with destination.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            update_data["image"] = f"http://localhost:8000/{destination}"

        result = product_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")

        return {"message": "Product updated successfully"}

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID")

def delete_product(product_id: str):
    try:
        result = product_collection.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID")
