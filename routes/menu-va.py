# routes/menu.py - Endpoint para listar componentes del menu

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

"""
# Crear componente
@router.post("/components")
def create_menu_component_route(
    name: str = Form(...),
    description: str = Form(None)
):
    component = MenuComponent(name=name, description=description)
    return create_menu_component(component)
"""

# Crear componente
@router.post('/')
def create_component_route(component: MenuComponent):
    return create_component(component)

"""
@router.post("/")
def create_component_route(
    name: str = Form(...),
    description: str = Form(None)
):
    return create_component(name, description)
"""

# Listar componentes
@router.get("/")
def get_components_route():
    return get_all_components()

# Obtener un componente por ID
@router.get("/{component_id}")
def get_component_by_id_route(component_id: str):
    return get_component_by_id(component_id)

# Editar componente
@router.put("/{component_id}")
def update_component_route(
    component_id: str,
    name: str = Form(...),
    description: str = Form(None)
):
    component = MenuComponent(name=name, description=description)
    return update_component(component_id, component)

"""
@router.put("/{component_id}")
def update_component_route(
    component_id: str,
    name: str = Form(...),
    description: str = Form(None)
):
    return update_component(component_id, name, description)
"""

# Eliminar componente y sus productos hijos
@router.delete("/{component_id}")
def delete_component_route(component_id: str):
    return delete_component(component_id)
