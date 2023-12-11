from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from config.database import permission_collection
# from schema.schemas import list_permissions
from schema.permissions import CreatePermission,DeletePermission
from utils.helper import list_permissions
from utils.authentication import validate_permission
from fastapi.security import HTTPBearer
security = HTTPBearer()

router = APIRouter(tags =["Permission"])

@router.post("/create_permission")
async def create_permission(permission:CreatePermission,
                            token:str= Depends(security)
        ):
    """
    API to create role and permission Mapping
    """
    
    # Check if permission already exist in DB then return 409 status code
    # Comment Below two lines for first user and permission
    if not await validate_permission("create_permission",token):
        raise HTTPException(status_code=403,detail=f"User is not authorised to perform this action")
    per = permission_collection.find_one(permission.dict())
    if per :
        raise  HTTPException(status_code=409,detail=f"Permission already exist for role")
    try:
        result = permission_collection.insert_one(permission.dict())
        return {"message":f"Permission for role {permission.role} created Successfully"}
    except Exception as e :
        print(e)
        raise HTTPException(status_code=500,detail=f"Error in creating Permission")

@router.get("/permissions")
async def list_permission(token:str= Depends(security)):
    """
    API to get the list of all permissions
    """
   
    if not await validate_permission("list_all_permissions",token):
        raise HTTPException(status_code=403,detail=f"User is not authorised to perform this action")
    try:
        permissions = permission_collection.find()
        return {"data":{"permissions":list_permissions(permissions)}}
    except Exception as e :
        print(e)
        raise HTTPException(status_code=500,detail=f"Error in list Permissions")


@router.get("/permissions/{role}")
async def list_permission(role:str,
                          token:str= Depends(security)):
    """
    API to get the list of permissions for a given role
    """
    if not await validate_permission("list_role_permissions",token):
        raise HTTPException(status_code=403,detail=f"User is not authorised to perform this action")
    try:
        permissions = permission_collection.find({"role":role})
        return {"data":{"permissions":list_permissions(permissions)}}
    except Exception as e:
         raise HTTPException(status_code=500,detail=f"Error list role permissions")


@router.delete("/permissions")
async def delete_permission(permission:DeletePermission,
                            token:str= Depends(security)):
    """API to delete a permission for a role"""
    
    if not await validate_permission("delete_permissions",token):
            raise HTTPException(status_code=403,detail=f"User is not authorised to perform this action")
    per = permission_collection.find_one(permission.dict())
    if not per :
        raise  HTTPException(status_code=404,detail=f"Permission not found for a given role")
    try:
        result = permission_collection.delete_one(permission.dict())
        return {"message":f"Permission for role {permission.role} deleted Successfully"}
    except Exception as e :
        print(e)
        raise HTTPException(status_code=500,detail=f"Error in creating Permission")