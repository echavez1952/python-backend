# routes/location.py

from fastapi import APIRouter, HTTPException, File, Form

from location_services import (
    list_locations,
    create_location,
    update_location,
    delete_location,
    get_location,
    as_detail_error,
)

router = APIRouter(prefix="/locations", tags=["locations"])

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
async def create_location_route(
    name = Form(...),
    address = Form(...),
    image = File(None),
):
    try:
        return create_location(name, address, image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=as_detail_error(e))

@router.put("/{location_id}")
async def update_location_route(
    location_id,
    name = Form(None),
    address = Form(None),
    image = File(None),
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
