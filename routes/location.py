# routes/location.py

from fastapi import APIRouter, HTTPException, File, Form

from services.location_service import (
    list_locations,
    create_location,
    update_location,
    delete_location,
    get_location,
)

router = APIRouter(prefix="/location", tags=["location"])

@router.get("/")
def list_locations_route():
    return list_locations()

@router.get("/{location_id}")
def get_location_route(location_id):
    try:
        return get_location(location_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=as_detail_error(e))

@router.post("/")
def create_location_route(
    name = Form(...),
    address = Form(...),
    image = File(None),   # opcional
):
    try:
        return create_location(name, address, image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=as_detail_error(e))

@router.put("/{location_id}")
def update_location_route(
    location_id,
    name = Form(None),
    address = Form(None),
    image = File(None),   # si lo envías, reemplaza la imagen anterior
):
    try:
        return update_location(location_id, name=name, address=address, image=image)
    except Exception as e:
        raise HTTPException(status_code=404, detail=as_detail_error(e))

@router.delete("/{location_id}")
async def delete_location_route(location_id):
    try:
        return delete_location(location_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=as_detail_error(e))
