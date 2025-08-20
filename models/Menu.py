# models/Menu.py
# modelo de los componentes del menú

from pydantic import BaseModel

# Modelo para los componentes del menú
class MenuComponent(BaseModel):
    name: str
