from fastapi import APIRouter, Depends, HTTPException, status
from models.subscriptionPlan import SubscriptionPlan, serialize_subscription_plan
from config.database import subscription_collection
from schema.schemas import list_serial
from bson import ObjectId
from utils.authentication import get_current_admin,validate_permission
from fastapi.security import HTTPBearer


security = HTTPBearer()
router = APIRouter(tags=["SubscriptionPlan"])

@router.get("/subscriptionpPlans")
async def get_subscription_plans(
    token:str= Depends(security)):
    # add validation func
    if not await validate_permission("list_all_subscriptions",token):
        raise HTTPException(status_code=403,detail=f"User is not authorised to perform this action")
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
    token:str= Depends(security)
    # current_admin: str = Depends(get_current_admin),
):
    # if current_admin is None:
    #     return HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    # add validation func
    if not await validate_permission("add_subscription",token):
        raise HTTPException(status_code=403,detail=f"User is not authorised to perform this action")
    subscription_collection.insert_one(serialize_subscription_plan(subscription))
    return {
        "statusMessage": "Added subscription plan successfully"
    }

@router.put("/updateSubscriptionPlan/{id}")
async def update_subscription_plan(
    id:str,
    subscription: SubscriptionPlan,
    token:str= Depends(security)
    # current_admin: str = Depends(get_current_admin)
):
    # if current_admin is None:
    #     return HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )

    if not await validate_permission("update_subscription",token):
        raise HTTPException(status_code=403,detail=f"User is not authorised to perform this action")
    subscription_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": serialize_subscription_plan(subscription)})
    return {
        "statusMessage": "Updated subscription plan successfully"
    }

@router.delete("/deleteSubscriptionPlan/{id}")
async def delete_subscription_plan(
    id:str,
    token:str= Depends(security)
    # current_admin: str = Depends(get_current_admin)
):
    # if current_admin is None:
    #     return HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    if not await validate_permission("delete_subscription",token):
        raise HTTPException(status_code=403,detail=f"User is not authorised to perform this action")
    subscription_collection.find_one_and_delete({"_id": ObjectId(id)})
    return {
        "statusMessage": "Deleted subscription plan successfully"
    }