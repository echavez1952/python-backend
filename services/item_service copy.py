# services/item_service.py

import shutil
import uuid
from pathlib import Path
from bson import ObjectId
from pydantic_core.core_schema import none_schema
from fastapi import HTTPException
from database.mongo import db

items_collection = db["items"]



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


