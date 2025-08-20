# models/Menu.py
# modelo de los componentes del menú

from pydantic import BaseModel
from typing import Optional

# Modelo para los componentes del menú
class MenuComponent(BaseModel):
    name: str
    description: Optional[str] = None