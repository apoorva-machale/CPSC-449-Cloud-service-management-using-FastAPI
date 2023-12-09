from fastapi import APIRouter, Depends, HTTPException, status
from models.subscriptionPlan import SubscriptionPlan, serialize_subscription_plan
from config.database import subscription_collection
from schema.schemas import list_serial
from bson import ObjectId
from utils.authentication import get_current_admin
router = APIRouter()

@router.get("/subscriptionpPlans")
async def get_subscription_plans():
    subscription_plans=list_serial(subscription_collection.find())
    if not subscription_plans:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong. Please try again later"
            )
    return subscription_plans


@router.post("/addSubscriptionPlans")
async def post_subscription_plan(
    subscription: SubscriptionPlan,
    current_admin: str = Depends(get_current_admin)
):
    if current_admin is None:
        return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    subscription_collection.insert_one(serialize_subscription_plan(subscription))
    return {
        "statusMessage": "Added subscription plan successfully"
    }

@router.put("/updateSubscriptionPlan/{id}")
async def update_subscription_plan(
    id:str,
    subscription: SubscriptionPlan,
    current_admin: str = Depends(get_current_admin)
):
    if current_admin is None:
        return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    subscription_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": serialize_subscription_plan(subscription)})
    return {
        "statusMessage": "Updated subscription plan successfully"
    }
@router.delete("/deleteSubscriptionPlan/{id}")
async def delete_subscription_plan(
    id:str,
    current_admin: str = Depends(get_current_admin)
):
    if current_admin is None:
        return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    subscription_collection.find_one_and_delete({"_id": ObjectId(id)})
    return {
        "statusMessage": "Deleted subscription plan successfully"
    }