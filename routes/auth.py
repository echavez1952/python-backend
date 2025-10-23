from fastapi import APIRouter, Response
from services.auth_service import register, login
from models.User import User, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/register')
def register_route(user: User):
    return register(user)

@router.post('/login')
def login_route(user_login: UserLogin):
    return login(user_login.email,user_login.password)

@router.post('/logout')
def logout_user_route(response: Response):
    return logout_user(user_logout, response)