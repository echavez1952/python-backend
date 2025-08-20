# services/menu_service.py - lógica para listar componentes del menu

from database.mongo import db
from models.Menu import MenuComponent
from bson import ObjectId
from fastapi import HTTPException

menu_collection = db["menu_components"]
product_collection = db["products"]

#Crear un componente del menu
def create_component(component: MenuComponent):
    data = component.model_dump()
    menu_collection.insert_one(data)
    return {"message": "Component created succesfully"}

"""
def create_component(name: str, description: str = None):
    new_component = {
        "name": name,
        "description": description
    }
    result = menu_collection.insert_one(new_component)
    return {"message": "Component created successfully", "id": str(result.inserted_id)}
"""

# Listar todos los componentes
def get_all_components():
    components = menu_collection.find()
    results = []
    for c in components:
        c["_id"] = str(c["_id"])
        results.append(c)
    return results

# Obtener un componente por ID
def get_component_by_id(component_id: str):
    try:
        component = menu_collection.find_one({"_id": ObjectId(component_id)})
        if not component:
            raise HTTPException(status_code=404, detail="Component not found")
        component["_id"] = str(component["_id"])
        return component
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid component ID")

# Editar componente por Id
def update_component(component_id: str, component: MenuComponent):
    update_data = component.model.dump()
    result = menu_collection.update_one(
        {"_id": ObjectId(component_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        return {"message": "Component not found"}
    return {"message": "Component updated successfully"}

"""
def update_component(component_id: str, name: str, description: str = None):
    try:
        result = menu_collection.update_one(
            {"_id": ObjectId(component_id)},
            {"$set": {"name": name, "description": description}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Component not found")
        return {"message": "Component updated successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid component ID")
"""

# Eliminar componente y sus productos hijos
def delete_component(component_id: str):
    try:
        object_id = ObjectId(component_id)  # Valida que el component_id tenga formato correcto de ObjectId.
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid component_id format")

# Verificar que el componente exista antes de borrar
    component = menu_collection.find_one({"_id": object_id})
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

# Primero eliminamos en cascada los productos hijos cuyo component_id coincida con el del padre.
    deleted_products = product_collection.delete_many({"component_id": component_id})

# Luego eliminamos el componente
    result = menu_collection.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        return {"message": "Component not found"}

    return {
        "message": "Component and related products deleted successfully",
        "deleted_products_count": deleted_products.deleted_count
    }

