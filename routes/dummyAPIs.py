from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from utils.permission import check_api_permission
router = APIRouter()

@router.get("/weather/{location}")
async def weather_data(location: str, permission: bool = Depends(check_api_permission)):
    if permission:
     return {
        "status": "You are now accessing the weather API"
    }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )
@router.get("/currency/exchange/{currencyCode}")
async def weather_data(currencyCode: str, permission: bool = Depends(check_api_permission)):
    if permission:
     return {
        "status": "You are now accessing the currency excahange API"
    }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )
@router.get("/image/process")
async def weather_data(approach: str, permission: bool = Depends(check_api_permission)):
    if permission:
     return {
        "status": "You are now accessing the image processing API"
    }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )
@router.get("/translate/{sourceLang}/{targetLang}")
async def weather_data(sourceLang: str,targetLang: str, permission: bool = Depends(check_api_permission)):
    if permission:
     return {
        "status": "You are now accessing the text translation API"
    }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )
@router.get("/geolocation/{ipAddress}")
async def weather_data(ipAddress: str, permission: bool = Depends(check_api_permission)):
    if permission:
     return {
        "status": "You are now accessing the geolocation  API"
    }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access to this API is not allowed with your subscription plan."
    )

