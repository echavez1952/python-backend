from fastapi import FastAPI
from routes import auth

app = FastAPI()


app.include_router(auth.router)

for route in app.routes:
    print(" Ruta registrada:", route.path, "-", route.methods)
