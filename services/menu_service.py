# services/menu_service.py - lógica para listar componentes del menu

from database.mongo import db
from models.Menu import MenuComponent
from bson import ObjectId
from fastapi import HTTPException

menu_collection = db["menu_components"]
product_collection = db["products"]
item_collection = db["items"]

# Crear un componente del menu
def create_component(component: MenuComponent):
    data = component.model_dump()
    menu_collection.insert_one(data)
    return {"message": "Component created succesfully"}

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

# Editar componente por Id  ----  (funciona ok)
def update_component(component_id: str, component: MenuComponent):
    update_data = component.model_dump()
    result = menu_collection.update_one(
        {"_id": ObjectId(component_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        return {"message": "Component not found"}
    return {"message": "Component updated successfully"}

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

    # Eliminamos el componente (falta eliminar productos e hijos asociados - implementar)
    result = menu_collection.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        return {"message": "Component not found"}

    return {
        "message": "Component deleted successfully",
        #        "deleted_products_count": deleted_products.deleted_count,
        #        "deleted_items_count": deleted_items.deleted_count,
        #       "deleted_items_nietos_count": deleted_items_nietos.deleted_count
    }

"""
# Primero eliminamos en cascada los productos hijos cuyo component_id coincida con el del padre.
    deleted_products = product_collection.delete_many({"component_id": component_id})

# Segundo eliminamos en cascada los items nietos cuyo item_id coincida con product_id
    deleted_items = item_collection.delete_many({"component_id": product_id})

# Tercero eliminamos en cascada los items que están bajo un componente directamente
# Es decir no tienen un padre producto, sino que son hijos del componente
    deleted_items_nietos = menu_collection.delete_many({"component_id": component_id})
"""


