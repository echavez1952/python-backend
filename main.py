# main.py

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from middleware.auth import AuthMiddleware

from routes import auth
from routes import users

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:5173",   # frontend (Vite, por ejemplo)
    "http://127.0.0.1:5173",   # También útil en algunos casos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # o ["*"] si es solo para pruebas
    allow_credentials=True,
    allow_methods=["*"],        # permite GET, POST, etc.
    allow_headers=["*"],        # permite todos los headers
)


app.add_middleware(AuthMiddleware)

app.include_router(auth.router)

app.include_router(users.router)