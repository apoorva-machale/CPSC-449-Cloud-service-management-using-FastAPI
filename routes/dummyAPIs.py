from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from utils.permission import check_api_permission
router = APIRouter()

@router.get("/compute")
async def compute_service( permission: bool = Depends(check_api_permission)):
    if permission:
     return {
        "status": "You are now accessing the compute API"
    }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )
@router.get("/database-service")
async def database_service(permission: bool = Depends(check_api_permission)):
    if permission:
     return {
        "status": "You are now accessing the database service API"
    }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )
@router.get("/ml")
async def ml_service(permission: bool = Depends(check_api_permission)):
    if permission:
     return {
        "status": "You are now accessing the machine learning API"
    }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )
@router.get("/data-analytics")
async def data_analytics_service(permission: bool = Depends(check_api_permission)):
    if permission:
     return {
        "status": "You are now accessing the data analytics API"
    }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )
@router.get("/iot-management")
async def iot_management_service(permission: bool = Depends(check_api_permission)):
    if permission:
     return {
        "status": "You are now accessing the iot management  API"
    }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )
@router.get("/cloud-storage")
async def cloud_storage_service(permission: bool = Depends(check_api_permission)):
    if permission:
     return {
        "status": "You are now accessing the cloud storage  API"
    }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )

@router.get("/cloud_storage/{service}")
async def cloud_storage_data(service: str, permission: bool = Depends(check_api_permission)):
    if permission:
        return {
            "status": "You are now using cloud service API"
        }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )
