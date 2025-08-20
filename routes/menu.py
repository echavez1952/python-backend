# routes/menu.py - Endpoints de los componentes del mqenu

from fastapi import APIRouter, Form
from models.Menu import MenuComponent
from services.menu_service import (
    get_all_components,
    get_component_by_id,
    create_component,
    update_component,
    delete_component
)

router = APIRouter(prefix="/menu", tags=["menu"])

# Crear componente
@router.post('/')
def create_component_route(component: MenuComponent):
    return create_component(component)

# Listar todos los componentes
@router.get("/")
def get_components_route():
    return get_all_components()

# Obtener un componente por ID
@router.get("/{component_id}")
def get_component_by_id_route(component_id: str):
    return get_component_by_id(component_id)

"""
# Editar componente por Id
@router.put("/{component_id}")
def update_component_route(
    component_id: str,
    name: str = Form(...),
):
    component = MenuComponent(name=name)
    return update_component(component_id)
"""

@router.put('/{component_id}')    # funciona ok
def update_component_route(component_id: str, component: MenuComponent):
    return update_component(component_id, component)


# Eliminar componente y sus productos hijos y sus items nietos
@router.delete("/{component_id}")
def delete_component_route(component_id: str):
    return delete_component(component_id)
