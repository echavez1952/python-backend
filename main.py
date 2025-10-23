# main.py

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from middleware.auth import AuthMiddleware
from fastapi.staticfiles import StaticFiles

from routes import auth
from routes import users
from routes import menu
from routes import product
from routes import item
from routes import location

app = FastAPI()
app.mount('/uploads', StaticFiles(directory='uploads'), name='uploads')

origins = [
    "http://localhost",
    "http://localhost:5173",   # frontend (Vite, por ejemplo)
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # o ["*"] si es solo para pruebas, usa el origen exacto en dev
    allow_credentials=True,    # True solo si usas cookies/Authorization
    allow_methods=["*"],        # o lista: ["GET","POST","PUT","DELETE","OPTIONS"]
    allow_headers=["*"],        # o lista concreta si quieres ser estricto
)

app.add_middleware(AuthMiddleware)

app.include_router(auth.router)

app.include_router(users.router)

app.include_router(menu.router)

app.include_router(product.router)

app.include_router(item.router)

app.include_router(location.router)

@app.get("/")
def health():
    return {"ok": True}

