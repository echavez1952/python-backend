# servicios de crear y loguear, lógica del negocio en la parte de autenticación

from database.mongo import db
import bcrypt
import jwt
import os


salt = bcrypt.gensalt()

user_db = db['users']

def register(user):
    data_user = user.model_dump()

    result_exist = user_db.find_one({'email': data_user['email']})
    print (result_exist)
    if result_exist:
        return {"message": "User already exists"}

    hash_password = bcrypt.hashpw(
        password = data_user['password'].encode('utf-8'),  # encode('utf-8') convierte un Unicode string a una secuencia de bytes
        salt = salt
    ).decode('utf-8')  # decode('utf-8') convierte una secuencia de bytes a un objeto string

    data_user['password'] = hash_password
    data_user['role'] = 'user'
    data_user['status'] = 'active'
    user_db.insert_one(data_user)
    return {'message': 'Register completed successfully'}


def login(email, password):
    user_exist = user_db.find_one({'email':email})
    if not user_exist:
        return {"message": "User not found"}

    check_password = bcrypt.checkpw(password.encode('utf-8'),user_exist['password'].encode('utf-8'))

    if not check_password:
        return {"message": "email or password is incorrect"}

    user_exist['_id'] = str(user_exist['_id'])
    user_exist['password'] = None
    secret_key = os.getenv("JWT_SECRET_KEY")
    token = jwt.encode(user_exist, secret_key, algorithm='HS256')

    return {
        "message": "Login Completed Successfully",
        "user": user_exist,
        "token": token
    }
