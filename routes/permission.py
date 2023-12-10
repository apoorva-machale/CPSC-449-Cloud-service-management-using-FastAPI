from fastapi import APIRouter, HTTPException, status
from models.permission import Permission
from config.database import permission_collection
from schema.schemas import permission_serial

router = APIRouter()

@router.post("/permissions")
async def add_permission(permission: Permission):
    # Check if permission with the same id already exists
    if permission_collection.find_one({"id": permission.id}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission with this ID already exists")

    # Insert the new permission into the database
    permission_collection.insert_one(permission.model_dump())
    return {
        "created": True
    } 