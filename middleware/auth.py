# middleware/auth.py
# Paso 1: Crear el middleware (ejemplo con autenticación)
# starlette.middleware.base -- es parte del motor de FastAPI que me permite interceptar solicitudes".

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import jwt

def verify_token(token: str):
    try:
        return jwt.decode(token, 'secret123', algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        print("⏰ Token expirado")
        return None
    except jwt.InvalidTokenError:
        print("❌ Token inválido")
        return None

class AuthMiddleware(BaseHTTPMiddleware):
    print("✅ Middleware cargado correctamente")  # <-- este print debe aparecer en el terminal

    async def dispatch(self, request: Request, call_next):
        print("📥 Middleware ejecutando:", request.url.path)   # /auth/register

        authorization = request.headers.get("Authorization")  # Obtener Authorization

        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]  # Obtener el token
            print("🔑 TOKEN:", token)

            payload = verify_token(token) # Obtiene el payload del token
            print("PAYLOAD:", payload)
            if payload:
                #request.state.user = get_user_by_email(payload['email'])
                request.state.user = payload
                print("🔐 Usuario autenticado:", payload["email"])
            else:
                print("❗ Token inválido o expirado")

        return await call_next(request)


