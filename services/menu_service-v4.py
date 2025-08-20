# services/menu_service.py - lógica para listar componentes del menu

from database.mongo import db
from models.Menu import MenuComponent
from bson import ObjectId
from fastapi import HTTPException

menu_collection = db["menu_components"]
product_collection = db["products"]

#Crear un componente del menu
def create_menu_component(component: MenuComponent):
    data = component.model_dump()
    menu_collection.insert_one(data)
    return {"message": "Component created succesfully"}

# Listar todos los componentes
def get_all_components():
    components = menu_collection.find()
    results = []
    for item in components:
        item["_id"] = str(item["_id"])
        results.append(item)
    return results

# Obtener un componente por ID
def get_component(component_id: str):
    component = menu_collection.find_one({"_id": ObjectId(component_id)})
    if not component:
        return {"message": "Component not found"}
    component["_id"] = str(component["_id"])
    return component

# Editar componente por Id
def update_menu_component(component_id: str, component: MenuComponent):
    update_data = component.model.dump()
    result = menu_collection.update_one(
        {"_id": ObjectId(component_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        return {"message": "Component not found"}
    return {"message": "Component updated successfully"}

# Eliminar componente y sus productos hijos
def delete_menu_component(component_id: str):
    try:
        object_id = ObjectId(component_id)  # Valida que el component_id tenga formato correcto de ObjectId.
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid component_id format")

# Verificar que el componente exista antes de borrar
    component = menu_collection.find_one({"_id": object_id})
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

# Eliminar el componente
    menu_result = menu_collection.delete_one({"_id": object_id})
    if menu_result.deleted_count == 0:
        return {"message": "Component not found"}

# Eliminar en cascada todosl los products cuyo component_id coincida con el del padre.
    deleted_items = product_collection.delete_many({"component_id": object_id})
    return {
        "message": "Component and related products deleted successfully",
        "deleted_items_count": deleted_items.deleted_count
    }

