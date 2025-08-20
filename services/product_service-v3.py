from pathlib import Path
from database.mongo import db
from bson import ObjectId
from fastapi import HTTPException
import shutil
import uuid

product_db = db['product']

def create_product(title, description, file):
    file_name = str(uuid.uuid4()) + "_" + file.filename
    path_name = Path('uploads')
    path_name.mkdir(exist_ok=True)  # Crea la carpeta si no existe
    destination = path_name / file_name

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    url = f"http://localhost:8000/{destination}"
    product_db.insert_one({
        "title": title,
        "description": description,
        "image": url
    })

    return {"message": "Product created successfully"}

def get_products():
    products = list(product_db.find())
    for p in products:
        p["_id"] = str(p["_id"])
    return products

def delete_product(product_id: str):
    try:
        object_id = ObjecttId(product_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    result = product_db.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

def update_product(product_id: str, title: str, description: str, file=None):
    try:
        object_id = ObjectId(product_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    update_data = {
        "title": title,
        "description": description
    }
    # Si se sube un nuevo archivo
    if file:
        file_name = str(uuid.uuid4()) + "_" + file.filename
        path_name = Path('uploads')
        path_name.mkdir(exist_ok=True)
        destination = path_name / file_name

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        url = f"http://localhost:8000/{destination}"
        update_data["image"] = url

    result = product_db.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product update successfully"}





