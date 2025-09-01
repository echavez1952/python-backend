
# services/location_service.py

"""
Servicios mínimos para Locations (sin type hints y con FormData).
- Colección Mongo: "locations"
- Imágenes guardadas bajo ./uploads/AAAA/MM/<uuid>.<ext>
- Devuelve diccionarios simples: {id, name, address, image}
"""
import os
import shutil, uuid
from datetime import datetime
from bson import ObjectId
from database.mongo import db

WEB_PREFIX = "/uploads"          # ruta pública para el navegador
UPLOAD_ROOT = "uploads"          # carpeta física en el backend
col = db["locations"]


def _serialize(doc):
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name", ""),
        "address": doc.get("address", ""),
        "image": doc.get("image") or None,
    }


def _ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def _bucket_paths():
    # crea subcarpetas por año/mes: uploads/YYYY/MM
    now = datetime.utcnow()
    bucket = os.path.join(f"{now.year:04d}", f"{now.month:02d}")
    disk_dir = os.path.join(UPLOAD_ROOT, bucket)
    web_prefix = f"{WEB_PREFIX}/{bucket}"
    return disk_dir, web_prefix


def _save_upload(file):
    if not file:
        return None
    _, ext = os.path.splitext(file.filename or "")
    ext = (ext or ".bin").lower()

    disk_dir, web_prefix = _bucket_paths()
    _ensure_dir(disk_dir)

    name = f"{uuid.uuid4().hex}{ext}"
    disk_path = os.path.join(disk_dir, name)
    with open(disk_path, "wb") as out:
        shutil.copyfileobj(file.file, out)

    return f"{web_prefix}/{name}"


def _delete_file_if_local(web_path):
    if not web_path or not str(web_path).startswith(WEB_PREFIX):
        return
    rel = str(web_path)[len(WEB_PREFIX):].lstrip("/")
    disk_path = os.path.join(UPLOAD_ROOT, rel)
    try:
        os.remove(disk_path)
    except FileNotFoundError:
        pass


# -------------------- CRUD --------------------

def list_locations():
    return [_serialize(d) for d in col.find().sort("_id", -1)]


def get_location(location_id):
    d = col.find_one({"_id": ObjectId(location_id)})
    if not d:
        raise ValueError("Location not found")
    return _serialize(d)


def create_location(name, address, image):
    payload = {"name": name, "address": address, "image": _save_upload(image)}
    res = col.insert_one(payload)
    return _serialize(col.find_one({"_id": res.inserted_id}))


def update_location(location_id, name=None, address=None, image=None):
    d = col.find_one({"_id": ObjectId(location_id)})
    if not d:
        raise ValueError("Location not found")

    patch = {}
    if name is not None:
        patch["name"] = name
    if address is not None:
        patch["address"] = address
    if image is not None:
        _delete_file_if_local(d.get("image"))
        patch["image"] = _save_upload(image)

    if patch:
        col.update_one({"_id": d["_id"]}, {"$set": patch})
    return _serialize(col.find_one({"_id": d["_id"]}))


def delete_location(location_id):
    d = col.find_one({"_id": ObjectId(location_id)})
    if d:
        _delete_file_if_local(d.get("image"))
        col.delete_one({"_id": d["_id"]})
    return {"ok": True}


def as_detail_error(e):
    msg = (str(e) or e.__class__.__name__).lower()
    if "not found" in msg:
        return "Location not found"
    return str(e)
