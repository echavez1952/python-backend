from pydantic import BaseModel

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    birth_date: str

class UserLogin(BaseModel):
    email: str
    password: str