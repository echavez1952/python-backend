# services/product_service.py

from bson import ObjectId
from fastapi import HTTPException

from database.mongo import db

product_collection = db["products"]
item_collection = db['items']

# Obtener todos los products que hay en la base - funciona ok
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
"""
# Crear un producto - JSON y form-data
def create_product(title: str, component_id: str):
    product_data = {
        "title": title,
        "component_id": component_id
    }
    result = product_collection.insert_one(product_data)

    # agregar el id generado a la respuesta
    product_data["_id"] = str(result.inserted_id)
    return {
       "message": "Product created successfully",
       "product": product_data
    }
"""

def create_product(title: str, component_id: str):
    product_data = {
        "title": title,
        "component_id": component_id  # se guarda como string
    }
    result = product_collection.insert_one(product_data)
    product_data["_id"] = str(result.inserted_id)
    return {
        "message": "Product created successfully",
        "product": product_data
    }


# Obtener los productos de un componente especifico - funciona ok
def get_products_by_component(component_id: str):
    products = list(product_collection.find({"component_id": component_id}))
    for p in products:
        p["_id"] = str(p["_id"])
    return products


# Obtener un producto por la ID - funciona ok
def get_product_by_id(product_id: str):
    try:
        product = product_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            return None

        # Convertir ObjectId a string y normalizar datos
        return {
            "_id": str(product["_id"]),
            "title": product.get("title", ""),
            "component_id": str(product.get("component_id", "")),
        }
    except Exception as e:
        print(f"Error getting product by id: {e}")
        return None


# Editar un producto (NO funciona)
def update_product(product_id, title, component_id):
    product = product_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        return {"message": "Product not found"}
    update_data = {
        "title": title,
        "component_id": component_id
    }
    result = product_collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})

    if result.modified_count == 0:
        return {"message": "No changes made (title is the same)"}

    return {
        "message": "Product title updated successfully",
        "product": {
            "_id": str(product["_id"]),
            "title": title,
            #"component_id": str(product["component_id"])
        }
    }



# Eliminar producto (funciona ok solo eliminación del producto
def delete_product(product_id):

# Verificar que el producto exista antes de borrar
    product = product_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

# Eliminamos en cascada los items hijos del producto
#    deleted_items = items_collection.delete_many(product_id)

# Luego eliminamos el producto
    result = product_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        return {"message": "Product not found"}

    return {
        "message": "Product (and related items) deleted successfully",
        #"deleted_items_count": deleted_items.deleted_count
        }



