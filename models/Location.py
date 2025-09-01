# models/Location.py
from pydantic import BaseModel
from typing import Optional



class LocationCreate(BaseModel):
    name: str
    address: str
    image: Optional[str] = None